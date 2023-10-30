import json
import math
from modules.speak import speak
from modules.recognize import recognize

def createReminder():
    speak("What should the reminder be?")
    message = recognize()

    with open("./data/reminders.json", "r+") as f:
        filedata = json.load(f)
        filedata["reminders"].append({
            "message": message
        })
        f.seek(0)
        json.dump(filedata, f, indent=4)
    speak(f"I have created the reminder: {message}")

def clearReminders():
    clearedData = {"reminders":[]}
    with open("./data/reminders.json", "w") as f:
        json.dump(clearedData, f, indent=4)

special = ['zeroth','first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelvth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth']
deca = ['twent', 'thirt', 'fourt', 'fift', 'sixt', 'sevent', 'eight', 'ninet']
def stringifyNumber(n):
    if n < 20:
        return special[n]
    if n%10 == 0:
        return deca[math.floor(n/10)-2] + 'ieth'
    return deca[math.floor(n/10)-2] + 'y-' + special[n%10]

def readReminders():
    with open("./data/reminders.json", "r+") as f:
        reminders = json.load(f)["reminders"]
        count = len(reminders)
        if count == 1:
            speak("You have one reminder")
            speak(f"The reminder is: {reminders[0]['message']}");
        elif count > 1:
            speak(f"You have {count} reminders")
            for i, reminder in enumerate(reminders):
                speak(f"The {stringifyNumber(i + 1)} reminder is: {reminder['message']}")