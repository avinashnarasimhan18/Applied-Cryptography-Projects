from difflib import SequenceMatcher

space_code_point = 96


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

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


def shift_cipher_decrypt(cipher_text, plaintext_dictionary):
    # Load the plaintext dictionary
    with open(plaintext_dictionary, 'r') as file:
        # Read the file and split it into lines
        lines = file.read().splitlines()
        # Join each line into a single string, and remove any empty strings
        dictionary = [' '.join(line.split()) for line in lines if line.strip()]

    # Function to decrypt a single character using a shift
    def decrypt_char(encrypted_text, shift_value):
        decrypted_text = ''
        for char in encrypted_text:
            decrypted_text += custom_ascii_translation(
                (custom_ord(char) - shift_value - space_code_point) % 27 + space_code_point)
        return decrypted_text

    for shift in range(0, 27):
        attempt = decrypt_char(cipher_text, shift)
        for plaintext in dictionary:
            sim = similarity(attempt, plaintext)
            if sim >= 0.9:
                print("Predicted Shift is", shift) # Debugger statement to be removed later
                return plaintext

    return None


def main():
    print("Enter the ciphertext:")
    ciphertext = input()

    # Provide the path to your plaintext dictionary file
    plaintext_dictionary = "plaintext_dictionary.txt"  # Change this to the actual file path

    # Perform cryptanalysis and print the result
    decrypted_text = shift_cipher_decrypt(ciphertext, plaintext_dictionary)
    print("My plaintext guess is:", decrypted_text)


if __name__ == "__main__":
    main()
