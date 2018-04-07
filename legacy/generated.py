import markovify
from json import dumps

nModel = markovify.Text.from_json(open("markov.json").read())  # reading a trained model from a JSON file and using that instead

def generateSentence():
    global nModel
    str = ""
    for i in range(20):  # Generates 20 sentences
        try:
            str += nModel.make_short_sentence(500, max_retries=200).replace("\\n", "\n")
        except:
            pass
    return str
file = open("twoThousandGenerated.json", "w").write(dumps([generateSentence() for i in range(2000)]))
file.close()
