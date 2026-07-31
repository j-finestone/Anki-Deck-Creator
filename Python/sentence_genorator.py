#Generate sentance using OpenAI's API.
import openai
from pathlib import Path
import config
import pandas as pd

#get paths
BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_PATH = BASE_DIR / "Data" / "cards.csv"
DATA_PATH = BASE_DIR / "Data"


def generate_prompts (start, batch_size):
    """Generates prompts from the columns in the Data/deck.csv
    requesting a Json file of new sentence, note, and breakdown
    for each word in the batch. """



    #Load the CSV file into a pandas DataFrame
    df = pd.read_csv(CARDS_PATH)
    words = df["Word"]

    end_of_batch = start+batch_size
    #Ensure input values are within range
    if start>len(words) or len(words)<0:
        raise Exception("starting word is out of range of word list")    
    if config.core_vocab_length > len(words)-1:
        raise Exception("Word list is too small or could not be found")
    if start+batch_size>(len(words)-1):
        end_of_batch = len(words)-1

    #Assign core vocab
    core_vocab = words[start:config.core_vocab_length]

    #Add suplimental words to the target words list if the batch small
    if config.core_vocab_length<end_of_batch:
        core_vocab.append(config.scaffolding_words)

    target_words = words[start:end_of_batch]

    #Get recent vocab
    if end_of_batch < config.recent_vocab_length:
        recent_vocab = words[0 : start]
    else:
        recent_vocab = words[end_of_batch-config.recent_vocab_length : start-1]

    print (recent_vocab)
    max_clauses = 2


    
    system_prompt = config.system_prompt(core_vocab)
    user_prompt = config.user_prompt(target_words, recent_vocab, max_clauses)

    return {"system_prompt": system_prompt, "user_prompt":user_prompt}




def generate_sentence(start, batch_size):

    print ("Generating prompts...")
    prompts = generate_prompts(start, batch_size)

    print("Connecting with ChatGPT...")
    # Set up the OpenAI API client
    client = openai.OpenAI()
    #request response
    response = client.chat.completions.create (
        model="gpt-5-mini",
        messages = [
            {
                "role": "system",
                "content": prompts["system_prompt"],
            },
            
            {
                "role": "user",
                "content": prompts["user_prompt"]
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name":"anki_batch",
                "strict": True,
                "schema": {
                    "type":"object",
                    "properties": {
                            "entries": { "type": "array", "items": {
                                "type": "object", 
                                "properties": {
                                    "rank": {"type": "integer"},
                                    "sentence":{"type": "string"},
                                    "sentence_meaning": {"type": "string"},
                                    "notes": {"type": "string"},
                                    "breakdown": {"type":"string"}
                                }, 
                                "required":["rank", "sentence", "sentence_meaning", "notes", "breakdown"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required":["entries"], 
                    "additionalProperties": False
                    }
                }
            }
        )
    print ("Response recived...")
    return response.choices[0].message.content



if __name__ == "__main__":
    print("Saving prompts to file...")
    with open (DATA_PATH/"prompt file.txt", "w", encoding="utf-8") as f:
        prompts = generate_prompts(5, 5)
        f.writelines(prompts["system_prompt"])
        f.writelines(prompts["user_prompt"])
    pass