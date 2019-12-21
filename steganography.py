from math import log as math_log
from random import randint
from math import floor
from PIL import Image
from os import path


class Steganography:
    @staticmethod
    def calculate_header_size(width, height):
        return floor(math_log(width * height, 2)) + 1

    @staticmethod
    def text_to_bits(message):
        message_bytes = bytes(message, "utf8")
        message_int = int.from_bytes(message_bytes, byteorder="big")
        message_bits = bin(message_int)[2:]
        message_bits_padded = message_bits.zfill(len(message_bytes) * 8)
        return message_bits_padded

    @staticmethod
    def bits_to_text(message_bits):
        message_bits_size = len(message_bits)
        message_int = int(message_bits, 2)
        message_bytes = message_int.to_bytes((message_bits_size // 8), byteorder="big")
        message = message_bytes.decode("utf8")
        return message

    @staticmethod
    def write_bits(message_image, message_bits, start_position):
        width, height = message_image.size
        for i in range(len(message_bits)):
            x, y = (i + start_position) % width, ((i + start_position) // width)
            if message_image.mode == "RGBA":
                r, g, b, a = message_image.getpixel((x, y))
            else:
                r, g, b = message_image.getpixel((x, y))
            if (r + g + b) % 2 != int(message_bits[i]):
                rgb = randint(0, 2)
                if rgb == 0:
                    r = r - 1 if r != 0 else r + 1
                elif rgb == 1:
                    g = g - 1 if g != 0 else g + 1
                else:
                    b = b - 1 if b != 0 else b + 1
            if message_image.mode == "RGBA":
                message_image.putpixel((x, y), (r, g, b, a))
            else:
                message_image.putpixel((x, y), (r, g, b))

    @staticmethod
    def write_header(message_image, message):
        width, height = message_image.size
        header_size = Steganography.calculate_header_size(width, height)
        message_bits = Steganography.text_to_bits(message)
        header = bin(len(message_bits))[2:]
        header_padded = header.zfill(header_size)
        Steganography.write_bits(message_image, header_padded, 0)

    @staticmethod
    def write_message(message_image, message):
        width, height = message_image.size
        header_size = Steganography.calculate_header_size(width, height)
        message_bits = Steganography.text_to_bits(message)
        Steganography.write_bits(message_image, message_bits, header_size)

    @staticmethod
    def save_image(message_image):
        base_filename, extension = path.splitext(message_image.filename)
        message_image.save(base_filename + "_with_message.png")

    @staticmethod
    def close_image(message_image):
        message_image.close()

    @staticmethod
    def hide_message(message_image, message):
        width, height = message_image.size
        message_bits = Steganography.text_to_bits(message)
        header_size = Steganography.calculate_header_size(width, height)
        try:
            assert len(bytes(message_bits, "utf8")) * 8 <= width * height - header_size
            Steganography.write_header(message_image, message)
            Steganography.write_message(message_image, message)
            Steganography.save_image(message_image)
        except AssertionError:
            print("Message too big for image size!")
        finally:
            Steganography.close_image(message_image)

    @staticmethod
    def read_bits(message_image, start_position, number_of_bits):
        width, height = message_image.size
        message = ""
        for i in range(number_of_bits):
            x, y = (i + start_position) % width, ((i + start_position) // width)
            if message_image.mode == "RGBA":
                r, g, b, a = message_image.getpixel((x, y))
            else:
                r, g, b = message_image.getpixel((x, y))
            if (r + g + b) % 2 == 1:
                message += "1"
            else:
                message += "0"
        return message

    @staticmethod
    def read_header(message_image):
        width, height = message_image.size
        header_size = Steganography.calculate_header_size(width, height)
        return Steganography.read_bits(message_image, 0, header_size)

    @staticmethod
    def read_message(message_image):
        header = Steganography.read_header(message_image)
        header_size = len(header)
        message_bits_size = int(header, 2)
        message_bits = Steganography.read_bits(
            message_image, header_size, message_bits_size
        )
        Steganography.close_image(message_image)
        return Steganography.bits_to_text(message_bits)


class Interface:
    @staticmethod
    def choose_mode():
        print("What would you like to do?")
        print("1 - Hide a message")
        print("2 - Read a message")
        while True:
            try:
                user_choice = input("Enter 1 or 2 to select option: ")
                assert user_choice in "12"
                break
            except AssertionError as err:
                print("Invalid option! Please try again...")
        return user_choice

    @staticmethod
    def choose_image():
        while True:
            try:
                filename = input("Enter file name (with extension): ")
                user_image = Image.open(filename)
                break
            except FileNotFoundError:
                print(f"Image '{filename}' not found! Please try again...")
        return user_image

    @staticmethod
    def choose_message():
        return input("Enter message to hide: ")


if __name__ == "__main__":
    print("Welcome to steganography v3.0")
    user_mode = Interface.choose_mode()

    with Interface.choose_image() as user_image:
        if user_mode == "1":
            user_message = Interface.choose_message()
            Steganography.hide_message(user_image, user_message)
        else:
            try:
                message = Steganography.read_message(user_image)
                print("<<<<< Message found below >>>>>")
                print(message)
                print("<<<<< End of message >>>>>")
            except:
                print("Error: unable to read message!")
