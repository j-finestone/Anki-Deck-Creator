import genanki
import card_creator



#Create Model (Defining the structure of the notes)
def create_final_file():
    print ("Creating model")
    my_model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        ],
        templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])

    #Create Deck
    print ("Creating deck")
    my_deck = genanki.Deck(
        2059400110,
        'Country Capitals')


    #Create note
    print("Creating notes")
    card_creator.add_notes(my_deck)



    #Export anki deck
    print ("Exporting deck")
    genanki.Package(my_deck).write_to_file('output.apkg')

    print ("Completed")