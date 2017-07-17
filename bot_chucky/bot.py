import requests as r
from .constants import API_URL
from .errors import BotChuckyInvalidToken, BotChuckyTokenError
from .helpers import (FacebookData, SoundCloudData,
                      StackExchangeData, TwitterData,
                      WeatherData, NewsData,
                      DictionaryData,)


class BotChucky:
    def __init__(self, token, open_weather_token=None,
                 tw_consumer_key=None, tw_consumer_secret=None,
                 tw_access_token_key=None, tw_access_token_secret=None,
                 soundcloud_id=None, news_api_key=None):
        """
        :param token: Facebook Token, required
        :param open_weather_token: not required
        :param tw_consumer_key: Twitter Consumer Key, not required
        :param tw_consumer_secret: Twitter Consumer Secret, not required
        :param tw_access_token_key: Twitter Access Token Key, not required
        :param tw_access_token_secret: Twitter Access Token Secret,
        not required
        :param gmail_credentials_path: Google Mail API Credentials Path,
        not required, default 'gmail-credentials.json'
        :param tw_access_token_secret: Twitter Access Token Secret,
        not required
        :param headers: Set default headers for the graph API, default
        :param fb: Instace of FacebookData class, default
        :param weather: Instace of WeatherData class, default
        :param twitter: Instance of TwitterData class, default
        :param soundcloud_id: SoundCloud Access Token, not required
        :param stack: Instance of StackExchange class, not required
        :param news_api_key: newsapi.org key, not required
        :param news: Instance of NewsData class, default
        """
        self.token = token
        self.open_weather_token = open_weather_token
        self.params = {'access_token': self.token}
        self.headers = {'Content-Type': 'application/json'}
        self.fb = FacebookData(self.token)
        self.weather = WeatherData(open_weather_token)
        self.twitter_tokens = {
            'consumer_key': tw_consumer_key,
            'consumer_secret': tw_consumer_secret,
            'access_token_key': tw_access_token_key,
            'access_token_secret': tw_access_token_secret
        }
        self.twitter = TwitterData(self.twitter_tokens)
        self.soundcloud_id = soundcloud_id
        self.soundcloud = SoundCloudData(self.soundcloud_id)
        self.stack = StackExchangeData()
        self.news = NewsData(news_api_key)
        self.dictionary = DictionaryData()

    def send_message(self, id_: str, text):
        """
        :param  id_: User facebook id, type -> str
        :param text: some text, type -> str
        """
        data = {
            'recipient': {'id': id_},
            'message': {'text': text}
        }
        message = r.post(API_URL, params=self.params,
                         headers=self.headers, json=data)
        if message.status_code is not 200:
            return message.text

    def send_attachment(self, id_: str,  attachment):
        """
        :param  id_: User facebook id, type -> str
        :param attachment: Attach any image
        """
        data = {
            'recipient': {'id': id_},
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'url': attachment
                    }
                }
            }
        }
        message = r.post(API_URL, params=self.params,
                         headers=self.headers, json=data)
        if message.status_code is not 200:
            return message.text

    def send_weather_message(self, id_: str, city_name: str):
        """
        :param id_: User facebook id, type -> str
        :param city_name: Find weather by city name
        :return send_message function, send message to a user,
        with current weather
        """

        if self.open_weather_token is None:
            raise BotChuckyTokenError('Open Weather')

        weather_info = self.weather.get_current_weather(city_name)
        if weather_info['cod'] == 401:
            error = weather_info['message']
            raise BotChuckyInvalidToken(error)

        if weather_info['cod'] == '404':
            msg = f'Sorry I cant find information ' \
                  f'about weather in {city_name}, '

            return self.send_message(id_, msg)

        description = weather_info['weather'][0]['description']

        code = weather_info['weather'][0]['icon']
        icon = f'http://openweathermap.org/img/w/{code}.png'

        msg = f'Current weather in {city_name} is: {description}\n'

        self.send_message(id_, msg)
        self.send_attachment(id_, icon)

    def send_tweet(self, status: str):
        """
        :param status: Tweet text, type -> str
        """
        if not all(self.twitter_tokens.values()):
            raise BotChuckyTokenError('Twitter')

        reply = self.twitter.send_tweet(status)

        if reply['success']:
            return f'I have placed your tweet with status \'{status}\'.'

        return f'Twitter Error: {reply["detail"]}.'

    def send_soundcloud_message(self, id_: str, artist: str):
        """
        :param id_: User facebook id, type -> str
        :param artist: artist to search for, type -> str
        :return send_message function
        """
        if not self.soundcloud_id:
            raise BotChuckyTokenError('SoundCloud')
        result = self.soundcloud.search(artist)

        if result['success']:
            tracks_from_artist = list(result['tracks'].title)
            msg = f'SoundCloud found {result["artists"]}, \n' \
                  f'Track Listing: {tracks_from_artist}'
            return self.send_message(id_, msg)

        msg = f'SoundCloud Error: {result["detail"]}'

        return self.send_message(id_, msg)

    def send_stack_questions(self, id_, **kwargs):
        """
        :param id_: a User id
        :param kwargs: find by title='Update Django'
                               tag='Django'
        :return: send_message function, send message to a user with questions
        """
        msg = 'I can\'t find questions for you;( try again'
        answers = self.stack.get_stack_answer_by(**kwargs)

        if answers:
            if len(answers) > 2:
                msg = f'I found questions for you, links below\n\n ' \
                      f'Question 1: {answers[0]}\n' \
                      f'Question 2: {answers[1]}'
                return self.send_message(id_, msg)

            if len(answers) == 1:
                msg = f'I found question for you, link below\n\n ' \
                      f'Question: {answers[0]}'
                return self.send_message(id_, msg)
        else:
            return self.send_message(id_, msg)

    def send_article(self, id_: str, source, count, order=None):
        """
        ## This function gets #count articles from 'source' sorted by 'order'
        :param id_: facebook user id
        :param source: Source of news article
        :param: count: Number of articles to be sent
        :order: latest, top, or popular
        """
        if self.news.get_key() is None:
            raise BotChuckyTokenError("Articles are available only with the newsapi.org key")

        count = min(count, 10)

        data = self.news.get_article(source, count, order)

        for article in data:
            message = f"\nBy {article['author']}\n"
            message += f"Title:{article['title']}\n"
            message += f"Desc: {article['description']}\n"
            message += f"Read more: {article['url']}"
            self.send_message(id_, message)

    def send_sources_list(self, id_: str,
                          count,
                          category=None,
                          language=None,
                          country=None):
        """
        :param id_: facebook user id
        :param count: # of sources user wants to list
        :param category: #Main category in which the source posts articles
        :language: Understandable -> en, de or fr
        :country: Country in which the source belongs
        """
        count = min(count, 20)

        data = self.news.get_sources(count, category, language, country)

        message = "Codes for sources:\n"

        for i in range(len(data)):
            message += f"{i+1}. {data[i]['id']}: {data[i]['name']}\n"

        self.send_message(id_, message)

    def send_definition(self, id_: str, word: str):
        """
        :param id_: facebook user id
        :param word: query word whose definitions are to be found
        """
        data = self.dictionary.get_meaning(word)

        message = ''
        for index, definition in enumerate(data):
            message += f'{index+1}) {definition}\n'

        if not data:
            message = f'Couldn\'t find definition for {word}'

        self.send_message(id_, message)
