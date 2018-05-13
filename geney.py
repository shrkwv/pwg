#!/usr/bin/env python
from __future__ import unicode_literals


from core.Pattern import Pattern
from core.Generator import Generator
from core.Profile import Profile
from core import Utils
import argparse
import itertools
import json
import sys


# def check_wordlist_limit(words_limit):
#     """
#     exit when limit
#     """
#     counter += 1
#     if counter == words_limit:
#         exit(0)

def argparser():
    """
    generates all options for the script
    """
    parser = argparse.ArgumentParser(description="customized and personalized dictionary maker")
    # mandatory
    parser.add_argument("pattern", type=str, help="Patterns file - *.pgeney")
    parser.add_argument("profile", type=str, help="Profile file - *.geney")

    # optional
    parser.add_argument("--size", type=str, nargs='+', help="Define size of word in wordlist ( a:b )")
    parser.add_argument("--limit", type=int, help="Define size of wordlist ( a:b )")

    parser.add_argument("-c", "--count", action="store_true", dest='count', default=False, help="Count wordlist size before generating.")
    parser.add_argument("-q", "--quiet", action='store_true', dest='quiet', help = "quiet mode")


    # parser.add_argument("--debug", action='store_true', dest='debug', help = "DEBUGGING")

    args = vars(parser.parse_args())

    return args, parser


def main():
    """
    main
    """
    args, parser = argparser()
    profile_file = args['profile']
    pattern_file = args['pattern']

    size = args['size']
    if size:
        size = ' '.join(size)
        if size.startswith("[") and size.endswith("]"):
            size = size[1:-1]

        min_word_size, max_word_size = Utils.part_to_min_max(size)

    words_limit = args['limit']
    count = args['count']
    quiet = args['quiet']
    # debug = args['debug']
    # if debug:
    #     logging.basicConfig(level=logging.DEBUG)

    # check for geney file
    if not pattern_file.endswith(".pgeney"):
        sys.stderr.write("Error: Pattern file must be *.pgeney\n")
        parser.print_help(sys.stderr)
        exit(1)
    if not profile_file.endswith(".geney"):
        sys.stderr.write("Error: Profile file must be *.geney\n")
        parser.print_help(sys.stderr)
        exit(1)
    try:
        with open(pattern_file, 'r') as f:
            data = f.read().splitlines()
            patterns = []
            for line in data:
                if not line.startswith('#') and not line.startswith('//'):
                    patterns.append(line)
    except IOError as e:
        sys.stderr.write("Error: Can\'t find file or read data\n")
        parser.print_help(sys.stderr)
        exit(1)

    try:
        with open(profile_file, 'r') as f:
            profile_as_json = json.load(f)
    except ValueError:
        sys.stderr.write("Error: Profile is not a valid json\n")
        parser.print_help(sys.stderr)
        exit(1)
    except IOError:
        sys.stderr.write("Error: Profile file is not found\n")
        parser.print_help(sys.stderr)
        exit(1)



    profile = Profile(profile_as_json)
    counter = 0
    word_limit_counter = 0
    # sys.stderr.write("geney start to generate a dictionary based on patterns: %s and profile: %s\n\n" %(pattern_file,profile_file))
    errors = []
    warnings = []
    printed_words = []
    for index, pattern_as_string in enumerate(patterns):
        pattern = Pattern(pattern_as_string)
        geney = Generator(pattern, profile)

        words_for_pattern, warning, error = geney.please_generate()
        if error:
            token, error_msg = error
            errors.append((index+1,pattern_as_string, token.token_as_string, error_msg))
            continue
        if warning:
            token, warning_msg = warning
            warnings.append((index+1,pattern_as_string, token.token_as_string, warning_msg))

        words_for_pattern_product = list(itertools.product(*words_for_pattern))
        words_for_pattern_strings = list(set([''.join(tup) for tup in words_for_pattern_product]))
        pattern_counter = 0
        pattern_counter = len(words_for_pattern_strings)

        if count:
            printed_words += words_for_pattern_strings
            continue

        for word in words_for_pattern_strings:
            if size and not Utils.valid_size(word, min_word_size, max_word_size):
                continue
            elif words_limit == word_limit_counter:
                sys.stderr.write("[+]Pattern Size: %d for pattern: %s%s" %(pattern_counter, pattern_as_string,"\n"))
                return

            elif word in printed_words:
                # pattern_counter -= 1
                # counter -= 1
                continue
            else:
                word_limit_counter += 1
                counter += 1
                printed_words.append(word)
                print word

        if not quiet:
            sys.stderr.write("[+]Pattern Size: %d for pattern: %s%s" %(pattern_counter, pattern_as_string,"\n"))

            if warnings or errors:
                for warn in warnings:
                    sys.stderr.write("[-]WARNING [pattern in line %s] {%s} token: {%s} - %s\n" %warn)
                for err in errors:
                    sys.stderr.write("[-]ERROR [pattern in line %s] {%s} token: {%s} - %s\n" %err)
    if count:
        counter = len(set(printed_words))
        if warnings or errors:
            for warn in warnings:
                sys.stderr.write("[-]WARNING [pattern in line %s] {%s} token: {%s} - %s\n" %warn)
            for err in errors:
                sys.stderr.write("[-]ERROR [pattern in line %s] {%s} token: {%s} - %s\n" %err)

    sys.stderr.write("[+]SIZE: %d%s" %(counter,"\n"))


if __name__ == "__main__":
    main()
