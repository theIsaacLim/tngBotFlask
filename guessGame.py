from flask import Flask, render_template, Markup, url_for
from random import choice, seed
from markovify import Text

seed()
lines = open("firstLines.json").read()
print("lines read")

file = open("guessGame.json")
chainJson = file.read()
file.close()
print("json read")

generator = Text.from_json(chainJson)
print("generated")

true = """
    <div id="aQuestion">
        <blockquote>
            <p><a id="number">$. </a>*</p>
        </blockquote>
        <center>
            <button  id="trueButton" onclick="raiseButton($)">This quote is  taken straight from the TV series!</button>
            <button onclick="lowerButton($)" id="falseButton">This quote is generated by a Markov Chain</button>
        </center>
    </div>
"""

false = """
    <div id="aQuestion">
        <blockquote>
            <p><a id="number">$. </a>*</p>
        </blockquote>
        <center>
            <button  id="trueButton" onclick="lowerButton($)">This quote is  taken straight from the TV series!</button>
            <button onclick="raiseButton($)" id="falseButton">This quote is generated by a Markov Chain</button>
        </center>
    </div>
"""

def substitute(realOrNot, actualQuote, num):
    global true, false

    num = str(num)

    if realOrNot:
        rVal = true
        rVal = rVal.replace("*", actualQuote).replace("$", num)

    else:
        rVal = false
        rVal = rVal.replace("*", actualQuote).replace("$", num)

    return rVal

app = Flask(__name__)


@app.route('/')
def generateQuiz():
    global template
    dict = {True: [], False: []}

    for i in range(5):
        done = False
        while not done:
            try:
                sentence = generator.make_short_sentence(140, max_retries=200).replace("\\n", "\n")
                dict[False].append(sentence)
                print(sentence)
                done = True
            except:
                print("b")
                pass

    for i in range(5):
        dict[True].append(choice(lines.split("\n")))

    finishedSubstitution = ""

    for i in range(10):
        myChoice = choice([True, False])
        finishedSubstitution += substitute(myChoice, choice(dict[myChoice]), i+1)

    #_template = _template.replace("@", finishedSubstitution)
    return render_template("tngTemplate.html", content=Markup(finishedSubstitution), fontUrl="https://fonts.googleapis.com/css?family=Saira+Extra+Condensed", cssUrl="../style.css")

app.run()
