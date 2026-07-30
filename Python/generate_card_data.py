import csv
from pathlib import Path
import config
import sentence_genorator

# This file generates the card data for the Anki deck. It reads from a Mandarin frequency list and creates a CSV file with the necessary fields for each card.

# Order of data set:
# "Frequency", "Word", "Pronunciation", "Meaning",
# "Sentence", "Sentence pronunciation",
# "Sentence meaning", "Notes", "Breakdown"

BASE_DIR = Path(__file__).resolve().parent.parent
CARDS_PATH = BASE_DIR / "Data" /"cards.csv"
FREQUENCY_LIST_PATH = BASE_DIR / "Data" / "frequency_list.csv"
WORDS_LIST_PATH =  BASE_DIR / "Data" / "words_list.txt"

# Extract data from the frequency list and write it to a new CSV file with the required fields for Anki cards.

def generate_card_data():
    print("Generating card data")
    # Create CSV file of the cards
    with open(CARDS_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(config.fields)
        for i in range(3995):  # Adjust the range as needed to limit the number of cards generated
            # Extract data from the frequency list
            #Extract data from the frequency list
            with open(FREQUENCY_LIST_PATH, "r", encoding="utf-8-sig") as d:
                reader = csv.reader(d)
                next(reader)  # Skip header row
                data = list(reader)
                row = data[i]

                frequency = row[0]
                word_traditional = row[1]
                word = row[2]
                pronunciation = row[3]
                meaning = row[4]


            #Generate epty feilds for the remaining columns
            sentence = ""  
            sentence_pronunciation = ""
            sentence_meaning = ""
            notes = ""
            breakdown = ""

            #write the data to the CSV file
            writer.writerow([frequency, word, word_traditional, pronunciation, meaning, sentence, sentence_pronunciation, sentence_meaning, notes, breakdown])


#Generate list of card data from the frequency list and generate a sentance for each card using OpenAI's API. The sentance will be in the target language and will use the word in context. The sentance will be generated using the word, pronunciation, and meaning of the word.
def generate_wordlist():
    full_word_list = []
    with open (CARDS_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.reader (f)
        header = next(reader)

        for row in reader:
            full_word_list.append(row[1])

    #Create file
    with open (WORDS_LIST_PATH, "w", encoding="utf-8-sig") as f:
        f.write(", ".join((full_word_list)))


generate_wordlist()