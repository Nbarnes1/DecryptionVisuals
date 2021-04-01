import os
from random import randint, choice, random
import time
import argparse
import getpass

OBFUSCATED_LEN = 80
SLEEP_TIME = 0.05
RAND_LOWER = 2
RAND_UPPER = 5

def revealChar(hiddenChars, revealedChars):
	revealedChars.append(hiddenChars.pop(0))

def revealChar_rand(hiddenChars, revealedChars):
	revealedChars.append(hiddenChars.pop(randint(0,len(hiddenChars)-1)))		

def pseudoDecrypt_seq(plaintext):
	hiddenChars = list(enumerate(plaintext))
	revealedChars = []

	obfuscated = generateObfuscated(OBFUSCATED_LEN)

	chrFixes = len(hiddenChars)
	chrRemovals = len(obfuscated) - len(plaintext)
	totalFixes = chrFixes + chrRemovals

	#Ensure that OBFUSCATED_LEN is at least 2x length of input?
	removalInterval = chrRemovals/chrFixes

	print "\033c"

	#Start larger than the plaintext, slowly chip off fluff characters
	for _ in range(chrFixes):
		for __ in range(removalInterval):
			obfuscated = truncate(obfuscated)
			partialPrint(obfuscated, revealedChars)
			time.sleep(SLEEP_TIME)
			print "\033c"
		revealChar(hiddenChars, revealedChars)
	
	#Handle leftover junk at end
	for _ in range(len(obfuscated)-len(plaintext)):
		print "\033c"
		obfuscated = truncate(obfuscated)
		partialPrint(obfuscated, revealedChars)
		time.sleep(SLEEP_TIME)

def pseudoDecrypt_rand(plaintext):
        hiddenChars = list(enumerate(plaintext))
        revealedChars = []
	obfuscated = generateObfuscated(len(plaintext))

	print "\033c"
	
	for _ in range(len(plaintext)):
		for __ in range(randint(RAND_LOWER,RAND_UPPER)):
			print "\033c"
			obfuscated = generateObfuscated(len(obfuscated))
			partialPrint(obfuscated, revealedChars)
			time.sleep(SLEEP_TIME)
		revealChar_rand(hiddenChars, revealedChars)

	print "\033c"
	partialPrint(obfuscated, revealedChars)

def partialPrint(obfuscated, revealedChars):
	obfuscated = generateObfuscated(len(obfuscated))
	
	#For each revealedChar, put the correct character in the correct place
	for tup in revealedChars:
		index = tup[0]
		obfuscated = obfuscated[:index] + tup[1] + obfuscated[index+1:]
	print obfuscated

def generateObfuscated(length):
	obfuscated = "".join(chr(choice([randint(97, 125),randint(65,93),randint(48,57)])) for x in range(length))
	return obfuscated	

def truncate(input):
	return input[:-1]	


def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-s", help="Sequential decryption with truncation.", action="store_true")
	group.add_argument("-r", nargs=2, help="Random decryption. Optional: include lower and upper randomization variables.")
	args = parser.parse_args()

	if args.s:
		input = getpass.getpass(prompt='Enter passcode: ')
		pseudoDecrypt_seq(input)
	elif args.r:
		input = getpass.getpass(prompt='Enter passcode: ')
		pseudoDecrypt_rand(input)
	else:
		parser.print_help()	

if __name__ == '__main__':
	main()
