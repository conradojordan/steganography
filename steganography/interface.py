from os import path

import steganography


class Interface:
    HIDE_MESSAGE = "1"
    READ_MESSAGE = "2"

    @staticmethod
    def welcome():
        print(f"Welcome to steganography v{steganography.version}")

    @staticmethod
    def choose_mode():
        print("What would you like to do?")
        print("1 - Hide a message")
        print("2 - Read a message")
        while True:
            try:
                user_choice = input("Enter 1 or 2 to select option: ")
                assert user_choice in ["1", "2"]
                break
            except AssertionError:
                print("Invalid option! Please try again...")
        return user_choice

    @staticmethod
    def choose_image():
        while True:
            try:
                filename = input("Enter file path (with extension): ")
                assert path.exists(filename)
                break
            except AssertionError:
                print(f"Image '{filename}' not found! Please try again...")
        return filename

    @staticmethod
    def choose_message():
        return input("Enter message to hide: ")

    @staticmethod
    def print_message(message):
        print("<<<<< Message found below >>>>>")
        print(message)
        print("<<<<< End of message >>>>>")
