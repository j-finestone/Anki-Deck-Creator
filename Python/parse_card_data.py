import csv
import config
import pypinyin



# Extract data from the frequency list and write it to a new CSV file with the required fields for Anki cards.
#(Rank, Word, Pronunciation)

def generate_card_data():
    """Generatres a cards.cvs file to the Input Data directory from 
    raw_frequency_list.csv that contains rank, and pronunciation fields"""
    print("Generating card data") 

    #Add basic info to cards from frequency list
    with open (config.FREQUENCY_LIST_PATH, "r", encoding="utf-8") as f:

        lines = f.readlines()
        for rank, line in enumerate(lines):
            line = line.strip()
            #Generates Header
            if rank==0:
                lines[0] = "Rank,Word,Pronunciation\n"
                continue
            
            #add pronunciation to the line based on the charaacter
            pronunciation = pypinyin.pinyin(line)
            pronunciation = "".join([item[0] for item in pronunciation])
            lines[rank] = f'{rank},{line},"{pronunciation}"\n'


        
    with open (config.ORIGINAL_CARDS_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

