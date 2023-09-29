from os import path
from random import randint
from sys import exit as sys_exit

from PIL import Image

version = "2.1.3"


def calculate_header_size(width: int, height: int) -> int:
    return (width * height).bit_length()


def text_to_bits(message: str) -> str:
    message_bytes = message.encode("utf8")
    message_bits = "".join(format(byte, "08b") for byte in message_bytes)
    return message_bits


def bits_to_text(message_bits: str) -> str:
    bytes_list_str = [message_bits[i : i + 8] for i in range(0, len(message_bits), 8)]
    bytes_list = [int(chunk, 2) for chunk in bytes_list_str]
    bytes_obj = bytes(bytes_list)
    return bytes_obj.decode("utf8")


def get_pixel(image, x, y) -> tuple:
    if image.mode == "RGBA":
        r, g, b, a = image.getpixel((x, y))
    else:
        r, g, b = image.getpixel((x, y))
        a = None

    return (r, g, b, a)


def put_pixel(image, x, y, pixel):
    r, g, b, a = pixel

    if image.mode == "RGBA":
        image.putpixel((x, y), (r, g, b, a))
    else:
        image.putpixel((x, y), (r, g, b))


def update_pixel(pixel: tuple, bit: int) -> tuple:
    r, g, b, a = pixel

    if (r + g + b) % 2 != bit:
        channel = randint(1, 3)
        if channel == 1:
            r = r - 1 if r != 0 else r + 1
        elif channel == 2:
            g = g - 1 if g != 0 else g + 1
        else:
            b = b - 1 if b != 0 else b + 1

    return (r, g, b, a)


def write_bits(image, message_bits: int, start_position: int) -> None:
    width, _ = image.size
    for i in range(len(message_bits)):
        x, y = (i + start_position) % width, ((i + start_position) // width)

        pixel = get_pixel(image, x, y)
        pixel = update_pixel(pixel, int(message_bits[i]))
        put_pixel(image, x, y, pixel)


def write_header(image, message: str) -> None:
    width, height = image.size
    header_size = calculate_header_size(width, height)
    message_bits = text_to_bits(message)
    header = bin(len(message_bits))[2:]
    header_padded = header.zfill(header_size)
    write_bits(image, header_padded, 0)


def write_message(image, message: str) -> None:
    width, height = image.size
    header_size = calculate_header_size(width, height)
    message_bits = text_to_bits(message)
    write_bits(image, message_bits, header_size)


def open_image(image_path: str):
    try:
        assert path.exists(image_path)
    except AssertionError:
        sys_exit("Image file not found!")
    else:
        return Image.open(image_path)


def save_image(image) -> None:
    base_filename, extension = path.splitext(image.filename)
    image.save(base_filename + "_with_message.png")


def close_image(image) -> None:
    image.close()


def hide_message(image, message: str) -> None:
    width, height = image.size
    header_size = calculate_header_size(width, height)

    message_bits = text_to_bits(message)
    try:
        assert len(message_bits) <= width * height - header_size
        write_header(image, message)
        write_message(image, message)
        save_image(image)
    except AssertionError:
        print("Message too big for image size!")
    finally:
        close_image(image)


def read_bits(image, start_position: int, number_of_bits: int):
    width, height = image.size
    message = ""
    for i in range(number_of_bits):
        x, y = (i + start_position) % width, ((i + start_position) // width)

        r, g, b, a = get_pixel(image, x, y)
        if (r + g + b) % 2 == 1:
            message += "1"
        else:
            message += "0"
    return message


def read_header(image: str):
    width, height = image.size
    header_size = calculate_header_size(width, height)
    return read_bits(image, 0, header_size)


def read_message(image: str):
    header = read_header(image)
    header_size = len(header)
    message_bits_size = int(header, 2)
    message_bits = read_bits(image, header_size, message_bits_size)
    close_image(image)
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
