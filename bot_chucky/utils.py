""" Utils functions"""


def get_sender_id(data: dict) -> str:
    """
    :param data: receives facebook object
    :return: User id which wrote a message, type -> str
    """
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    return sender_id


def get_user_text(data: dict) -> str:
    """
    :param data: receives facebook object
    :return: User text, type -> str
    """
    text = data['entry'][0]['messaging'][0]['message']['text']
    return text
