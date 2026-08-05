"""Takes data from the frequency_list.csv, and generates a copy with
newly generated fields"""
import asyncio

import pandas as pd
import field_generator
import json
import config
import get_char_data

def initialize_global_dataframe():
    print ("Initializing data frame...")
    #Make copy of original cards.csv as a dataframe file
    global df_cards
    #df_cards = pd.read_csv(config.FIELD_DATA_OUTPUT)
    df_cards = pd.read_csv(config.ORIGINAL_CARDS_PATH)
    return df_cards



#Add fields to a batch of the cards
async def add_ai_field_batch(df, start, batch_size):
    print("----------------")
    print(f"Generating new field batch for {start}-{start+batch_size} batch..." )
    new_fields_json = await field_generator.generate_fields(start, batch_size)

    
    new_fields = json.loads(new_fields_json)

    #Make a dictionary of rank to ID to prevent offset
    rank_to_index = dict(zip(df["Rank"], df.index))

    #add sata to data-frame
    for i, item in enumerate(new_fields["entries"]):
        rank = item["rank"]
        index = rank_to_index[rank]

        if index not in rank_to_index:
            print(f"WARNING: got rank {index}, not in dataframe — skipping")
            continue
        
        df.at[index, "meaning"] = item["meaning"]
        df.at[index, "sentence"] = item["sentence"]
        df.at[index, "sentence meaning"] = item["sentence_meaning"]
        df.at[index, "notes"] = item["notes"]


#Adds character info
def add_character_info(df):
    print ("Adding character info...")
    for index, word in enumerate(df["Word"]):
        df.at[index, "Character Info"] = get_char_data.word_char_analysis_html(word)
    print("Character info added!")

        

async def add_ai_fields_async(df, start, card_count):
    """Adds ai fields in batches to the dataframe for all the cards requested in the parameters
    Start at 0"""
    print (f"Adding fields for {start}-{card_count} in batches")
    tasks = []
    for card_index in range (start, start+card_count, config.prompt_batch_size):
        tasks.append(add_ai_field_batch (df, card_index, config.prompt_batch_size))

    await asyncio.gather(*tasks)





if __name__=="__main__":



    output_df = initialize_global_dataframe()

    asyncio.run(add_ai_fields_async(output_df, 150, 30))
    #add_character_info(output_df)
    output_df.to_csv(config.FIELD_DATA_OUTPUT, index=False, encoding="utf-8-sig")
    print("Data succesfully written!")

    pass

