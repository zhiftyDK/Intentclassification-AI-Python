import shutil, os, json
import modules.intentclassification as nn
from modules.speak import speak
from modules.studieplus import getAssignments

# Remove pycache folder on run
pycachepath = "./modules/__pycache__"
if os.path.exists(pycachepath):
    shutil.rmtree(pycachepath)
os.system("pip freeze > requirements.txt")

response = json.loads(nn.run("What assignments do i currently have?"))
print(response)
if response["trigger"]:
    print(response)
else:
    speak(response["rnd_response"])

# nn.train()