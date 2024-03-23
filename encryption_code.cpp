#include <iostream>
#include <string>
#include <random>

using namespace std;

const string MESSAGE_SPACE = " abcdefghijklmnopqrstuvwxyz";

// Included for testing purposes:
// Function to perform the cipher encryption
string encrypt_scheme(const int key, const string& message, const double prob_of_random_ciphertext) {

    random_device rd;
    mt19937 generator(rd());
    uniform_real_distribution<double> distribution(0.0,1.0);
    uniform_int_distribution<int> intdistribution(0, MESSAGE_SPACE.length()-1);

    string ciphertext = "";
    int ciphertext_pointer = 0;
    int message_pointer = 0;
    int num_rand_characters = 0;

    while (ciphertext_pointer < message.length() + num_rand_characters) {
        double coin_value = distribution(generator);

        if (prob_of_random_ciphertext <= coin_value) {
            // Encryption using the key
            int new_char = (MESSAGE_SPACE.find(message[message_pointer]) + key) % MESSAGE_SPACE.length();
            ciphertext += MESSAGE_SPACE[new_char];
            message_pointer++;
        } else {
            // Insert random character
            int random_char = intdistribution(generator);
            ciphertext += MESSAGE_SPACE[random_char];
            num_rand_characters++;
        }

        ciphertext_pointer++;
    }

    return ciphertext;
}

int main(int argc, char *argv[]) {
  string message = argv[2];
  double prob;
  if (argc == 4){
    prob = stod(argv[3]);
  }else{
    prob = 0.30;
  }
  cout << encrypt_scheme(stoi(argv[1]), message, prob);
  return 0;
}
