#!/usr/bin/env python
from __future__ import unicode_literals

import re


class Token:
    # name
    simple_token = re.compile("^[\w]*$")
    simple_token_type = "simple"

    # names[1:2] or names[1] (get specified char for string)
    partial_simple_token_regex = re.compile("^\w+[\[][\-?\d]*[\:]*[\-?\d]*[\]]$")
    partial_simple_token_type = "partial_simple"

    # hobbies[hobby_a]
    specific_token_regex = re.compile("""^\w+[\.]\w+$""")
    specific_token_type = "specific"

    # specified_chars
    partial_specific_token_regex = re.compile("^\w+[\.]\w+[\[][\-?\d]*[\:]*[\-?\d]*[\]]$")
    partial_specific_token_type = "partial_specific"

    # simple_string
    simple_string_token_regex = re.compile("""^["|'].+[\"\']""")
    simple_string_token_type = "simple_string"

    # regex
    regex_token_regex = re.compile(r"^r[\"|\'].+[\"|\']$")
    regex_token_type = "regex"


    # function token
    function_token_regex = re.compile("^\w+[\(].+[\)]$")

    # "functions"
    scramble_function_type = "scramble"
    upper_function_type = "upper"
    lower_function_type = "lower"
    capitalize_function_type = "capitalize"
    title_function_type = "title"
    basic_leet_function_type = "leet"

    strip_function_type = "strip"
    splitall_function_type = "splitall"

    reverse_function_type = "reverse"
    initials_function_type = "initials"

    functions = []
    functions.append(scramble_function_type)
    functions.append(upper_function_type)
    functions.append(lower_function_type)
    functions.append(capitalize_function_type)
    functions.append(title_function_type)
    functions.append(basic_leet_function_type)
    functions.append(reverse_function_type)
    functions.append(initials_function_type)




    # special functions - with args

    add_s_function_type = "add"
    replace_s_function_type = "replace"
    multiply_s_function_type = "multiply"
    split_s_function_type = "split"

    special_functions = []
    special_functions.append(add_s_function_type)
    special_functions.append(replace_s_function_type)
    special_functions.append(multiply_s_function_type)
    special_functions.append(split_s_function_type)

    def __init__(self, token_as_string):
        self.token_as_string = token_as_string
        self.token_function = None
        self.token_args = None
        self.functions_and_args = list()
        self.token_function_args = None
        self.token_category = None
        self.token_field = None
        self.token_part = None
        self.token_simple_string = None
        self.token_regex = None
        self.token_type = self.parse_token()

        if self.token_type == Token.simple_token_type:
            self.token_category = self.token_as_string

        elif self.token_type == Token.partial_simple_token_type:
            self.token_category = self.find_token_category()
            self.token_part = self.find_token_part()

        elif self.token_type == Token.specific_token_type:
            self.token_category = self.find_token_category()
            self.token_field = self.find_token_field()

        elif self.token_type == Token.partial_specific_token_type:
            self.token_category = self.find_token_category()
            self.token_field = self.find_token_field()
            self.token_part = self.find_token_part()

        elif self.token_type == Token.simple_string_token_type:
            self.token_simple_string = self.find_token_simple_string()

        elif self.token_type == Token.regex_token_type:
            self.token_regex = self.find_token_regex()



    def parse_token(self):
        """
        Check token type
        """

        if re.match(Token.function_token_regex, self.token_as_string):
            self.find_functions_and_args()
        token_type = None
        if re.match(Token.simple_token, self.token_as_string):
            token_type =  Token.simple_token_type
        elif re.match(Token.partial_simple_token_regex, self.token_as_string):
            token_type =  Token.partial_simple_token_type
        elif re.match(Token.specific_token_regex, self.token_as_string):
            token_type =  Token.specific_token_type
        elif re.match(Token.partial_specific_token_regex, self.token_as_string):
            token_type =  Token.partial_specific_token_type
        elif re.match(Token.simple_string_token_regex, self.token_as_string):
            token_type =  Token.simple_string_token_type
        elif re.match(Token.regex_token_regex, self.token_as_string):
            token_type =  Token.regex_token_type

        return token_type

    def find_functions_and_args(self):
        """
        extract all function and args to stack
        :return: tuple of (function,list_args)
        """
        split_by_coma = re.compile("\,(?![^\(]*\))")
        list_function_args = []
        splited_token = self.token_as_string.split("(",1)

        function = splited_token[0]
        inside_function = splited_token[1][:-1]


        if function in Token.special_functions:
            splited_inside_function = re.split(split_by_coma,inside_function)
            splited_inside_function = [x.lstrip() for x in splited_inside_function]
            splited_inside_function = [x.rstrip() for x in splited_inside_function]
            args = splited_inside_function[1:]
            tup  = (function,args)
            self.functions_and_args.append((tup))
            self.token_as_string = splited_inside_function[0]

        else:
            args = None
            tup  = (function,args)
            self.functions_and_args.append((tup))
            self.token_as_string = inside_function

        if re.match(Token.function_token_regex, self.token_as_string):
            self.find_functions_and_args()


    def find_token_category(self):
        """
        return category from token
        :return:category
        """

        category = re.split("[\.\[]", self.token_as_string, maxsplit=1)
        category = category[0]
        return category


    def find_token_field(self):
        """
        gets field from category.
        :return:field
        """

        token_splitted = self.token_as_string.split(".")
        field = token_splitted[1]
        if "[" in self.token_as_string:
            field = field.split("[")
            field = field[0]

        return field


    def find_token_part(self):
        token_splitted = self.token_as_string.split("[")
        part = token_splitted[1][:-1]

        return part


    def find_token_simple_string(self):
        """find simple string in simple string tokens.
        :return:simple string
        """

        simple_string = self.token_as_string[1:-1]

        return simple_string


    def find_token_regex(self):
        """ find regex pattern in token
        :return:regex
        """
        # token_splitted = re.split(r"[r\'|r\"]", self.token_as_string)
        regex_pattern = re.compile(r"^r[\"|\'](.+)[\"|\']$")
        regex = re.findall(regex_pattern, self.token_as_string)
        regex_string = regex[0]

        return regex_string


    def get_token_type(self):
        """

        :return: token_type
        """

        return self.token_type


    # def get_function(self):
    #     """
    #     get function name if available
    #     :return: function
    #     """
    #
    #     return self.functions_and_args[0]

    def get_function_and_args(self):
        """
        get function name if available
        :return: function
        """

        return self.functions_and_args


    # def get_args(self):
    #     """
    #     get the arguments for special functions
    #     :return:list of args
    #     """
    #     return self.token_args


    def get_category(self):
        """

        :return: category
        """
        return self.token_category


    def get_field(self):
        """
        get part
        :return:
        """

        return self.token_field


    def get_part(self):
        """
        get part
        :return:
        """
        return self.token_part


    def get_simple_string(self):
        """
        get part
        :return:
        """
        return self.token_simple_string


    def get_regex(self):
        """

        :return:
        """

        return self.token_regex
