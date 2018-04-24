#!/usr/bin/env python
from __future__ import unicode_literals

import operator
from Profile import Profile
from Pattern import Pattern
import Utils
from Token import Token
import exrex
import re


class Generator:


    def __init__(self, pattern, profile):
        self.pattern = pattern
        self.profile = profile


    def get_values_for_simple_token(self, category):
        """
        get simple pattern (for example: names) and profile.
        return list of all values matching the pattern (pat).
        """
        result = []
        result = self.profile.get_values_for_category(category)

        return result


    def get_partial_values_for_simple_tokens(self, category, part):
        """
        get pattern with range select (for example: names[1:4]) and profile,
        return list of all options to pattern based on profile.
        """
        result = []
        values = self.get_values_for_simple_token(category)
        result = Utils.get_partial_values(values, part)
        return result


    def get_value_for_specified_field(self, category, field):
        """
        get pattern with two levels and profile that contains the pattern.
        return all matching values from profile for the pattern.
        """
        result = []
        result = self.profile.get_value_for_field(category, field)
        return result


    def get_partial_value_for_specified_field(self, category, field, part):
        """
        get pattern with specific attribute and specific chars (for example: hobbies["hobby_A"][1:4]).
        return all matchin values from the profile.
        """
        result = []
        value = self.get_value_for_specified_field(category, field)
        result = Utils.get_partial_values(value, part)
        return result

    def get_value_for_simple_string(self, simple_string):
        """ get the value of simple_string inside list
        :param simple_string:
        :return:simple_string_as_list
        """
        simple_string_as_list = []
        simple_string_as_list.append(simple_string)
        return simple_string_as_list

    def get_values_for_regex(self, regex_token):
        """
        get all regex values using the exrex methods.
        """
        result = list(exrex.generate(regex_token))
        return result


    def please_generate(self):
        """
        get profile and pattern,
        check what pattern used,
        generat the wordlist based on the pattern.
        """

        pattern_contents = []
        error = ()
        warning = ()
        tokens = self.pattern.get_tokens()
        for token in tokens:
            function_and_args = token.get_function_and_args()
            token_type = token.get_token_type()
            if token_type is None:

                pattern_contents = None
                error = (token, "syntax error - token type is not recognized")
                break

            if token_type == Token.simple_token_type:
                category = token.get_category()
                simple_contents = self.get_values_for_simple_token(category)
                while function_and_args:
                    cur_function, args = function_and_args.pop()

                    if cur_function in Token.special_functions:
                        simple_contents = Utils.special_manipulate_list(cur_function,simple_contents, args)
                    else:
                        simple_contents = Utils.manipulate_list(cur_function, simple_contents)
                token_results = simple_contents

            elif token_type == Token.partial_simple_token_type:
                category = token.get_category()
                part = token.get_part()
                simple_chars_contents = self.get_partial_values_for_simple_tokens(category,part)
                while function_and_args:
                    cur_function, args = function_and_args.pop()

                    if cur_function in Token.special_functions:

                        simple_chars_contents = Utils.special_manipulate_list(cur_function,simple_chars_contents, args)
                    else:
                        simple_chars_contents = Utils.manipulate_list(cur_function, simple_chars_contents)
                token_results = simple_chars_contents

            elif token_type == Token.specific_token_type:
                category = token.get_category()
                field = token.get_field()
                specified_contents = self.get_value_for_specified_field(category, field)
                while function_and_args:
                    cur_function, args = function_and_args.pop()

                    if cur_function in Token.special_functions:

                        specified_contents = Utils.special_manipulate_list(cur_function,specified_contents, args)
                    else:

                        specified_contents = Utils.manipulate_list(cur_function, specified_contents)
                token_results = specified_contents

            elif token_type == Token.partial_specific_token_type:
                category = token.get_category()
                field = token.get_field()
                part = token.get_part()
                specified_chars_contents = self.get_partial_value_for_specified_field(category,field, part)
                while function_and_args:
                    cur_function, args = function_and_args.pop()

                    if cur_function in Token.special_functions:

                        specified_chars_contents = Utils.special_manipulate_list(cur_function,specified_chars_contents, args)
                    else:

                        specified_chars_contents = Utils.manipulate_list(cur_function, specified_chars_contents)
                token_results = specified_chars_contents

            elif token_type == Token.simple_string_token_type:
                simple_string = token.get_simple_string()
                simple_string_as_list = self.get_value_for_simple_string(simple_string)
                while function_and_args:
                    cur_function, args = function_and_args.pop()

                    if cur_function in Token.special_functions:

                        simple_string_as_list = Utils.special_manipulate_list(cur_function,simple_string_as_list, args)
                    else:

                        simple_string_as_list = Utils.manipulate_list(cur_function, simple_string_as_list)
                token_results = simple_string_as_list


            elif token_type == Token.regex_token_type:
                regex = token.get_regex()
                regex_contents = self.get_values_for_regex(regex)
                while function_and_args:
                    cur_function, args = function_and_args.pop()

                    if cur_function in Token.special_functions:

                        regex_contents = Utils.special_manipulate_list(cur_function,regex_contents, args)
                    else:
                        regex_contents = Utils.manipulate_list(cur_function, regex_contents)

                token_results = regex_contents
            if not token_results:
                warning = (token, "Token return no result - results are wrong")
                continue

            pattern_contents.append(token_results)

        return pattern_contents,warning, error
