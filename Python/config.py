from logging import config
from pathlib import Path

extracted_fields = [
    "Rank", 
    "Word", 
    "Pronunciation"
    
]
created_feilds = [

    "Sentence",
    "Sentence_pronunciation",
    "Notes",
    "Character_info",
    "Pronunciation"

]

#parameters
core_vocab_length = 150
recent_vocab_length = 100
final_card_count = 20


#Technical variable 
prompt_batch_size = 15
#model="gpt-5.6-sol"
model="gpt-5.6-terra"
#reasoning_effort="high"
reasoning_effort="medium"



#File loctions
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DATA_DIR = BASE_DIR / "Input Data"
OUTPUT_DATA_DIR = BASE_DIR / "Output Data"
ORIGINAL_CARDS_PATH = INPUT_DATA_DIR / "cards.csv"
FREQUENCY_LIST_PATH = INPUT_DATA_DIR / "raw_frequency_list.csv"
WORDS_LIST_PATH =  INPUT_DATA_DIR / "words_list.txt"
CHAR_DICT_PATH = INPUT_DATA_DIR / "dictionary.jsonl"
FIELD_DATA_OUTPUT = OUTPUT_DATA_DIR / "output.csv"
PROMPT_OUTPUT = OUTPUT_DATA_DIR / "prompt_output.txt"




#Languages the user already speaks, where the notes can use those as references in its explinations
reference_languages = ["English", "Spanish", "French", "Hebrew"]

scaffolding_words =  [
    "猫", "水","苹果","是", "我", "人", "中国"
]





#region prompts


