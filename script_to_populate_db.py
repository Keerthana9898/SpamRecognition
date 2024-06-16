import requests
import json

URL = "http://localhost:8000/api/v1/"

def register():
    registration = URL + "registeration"
    payload = {
                "phone_number": "9765112340",
                "username": "User007",
                "password": "Password@123"
            }
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", registration, headers=headers, data=json.dumps(payload))

    print(response.text)

def login():
    login = URL + "login"
    payload = {
                "phone_number": "9765112340",
                "username": "User007",
                "password": "Password@123"
            }
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", login, headers=headers, data=json.dumps(payload))
    print(response.text)
    response = response.json()
    return response["access"]

def populate_global_db(token):
    globaldb = URL + "globaldb"
    names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Ansh", "Reyansh", "Aryan", "Shaurya", "Ayaan", "Rohan", "Krish", "Om", "Dhruv", "Kabir", "Advait", "Ishan", "Samarth", "Kian", "Laksh", "Yash", "Rudra", "Aaryan", "Manan", "Aaradhya", "Aanya", "Diya", "Anaya", "Ira", "Saanvi", "Kiara", "Pari", "Navya", "Ishita", "Meera", "Myra", "Riya", "Siya", "Anika", "Kavya", "Gauri", "Lavanya", "Tanya", "Aditi", "Zara", "Sneha", "Radhika", "Trisha", "Nidhi"]
    num = '98765432'
    phone_numbers = [num +str(i)+str(j) for i in range(5) for j in range(10)]

    for i in range(50):
        payload = {
                    "name": names[i],
                    "phone_number": phone_numbers[i]
                }
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
        }

        response = requests.request("POST", globaldb, headers=headers, data=json.dumps(payload))

        print(response.status_code)


register()
token = login()
populate_global_db(token)
