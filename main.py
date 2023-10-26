import shutil, os
import modules.intentclassification as nn

# Remove pycache folder on run
pycachepath = "./modules/__pycache__"
if os.path.exists(pycachepath):
    shutil.rmtree(pycachepath)
os.system("pip freeze > requirements.txt")

result = nn.run("See you later")
print(result)

# nn.train()