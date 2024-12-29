#include <iostream>
#include <string>
#include <vector>

using namespace std;

// The message space provided in the Project 1 directions
const string MESSAGE_SPACE = " abcdefghijklmnopqrstuvwxyz";


// The dictionary provided in the Project 1 directions
vector<string> dictionary = {"unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit", 
    "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
    "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
    "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
    "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"};

// Function checks if a string (sub_string) is a sub string of another string (main_string)
bool is_substring(const std::string &main_string, const std::string &sub_string)
{
  int i = 0;
  int j = 0;
  while (i < main_string.length() && j < sub_string.length())
  {
    if (main_string[i] == sub_string[j])
    {
      j++; // Found a matching character, advance in the substring
    }
    i++; // Always advance in the main string
  }

  return j == sub_string.length(); // Did we match all characters of the substring?
}

// This function applies the decryption given a string message and a key
string decrypt_scheme(const int key, const string &message)
{
  string output_text = "";
  for (int i = 0; i < message.length(); ++i)
  {
    output_text += MESSAGE_SPACE[(MESSAGE_SPACE.find(message[i]) + (MESSAGE_SPACE.length() - key)) % MESSAGE_SPACE.length()];
  }
  return output_text;
}

// This is the main logic of the code, tries every possible key until it finds
// a valid substring, ran some benchmarks for different values of prob_random_ciphertext
// and the code works at 100% accuracy and runs under 0.01 seconds for values up to 0.95
// full benchmarks in the write up
string break_code(const string &ciphertext, vector<string> dictionary)
{
  // trying every possible key value
  for (int k = 0; k < MESSAGE_SPACE.length(); ++k)
  {
    string decrypt_text = decrypt_scheme(k, ciphertext);
    for (int i = 0; i < dictionary.size(); ++i)
    {
      // first checks if the last characters are equal, because of the encryption scheme the last
      // character will never be a random character and therefore we can first check if they are
      // the same, both for efficiency and performance
      if (decrypt_text.back() == dictionary[i].back() && is_substring(decrypt_text, dictionary[i]))
      {
        return dictionary[i];
      }
    }
  }
  // if it is unable to find a matching plaintext for some reason it tries to output
  // the first plaintext in the dictionary
  return dictionary[0];
}

int main()
{
  string message;
  cout << "Enter the ciphertext:";
  getline(cin, message);
  cout << "My plaintext guess is:" << break_code(message, dictionary) << endl;
  return 0;
}