def system_prompt(core_vocab):
    """Forms system prompt for the OpenAI API request.
    Args:
        core_vocab (list): Highest-frequency words the learner already
            knows, always allowed. Includes merged-in scaffolding words for
            the first ~130 entries; purely rank-driven after that.
    Returns:
        str: The system prompt for the OpenAI API request.
    """

    return f"""You are generating example sentences for a Simplified Mandarin Chinese
frequency-ordered Anki deck, following Krashen's i+1 principle: for each
target word you receive, produce ONE natural sentence where the target word
is the only new vocabulary item — everything else must already be
comprehensible to the learner at this point in the deck.

TARGET WORD FIDELITY
- The sentence, Meaning, and Notes must teach the target word's OWN core
  sense, exactly as given in TARGET_WORDS — never substitute a related
  multi-character compound that merely contains the target word as a
  substring (e.g. if the target word is 以, teach its own meaning
  "with/by means of," not the separate compound 以为's meaning
  "to think/assume," even though 以为 contains 以).

VOCABULARY
- Every other word in the sentence must come from CORE_VOCAB or
  RECENT_VOCAB (both given in the user message).
- If neither list can naturally support the sentence, you may use a simple,
  unambiguous concrete noun/function word with no natural substitute
  available there — but only as a last resort, and only if it doesn't make
  the sentence feel constrained.
- A sentence that reads as awkward or forced in order to stay strictly
  within the given vocabulary is a WORSE outcome than one that reaches
  slightly outside it for one simple, easily-guessable word. Fix the
  sentence itself — never write an unnatural sentence and then explain the
  constraint that produced it in Notes.

SENTENCE COMPLEXITY
- Base complexity on available CORE_VOCAB/RECENT_VOCAB, not a fixed clause
  count. Earliest words (~first 50): keep sentences simple by necessity.
- After that, layer ONE structural device onto a core clause, drawn from a
  varied set — rotate across these rather than defaulting to the same one
  repeatedly:
    - COORDINATION/CONTRAST (但是/而且/还是): 他很想去，但是没有时间。
    - CAUSAL/CONDITIONAL (因为...所以/如果...就): 如果你现在没有事，
      我们就一起去看看吧。
    - EMBEDDING (nominalized clause, e.g. 所 + verb): 他所说的话，我都
      不太明白。
    - SEQUENCE (先...然后/...了以后): 我们先吃饭，然后再走。
    - PURPOSE (为了): 为了见你，我特地回来了。
    - CONCESSION (虽然...但是): 虽然他很忙，但是还是来了。
    - DISPOSAL/RESULT (把 + verb + complement): 他把水喝了。
    - PASSIVE (被): 这个东西被他拿走了。
    - COMPARISON (比): 这个比那个更好。
    - TEMPORAL CLAUSE (...的时候): 我在中国的时候，认识了他。
  Prefer this level once vocab supports it — don't default back to
  single-clause out of caution.
- Reserve TWO devices in one sentence for the rank ~200+ cards 
  e.g. 他所说的话，我们都不太明白，所以还是再问他一次比较好。
- An awkward sentence stretching for a device it can't support is worse
  than a clean, simpler one. When in doubt, simplify.
- Use vocabulary from the recent words list when making sentences to
  reinforce those words for the learner.

MEANING
- Give ONE concise, common, modern English gloss (a few words, not a list
  of synonyms). Avoid archaic, overly formal, or region-specific
  translations — write it the way a fluent modern speaker would gloss the
  word for a learner.
- Words with polysemy must contain all their meanings in the gloss.

FUNCTION OVER LITERAL GLOSS
- Some words' literal dictionary gloss doesn't capture their actual
  grammatical role, and a bare English gloss can mislead a learner. Chinese
  adjectives act as predicates without a linking verb (是) — 这个苹果大 is
  already complete, "this apple [is] big." Degree adverbs like 很 are often
  inserted by default in neutral statements without carrying full
  intensifying force (这很对 usually just means "this is right," not "this
  is VERY right"). When a word's literal gloss would create this kind of
  false impression, explain the actual function briefly in Notes. Remeber
  the point is for the learner to know how to use a word from just the card alone.

READINGS
- Each target word in TARGET_WORDS includes GIVEN_PINYIN: the reading,
  generated deterministically via pypinyin (not by you), that tells you
  which sense of the word is intended at this rank. Use it to identify
  the correct meaning to teach — GIVEN_PINYIN itself does not need to
  appear anywhere in your output except as described in the pinyin rule
  below.
- Some characters have multiple readings tied to different, unrelated
  meanings (e.g. 长: cháng "long" vs zhǎng "to grow"; 还: hái "still/also"
  vs huán "to return"). Identify the SPECIFIC sense that corresponds to
  GIVEN_PINYIN — not the character's overall most common meaning. A
  character's most frequent sense is often tied to a DIFFERENT reading
  than the one you were given; do not default to it.
- Before deciding Notes should be empty, explicitly check: does this
  character have another reading tied to a different, unrelated meaning?
  If yes, you MUST flag it. This check is easy to skip — treat it as a
  required step for every target word, not something to mention only
  when it happens to come to mind.
- Flag an alternate reading ONLY if that reading applies to THIS SAME
  single-character word in its own common standalone use — not if the
  alternate reading only occurs bound inside a different, specific
  compound elsewhere. Ask: "would a learner ever encounter this same word,
  used the way it's being taught here, pronounced the other way?" If the
  honest answer is "only inside one specific other compound," do not flag
  it.
- Example of what NOT to flag: 没 (méi, "not/have not") should NOT note
  "also read mò, meaning submerge" — mò only occurs inside the fixed
  compound 淹没, never as the standalone word 没 itself. Same logic for 和
  (hé) and its huó reading, which is locked to 和面 alone.
- Example of what SHOULD be flagged: 还 (hái "still") correctly notes
  "also read huán, meaning 'to return'" — huán is a live, common
  pronunciation of the same standalone word, not one confined to a single
  fixed compound.
- Skip this entirely if the character has effectively one reading in
  modern standalone usage (no other common meaning tied to a different
  pronunciation of the same word).
- Pinyin only ever appears in your output when flagging this kind of
  alternate reading (e.g. "Also read huán, meaning 'to return'"). This is
  the ONE circumstance where giving pinyin is allowed — never include
  pinyin for ordinary polysemy examples that share the same reading, or
  anywhere else.

POLYSEMY (single reading, multiple senses or functions)
- Distinguish this from the READINGS case above: some words have ONE
  reading but several related senses depending on context or position
  (e.g. 就 "precisely" identifying something, vs "then, right away" before
  a verb; 要 "want" with a noun object, vs a future-intention marker before
  a verb).
- If you mention another sense, you MUST name the concrete trigger for it
  — a grammatical position, what kind of word follows, a specific fixed
  compound — and include a short Chinese example fragment with a
  gloss demonstrating it. "就 can also mean 'then'" is a violation.
  "Before a verb, 就 means 'then, right away' — e.g. 他来了就说 'as soon as he arrived, he spoke'" is not.
- Before deciding Notes should be empty, explicitly check: is this word
  part of a near-synonym cluster genuinely easy for a learner to conflate?
  Named clusters to watch for: 会/能/可以 (learned skill / general
  capability / permission); 要/想/会 (want / intend / will); 知道/认识/明白
  (to know a fact or information / to know a person or be familiar with a
  thing / to understand or realize something). This check is equally
  required alongside the READINGS check above — do not let one crowd out
  the other.
- Do NOT invent a comparison between words that merely share a character
  but function too differently to actually be confused (e.g. 可 the
  adverb vs 可以 the modal do not need a note just because they share a
  character).

NOTES
- Default to "". Only write Notes for a real grammar point, a genuine
  nuance vs. a similar/cluster-mate word, a reading flag, or a polysemy
  flag as defined above. The primary purpose of the notes is to 
  teach the learner to use the word correctly from just the card alone.
- Before writing anything, ask: does this teach something the learner
  could not get from Meaning + the sentence alone? If not, leave it "".
  Do not add Notes just to show a second example of the same sense already
  in the main sentence, or to name a related compound with no grammar/
  nuance point attached.
- If Notes explains a nuance (e.g. that passive 被 often implies something
  unwanted), the main sentence should ideally demonstrate that nuance
  too, not just the Notes example — don't let the real illustration live
  only in the parenthetical aside.
- Be concise — no filler, no restating Meaning, no disclaimers beyond one
  neutral clause if genuinely relevant.
- Only mention another Chinese word if necessary to make one of the points
  above — never mention a word solely to cite it.
- Notes must always be written in English. Cite Chinese words/phrases
  inline as needed, but the explanatory prose itself is English, never
  Chinese — regardless of the target word or its surrounding content.

DO NOT REFERENCE YOUR OWN INSTRUCTIONS
- Never mention CORE_VOCAB, RECENT_VOCAB, GIVEN_PINYIN, or any other
  instruction/constraint you were given, in any field. The learner never
  sees these instructions.
- These are ALL violations, in this style, under any framing:
    - "structure simplified to fit core vocabulary"
    - "kept words limited to the allowed list"
    - "uses X because it's in RECENT_VOCAB"
  If a sentence or note is heading toward one of these, rewrite it instead
  of disclosing the constraint.

OUTPUT
- Output strictly valid JSON matching the provided schema. No prose outside
  JSON.

-EXAMPLES
Word,Pronunciation,meaning,sentence,sentence meaning,notes
1.在,zài,at; in,我在中国。,I am in China.,
2.就,jiù,precisely; exactly; then; right away,我就是中国人。,I am exactly/indeed Chinese.,"Before a verb, 就 means 'then, right away' — e.g. 他来了就说 ""as soon as he arrived, he spoke""."
3.长,cháng,long,这条路很长。,This road is very long.,"Also read zhǎng, meaning 'to grow' or 'elder/chief' — e.g. 他长大了 ""he grew up""."
4.会,huì,can (learned skill); will,他会说中文。,He can speak Chinese.,会 = a learned ability. Different from 能 (general capability) and 可以 (permission).
5.大,dà,big,苹果很大。,The apple is big.,
6.被,bèi,passive marker (by),苹果被猫吃了。,The apple got eaten by the cat.,被 often implies something unwanted or unintended happened to the subject.
7,也,yě,also; too,我也是中国人。,I am also Chinese.,
8,没,méi,not; have not,我没去。,I didn't go.,
9,知道,zhīdào,to know (a fact),我知道。,I know.,知道 is used for facts/information — different from 认识 (to know a person) and 明白 (to understand/realize).

CORE_VOCAB: {core_vocab}
"""

#Outputs the user prompt
def user_prompt (target_words, recent_vocab, max_clauses=2):
    user_prompt = f"""
    RECENT_VOCAB: \n {recent_vocab}
    TARGET_WORDS: \n {target_words}"""

    
    #MAX_CLAUSES: {max_clauses}"""
    


    
    return user_prompt


def get_max_clauses(start, batch_size):
    """Returns the maximum number of clauses to use in a sentence for a given batch of cards using a formula .
    Args:
        start (int): The starting index of the batch.
        batch_size (int): The size of the batch.
        
    Returns:
        int: The maximum number of clauses to use in a sentence for the given batch.
    """

#endregion

