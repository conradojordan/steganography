from Steganography import Steganography
from Interface import Interface


if __name__ == "__main__":
    Interface.welcome()
    user_mode = Interface.choose_mode()
    user_image_path = Interface.choose_image()
    user_image = Steganography.open_image(user_image_path)

    if user_mode == "1":
        user_message = Interface.choose_message()
        Steganography.hide_message(user_image, user_message)
    else:
        hidden_message = Steganography.read_message(user_image)
        Interface.print_message(hidden_message)
