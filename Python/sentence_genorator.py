#Generate sentance using OpenAI's API.
import openai
import csv
from pathlib import Path

#get paths
BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_PATH = BASE_DIR / "Data" / "cards.csv"




def generate_sentence():
    # Set up the OpenAI API client
    client = openai.OpenAI()
    response = client.chat.completions.create (
        model="gpt-5-mini",
        messages = [
            {
                "role": "system",
                "content": "",
            },

            
            {
                "role": "user",
                "content": ""
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name":"anki_batch",
                "strict": True,
                "schema":{
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
                                "required":["sentence", "sentence_meaning", "notes", "breakdown"],
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