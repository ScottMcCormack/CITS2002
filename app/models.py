from . import mongo
import hashlib
import datetime
from Crypto.PublicKey import RSA
from Crypto import Random


class User(object):
    def __init__(self, username, password):
        # Values to capture for a user, hash the password when received
        self.username = username
        self.password = self.hash_password(password)
        self.users = mongo.db.users

    def hash_password(self, password):
        # Hash the password and store it as a hexdigest
        hashed_password = hashlib.sha256(password.encode('UTF-8')).hexdigest()
        return hashed_password

    def register_new_user(self):
        # Attempt to register a new user
        # Return a response, depending on whether it was successful

        # Look for a user in the database
        user = self.users.find_one({'username': self.username})
        registration_success = False # Init as False before creation

        if user is None:
            # Generate private and public keys
            private_key, public_key = self.create_RSA_keys()

            user_obj_id = self.users.insert_one({
                'username': self.username,
                'password': self.password,
                'created': datetime.datetime.utcnow(),
                'private_key': private_key,
                'public_key': public_key
            }).inserted_id

            self.user_obj_id = user_obj_id
            self.public_key = public_key

            # If a user_id was successfully returned, user has been created
            if user_obj_id is not None:
                response = 'User was successfully created!'
                registration_success = True
            else:
                response = 'Error: User could not be created!'
        else:
            response = 'User already exists!'

        return registration_success, response

    def create_RSA_keys(self):
        # Method to create private and public keys for users
        random_generator = Random.new().read
        rsa_object = RSA.generate(2048, random_generator)

        # Export the private and public keys
        private_key = rsa_object.exportKey(format='PEM')
        public_key_obj = rsa_object.publickey()
        public_key = public_key_obj.exportKey(format='PEM')

        return (private_key, public_key)

    def login_user(self):
        # Attempt to login
        users = mongo.db.users
        login_success = False  # Init as False until login confirmed

        # Look for the user in the database
        # Look for a user in the database
        user = users.find_one({'username': self.username})
        if user is not None:
            # Check the hashed password to see if it matches the entry in the database
            if user['password'] == self.password:
                response = 'Successfully logged in!'
                login_success = True
            else:
                response = 'Incorrect password!'
        else:
            response = 'User: \'{0}\' does not exist! Please register'.format(self.username)

        return (login_success, response)


class Miner(object):
    def __init__(self):
        self.blockchain = mongo.db.blockchain

    def initialise_new_user(self, user, timestamp, chriscoins=100):
        # Initialise the user on the blockchain and give the user an amount of chriscoins
        self.blockchain.insert_one({
            'from_user_pk': '<miner>',
            'to_user_pk': user.public_key,
            'cc_amount': chriscoins,
            'timestamp': timestamp,
            'nonce': '-',
            'miner_verify': True
        })
