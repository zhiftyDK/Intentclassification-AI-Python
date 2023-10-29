def joke():
    import random
    with open("./data/jokes.txt", "r") as f:
        return random.choice(f.readlines()).strip()

def time():
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The time is currently {current_time}"

def weather():
    import requests
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Silkeborg&units=metric&appid=f4e80e2071fcae0bd7c122d2f82fd284")
    tempValue = response.json()["main"]["temp"]
    nameValue = response.json()["name"]
    descValue = response.json()["weather"][0]["main"]
    return f"In {nameValue} it is {str(tempValue)[:2]} degrees and {descValue}"

def assignments():
    return "I dont know check for yourself!"