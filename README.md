# steganography

This repository contains a program to hide and read text messages in image files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

The only prerequisite are Python 3.6 or higher, the "Pillow" image manipulation library and "pytest" for testing. To install dependencies run:

```
pip install -r requirements.txt
```

### Running

Simply run `python main.py` to use the command line interface or use the following commands:

##### Hiding a message
```
python Steganography.py hide <image_path> "<message>"
```
##### Reading a message
```
python Steganography.py read <image_path>
```

### Testing

To test run `pytest` while in the main directory of the repository.


## Built With

* [Pillow](https://pillow.readthedocs.io/en/stable/) - A python image manipulation library
* [pytest](https://docs.pytest.org/en/latest/) - Python testing framework


## Authors

* **Conrado Jordan** - [GitHub](https://github.com/conradojordan/)


## License

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE](LICENSE) file for details.
