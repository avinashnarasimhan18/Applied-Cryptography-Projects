from concrete.ml.deployment import FHEModelClient, FHEModelDev, FHEModelServer

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from copy import deepcopy

from concrete.ml.sklearn import LogisticRegression
from sklearn.datasets import load_breast_cancer
from concrete.ml.sklearn import XGBClassifier

import numpy as np

import os
import shutil

import time

from dataclasses import dataclass
from shutil import copyfile

# NETWORK class used to transfer files between:
# Dev/Client/Server
@dataclass
class Network():

    # holds the paths (emulates location) of the
    # Dev/Client/Server
    dev_dir: str
    client_dir: str
    server_dir: str

    def send_parameters_to_client(self):
        copyfile(self.dev_dir + "/client.zip", self.client_dir + "/client.zip")
        return 0

    def send_model_to_server(self):
        copyfile(self.dev_dir + "/server.zip", self.server_dir + "/server.zip")
        return 0

    def send_public_key_to_server(self, public_keys):
        with open(self.server_dir + "/public_keys.ekl", "wb") as f:
            f.write(public_keys)


def generate_data():

    # Let's first get some data and train a model.
    X, y = load_breast_cancer(return_X_y=True)

    # Split X into X_model_owner and X_client
    X, client_X = X[:-10], X[-10:]
    y, client_y = y[:-10], y[-10:]
    
    return X, y, client_X, client_y


def create_and_train_model(X, y):
    # Train the model and compile it
    _devmodel = XGBClassifier(n_bits=2, n_estimators=10, max_depth=3)
    _devmodel.fit(X, y)
    
    model = deepcopy(_devmodel)
    model.compile(X)

    print("Model trained and compiled.")

    return model, _devmodel


def main():

    # ---------------- Emulate Client/Server/Dev with directories -------
    dev_dir = "./dev"
    client_dir = "./client"
    server_dir = "./server"

    # Create the Dev Directory
    if os.path.exists(dev_dir):
        shutil.rmtree(dev_dir)
    os.makedirs(dev_dir)

    # Create the Client Directory
    if os.path.exists(client_dir):
        shutil.rmtree(client_dir)
    os.makedirs(client_dir)

    # Create the Server Directory
    if os.path.exists(server_dir):
        shutil.rmtree(server_dir)
    os.makedirs(server_dir)

    # ---------------------------------------------------------------------

    # First generate the data for the model and client
    X, y, client_X, client_y = generate_data()

    # Creating the model away from the Client and Server and saving the model
    # specs for the client and server in the dev environment
    model, _devmodel = create_and_train_model(X, y)
    modelDev = FHEModelDev(dev_dir, model)
    modelDev.save()

    # Network emulating knowing the addresses of Dev/Clint/Server and sends
    # the packets between them
    network = Network(dev_dir, client_dir, server_dir)

    # Network can now send the necessary client packets to the Client and the
    # Server packets to the server
    network.send_parameters_to_client()
    network.send_model_to_server()

    # Creating the Client and generating its keys
    fhemodel_client = FHEModelClient(client_dir, key_dir=client_dir)
    fhemodel_client.generate_private_and_evaluation_keys()
    public_keys = fhemodel_client.get_serialized_evaluation_keys()

    # Creating the Server and receiving the clients serialized key
    fheserver = FHEModelServer(server_dir)
    network.send_public_key_to_server(public_keys)

    # --------------- Sending Encrypted Data to the server for Classification -------------
    
    starting_time = time.time()
    decrypted_outputs = []
    for datapoint in client_X:
        encrypted_input = fhemodel_client.quantize_encrypt_serialize(np.expand_dims(datapoint, axis=0))
        encrypted_output = fheserver.run(encrypted_input, public_keys)
        decrypted_output = fhemodel_client.deserialize_decrypt_dequantize(encrypted_output)[0]
        decrypted_outputs.append(decrypted_output)
    print(f"Time for predictions with FHE: {100*(time.time() - starting_time):.2f}ms")

    # ------------------------------------------------------------------------------------

   # Let's check the results and compare them against the clear model
    starting_time = time.time()
    clear_prediction_classes = _devmodel.predict_proba(client_X).argmax(axis=1)
    print(f"Time for predictions without FHE: {100 * (time.time() - starting_time):.2f}ms")
    decrypted_predictions_classes = np.array(decrypted_outputs).argmax(axis=1)
    accuracy = (clear_prediction_classes == decrypted_predictions_classes).mean()
    print(f"Accuracy between FHE prediction and clear model is: {accuracy*100:.0f}%") 
    return 0

if __name__=="__main__":
    main()
