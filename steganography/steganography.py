from os import path
from random import randint
from sys import exit as sys_exit

from PIL import Image

version = "2.1.2"


def calculate_header_size(width, height):
    return (width * height).bit_length()


def text_to_bits(message):
    message_bytes = message.encode("utf8")
    message_bits = "".join(format(byte, "08b") for byte in message_bytes)
    return message_bits


def bits_to_text(message_bits):
    bytes_list_str = [message_bits[i : i + 8] for i in range(0, len(message_bits), 8)]
    bytes_list = [int(chunk, 2) for chunk in bytes_list_str]
    bytes_obj = bytes(bytes_list)
    return bytes_obj.decode("utf-8")


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


def write_header(message_image, message):
    width, height = message_image.size
    header_size = calculate_header_size(width, height)
    message_bits = text_to_bits(message)
    header = bin(len(message_bits))[2:]
    header_padded = header.zfill(header_size)
    write_bits(message_image, header_padded, 0)


def write_message(message_image, message):
    width, height = message_image.size
    header_size = calculate_header_size(width, height)
    message_bits = text_to_bits(message)
    write_bits(message_image, message_bits, header_size)


def open_image(image_path):
    try:
        assert path.exists(image_path)
    except AssertionError:
        sys_exit("Image file not found!")
    else:
        return Image.open(image_path)


def save_image(message_image):
    base_filename, extension = path.splitext(message_image.filename)
    message_image.save(base_filename + "_with_message.png")


def close_image(message_image):
    message_image.close()


def hide_message(message_image, message):
    width, height = message_image.size
    message_bits = text_to_bits(message)
    header_size = calculate_header_size(width, height)
    try:
        assert len(message_bits) <= width * height - header_size
        write_header(message_image, message)
        write_message(message_image, message)
        save_image(message_image)
    except AssertionError:
        print("Message too big for image size!")
    finally:
        close_image(message_image)


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


def read_header(message_image):
    width, height = message_image.size
    header_size = calculate_header_size(width, height)
    return read_bits(message_image, 0, header_size)


def read_message(message_image):
    header = read_header(message_image)
    header_size = len(header)
    message_bits_size = int(header, 2)
    message_bits = read_bits(message_image, header_size, message_bits_size)
    close_image(message_image)
    try:
        message = bits_to_text(message_bits)
    except:
        sys_exit("Error: unable to find message in image!")
    return message


if __name__ == "__main__":
    import sys

    if sys.argv[1] in ["--version", "-v"]:
        print(f"Steganography v{version}")
    elif sys.argv[1] == "read":
        print(read_message(open_image(sys.argv[2])))
    elif sys.argv[1] == "hide":
        hide_message(open_image(sys.argv[2]), sys.argv[3])
    else:
        print("Wrong usage! Run one of the comands below:")
        print(f"python {path.basename(__file__)} read <image_path>")
        print(f'python {path.basename(__file__)} hide <image_path> "<message>"')
