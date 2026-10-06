import table_generator
import parse_card_data

if __name__ == "__main__":

    #Execute this function to create a cards.csv file from a raw_frequency_list.csv file
    parse_card_data.generate_card_data()

    #Change start and amount to input how many words should fields be generated for. 
    #HIGHLY RECOMENDED TO START SMALL AS A SAMPLE BATCH
    start = 1 #Which is the first word index for which the program generated fields 
    amount = 2500 #How many cards from that point on for which it will it genrerate fields 

    #Generate fields and save them to "Final Output.csv"
    table_generator.genarate_fields(start, amount) 

