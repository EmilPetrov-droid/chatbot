import json
from getpass import getpass  # For password masking

class User:
    def __init__(self):
        self.error_db = self.load_error_data()

    def load_error_data(self):
        try:
            with open("error_codes.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Could not load 'error_codes.json'.")
            return {}

    def get_error_response(self, brand, appliance_type, error_code):
        brand_errors = self.error_db.get(brand, {})
        appliance_errors = brand_errors.get(appliance_type, {})
        return appliance_errors.get(error_code.upper(), "Unknown error. Please contact support.")


class RegularUser(User):
    def request_error_info(self):
        brand = input("Enter the brand (e.g., Bosch, Samsung) or 'q' to quit: ").strip()
        if brand.lower() == "q":
            return None
        appliance_type = input("Enter the appliance type: ").strip().lower()
        error_code = input("Enter error code: ").strip().upper()
        return self.get_error_response(brand, appliance_type, error_code)


class RegisteredUser(User):
    def __init__(self):
        super().__init__()
        self.user_db = self.load_user_password_data()
        self.registered_error_db = self.load_registered_error_data()

    def load_user_password_data(self):
        try:
            with open("username_passwords.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Could not load 'username_passwords.json'.")
            return {}

    def load_registered_error_data(self):
        try:
            with open("registered_user_error_codes.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Could not load 'registered_user_error_codes.json'.")
            return {}

    def authenticate_user(self):
        attempts = 0
        while attempts < 3:
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            if self.user_db.get(username) == password:
                print("Login successful!")
                return True
            attempts += 1
            print(f"Invalid login attempt {attempts}/3")
        print("Too many failed login attempts. Exiting.")
        return False

    def request_error_info(self):
        brand = input("Enter the brand (e.g., Bosch, Samsung) or 'q' to quit: ").strip()
        if brand.lower() == "q":
            return None
        appliance_type = input("Enter the appliance type: ").strip().lower()
        error_code = input("Enter error code: ").strip().upper()
        brand_errors = self.registered_error_db.get(brand, {})
        appliance_errors = brand_errors.get(appliance_type, {})
        return appliance_errors.get(error_code, "Unknown error. Please refer to the service manual.")
