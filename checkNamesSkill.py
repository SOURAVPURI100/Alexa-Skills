import json

def lambda_handler(event, context):
    
   if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.736af5f8-7af6-459e-915c-185196650664"):
        raise ValueError("Invalid Application ID")
   if event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
   elif event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
   elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
   

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetMessage":
        return get_message(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_launch(launch_request, session):
    return get_welcome_response()
    
def on_session_ended(session_ended_request, session):
    print ("Ending session.")

def get_welcome_response():
    session_attributes = {}
    card_title = "Name"
    speech_output = "Welcome to What Alexa Thinks about my name skill. " 

    reprompt_text = "Please ask me for what Do I think about your name"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "BART - Thanks"
    speech_output = "Thank you for using the What Alexa thinks about my Name skill. Bye!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))
def get_message(intent):
    session_attributes = {}
    card_title = "Names System Status"
    reprompt_text = ""
    should_end_session = False
    nameValue = intent["slots"]["name"]["value"]
    if(len(nameValue) > 2):
        speech_output = nameValue + " "+ fetch_answer(nameValue)
    else:
        speech_output = "Name seems to be too short or I don't understand well."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

    
#  Define the function to genenare Alexa answer based on name

def fetch_answer(name):
    # Create a set to form unique messages
    messageSet = set()
    name = str(name)
    
    if (name.startswith("div")):
        return "is my owner. I cannot bad-mouth about him. He is very generous"
    # Build first message
    value1 = ord(name[0])
    nameLen = len(name) 
    value2 = ord(name[nameLen -1])
    message = get_user_message((value1 + value2) % 22)
    messageSet.add(message)
    output = message
    
    # Build second message
    value1 = ord(name[1])
    value2 = ord(name[nameLen -2])
    while True:
        message = get_user_message((value1 + value2) % 22)
        if(message in messageSet):
            value2 = value2 +1
        else:
            break
    messageSet.add(message)
    output = output + ". " + name + " "+ message
    
    value3 = (ord(name[2]))
    # Build third message
    while True:   
        message = get_user_message((value3) % 22)
        if(message in messageSet):
            value3 = value3 +1
        else:
            break
    output = output + ". " + name + " "+ message
    
    return output
     

#  Dictionary items for messages
def get_user_message(id):
    return {
        0: "looks like he's got a hidden secret! HAHAHA!",
        1: "seems like a nice guy",
        2: "is smart and intelligent! HAHAHA!",
        3: "seems like a naughty fellow",
        4: "seems like he cries a lot",
        5: "I don't like you",
        6: "is a funny guy. One time he asked me can I play a lullaby for him",
        7: "I believe he is bored. Thats why he probably playing with me",
        8: "seems a little geeky to me",
        9: "Well, What can I say, Look at this guy and judge",
        10: "seems like a lonely soul to me. Don't worry you will be alright",
        11: "seems like a odd guy to me.",
        12: "seems a little anti-social",
        13: "I find you smart, someone who knows his things well",
        14: "is probably a computer programmer ",
        15: "hey, don't bother I have no intention to say bad things about you",
        16: "Hmmm... Let me think",
        17: "Hey, you seem like a guy who is social, friendly and party-rockstar",
        18: "you are someone who is allegric to alcohol",
        19: "you probably smoke, drink regularly. That's a calculated guess by the way",
        20: "What the hell man",
        21: "Better, If I don't say anything",
    }.get(id, "I think you are as smart as a kindergarten student")

#  Build output for alexa
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }