""" Exception classes """


class BotChuckyTokenError(Exception):
    def __init__(self, api_name):
        """
        :param api_name: Api Name to show error for
        """
        self._api_name = api_name

    def __str__(self):
        return f'Seems like you missing add'\
               f' \'{self._api_name}\' token to the ChuckyBot class'


class BotChuckyInvalidToken(Exception):
    pass
