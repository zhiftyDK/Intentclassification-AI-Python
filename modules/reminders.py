import json
from modules.speak import speak
from time import sleep
from datetime import datetime
def createReminder(reminder):
    with open("data/reminders.json", "r+") as f:
        filedata = json.load(f)
        filedata["reminders"].append(reminder)
        f.seek(0)
        json.dump(filedata, f, indent=4)

def clearReminders():
    clearedData = {"reminders":[]}
    with open("data/reminders.json", "w") as f:
        json.dump(clearedData, f, indent=4)

while True:
    with open("data/reminders.json", "r") as f:
        filedata = json.load(f)
        for data in filedata["reminders"]:
            currenttime = datetime.now().time().strftime('%H:%M:00')
            remindertime = str(datetime.strptime(data["time"], '%H:%M').time())
            print(type(currenttime), type(remindertime))
            print(currenttime, remindertime)
            if currenttime == remindertime:
                print(data["msg"])
                speak(data["msg"])
    sleep(60)