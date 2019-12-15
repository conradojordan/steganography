from math import log as math_log
from random import randint
from math import floor
from PIL import Image
from os import path


def hide_message():
    while True:
        try:
            filename = input("Enter file name (with extension): ")
            message_image = Image.open(filename)
            break
        except FileNotFoundError:
            print(f"Image {filename} not found! Please try again...")

    base_filename, extension = path.splitext(filename)
    width, height = message_image.size
    header_size = floor(math_log(width * height, 2)) + 1

    while True:
        try:
            message = input("Enter message to hide: ")
            assert len(bytes(message, "utf8")) * 8 <= width * height - header_size
            break
        except AssertionError:
            print(f"Message too big for image size! Please try again...")

    message_bytes = bytes(message, "utf8")
    message_int = int.from_bytes(message_bytes, byteorder="big")
    message_bits = bin(message_int)[2:]
    message_bits = message_bits.zfill(len(message_bytes) * 8)
    message_bits_size = len(message_bits)
    print(f"Size of message is {message_bits_size} bits.")

    ## Write header
    header = bin(message_bits_size)[2:]
    header = header.zfill(header_size)
    for i in range(header_size):
        x, y = i % width, (i // width)
        if message_image.mode == "RGBA":
            r, g, b, a = message_image.getpixel((x, y))
        else:
            r, g, b = message_image.getpixel((x, y))
        if (r + g + b) % 2 != int(header[i]):
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

    ## Write message
    for i in range(message_bits_size):
        x, y = (i + header_size) % width, ((i + header_size) // width)
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

    message_image.save(base_filename + "_with_message.png")
    message_image.close()
    print(f"Message succesfully hidden in '{base_filename}_with_message.png'")


def read_message():
    while True:
        try:
            filename = input("Enter file name (with extension): ")
            message_image = Image.open(filename)
            break
        except FileNotFoundError:
            print(f"Image '{filename}' not found! Please try again...")

    base_filename, extension = path.splitext(filename)
    width, height = message_image.size
    header_size = floor(math_log(width * height, 2)) + 1

    ## Read header
    header = ""
    for i in range(header_size):
        x, y = i % width, (i // width)
        if message_image.mode == "RGBA":
            r, g, b, a = message_image.getpixel((x, y))
        else:
            r, g, b = message_image.getpixel((x, y))
        if (r + g + b) % 2 == 1:
            header = header + "1"
        else:
            header = header + "0"
    message_size_bits = int(header, 2)

    ## Read message
    message_bits = ""
    for i in range(message_size_bits):
        x, y = (i + header_size) % width, ((i + header_size) // width)
        if message_image.mode == "RGBA":
            r, g, b, a = message_image.getpixel((x, y))
        else:
            r, g, b = message_image.getpixel((x, y))
        if (r + g + b) % 2 == 1:
            message_bits = message_bits + "1"
        else:
            message_bits = message_bits + "0"

    print(f"Message found: {message_bits}")
    print(f"Translating message...")
    message_bits_size = len(message_bits)
    message_int = int(message_bits, 2)
    message_bytes = message_int.to_bytes((message_bits_size // 8), byteorder="big")
    message = message_bytes.decode("utf8")
    print("Hidden message:")
    print(message)


if __name__ == "__main__":
    print("Welcome to steganography v2.0")
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

    if user_choice == "1":
        hide_message()
    else:
        read_message()
