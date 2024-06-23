from argparse import ArgumentParser
import secrets
import random
import string
#Setting up the Argument Parser
parser=ArgumentParser(
prog='Password Generator',
description='Generate any number of passwords with this tool'
)
#adding the arguments to the parser
parser.add_argument("-n","--numbers",default=0, help="Number of characters in the password",type=int)
parser.add_argument("-l","--lowercase",default=0, help="Number of lowercase characters in the password",type=int)
parser.add_argument("-u","--uppercase",default=0, help="Number of uppercase characters in the password",type=int)
parser.add_argument("-s","--special-chars",default=0, help="Number of special symbols in the password",type=int)
parser.add_argument("-t","--total-length",default=0, help="Number of total characters in the password",type=int)
parser.add_argument("-a","--amount", default=1,type=int)
parser.add_argument("-o","--output-file")
args=parser.parse_args()
#list of passwords
passwords=[]
#looping through the amount of passwords
for _ in range(args.amount):
    if args.total_length:
        #generate random password with the length of total_length based on all available characters
        passwords.append("".join([secrets.choice(string.digits+string.ascii_letters+string.punctuation)\
            for _ in range(args.total_length)]))
    else:
        password=[]
        #how many numbers the password should contain
        for _ in range(args.numbers):
            password.append(secrets.choice(string.digits))
        #how many uppercase character the password should contain
        for _ in range(args.uppercase):
            password.append(secrets.choice(string.ascii_uppercase))
        #how many lowercase character the password should contain
        for _ in range(args.lowercase):
            password.append(secrets.choice(string.ascii_lowercase))
        #how many special characters the password should contain
        for _ in range(args.special_chars):
            password.append(secrets.choice(string.punctuation))
        random.shuffle(password)
        password=''.join(password)
        passwords.append(password)
#store the generated passwords into a txt file
if args.output_file:
    with open(args.output_file,'w') as f:
        f.write('\n'.join(passwords))
print('\n'.join(passwords))


        
        
        
