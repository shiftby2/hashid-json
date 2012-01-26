#!/usr/bin/env python
# encoding: utf-8
# HashID-json
# a tool inspired by Zion3R's HashID
# uses a JSON database to allow easy extensibility of hash types.
import json
import string
import argparse
import sys

parser = argparse.ArgumentParser(description = "Attempts to determine which hashing algorithm was used for a hash.")
parser.add_argument('-i', '--input', default='', help="the hash, or a file containing whitespace-separated hashes.")
parser.add_argument('-t', '--tests', default='tests.txt', help="the tests to try.")
parser.add_argument('-o', '--output', default='', help="output results to this file (prints to screen by default)")


def evaluate_hash(input_hash, algorithm_object):
    '''Evaluates a hash, given the JSON description of the hash. Returns True if hash fits the description.'''
    # TODO: make more pythonic, less hacky

    # check whether lowercase/uppercase letters are present,
    # by using upper() and seeing if the string changes
    if algorithm_object.has_key("lower"):
        if algorithm_object["lower"] != (input_hash != input_hash.upper()): return False
    if algorithm_object.has_key("upper"):
        if algorithm_object["lower"] != (input_hash != input_hash.lower()): return False
    if algorithm_object.has_key("length"):
        if algorithm_object["length"] != len(input_hash): return False
    if algorithm_object.has_key("letters"):
        if algorithm_object["letters"] != (input_hash != ''.join([char for char in input_hash if char not in string.letters])): return False
    if algorithm_object.has_key("numbers"):
        if algorithm_object["numbers"] != (input_hash != ''.join([char for char in input_hash if char not in string.digits])): return False
    if algorithm_object.has_key("symbols"):
        if algorithm_object["symbols"] != (input_hash != ''.join([char for char in input_hash if char not in string.letters + string.digits])): return False

    if algorithm_object.has_key("eval"):
        for check in algorithm_object["eval"]:
            if eval(check) != True: return False
        
    #none of the criteria have been tripped, assume it fits!
    return True


def main():
    args = parser.parse_args()
    try:
        ChecksFile = open(args.tests, 'r')
        ChecksList = [json.loads(line) for line in ChecksFile.readlines()]
        ChecksFile.close()
    
    except IOError:
        print("Couldn't find tests - quitting.")
        parser.print_help()
        return 1

    try:
        InputFile = open(args.input, 'r')
        InputList = InputFile.read().split()
        InputFile.close()
    
    except IOError:
        if len(args.input) > 0:
            InputList = [args.input]
        else:
            InputList = [raw_input("Hash: ")]

    try:
        OutputFile = open(args.output, 'w')

    except IOError:
        OutputFile = sys.stdout

    for Hash in InputList:
        matches = []
        for Check in ChecksList:
            if evaluate_hash(Hash, Check): matches += [Check["name"]]
        if len(matches) == 0:
            matches = ["No matches found."]
        OutputFile.write("Possible matches for {0}:\n{1}\n".format(Hash, ", ".join(matches)))
    
    return 0

if __name__ == "__main__":
    main()
