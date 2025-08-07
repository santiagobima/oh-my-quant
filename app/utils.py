import csv
import os

def check_user_credentials(username, password):
    filepath = os.path.join('data', 'users.csv')
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

