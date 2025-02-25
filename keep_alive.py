from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def main():
  return "Your bot is alive!"

def run():
    port = int(os.environ.get("PORT")) 
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    server = Thread(target=run)
    server.start()
