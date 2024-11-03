import os
import sys
import json
import requests
import subprocess

class PythonOS:
    def __init__(self):
        self.config_file = "pythonos_config.json"
        self.default_accounts = {
            "root": {"password": "1234", "level": "administrator"},
            "guest": {"password": "guest", "level": "guest"}
        }
        self.users = self.load_config()
        self.logged_in_user = None
        self.built_in_apps = {
            "pythonosfetch": self.pythonosfetch,
            "uac": self.uac
        }
        self.appstore_url = "https://sctech.netlify.app/pythonos_appstore.json"
        self.app_folder = "./pythonos_apps/"
        os.makedirs(self.app_folder, exist_ok=True)

    def run(self):
        self.show_banner()
        self.login()
        self.main_menu()
        self.save_config()

    def show_banner(self):
        try:
            subprocess.run(["figlet", "PythonOS"], check=True)
        except FileNotFoundError:
            print("PythonOS (Install figlet for a fancy banner)")

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return self.default_accounts

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def login(self):
        print("Welcome to PythonOS!")
        username = input("Username: ")
        password = input("Password: ")

        if username in self.users and self.users[username]["password"] == password:
            self.logged_in_user = username
            print(f"Welcome, {username}! Account Level: {self.users[username]['level']}")
        else:
            print("Invalid credentials.")
            sys.exit()

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Run Apps")
            print("2. App Store")
            print("3. Manage Apps")
            print("4. Account Settings")
            print("5. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                self.run_app()
            elif choice == "2":
                self.app_store()
            elif choice == "3":
                self.manage_apps()
            elif choice == "4":
                self.account_settings()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Try again.")
        self.save_config()

    def run_app(self):
        print("\nAvailable Apps:")
        for app in self.built_in_apps:
            print(f"- {app} (Built-in)")

        downloaded_apps = [app[:-3] for app in os.listdir(self.app_folder) if app.endswith(".py")]
        for app in downloaded_apps:
            print(f"- {app} (Downloaded)")

        app_choice = input("Enter the name of the app to run: ")

        if app_choice in self.built_in_apps:
            self.built_in_apps[app_choice]()
        elif app_choice in downloaded_apps:
            self.run_downloaded_app(app_choice)
        else:
            print("App not found.")

    def run_downloaded_app(self, app_name):
        app_path = os.path.join(self.app_folder, f"{app_name}.py")
        if os.path.exists(app_path):
            with open(app_path, "r") as f:
                app_code = f.read()
            print(f"Running {app_name}...")
            exec(app_code, {"__name__": "__main__"})
        else:
            print("App not found.")

    def app_store(self):
        try:
            response = requests.get(self.appstore_url)
            appstore = response.json()
            print("\nApp Store:")
            for app, info in appstore.items():
                print(f"- {app}: {info['description']} (Download URL: {info['download_url']})")

            app_choice = input("Enter the name of the app to download: ")
            if app_choice in appstore:
                self.download_app(app_choice, appstore[app_choice]["download_url"])
            else:
                print("App not found.")
        except requests.RequestException:
            print("Error fetching the app store data.")

    def download_app(self, app_name, download_url):
        try:
            response = requests.get(download_url)
            with open(os.path.join(self.app_folder, f"{app_name}.py"), "w") as file:
                file.write(response.text)
            print(f"{app_name} downloaded successfully!")
        except requests.RequestException:
            print("Error downloading the app.")

    def manage_apps(self):
        print("\nManage Apps:")
        print("Downloaded Apps:")
        for app in os.listdir(self.app_folder):
            if app.endswith(".py"):
                print(f"- {app[:-3]}")

        app_choice = input("Enter the name of the app to delete (or type 'back' to go back): ")
        if app_choice != "back":
            self.delete_app(app_choice)

    def delete_app(self, app_name):
        if app_name == "uac":
            print("Cannot delete the UAC app.")
            return
        app_path = os.path.join(self.app_folder, f"{app_name}.py")
        if os.path.exists(app_path):
            os.remove(app_path)
            print(f"{app_name} deleted successfully.")
        else:
            print("App not found.")

    def account_settings(self):
        print("\nAccount Settings:")
        print("1. Change Password")
        print("2. User Account Control (UAC)")
        print("3. Add New User")
        choice = input("Choose an option: ")

        if choice == "1":
            self.change_password()
        elif choice == "2":
            self.uac()
        elif choice == "3":
            self.add_user()
        else:
            print("Invalid choice.")

    def add_user(self):
        if self.users[self.logged_in_user]["level"] != "administrator":
            print("Access denied. Only administrators can add new users.")
            return
        username = input("Enter new username: ")
        if username in self.users:
            print("User already exists.")
            return
        password = input("Enter password for the new user: ")
        level = input("Enter user level (administrator, normal, guest): ")
        if level not in ["administrator", "normal", "guest"]:
            print("Invalid user level.")
            return
        self.users[username] = {"password": password, "level": level}
        print(f"User '{username}' added successfully.")

    def change_password(self):
        if self.logged_in_user:
            new_password = input("Enter new password: ")
            self.users[self.logged_in_user]["password"] = new_password
            print("Password changed successfully.")
        else:
            print("No user logged in.")

    def uac(self):
        if self.users[self.logged_in_user]["level"] == "administrator":
            print("UAC - User Account Control:")
            for user, details in self.users.items():
                print(f"{user}: Level - {details['level']}")
            user_to_modify = input("Enter username to change level (or 'back' to return): ")
            if user_to_modify in self.users:
                new_level = input("Enter new level (administrator, normal, guest): ")
                if new_level in ["administrator", "normal", "guest"]:
                    self.users[user_to_modify]["level"] = new_level
                    print(f"{user_to_modify}'s level updated to {new_level}.")
                else:
                    print("Invalid level.")
            elif user_to_modify != "back":
                print("User not found.")
        else:
            print("Access denied. Administrator rights required.")

    def pythonosfetch(self):
        print(f"PythonOS v1.0 - Logged in as {self.logged_in_user}")
        print(f"Built-in Apps: {', '.join(self.built_in_apps.keys())}")
        print(f"Downloaded Apps: {', '.join(os.listdir(self.app_folder))}")


# Run the OS
os_simulator = PythonOS()
os_simulator.run()
