"""
This is a helper code to encrypt plaintext according to the project guidelines. Enter the plaintext and the desired shift. Output is ciphertext.
"""

space_code_point = 96


def custom_ord(char):
    if char == ' ':
        return space_code_point
    else:
        return ord(char)


def custom_ascii_translation(ascii_value):
    if ascii_value == 96:
        return ' '
    else:
        return chr(ascii_value)


def shift_cipher_encrypt(plaintext, shift_value):
    # Function to decrypt a single character using a shift
    encrypted_text = ''
    for char in plaintext:
        encrypted_text += custom_ascii_translation(
            (custom_ord(char) + int(shift_value) - space_code_point) % 27 + space_code_point)

    return encrypted_text


def main():
    print("Enter the plaintext:")
    plaintext = input()
    print("Enter the shift:")
    shift = input()

    # Perform cryptanalysis and print the result
    encrypted_text = shift_cipher_encrypt(plaintext, shift)
    print(encrypted_text)


if __name__ == "__main__":
    main()
