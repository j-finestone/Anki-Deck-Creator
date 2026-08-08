import table_generator

if __name__ == "__main__":

    #Change start and amount to input how many words should fields be generated for. 
    #HIGHLY RECOMENDED TO START SMALL AS A SAMPLE BATCH
    start = 1 #Which is the first word index for which the program generated fields 
    amount = 20 #How many cards from that point on for which it will it genrerate fields 

    #Generate fields and save them to "Final Output.csv"
    table_generator.genarate_fields(start, amount) 

