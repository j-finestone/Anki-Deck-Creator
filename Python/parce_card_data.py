import csv
import config
import pypinyin



# Extract data from the frequency list and write it to a new CSV file with the required fields for Anki cards.
#(Rank, Word, Pronunciation)

def generate_card_data():
    print("Generating card data")
    # Create CSV file of the cards with the rank and 

    #Add basic info to cards from frequency list
    with open (config.FREQUENCY_LIST_PATH, "r", encoding="utf-8") as f:

        lines = f.readlines()
        for rank, line in enumerate(lines):
            line = line.strip()
            #Skip headers
            if rank==0:
                continue
            
            #add pronunciation to the line based on the charaacter
            pronunciation = pypinyin.pinyin(line)
            pronunciation = "".join([item[0] for item in pronunciation])
            lines[rank] = f'{rank},{line},"{pronunciation}"\n'


        
    with open (config.ORIGINAL_CARDS_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


generate_card_data()