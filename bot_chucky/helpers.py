""" Helper classes """

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
