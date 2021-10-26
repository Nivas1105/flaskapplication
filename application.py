from flask import Flask
application = Flask(__name__)
@app.route("/")
def index():
    return "Test from Git"
if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
