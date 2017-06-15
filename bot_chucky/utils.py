""" Utils functions"""


def get_sender_id(data):
    """
    :param data: receives facebook object
    :return: User id which wrote a message, type -> str
    """
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    return sender_id


def get_user_text(data):
    """
    :param data: receives facebook object
    :return: User text, type -> str
    """
    text = data['entry'][0]['messaging'][0]['message']['text']
    return text


def get_tweet_text(tweet):
    """
    :param tweet: Twitter Status Object
    :return: Tweet text, type -> str
    """
    id_ = tweet.id
    user_screen_name = tweet.user.screen_name
    status = tweet.text
    tweet_url = f'https://twitter.com/{user_screen_name}/status/{id_}'

    text = f'User: {user_screen_name},\r\n\r\n' \
           f'Status: {status},\r\n\r\n' \
           f'Url: {tweet_url}'

    return text
