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

    def hash_password(self, password):
        # Hash the password and store it as a hexdigest
        hashed_password = hashlib.sha256(password.encode('UTF-8')).hexdigest()
        return hashed_password

    def register_new_user(self):
        # Attempt to register a new user
        # Return a response, depending on whether it was successful
        users = mongo.db.users

        # Look for a user in the database
        user = users.find_one({'username': self.username})

        if user is None:
            # Generate private and public keys
            private_key, public_key = self.create_RSA_keys()

            user_id = users.insert_one({
                'username': self.username,
                'password': self.password,
                'created': datetime.datetime.utcnow(),
                'private_key': private_key,
                'public_key': public_key
            })

            # If a user_id was successfully returned, user has been created
            if user_id is not None:
                response = 'User was successfully created!'

            else:
                response = 'Error: User could not be created!'
        else:
            response = 'User already exists!'

        return response

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

        # Look for the user in the database
        # Look for a user in the database
        user = users.find_one({'username': self.username})
        if user is not None:
            # Check the hashed password to see if it matches the entry in the database
            if user.password == self.password:
                response = 'Successfully logged in!'
            else:
                response = 'Incorrect password!'
        else:
            response = 'User does not exist, please register'

        return response

