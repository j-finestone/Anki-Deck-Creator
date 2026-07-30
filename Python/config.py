fields = [
    "Frequency",
    "Word", #Foreign word
    "Traditional", #The word in traitional chinese script
    "Pronunciation", 
    "Meaning", #Meaning of word
    "Sentence", #Example sentence using the word
    "Sentance pronunciation", #example sentance that has the pronunciation in brackets
    "Sentence meaning",
    "Notes", #Explains how to use word, difference between similar words, other gramatical quircks etc
    "Breakdown" #Break down the characters or etomology of the word
]

#How long the list of core vocb (the number 1 most common words) can be
core_vocab_length = 150


#Languages the user already speaks, where the notes can use those as references in its explinations
reference_languages = ["English", "Spanish", "French", "Hebrew"]






#region prompts
def system_prompt(core_vocab):
    """Forms system prompt for the OpenAI API request.
    Args
        scaffolding_vocab (list): List of basic content words it is allowed so it can make sentences before content words
        core (list): List of words that are considered basic vocabulary.
    Returns
        str: The system prompt for the OpenAI API request."""


    system_prompt = f"""You are generating example sentences for a Simplified Mandarin Chinese
        frequency-ordered Anki deck. For each target word you receive, produce ONE natural sentence
        where the target word is the only new vocabulary item.

        Rules:
        - Every other word in the sentence must appear in CORE_VOCAB,
        or RECENT_VOCAB (given in the user message), or be a simple, unambiguous
        concrete noun/function word with no natural substitute available there.
        - Keep grammatical complexity appropriate for how far into the frequency list
        this word is. Infer this mostly from what's available in CORE_VOCAB / 
        RECENT_VOCAB. a word early in the list should get a simple,
        direct sentence; later words can support more elaborate structure. Stay
        within MAX_CLAUSES (given in the user message) regardless.
        - Notes: only include if there's a real grammar point or a genuine nuance vs.
        a similar word. Leave "" if the meaning is a clean 1:1 gloss. Be concise —
        no filler, no disclaimers about vulgarity beyond one neutral clause if
        relevant. Reference {reference_languages} parallels when that's
        more efficient than explaining from scratch.
        - Breakdown: give the meaning of each character/morpheme for compound words.
        Add more detail only where the morpheme split is genuinely illuminating.
        Leave "" otherwise.
        - Pinyin in Notes/Breakdown: whenever either field mentions a Chinese word
        other than the target word itself (e.g. comparing 知道 vs 认识), include
        that word's pinyin in parentheses so it's readable without a lookup. Don't
        repeat the target word's own pinyin here — that's handled separately.
        - Output strictly valid JSON matching the provided schema. No prose outside
        JSON.

        CORE_VOCAB: {core_vocab}
        """



#Outputs the user prompt
def user_prompt (target_words, recent_vocab, max_clauses=2):
    user_prompt = f"""
    ALLOWED_VOCAB (recent_vocb): {recent_vocab}
    MAX_CLAUSES: {max_clauses}

    TARGET_WORDS: {target_words}"""
    
    return user_prompt


#endregion