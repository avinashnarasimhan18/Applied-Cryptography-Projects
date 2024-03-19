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


def shift_cipher_decrypt(cipher_text, dictionary):
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
        sim = []
        for index in range(len(dictionary)):
            similarity_score = similarity(attempt, dictionary[index])
            sim.append(similarity_score)  # Store similarity score with plaintext
        highest_similarity_score = max(sim)
        if highest_similarity_score >= 0.25:
            return dictionary[sim.index(highest_similarity_score)]
        else:
            continue

    return None


def main():
    print("Enter the ciphertext:")
    ciphertext = input()

    # Provide the path to plaintext dictionary file
    plaintext_dictionary = [
        "unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
        "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
        "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
        "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
        "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
    ]

    # Perform cryptanalysis and print the result
    decrypted_text = shift_cipher_decrypt(ciphertext, plaintext_dictionary)
    print("My plaintext guess is:", decrypted_text)


if __name__ == "__main__":
    main()