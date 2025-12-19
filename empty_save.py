import os
import shutil

def empty_save():
    if os.path.exists("./save"):
        shutil.rmtree("./save")
        os.mkdir("./save")

# empty_save()