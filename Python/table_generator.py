"""Takes data from the frequency_list.csv, and generates a copy with
newly generated fields"""
import asyncio

import pandas as pd
import field_generator
import json
import config
import get_char_data
import misc_functions

def initialize_global_dataframe(path = config.ORIGINAL_CARDS_PATH):
    print ("Initializing data frame...")
    #Make copy of original cards.csv as a dataframe file
    global df_cards
    #df_cards = pd.read_csv(config.FIELD_DATA_OUTPUT)
    df_cards = pd.read_csv(path )
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
        
        df.at[index, "Meaning"] = item["meaning"]
        df.at[index, "Sentence"] = item["sentence"]
        df.at[index, "Sentence Meaning"] = item["sentence_meaning"]
        df.at[index, "Notes"] = item["notes"]


#Adds character info
def add_character_info(df):
    print ("Adding character info...")
    for index, word in enumerate(df["Word"]):
        df.at[index, "Character Info"] = get_char_data.word_char_analysis_html(word)
    print("Character info added!")

def add_pinyin_to_notes(df):
    #Adding pinyin to notes with ruby
    for index, word in enumerate(df["Word"]):
        df.at[index, "Notes"] = misc_functions.add_ruby(str(df.at[index, "Notes"]))
    print("Pinyin added to notes!")

    pass

def add_sentence_pronunciation(df):
    #Adding pronuncition to notes with ruby
    for index, word in enumerate(df["Word"]):
        df.at[index, "Sentence Pronunciation"] = misc_functions.add_ruby(str(df.at[index, "Sentence"]))
    print("Pinyin added to Sentences!")

    pass

def add_word_pinyin_ruby(df):
    #Adding pronuncition to notes with ruby
    for index, word in enumerate(df["Word"]):
        df.at[index, "Word Ruby"] = misc_functions.add_ruby(str(df.at[index, "Word"]))
    print("Ruby added to words!")

async def add_ai_fields_async(df, start, card_count):
    """Adds ai fields in batches to the dataframe for all the cards requested in the parameters
    Start at 0"""
    print (f"Adding fields for {start}-{start+card_count} in batches")
    tasks = []
    for card_index in range (start, start+card_count, config.prompt_batch_size):
        tasks.append(add_ai_field_batch (df, card_index, config.prompt_batch_size))

    await asyncio.gather(*tasks)






def genarate_fields(start, amount):
    """Generates all the fields that were in config.generated_fields. """

    #Initialize Pandas dataframe that will become the output
    output_df = initialize_global_dataframe(config.ORIGINAL_CARDS_PATH)

    if ("Meaning/Sentence/Sentence Meaning/Notes" in config.generated_fields):
        asyncio.run(add_ai_fields_async(output_df, start, amount ))
    else:
        raise Exception ("Must generate AI fields to run program")

    if "Notes Pinyin" in config.generated_fields:
        add_pinyin_to_notes(output_df)

    if "Sentence Pronunciation" in config.generated_fields:
        add_sentence_pronunciation(output_df)
    
    if "Word Pronunciation" in config.generated_fields:
        add_word_pinyin_ruby(output_df)

    if "Character Info" in config.generated_fields:
        add_character_info(output_df)
    #Save result to CSV
    output_df.to_csv(config.FINAL_OUTPUT, index=False, encoding="utf-8-sig")
    print("Data succesfully written!")



    pass

