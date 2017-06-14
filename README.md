# Bot-Chucky

Python bot which able to work with messenger of facebook

[![Build Status](https://travis-ci.org/MichaelYusko/Bot-Chucky.svg?branch=master)](https://travis-ci.org/MichaelYusko/Bot-Chucky)
[![PyPI version](https://badge.fury.io/py/bot_chucky.svg)](https://badge.fury.io/py/bot_chucky)

Installation
=================================
```
pip install bot_chucky  
```

Recommendations
=================================
If you want test your application on local machine
 * [Install ngrok](https://ngrok.com/download) - will make `HTTPS` for you 
 * [Open Weather Map](https://openweathermap.org/api) - create a `TOKEN` you will  be able to send weather information to a user
 

Usage
=================================
Chucky provide the next thigs:

 * Send message
 * Send weather information
 * Send tweets
 
the list will be expanded.

### Flask Example
```python
from flask import Flask, request
from bot_chucky.bot import BotChucky
from bot_chucky.utils import get_sender_id, get_user_text

token = 'YOUR_FACEBOOK_PAGE_TOKEN'

# Init a Flask app
app = Flask(__name__)

# Create an instance of Chucky object
# If you want to send weather information
# You need to set your Open Weather API key
bot = BotChucky(
    token,
    open_weather_token='YOUR_OPEN_WEATHER_TOKEN',
    tw_consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
    tw_consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET'
    tw_access_token_key = 'YOUR_TWITTER_ACCESS_TOKEN_KEY'
    tw_access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'
)


@app.route('/', methods=['GET'])
def handle_verification():
    # Verify your facebook PAGE.
    return request.args['hub.challenge']


@app.route('/', methods=['POST'])
def handle_messages():
    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            for event in entry.get('messaging'):
                if event.get('message'):
                
                    # Get a user id
                    sender_id = get_sender_id(data)
                    
                    # Get a user text
                    text = get_user_text(data)
                    
                    # Send message with weather information to the user
                    bot.send_message(sender_id, city)
                    
                    # Send weather information
                    # Where 'text' is name of city
                    bot.send_weather_message(sender_id, text)
                    
                if event.get('delivery'):
                    pass
                
    return 'ok', 200


@app.route('/tweet', methods=['POST'])
def send_tweet():
    data = request.json
    if data['status']:
        return (bot.send_tweet(data['status']), 200

if __name__ == '__main__':
    app.run(debug=True)
```

Contribution
=================================
1. Fork or clone repository
2. Create a branch such as **feature/bug/refactor** and send a Pull request

P.S. Feel free to make a PR;)
