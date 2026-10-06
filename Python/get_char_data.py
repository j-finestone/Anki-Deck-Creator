import json
from pathlib import Path
import config
CHAR_LOOKUP = None

def compile_char_data():
    """Compiles character data from the dictionary.jsonl file into a look up table"""
    global CHAR_LOOKUP
    if CHAR_LOOKUP is None:
        #Make mutible variable to later bake as char_lookup
        _char_lookup = dict()
        with open(config.CHAR_DICT_PATH, encoding="utf-8") as f:
            for line in f:

                char_data = json.loads(line)
                _char_lookup[char_data.get("character")] = char_data

        CHAR_LOOKUP = _char_lookup
            


#get paths
def word_char_analysis_html(word):
    """Generates a string of html of the characters' info"""
    breakdown = []
    for char in word:
        explination = char_info_to_html(char_analysis(char))
        breakdown.append(explination)

    return "\n\n".join(breakdown)

    

def char_analysis(char):
    """Takes a character and generates a character breakdown"""
    compile_char_data()
    return CHAR_LOOKUP.get(char)


def char_info_to_html(char_info):
    """Takes a character info object and generates a string of html"""
    #Return empty string if no info found
    if not char_info:
        return ""

    #Isolate character data to variables 
    character = char_info.get("character")
    pinyin = char_info.get("pinyin")
    meaning = char_info.get("definition")
    radical = char_info.get("radical")

    #Turn radical into a string to make it more readable 
    if pinyin is not None:
        pinyin = ", ".join(pinyin)
        

    #Get etomology subfields if existing 
    #Initialize etymology variables as none to avoid reference errors
    etymology_type = None
    hint = None
    phonetic = None
    semantic = None

       
    etymology = char_info.get("etymology")
    if etymology is not None:
        etymology_type = etymology.get("etymology_type")
        hint = etymology.get("hint")
        etymology_type = etymology.get("type")
        if etymology_type =="pictophonetic":
            phonetic = etymology.get("phonetic")
            semantic = etymology.get("semantic")
            
            pass



    #Generate html string of the character data
    html_string = f'''
    <div class="char-info">
        <h2>{character}</h2>
        <p>Pinyin: {pinyin}</p>
        <p>Meaning: {meaning}</p>
        <p>Radical: {radical}</p>
        <p>Etymology Type: {etymology_type}</p>
        <p>Hint: {hint}</p>
        <p>Phonetic: {phonetic}</p>
        <p>Semantic: {semantic}</p>
    </div>'''

    return html_string

