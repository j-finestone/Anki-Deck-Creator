#Generate sentance using OpenAI's API.
import openai
import config
import pandas as pd
import misc_functions
import asyncio

# Set up the OpenAI API client
client = openai.AsyncOpenAI()


def generate_prompts (start, batch_size):
    """Generates prompts from the columns in the Data/deck.csv
    requesting a Json file of new sentence, note, and breakdown
    for each word in the batch. """



    #Load the CSV file into a pandas DataFrame
    df = pd.read_csv(config.ORIGINAL_CARDS_PATH)
    words = df[["Word", "Rank", "Pronunciation"]]



    end_of_batch = start+batch_size
    
    #Ensure input values are within range
    if start>len(words["Word"]) or len(words["Word"])<0:
        raise Exception("starting word is out of range of word list")    
    if config.core_vocab_length > len(words["Word"])-1:
        raise Exception("Word list is too small or could not be found")
    if start+batch_size>(len(words["Word"])-1):
        end_of_batch = len(words["Word"])-1

    #Assign core vocab
    if config.core_vocab_length>end_of_batch:
        core_vocab = misc_functions.df_to_txt(words, 0, start)
    else:
        core_vocab = misc_functions.df_to_txt(words, 0, config.core_vocab_length)
 



    #Add suplimental words to the core_vocab words list if the batch small

    #Target Words
    target_words = misc_functions.df_to_txt(words, start, end_of_batch)
 


    #Get recent vocab
    if end_of_batch < config.recent_vocab_length:
        recent_vocab = misc_functions.df_to_txt(words, 0, start)

        #Add suplimentry vocab for early words
        recent_vocab+="\n".join(config.scaffolding_words)
 
    else:
        recent_vocab = misc_functions.df_to_txt(words, end_of_batch-config.recent_vocab_length, start-1)


    max_clauses = 2


    
    system_prompt = config.system_prompt(core_vocab)
    user_prompt = config.user_prompt(target_words, recent_vocab, max_clauses)

    return {"system_prompt": system_prompt, "user_prompt":user_prompt}




async def generate_fields(start, batch_size):

    """#Bypass this for testing:
    with open(config.GPT_JSON_OUTPUT_PATH, encoding="utf-8") as f:
        print ("Outputing prebaked data")
        return str("\n".join(f.readlines()))"""

    prompts = generate_prompts(start, batch_size)

    """#Save prompt to file for debuging
    with open(config.PROMPT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"System Prompt:\n{prompts['system_prompt']}\n\nUser Prompt:\n{prompts['user_prompt']}")
    return"""

    #print(f"Generating fields for {start}-{start+batch_size}...")

    #request response
    response = await client.chat.completions.create (
        model=config.model,
        reasoning_effort=config.reasoning_effort,
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
                                    "meaning": {"type": "string"},
                                    "sentence":{"type": "string"},
                                    "sentence_meaning": {"type": "string"},
                                    "notes": {"type": "string"},
                                }, 
                                "required":["rank", "meaning", "sentence", "sentence_meaning", "notes"],
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
    print (f"Response recived for {start}-{start+batch_size}...")
    response = response.choices[0].message.content
    return response


