import json, sys, os
import modules.trigger as trigger
import modules.intentclassification as nn
from modules.speak import speak
from modules.recognize import recognize
from modules.reminders import createReminder, readReminders

if "--train" in sys.argv:
    nn.train()
    exit()

if "--test" in sys.argv:
    createReminder()
    createReminder()
    readReminders()

try:
    while True:
        print("Recognizing!")
        question = recognize()
        if len(question) == 0:
            continue
        print("Question: " + question)
        response = json.loads(nn.run(question))
        if response["rnd_response"]:
            print("Answer: " + response["rnd_response"])
            speak(response["rnd_response"])
        if response["trigger"]:
            message = eval(f"trigger.{response['tag']}()")
            print("Answer: " + message)
            speak(message)

except KeyboardInterrupt:
    os.system("pip freeze > requirements.txt")
    print("Closing program!")