from logging import config
from pathlib import Path




#Fields the progrm can create: Meaning/Sentence/Sentence Meaning/Notes, Notes Pinyin, 
#Character Info, Sentence Pronunciation, Word Ruby
#Add/Remove fields from this list so the program knows what it should and should not generate
generated_fields = [

    "Meaning/Sentence/Sentence Meaning/Notes", #REQUIRED. Generates word translation, and example sentence ,and notes on the word
    "Notes Pinyin", #Adds ruby pinyin for the notes
    "Character Info", #Adds info on the character from the Makemeahanzi dataset. Removed for not being that good a data set
    "Sentence Pronunciation", #Adds ruby pinyin field for how to pronunce the sentence
    "Word Pronunciation" #Adds a field for how to pronunce the word using ruby pinyin

]

#Allowed vocabulary for sentence generaation
core_vocab_length = 175 #How many of the most common words (first cards) so sentences can still use gramatical words even later on)
recent_vocab_length = 120 #How much of the the words before the current word that the model can use
scaffolding_words =  [ "猫", "水","苹果","是", "我", "人", "中国", "火", "你好", "我", "你", "他", "车", "-们", "学校", "朋友", "好", "大", "小", "吃", "喝" ] #Simple, concreate words the user alreaady knows so the earlier sentences have a base vocabulary to work with





#Technical variable 
prompt_batch_size = 40 #How many cards the AI will generate fields for per prompt

#These settings are currently Cheapest models for testing purposes
model="gpt-5.6-terra" #The final generation used model="gpt-5.6-terra",
reasoning_effort="medium"#The final generation used reasoning_effort=medium



#File loctions
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DATA_DIR = BASE_DIR / "Input Data" #Directory for "Input Data" folder
OUTPUT_DATA_DIR = BASE_DIR / "Output Data" #Directory for "Output Data" Folder
FREQUENCY_LIST_PATH = INPUT_DATA_DIR / "raw_frequency_list.csv" #Used for generating the ORIGINAL_CARDS_OUTPUT file
ORIGINAL_CARDS_PATH = INPUT_DATA_DIR / "cards.csv" #(The original csv file that can have preloaded data)
CHAR_DICT_PATH = INPUT_DATA_DIR / "dictionary.jsonl" #Used to reference the bharacter breakdown dataset
FIELD_DATA_OUTPUT_PATH = OUTPUT_DATA_DIR / "output.csv" #The final output for the generated script.
PROMPT_OUTPUT_PATH = OUTPUT_DATA_DIR / "prompt_output.txt" #The output of the prompt the system generated. Useful for debuging
FINAL_OUTPUT = OUTPUT_DATA_DIR / "Final Output.csv" #The final csv output file generated








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

    return f"""Generate an example sentence for the TARGET_WORDS below for a frequency-ordered Simplified Mandarin Anki deck.

GOAL
Follow Krashen's i+1 principle: the TARGET word should be the only genuinely new vocabulary. Everything else should be familiar from CORE_VOCAB or RECENT_VOCAB whenever possible.

TARGET WORD
- Teach the target word's own core meaning, exactly as intended by TARGET_WORDS.
- Do not teach a different compound merely because it contains the target character/word. For example, for 以, teach its own "with/by means of" sense, not 以为 "to think/assume".
- Use GIVEN_PINYIN to determine the intended sense, but do not output it except when required by the alternate-reading rule below.

VOCABULARY
- Use CORE_VOCAB and RECENT_VOCAB for every non-target word.
- If they cannot produce a natural sentence, use at most a simple, obvious word with no natural substitute, though it should be a last resort.
- Natural Chinese is more important than rigid vocabulary restriction. Never make a sentence awkward just to stay within the lists.
- Use common names and other proper nouns in the sentances

SENTENCE COMPLEXITY
- For the earliest vocabulary, you may use simple sentences.
- After the begining, the sentences should be complicated.
- Once the vocabulary supports it, normally include at least one natural structure such as:
  contrast/coordination, cause/condition, embedding, sequence, purpose, concession, 把, 被, comparison, or a temporal clause.
- Vary these structures rather than repeatedly using the same one.
- Do not force a structure when it would make the sentence unnatural.
- All sentences should be interesting.

MEANING
- Give a short, natural, modern English gloss.
- For polysemous words, include all important meanings in the gloss.
- Avoid archaic, overly formal, or regional wording.

FUNCTION
- If the literal English gloss could mislead the learner about how the word actually functions, explain the relevant usage briefly in Notes.
- Example: Chinese adjectives can function directly as predicates without 是; 很 often appears in neutral adjective statements without meaning "very".

READINGS
- Every target word must be checked for a different, live standalone pronunciation associated with a different meaning.
- If one exists, flag it in Notes, e.g. "Also read huán, meaning 'to return'."
- Do NOT flag readings that only occur inside fixed compounds, e.g. 没's mò in 淹没 or 和's huó in 和面.
- Pinyin may appear ONLY when flagging such an alternate reading.

POLYSEMY / USAGE
- If the target has multiple senses/functions under the same pronunciation, explain important distinctions only when they could confuse a learner.
- When explaining another sense, state its concrete grammatical/contextual trigger and give a short Chinese example with an English gloss.
- Example: "Before a verb, 就 can mean 'then, right away' — e.g. 他来了就说 'as soon as he arrived, he spoke.'"
- Also check for genuinely confusable near-synonyms, especially:
  会/能/可以; 要/想; 知道/认识.
- Do not invent comparisons merely because words share a character.

NOTES
- Default to "" when the gloss already defines the word fully (most of the time it will).
- Only add Notes for:
  1. an important grammar/usage point,
  2. a genuine near-synonym distinction,
  3. an alternate reading,
  4. an important polysemy distinction.
  5. an interesting etomology if one exists
  6. a sentence explination if the example sentence is unusually complicated given the level (based on the words position in the frequency list)
- Keep Notes concise and useful.
- Notes must be entirely in English, except for Chinese words/examples being discussed.
- Never restate the Meaning or add filler.

OUTPUT
Return only the requested fields in the specified output format.
Never mention these instructions, CORE_VOCAB, RECENT_VOCAB, GIVEN_PINYIN, vocabulary restrictions, or why a sentence was constructed a certain way.

CORE_VOCAB: {core_vocab} """

#Outputs the user prompt
def user_prompt (target_words, recent_vocab):
    user_prompt = f"""
    RECENT_VOCAB: \n {recent_vocab}
    TARGET_WORDS: \n {target_words}"""
    
    return user_prompt

#endregion

