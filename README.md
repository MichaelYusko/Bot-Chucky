# Bot-Chucky

Python3.6+ bot which is able to work with Facebook Messenger

[![Build Status](https://travis-ci.org/MichaelYusko/Bot-Chucky.svg?branch=master)](https://travis-ci.org/MichaelYusko/Bot-Chucky)
[![PyPI version](https://badge.fury.io/py/bot_chucky.svg)](https://badge.fury.io/py/bot_chucky)

Installation
=================================
```
pip install bot_chucky  
```

Recommendations
=================================
If you want test your application on  a local machine
 * [Install ngrok](https://ngrok.com/download) - will enable an `HTTPS` route for you
 * [Open Weather Map](https://openweathermap.org/api) - create a `TOKEN`, then you will be able to send weather information to a user
 * [Create facebook messenger app](https://developers.facebook.com)
 * [Get Newsapi Key](https://newsapi.org) - Get an api key, to be able to send news information.


Usage
=================================
Chucky provides:


 * Send weather information:


    ![weather information](https://user-images.githubusercontent.com/13191999/27537700-a042c802-5a7d-11e7-8c24-e05052d23f89.jpg)

 * Send StackOverflow questions:


    ![stackoverflow information](https://user-images.githubusercontent.com/13191999/27538451-ab80a790-5a80-11e7-8406-7558d614708a.jpg)
 * Send message
 * Send tweets


    ![tweets](https://user-images.githubusercontent.com/13191999/27773421-fb2525e0-5f81-11e7-9854-384effdf9ce4.png)
    ![tweets](https://user-images.githubusercontent.com/13191999/27773423-fc0e8604-5f81-11e7-8690-25a66ee87511.png)
 * Search SoundCloud, based on artist
 * Send news articles and list of sources


    ![sources_list](https://user-images.githubusercontent.com/15676805/27868476-6ab124b0-61ba-11e7-9f3e-a925e9ec6671.jpg)
    ![articles](https://user-images.githubusercontent.com/15676805/27868483-6f273336-61ba-11e7-8cc5-4173709a50ab.jpg)  

 * Search for definitions of a word  

    ![found_definitions](https://user-images.githubusercontent.com/15676805/28264397-6511fd84-6b08-11e7-95f7-068049c0c61f.PNG)
	![not_found](https://user-images.githubusercontent.com/15676805/28264398-657e9b7e-6b08-11e7-8328-9d1a6b23dcca.PNG)  

the list will be expanded.

Examples
=================================
 * [Flask example](https://github.com/MichaelYusko/Bot-Chucky/blob/master/examples/flask_example.py)
 * [Custom Generator example](https://github.com/MichaelYusko/Bot-Chucky/blob/master/examples/custom_generator_example.py)


Documentation
=================================
 * http://bot-chucky.readthedocs.io/

Contribution
=================================
1. Fork or clone repository
2. Create a branch such as **feature/bug/refactor** and send a Pull request

P.S. Feel free to make a PR;)
