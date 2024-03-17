from difflib import SequenceMatcher

space_code_point = 96


# Function to calculate the similarity ratio between two strings using the Levenshtein distance
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Custom function to return the ASCII value for characters including the space character which has been set to 96
def custom_ord(char):
    if char == ' ':
        return space_code_point
    else:
        return ord(char)


# Custom function to fetch the character it's ASCII value
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
        # Join each line into a single string, and remove any empty strings/lines
        dictionary = [' '.join(line.split()) for line in lines if line.strip()]

    # Function to decrypt a ciphertext message using a particular shift
    def decrypt_char(encrypted_text, shift_value):
        decrypted_text = ''
        for char in encrypted_text:
            # For each character, perform a backward shift with the shift value
            decrypted_text += custom_ascii_translation(
                (custom_ord(char) - shift_value - space_code_point) % 27 + space_code_point)
        return decrypted_text

    # Iterate through all possible shift values from 0 to 26
    for shift in range(0, 27):
        attempt = decrypt_char(cipher_text, shift)
        for plaintext in dictionary:
            sim = similarity(attempt, plaintext)
            # If the similarity between the plaintext guess and the plaintext in dictionary is >=90%, return that as the code's guess
            if sim >= 0.9:
                print("Predicted Shift is", shift)  # Debugger statement (To be removed later)
                return plaintext

    return None


def main():
    print("Enter the ciphertext:")
    ciphertext = input()

    # Provide the path to plaintext dictionary file
    plaintext_dictionary = "plaintext_dictionary.txt"  # Change this to the actual file path

    # Perform cryptanalysis and print the result
    decrypted_text = shift_cipher_decrypt(ciphertext, plaintext_dictionary)
    print("My plaintext guess is:", decrypted_text)


if __name__ == "__main__":
    main()
