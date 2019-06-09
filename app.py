from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to GitBot"

@app.route("/sms", methods=['POST'])
def sms_reply():
    
    msg = request.form.get('Body')
    sender = request.form.get('From')

    resp = MessagingResponse()
    resp.message(fetch_reply(msg,sender))
    

    return str(resp)

if __name__ == "__main__":
    app.run(port=5001,use_reloader = True)