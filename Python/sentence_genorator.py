#Generate sentance using OpenAI's API.
import openai
from pathlib import Path
import config

#get paths
BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_PATH = BASE_DIR / "Data" / "cards.csv"




def generate_sentence():

    #generate prompts
    core_vocab = []

    target_words = []
    recent_vocab = []
    max_clauses = 2
    
    system_prompt = config.system_prompt(core_vocab)
    user_prompt = config.user_prompt(target_words, recent_vocab, max_clauses)

    # Set up the OpenAI API client
    client = openai.OpenAI()
    #request response
    response = client.chat.completions.create (
        model="gpt-5-mini",
        messages = [
            {
                "role": "system",
                "content": config.system_prompt(),
            },
            
            {
                "role": "user",
                "content": config.user_prompt()
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
    return response.choices[0].message.content



if __name__ == "__main__":
    #print(generate_sentence())
    pass