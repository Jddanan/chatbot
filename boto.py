"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import requests

GREETING = ['hi', 'hello', 'yo', 'hey']
GREETING_USER = ["my name is", "i am", "i'm", 'im']
JOKE_LIST = ["What is the difference between a snowman and a snowwoman? Snowballs.",
             "In a boomerang shop: 'I'd like to buy a new boomerang please. Also, can you tell me how to throw the old one away?",
             "What's the difference between my ex and the titanic? The titanic only went down on 1,000 people.",
             "How do you keep an idiot in suspense?"
             ]
SWEAR_WORD = ["arse", "ass", "asshole", "bastard", "bitch", "bollocks", "fuck", "crap", "cunt", "shit", "motherfucker",
              "twat", "goddamn", "connard", "pd", "encul", "nique", "con"
              ]
SWEAR_ANSWER = ["Watch your language !!",
                "After all I've done for you?",
                "That's not nice"
                ]
LYRICS = [
    "I see a little silhouetto of a man\n"
    "Scaramouche, Scaramouche, will you do the Fandango\n"
    "Thunderbolt and lightning, very, very fright'ning me\n"
    "(Galileo) Galileo, (Galileo) Galileo, Galileo figaro magnifico\n"
    "(I'm just a poor boy, nobody loves me)\n"
    "He's just a poor boy from a poor family\n"
    "Spare him his life from this monstrosity\n"
    "Easy come, easy go, will you let me go?\n"
    "Bismillah! No, we will not let you go\n"
    "(Let him go) Bismillah! We will not let you go\n"
    "(Let him go) Bismillah! We will not let you go\n"
    "(Let me go) Will not let you go\n"
    "(Let me go) Will not let you go\n"
    "(Let me go) Ah, no, no, no, no, no, no, no\n"
    "(Oh mamma mia, mamma mia) Mama mia, let me go\n"
    "Beelzebub has a devil put aside for me, for me, for me"
    ]


@route('/', method='GET')
def index():
    return template("chatbot.html")


def greeting():
    return "Hey !"


def get_name(name):
    split_name = name.split()
    if split_name[-1].lower() == "yoav" or split_name[-1].lower() == "aviram" or split_name[-1].lower() == "ariel":
        return "Hey {0}. How are you my favorite TA ?".format(split_name[-1])
    else:
        return "Hello {0}. How can I help you ?".format(split_name[-1])


def joke():
    return random.choice(JOKE_LIST)


def check_swear_word():
    return random.choice(SWEAR_ANSWER)


def sing():
    return LYRICS


def get_weather():
    api_address = "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=tel%20aviv"
    json_data = requests.get(api_address).json()
    weather_description = json_data['weather'][0]['description']
    weather_temperature = round(int(json_data['main']['temp']) - 273.15)
    return 'The weather in Tel Aviv is {0} and the temperature is {1} degree celsius'.format(weather_description, weather_temperature)


def dance():
    return 'YEAH SURE !!'


def out_of_range():
    return "Sorry, I don't understand, you can type 'detail' to check all my functionality"


def more_detail():
    return "Try typing keyword like 'dance', 'sing', 'joke', 'weather'"


def action(user_message):
    if any(x in user_message.lower() for x in GREETING_USER):
        return json.dumps({"animation": "excited", "msg": get_name(user_message)})
    elif "joke" in user_message:
        return json.dumps({"animation": "laughing", "msg": joke()})
    elif any(x in user_message.lower() for x in SWEAR_WORD):
        return json.dumps({"animation": "no", "msg": check_swear_word()})
    elif "sing" in user_message:
        return json.dumps({"animation": "takeoff", "msg": sing()})
    elif "dance" in user_message:
        return json.dumps({"animation": "dancing", "msg": dance()})
    elif "detail" in user_message:
        return json.dumps({"animation": "ok", "msg": more_detail()})
    elif "weather" in user_message:
        return json.dumps({"animation": "money", "msg": get_weather()})
    elif any(x in user_message.lower() for x in GREETING):
        return json.dumps({"animation": "inlove", "msg": greeting()})
    else:
        return json.dumps({"animation": "crying", "msg": out_of_range()})

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return action(user_message)


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
