""" Helper classes """

from collections import Callable
from urllib import parse

import facebook
import requests as r
import twitter

from bot_chucky.errors import BotChuckyError


class FacebookData:
    def __init__(self, token):
        """
        :param token: Facebook Page token
        :param _api: Instance of the GraphAPI object
        """
        self.token = token
        self._api = facebook.GraphAPI(self.token)

    def get_user_name(self, _id):
        """
        :param _id: find user object by _id
        :return: first name of user, type -> str
        """
        if not isinstance(_id, str):
            raise ValueError('id must be a str')
        user = self._api.get_object(_id)
        return user['first_name'] if user else None


class WeatherData:
    """
    Class which collect weather data
    """
    def __init__(self, api_token):
        """
        :param api_token: Open Weather TOKEN
        """
        self.token = api_token

    def get_current_weather(self, city_name):
        """
        :param city_name: Open weather API, find by city name
        :return dictionary object with information

        for example:

        {'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky'}]}
        """
        api_url = f'http://api.openweathermap.org' \
                  f'/data/2.5/weather?q={city_name}&APPID={self.token}'

        info = r.get(api_url).json()
        return info


class TwitterData:
    """
    Class which collect Twitter data
    """
    def __init__(self, tokens):
        """
        :param tokens: Dictionary of all tokens
                       [consumer_key, consumer_secret, access_token_key, access_token_secret]
                       required to initialize the Twitter Api
        """
        self.api = twitter.Api(
            consumer_key=tokens['consumer_key'],
            consumer_secret=tokens['consumer_secret'],
            access_token_key=tokens['access_token_key'],
            access_token_secret=tokens['access_token_secret']
        )

    def send_tweet(self, status):
        if status:
            try:
                return {
                    'success': True,
                    'tweet': self.api.PostUpdate(status)
                }
            except twitter.error.TwitterError as TWE:
                return {
                    'detail': TWE.message[0]['message'],
                    'success': False
                }

        return {
            'success': False,
            'detail': 'Status text is empty.'
        }

    def get_home_tweets(self):
        try:
            return {
                'success': True,
                'tweets': self.api.GetHomeTimeline()
            }
        except twitter.error.TwitterError as TWE:
            return {
                'detail': TWE.message[0]['message'],
                'success': False
            }

    def get_user_tweets(self, screen_name):
        try:
            return {
                'success': True,
                'tweets': self.api.GetUserTimeline(screen_name=screen_name)
            }
        except twitter.error.TwitterError as TWE:
            return {
                'detail': TWE.message[0]['message'],
                'success': False
            }


class StackExchangeData:
    """
    Class which collect StackExchange data
    """
    _default_parameters = {
        'order': 'desc',
        'sort': 'activity',
        'site': 'stackoverflow',
    }

    def get_stack_answer_by(self, **kwargs):
        """
        :param kwargs: create a query by arguments
                       for example:
                            tag='Python', will be search by tag
                            title='Update Python', will be search by title
                            and etc.

        :return: an array with links
        """
        if len(kwargs) > 1:
            raise BotChuckyError('The argument must be one')

        for key in kwargs.keys():
            query = kwargs.get(key)
            self._default_parameters.update({key: query})

            if not isinstance(query, str):
                raise TypeError(f'{query} must be a string')

        encode_query = parse.urlencode(self._default_parameters)

        stack_url = f'https://api.stackexchange.com/2.2/search/advanced?' \
                    f'{encode_query}'

        questions = r.get(stack_url).json()
        links = [obj['link'] for obj in questions['items']]
        return links


class ChuckyCustomGenerator(Callable):
    """
    warnings:: Class not completed yet
    description:: Class will allow to add customs unique words/functions,
                  If user want to create own realization of the bot,
                  he should use the CustomGenerator class.
    future:: It will be imported into BotChucky class.

    :Example:
          # first create custom functions
          def hello_python():
            return 'Hello Python!'

          def news_python():
            return 'Python news!'

          my_config = {
            '#Python': hello_python
          }

          # Create instance of ChuckyGenerator
          bot = ChuckyCustomGenerator()
          bot.config = my_config

          # If we get some text from messenger
          # And we pass an argument to the bot

          my_message = 'Hello I want to learn #Python'
          bot(my_message)

          The bot will return the result of a custom function: 'Hello Python!'

          Update our config, and add topics:

          # Add topics
          # For example
          # If we got text with #Python and 'bye' word
          my_config = {
            '#Python': {'news': news_python}
           }
          bot.config = my_config

          my_message = 'Hey #Python, and send me your news'
          bot(my_message)

          bot will return the result of a custom function: 'Python news!'
    """
    config = {}

    def exclude_param(self, *args):
        if len(args) > 1:
            raise ValueError('Argument must be one')
        text = args[0].split()
        return text

    @property
    def config_keys(self):
        return self.config.keys()

    def check_and_run(self, text):
        func = None
        for key in self.config_keys:
            if key not in text:
                msg = 'Sorry could you repeat please?'
                return msg
            if key in text:
                func = self.config.get(key)
            if isinstance(func, Callable):
                return func()
            else:
                for topic in self.config.get(key):
                    if topic in text:
                        func = self.config[key][topic]
                        return func()

    def __call__(self, *args, **kwargs):
        text = self.exclude_param(*args)
        return self.check_and_run(text)

    def __str__(self):
        return f'{self.__class__.__name__}' \
               f'(Your config: {self.config})'
