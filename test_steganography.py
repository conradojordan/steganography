from steganography import Steganography
import pytest


class TestSteganography:
    @pytest.mark.parametrize(
        "width, height, header_size", [(10, 20, 8), (1920, 1080, 21), (50, 50, 12)]
    )
    def test_calculate_header_size(self, width, height, header_size):
        assert Steganography.calculate_header_size(width, height) == header_size

    @pytest.mark.parametrize(
        "message, bits",
        [
            (
                "test message",
                "011101000110010101110011011101000010000001101101011001010111001101110011011000010110011101100101",
            ),
            (
                "统🙅Ȭ⚓",
                "111001111011101110011111111100001001111110011001100001011100100010101100111000101001101010010011",
            ),
            (" ", "00100000",),
        ],
    )
    def test_text_to_bits(self, message, bits):
        assert Steganography.text_to_bits(message) == bits

    @pytest.mark.parametrize(
        "bits, message",
        [
            (
                "011101000110010101110011011101000010000001101101011001010111001101110011011000010110011101100101",
                "test message",
            ),
            (
                "111001111011101110011111111100001001111110011001100001011100100010101100111000101001101010010011",
                "统🙅Ȭ⚓",
            ),
            ("00100000", " ",),
        ],
    )
    def test_bits_to_text(self, bits, message):
        assert Steganography.bits_to_text(bits) == message

    @pytest.mark.parametrize(
        "color_mode, message",
        [
            ("RGB", "This is a test message"),
            ("RGBA", "Test message"),
            ("RGB", "统🙅Ȭ⚓"),
            ("RGBA", "☃⚆♽ĨÍŝǤÑÏ⚃"),
            ("RGB", " "),
        ],
    )
    def test_hiding_and_reading_messages(self, color_mode, message):
        from PIL import Image

        img = Image.new(color_mode, (200, 200))

        Steganography.write_header(img, message)
        Steganography.write_message(img, message)

        assert Steganography.read_message(img) == message
