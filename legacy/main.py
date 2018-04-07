import markovify
from flask import Flask

nModel = markovify.Text.from_json(open("markov.json").read())  # reading a trained model from a JSON file and using that instead

def generateSentence():
    global nModel
    str = None
    while str == None:
        str = nModel.make_short_sentence(140, max_retries=200)
    return str
"""
    for i in range(20):  # Generates 20 sentences
        try:
            str += nModel.make_short_sentence(500, max_retries=200).replace("\\n", "\n")
        except:
            pass
    return str
"""

app = Flask(__name__)


@app.route('/')
def landing():
    return generateSentence().replace('\n', '<br>')

app.run()
