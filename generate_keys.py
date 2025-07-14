import pickle
from pathlib import Path

import streamlit_authenticator as stauth

# 1. User Data

names = ["Admin", "Guillermo Anhuaman", "Aldo Urata", "Sayuri Mattos"]
usernames = ["admin","guillermo_201", "aldo_101", "sayuri_301"]
passwords = ["abc123", "guille201", "aldo101", "sayuri301"]
#passwords = ["xxx", "xxx", "xxx", "xxx"]

# 2. Hash each password

hasher = stauth.Hasher()
hashed_passwords = [hasher.hash(pw) for pw in passwords]

# 3. Construct credentials dictionary

credentials = {"usernames":{}}

for uname, name, pw in zip(usernames, names, hashed_passwords):
    credentials["usernames"][uname] = {
        "name": name,
        "password": pw
    }


file_path = Path(__file__).parent / "hashed_passwords.pkl"
with open(file_path, "wb") as file:
    pickle.dump(credentials, file)