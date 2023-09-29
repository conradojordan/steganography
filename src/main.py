from sys import exit as sys_exit

from interface import Interface

import steganography

if __name__ == "__main__":
    Interface.welcome()
    user_mode = Interface.choose_mode()
    user_image_path = Interface.choose_image()
    user_image = steganography.open_image(user_image_path)

    if user_mode == Interface.HIDE_MESSAGE:
        user_message = Interface.choose_message()
        steganography.hide_message(user_image, user_message)

    elif user_mode == Interface.READ_MESSAGE:
        hidden_message = steganography.read_message(user_image)
        Interface.print_message(hidden_message)

    else:
        print("Invalid option, exiting...")
        sys_exit()
