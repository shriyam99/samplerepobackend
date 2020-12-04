import sys
from flask import Flask
from flask_cors import CORS
from finalpythoncode import para

app = Flask(__name__)
CORS(app)

@app.route("/<int:dur>/<int:amt>")
def index(dur, amt):
    #duration = dur
    #amount = amt
    #run([sys.executable, 'finalpythoncode.py'])
    print(dur)
    print(amt)
    para(dur, amt)
    return "Hello"


if __name__=="__main__":
    app.run(debug=True)
