import json, sys
import modules.trigger as trigger
import modules.intentclassification as nn
from modules.speak import speak
from modules.recognize import recognize

if "--train" in sys.argv:
    nn.train()
    exit()

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
    print("Closing program!")