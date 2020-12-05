import sys
from flask import Flask
from flask_cors import CORS
from finalpythoncode import para

app = Flask(__name__)
CORS(app)

@app.route("/<int:dur>/<int:amt>")
def index(dur, amt):
    print(amt)
    print(dur)
    para(dur, amt)
    return "data_fetched"

if __name__=="__main__":
    app.run(debug=True)
