from argparse import ArgumentParser
import secrets
import string
import hashlib
import csv
import os

# Setting up the Argument Parser
parser = ArgumentParser(
    prog='Password Generator',
    description='Generate any number of passwords with this tool'
)

# Adding the arguments to the parser
parser.add_argument("-n", "--numbers", default=0, help="Number of digits in the password", type=int)
parser.add_argument("-l", "--lowercase", default=0, help="Number of lowercase characters in the password", type=int)
parser.add_argument("-u", "--uppercase", default=0, help="Number of uppercase characters in the password", type=int)
parser.add_argument("-s", "--special-chars", default=0, help="Number of special symbols in the password", type=int)
parser.add_argument("-t", "--total-length", default=0, help="Number of total characters in the password", type=int)
parser.add_argument("-a", "--amount", default=1, type=int, help="Number of passwords to generate")
parser.add_argument("--account", required=True, help="Account for which the password is generated")
parser.add_argument("-o", "--output-file", required=True, help="Output CSV file to store passwords and hashes")
parser.add_argument("--hash-algorithm", choices=hashlib.algorithms_guaranteed, help="Hashing algorithm to use. Choices are: " + ', '.join(hashlib.algorithms_guaranteed))
parser.add_argument("--salt", help="Salt value for hashing", type=str)
args = parser.parse_args()

# List of passwords and their details
passwords = []
hashes = set()

# Check if the output file already exists and read existing hashes
if os.path.exists(args.output_file):
    with open(args.output_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        for row in csvreader:
            if len(row) > 2:
                hashes.add(row[2])  # Assuming the hash is in the third column

# Function to generate a password
def generate_password():
    if args.total_length:
        # Generate random password with the length of total_length based on all available characters
        return ''.join(secrets.choice(string.digits + string.ascii_letters + string.punctuation) 
                       for _ in range(args.total_length))
    else:
        password_chars = []

        # How many numbers the password should contain
        for _ in range(args.numbers):
            password_chars.append(secrets.choice(string.digits))

        # How many uppercase characters the password should contain
        for _ in range(args.uppercase):
            password_chars.append(secrets.choice(string.ascii_uppercase))

        # How many lowercase characters the password should contain
        for _ in range(args.lowercase):
            password_chars.append(secrets.choice(string.ascii_lowercase))

        # How many special characters the password should contain
        for _ in range(args.special_chars):
            password_chars.append(secrets.choice(string.punctuation))

        # Shuffle to ensure random order of characters
        secrets.SystemRandom().shuffle(password_chars)

        # Ensure the password length meets requirements and does not repeat characters
        return ''.join(password_chars)

# Looping through the amount of passwords
for _ in range(args.amount):
    while True:
        try:
            password = generate_password()
            
            if args.hash_algorithm:
                hash_func = hashlib.new(args.hash_algorithm)
                salt = args.salt if args.salt else secrets.token_hex(16)
                hash_func.update(salt.encode() + password.encode())
                hashed_password = f'{salt}${hash_func.hexdigest()}'
            else:
                hashed_password = ''
            
            # Check if the hash already exists
            if hashed_password not in hashes:
                hashes.add(hashed_password)
                passwords.append((args.account, password, hashed_password))
                break
            else:
                raise ValueError("Hash collision detected, generating a new password.")
        except ValueError as e:
            print(f"Error: {e}. Retrying password generation...")

# Write the generated passwords and their hashes into a CSV file
with open(args.output_file, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    if os.stat(args.output_file).st_size == 0:
        csvwriter.writerow(['Account (-a)', 'Password (pswd)', 'Hash (#)'])
    csvwriter.writerows(passwords)

# Print the generated passwords and their hashes
for account, password, hashed_password in passwords:
    print(f"Account: {account}, Password: {password}, Hash: {hashed_password}")
