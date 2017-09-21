from flask import Flask, request

from bot_chucky.bot import BotChucky
from bot_chucky.utils import get_sender_id, get_user_text

token = 'YOUR_FACEBOOK_PAGE_TOKEN'

# Init a Flask app
app = Flask(__name__)

# Create an instance of Chucky object
# If you want to send weather information
# You need to set your Open Weather API key
bot = BotChucky(token,
                open_weather_token='YOUR_OPEN_WEATHER_TOKEN',
                news_api_key='YOUR_NEWSAPI_KEY')


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

                    # NOTICE: if you want send message to a user
                    # Use only one function.

                    # Send message to a user
                    bot.send_message(sender_id, text)

                    # Send weather information
                    bot.send_weather_message(sender_id, text)

                    # Send stackoverflow questions
                    bot.send_stack_questions(sender_id, title=text)

                    """
                    # Send List of News Sources
                    # Command: news list
                    """
                    if text[:9].lower() == 'news list':
                        bot.send_sources_list(sender_id, count=10, country="in")

                    """
                    # Send 5 latest news articles from source
                    # Command: news the-hindu
                    """
                    if text[:4].lower() == 'news':
                        source = text[5:]
                        bot.send_article(sender_id, source, 5)

                    """
                    # Send definitions of query word
                    # If not found send, not found message
                    # Command: define stereotype
                    """
                    if text[:6] == 'define':
                        bot.send_definition(sender_id, text[7:])

                if event.get('delivery'):
                    pass

    return 'ok', 200


if __name__ == '__main__':
    app.run(debug=True)
