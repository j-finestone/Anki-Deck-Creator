import genanki
import pandas
import config

#Create Model (Defining the structure of the notes)
def create_final_file(source_csv):
    print ("Creating model")
    model = genanki.Model(
    1607392319,
    "Mandarin Vocabulary",
    fields=[
        {'name': "Rank"},
        {'name': "Word"},
        {'name': "Pronunciation"},
        {'name': "Meaning"},
        {'name': "Sentence"},
        {'name': "Sentence Meaning"},
        {'name': "Notes"},
        {'name': "Character Info"},
        {'name': "Sentence Pronunciation"},
        {'name': "Word Ruby"},
    ],
    templates=[
        {
            'name': 'Recognition',
            'qfmt': '''
{{Word}}
''',
            'afmt': '''
{{FrontSide}}
<hr>

{{Pronunciation}}<br>
{{Meaning}}<br><br>

{{Sentence}}<br>
{{Sentence Pronunciation}}<br>
{{Sentence Meaning}}<br><br>

{{Notes}}<br><br>

{{Character Info}}
'''
        },
        {
            'name': 'Recall',
            'qfmt': '''
{{Meaning}}
''',
            'afmt': '''
{{FrontSide}}
<hr>

{{Word}}<br>
{{Pronunciation}}<br><br>

{{Sentence}}<br>
{{Sentence Pronunciation}}<br>
{{Sentence Meaning}}<br><br>

{{Notes}}<br><br>

{{Character Info}}
'''
        }
    ]
)

    # Read the CSV
    df = pandas.read_csv(source_csv, encoding="utf-8").fillna("")

    deck = genanki.Deck(1607392319, "Mandarin Vocabulary")

    for _, row in df.iterrows():
        note = genanki.Note(
            model=model,
            fields=[
                str(row["Rank"]),
                str(row["Word"]),
                str(row["Pronunciation"]),
                str(row["Meaning"]),
                str(row["Sentence"]),
                str(row["Sentence Meaning"]),
                str(row["Notes"]),
                str(row["Character Info"]),
                str(row["Sentence Pronunciation"]),
                str(row["Word Ruby"]),
            ]
        )

        deck.add_note(note)

    genanki.Package(deck).write_to_file(config.OUTPUT_DATA_DIR / "Mandarin Vocabulary.apkg")
    print("Creating final deck creted")

create_final_file(config.OUTPUT_DATA_DIR /  "finished notes.csv")