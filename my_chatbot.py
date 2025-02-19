""" /appliance_chatbot/
│── main.py  # Main script
│── user_classes.py  # Contains all user-related classes
│── error_codes.json  # Public error codes
│── registered_user_error_codes.json  # Registered user error codes
│── username_passwords.json  # User authentication data
"""

from user_classes import RegularUser, RegisteredUser  # Import the classes
import time

def get_greeting():
    current_hour = int(time.strftime('%H'))  # Extracting the Hour Part

    # Determine the greeting based on the hour of the day
    if current_hour < 12:
        return "Good Morning! Hi!"
    elif current_hour < 16:
        return "Good Afternoon! Hi!"
    elif current_hour < 20:
        return "Good Evening! Hello!"
    else:
        return "Late Night! Hello!"

def main():
    print(get_greeting())
    print("Welcome to the Appliance Troubleshooting Chatbot!")
    user_type = input("Are you a registered technician? (y/n): ").strip().lower()

    if user_type == "y":
        user = RegisteredUser()
        if not user.authenticate_user():
            return  # Exit if login fails
    else:
        user = RegularUser()

    while True:
        response = user.request_error_info()
        if response is None:
            break  # User chose to quit
        print("Bot:", response)


if __name__ == "__main__":
    main()
