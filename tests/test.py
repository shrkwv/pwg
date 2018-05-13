#!/usr/bin/env python
from __future__ import unicode_literals
import json

import unittest
import itertools
from Generator import Generator
from Profile import Profile
from Pattern import Pattern
from Token import Token
import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        """
        initialization
        :return:
        """
        self.test_list = ["john", "John123", "JOHN doe", "John 123"]

    # functions tests
    def test_lower_function(self):
        function = "lower"
        lower_test_result = ["john", "john123", "john doe", "john 123"]
        self.assertEqual(Utils.manipulate_list(function, self.test_list), lower_test_result)

    def test_upper_function(self):
        function = "upper"
        upper_test_result = ["JOHN", "JOHN123", "JOHN DOE", "JOHN 123"]
        self.assertEqual(Utils.manipulate_list(function, self.test_list), upper_test_result)

    def test_capitalize_function(self):
        function = "capitalize"
        capitalize_test_result = ["John", "John123", "John doe", "John 123"]
        self.assertEqual(Utils.manipulate_list(function, self.test_list), capitalize_test_result)

    def test_title_function(self):
        function = "title"
        title_test_result = ["John", "John123", "John Doe", "John 123"]

        self.assertEqual(Utils.manipulate_list(function, self.test_list), title_test_result)

    def test_basic_leet_function(self):
        function = "leet"
        leet_test_result = ['J0HN d03', 'J0HN d0e', 'J0HN do3', 'J0HN doe', 'J0hn 123', 'J0hn123', 'JOHN d03',
                            'JOHN d0e', 'JOHN do3', 'JOHN doe', 'John 123', 'John123', 'j0hn', 'john']

        leet_test_result = sorted(leet_test_result)
        result = sorted(Utils.manipulate_list(function, self.test_list))
        self.assertEqual(result, leet_test_result)

    def test_reverse_function(self):
        function = "reverse"
        reverse_test_result = ["nhoj", "321nhoJ", "eod NHOJ", "321 nhoJ"]
        self.assertEqual(Utils.manipulate_list(function, self.test_list), reverse_test_result)

    def test_initials_function(self):
        function = "initials"
        initials_test_result = ["j", "J", "Jd", "J1"]
        self.assertEqual(Utils.manipulate_list(function, self.test_list), initials_test_result)

    # special function check
    def test_add_s_function(self):
        function = "add"
        add_args = ["\"test\"", 3]
        add_test_result = ["johtestn", "Johtestn123", "JOHtestN doe", "Johtestn 123"]
        self.assertEqual(Utils.special_manipulate_list(function, self.test_list, add_args), add_test_result)

    def test_replace_s_function(self):
        function = "replace"
        replace_args = ["\" \"", "\".\""]
        add_test_result = ["john", "John123", "JOHN.doe", "John.123"]

        self.assertEqual(Utils.special_manipulate_list(function, self.test_list, replace_args), add_test_result)

    def test_split_s_function(self):
        function = "split"
        cut_args = ["\"h\"", "1"]
        right_result = ["n", "n123", "n 123"]
        result = Utils.special_manipulate_list(function, self.test_list, cut_args)
        self.assertEqual(result, right_result)


# class TestProfile(unittest.TestCase):
#     def setUp(self):
#         profile_file = "tests/target.geney"
#         pattern_file = "tests/patterns.pgeney"
#         with open(profile_file, 'r') as f:
#             profile_as_json = json.load(f)
#
#         with open(pattern_file, 'r') as f:
#             data = f.read().splitlines()
#             patterns = []
#             for line in data:
#                 if not line.startswith('#') and not line.startswith('//'):
#                     patterns.append(line)
#         self.profile = Profile(profile_as_json)
#         self.patterns = patterns
#
#     def tearDown(self):
#         del self.profile
#         del self.patterns
#
#     def test_get_values_for_category(self):
#         for pattern_as_string in self.patterns:
#             pattern = Pattern(pattern_as_string)
#             geney = Generator(pattern, self.profile)

class testTokenType(unittest.TestCase):
    def test_token_type_for_simple_token(self):
        pattern = Pattern("|names|")
        tokens = pattern.get_tokens()
        correct_token_type = Token.simple_token_type
        for token in tokens:
            token_type = token.get_token_type()
            self.assertEqual(token_type, correct_token_type)

    def test_token_type_for_partial_simple_token(self):
        pattern = Pattern("|names[:1]|names[1:]|names[1:3]|names[-1:]|names[:-3]|names[-3:-1]")
        tokens = pattern.get_tokens()
        correct_token_type = Token.partial_simple_token_type
        for token in tokens:
            token_type = token.get_token_type()
            self.assertEqual(token_type, correct_token_type)

    def test_token_type_for_specific_token(self):
        pattern = Pattern("|names.target_first|names.test|")
        tokens = pattern.get_tokens()
        correct_token_type = Token.specific_token_type
        for token in tokens:
            token_type = token.get_token_type()
            self.assertEqual(token_type, correct_token_type)

    def test_token_type_for_partial_specific_token(self):
        pattern = Pattern(
            "|names.test[:1]|names.test[1:]|category.hars_one[1:3]|test.funct[-1:]|test.funct[:-3]|test.funct[-3:-1]")
        tokens = pattern.get_tokens()
        correct_token_type = Token.partial_specific_token_type
        for token in tokens:
            token_type = token.get_token_type()
            self.assertEqual(token_type, correct_token_type)

    def test_token_type_for_simple_string_token(self):
        pattern = Pattern("|\"sdfklnsdnsd\"|\"[abs]{1,6}\"|")
        tokens = pattern.get_tokens()
        correct_token_type = Token.simple_string_token_type
        for token in tokens:
            token_type = token.get_token_type()
            self.assertEqual(token_type, correct_token_type)

    def test_token_type_for_regex_token(self):
        pattern = Pattern("|r\"sdfklnsdnsd\"|r\"[abs]{1,6}\"|")
        tokens = pattern.get_tokens()
        correct_token_type = Token.regex_token_type
        for token in tokens:
            token_type = token.get_token_type()
            self.assertEqual(token_type, correct_token_type)


class testGetValues(unittest.TestCase):
    def setUp(self):
        # profile_file = "tests/default_profile.geney"
        # pattern_file = "tests/default_patterns.pgeney"
        # result_file = "tests/default_result.dic"
        #
        # with open(profile_file, 'r') as f:
        #     profile_as_json = json.load(f)
        #
        # with open(pattern_file, 'r') as f:
        #     data = f.read().splitlines()
        #     patterns = []
        #     for line in data:
        #         if not line.startswith('#') and not line.startswith('//'):
        #             patterns.append(line)
        # with open(result_file, 'r') as f:
        #     self.default_result_list = f.read().splitlines()

        profile_as_json = {
            u'dates': {u'birth_day': u'16/01/1993', u'mom_birth': u'17/03/1974', u'dad_birth': u'03/06/1973'},
            u'phones': {u'target_phone': u'0525432156', u'mom_phone': u'0546656565'},
            u'hobbies': {u'hobby_B': u'football', u'hobby_A': u'basketball'},
            u'names': {u'target_name': u'tal cohen', u'target_son': u'dvora tal', u'target_mother': u'dana giladi',
                       u'target_husband': u'david man'},
            u'address': {u'home': u'5th avenu new york', u'work': u'brooklyn street new york'},
            u'work_phones': {u'work_phone': u'065412345', u'home_phone': u'0773658844'}}

        self.profile = Profile(profile_as_json)

    def test_get_values_for_simple_token(self):
        right_result = [u'tal cohen', u'dvora tal', u'dana giladi', u'david man']
        pattern = Pattern("|names|")
        tokens = pattern.get_tokens()
        result = []
        for token in tokens:
            category = token.get_category()
            generator = Generator(pattern, self.profile)
            result += generator.get_values_for_simple_token(category)
        self.assertEqual(right_result, result)

    def test_get_partial_values_for_simple_token(self):
        right_result = [u'al', u'vo', u'an', u'av']
        patterns = Pattern("|names[1:3]|")
        tokens = patterns.get_tokens()
        result = []
        for token in tokens:
            category = token.get_category()
            part = token.get_part()
            generator = Generator(patterns, self.profile)

            result += generator.get_partial_values_for_simple_tokens(category, part)
        self.assertEqual(right_result, result)

    def test_get_values_for_specific_token(self):
        right_result = [u'basketball']
        patterns = Pattern("|hobbies.hobby_A|")
        tokens = patterns.get_tokens()
        result = []
        for token in tokens:
            category = token.get_category()
            field = token.get_field()
            generator = Generator(patterns, self.profile)

            result += generator.get_value_for_specified_field(category, field)
        self.assertEqual(right_result, result)

    def test_get_partial_values_for_specific_token(self):
        right_result = [u'baske']
        patterns = Pattern('|hobbies.hobby_A[:5]|')
        tokens = patterns.get_tokens()
        result = []
        for token in tokens:
            category = token.get_category()
            field = token.get_field()
            part = token.get_part()

            generator = Generator(patterns, self.profile)

            result += generator.get_partial_value_for_specified_field(category, field, part)
        self.assertEqual(right_result, result)

    def test_get_values_for_simple_string(self):
        right_result = ['test']
        patterns = Pattern('|"test"|')
        tokens = patterns.get_tokens()
        result = []
        for token in tokens:
            simple_string = token.get_simple_string()
            generator = Generator(patterns, self.profile)

            result += generator.get_value_for_simple_string(simple_string)
        self.assertEqual(right_result, result)

    def test_get_values_for_regex_token(self):
        right_result = [u'a', u'b', u'c', u'aa', u'ab', u'ac', u'ba', u'bb', u'bc', u'ca', u'cb', u'cc', u'aaa', u'aab',
                        u'aac', u'aba', u'abb', u'abc', u'aca', u'acb', u'acc', u'baa', u'bab', u'bac', u'bba', u'bbb',
                        u'bbc', u'bca', u'bcb', u'bcc', u'caa', u'cab', u'cac', u'cba', u'cbb', u'cbc', u'cca', u'ccb',
                        u'ccc']

        patterns = Pattern('|r"[abc]{1,3}"|')
        tokens = patterns.get_tokens()
        result = []
        for token in tokens:
            regex = token.get_regex()
            generator = Generator(patterns, self.profile)

            result += generator.get_values_for_regex(regex)
        self.assertEqual(right_result, result)

    def test_get_values_for_simple_function(self):
        right_result = [u'FOOTBALL', u'BASKETBALL']

        patterns = Pattern('|upper(hobbies)|')
        tokens = patterns.get_tokens()
        manipulated_result = []
        for token in tokens:
            # function = token.get_function()
            function_and_args = token.get_function_and_args()

            category = token.get_category()
            generator = Generator(patterns, self.profile)

            result = generator.get_values_for_simple_token(category)
            while function_and_args:
                cur_function, args = function_and_args.pop()
                result = Utils.manipulate_list(cur_function, result)
            manipulated_result += result

        self.assertEqual(right_result, manipulated_result)

    def test_get_values_for_special_function(self):
        right_result = [u'tal testcohen', u'dvortesta tal', u'danatest giladi', u'davitestd man']

        patterns = Pattern('|add(names, "test", 4)|')
        tokens = patterns.get_tokens()
        manipulated_result = []
        for token in tokens:
            # function = token.get_function()
            function_and_args = token.get_function_and_args()

            category = token.get_category()
            generator = Generator(patterns, self.profile)
            result = generator.get_values_for_simple_token(category)

            while function_and_args:
                cur_function, args = function_and_args.pop()
                result = Utils.special_manipulate_list(cur_function, result, args)
            manipulated_result += result

        self.assertEqual(right_result, manipulated_result)

    def test_get_values_for_recursive_simple_functions(self):
        right_result = ['114BT00F', '114BT0OF', '114BTO0F', '114BTOOF', '11ABT00F', '11ABT0OF', '11ABTO0F', '11ABTOOF',
                        '1L4BT00F', '1L4BT0OF', '1L4BTO0F', '1L4BTOOF', '1LABT00F', '1LABT0OF', '1LABTO0F', '1LABTOOF',
                        'L14BT00F', 'L14BT0OF', 'L14BTO0F', 'L14BTOOF', 'L1ABT00F', 'L1ABT0OF', 'L1ABTO0F', 'L1ABTOOF',
                        'LL4BT00F', 'LL4BT0OF', 'LL4BTO0F', 'LL4BTOOF', 'LLABT00F', 'LLABT0OF', 'LLABTO0F', 'LLABTOOF',
                        '114BT3KS4B', '114BT3KSAB', '114BTEKS4B', '114BTEKSAB', '11ABT3KS4B', '11ABT3KSAB',
                        '11ABTEKS4B', '11ABTEKSAB', '1L4BT3KS4B', '1L4BT3KSAB', '1L4BTEKS4B', '1L4BTEKSAB',
                        '1LABT3KS4B', '1LABT3KSAB', '1LABTEKS4B', '1LABTEKSAB', 'L14BT3KS4B', 'L14BT3KSAB',
                        'L14BTEKS4B', 'L14BTEKSAB', 'L1ABT3KS4B', 'L1ABT3KSAB', 'L1ABTEKS4B', 'L1ABTEKSAB',
                        'LL4BT3KS4B', 'LL4BT3KSAB', 'LL4BTEKS4B', 'LL4BTEKSAB', 'LLABT3KS4B', 'LLABT3KSAB',
                        'LLABTEKS4B', 'LLABTEKSAB']

        patterns = Pattern('|upper(leet(reverse(hobbies)))|')
        tokens = patterns.get_tokens()
        manipulated_result = []
        for token in tokens:
            # function = token.get_function()
            function_and_args = token.get_function_and_args()
            category = token.get_category()
            generator = Generator(patterns, self.profile)
            result = generator.get_values_for_simple_token(category)

            while function_and_args:
                cur_function, args = function_and_args.pop()
                result = Utils.manipulate_list(cur_function, result)
            manipulated_result += result

        self.assertEqual(right_result, manipulated_result)

    def test_get_values_for_recursive_special_functions(self):
        right_result = ['t41.c0h3n', 't41.c0hen', 't41.coh3n', 't41.cohen', 't4l.c0h3n', 't4l.c0hen', 't4l.coh3n',
                        't4l.cohen', 'ta1.c0h3n', 'ta1.c0hen', 'ta1.coh3n', 'ta1.cohen', 'tal.c0h3n', 'tal.c0hen',
                        'tal.coh3n', 'tal.cohen', 'dv0r4.t41', 'dv0r4.t4l', 'dv0r4.ta1', 'dv0r4.tal', 'dv0ra.t41',
                        'dv0ra.t4l', 'dv0ra.ta1', 'dv0ra.tal', 'dvor4.t41', 'dvor4.t4l', 'dvor4.ta1', 'dvor4.tal',
                        'dvora.t41', 'dvora.t4l', 'dvora.ta1', 'dvora.tal', 'd4n4.g114d1', 'd4n4.g114di', 'd4n4.g11ad1',
                        'd4n4.g11adi', 'd4n4.g1l4d1', 'd4n4.g1l4di', 'd4n4.g1lad1', 'd4n4.g1ladi', 'd4n4.gi14d1',
                        'd4n4.gi14di', 'd4n4.gi1ad1', 'd4n4.gi1adi', 'd4n4.gil4d1', 'd4n4.gil4di', 'd4n4.gilad1',
                        'd4n4.giladi', 'd4na.g114d1', 'd4na.g114di', 'd4na.g11ad1', 'd4na.g11adi', 'd4na.g1l4d1',
                        'd4na.g1l4di', 'd4na.g1lad1', 'd4na.g1ladi', 'd4na.gi14d1', 'd4na.gi14di', 'd4na.gi1ad1',
                        'd4na.gi1adi', 'd4na.gil4d1', 'd4na.gil4di', 'd4na.gilad1', 'd4na.giladi', 'dan4.g114d1',
                        'dan4.g114di', 'dan4.g11ad1', 'dan4.g11adi', 'dan4.g1l4d1', 'dan4.g1l4di', 'dan4.g1lad1',
                        'dan4.g1ladi', 'dan4.gi14d1', 'dan4.gi14di', 'dan4.gi1ad1', 'dan4.gi1adi', 'dan4.gil4d1',
                        'dan4.gil4di', 'dan4.gilad1', 'dan4.giladi', 'dana.g114d1', 'dana.g114di', 'dana.g11ad1',
                        'dana.g11adi', 'dana.g1l4d1', 'dana.g1l4di', 'dana.g1lad1', 'dana.g1ladi', 'dana.gi14d1',
                        'dana.gi14di', 'dana.gi1ad1', 'dana.gi1adi', 'dana.gil4d1', 'dana.gil4di', 'dana.gilad1',
                        'dana.giladi', 'd4v1d.m4n', 'd4v1d.man', 'd4vid.m4n', 'd4vid.man', 'dav1d.m4n', 'dav1d.man',
                        'david.m4n', 'david.man']

        patterns = Pattern('|replace(leet(names)," ", ".")|')
        tokens = patterns.get_tokens()
        manipulated_result = []
        for token in tokens:
            # function = token.get_function()
            function_and_args = token.get_function_and_args()
            category = token.get_category()
            generator = Generator(patterns, self.profile)
            result = generator.get_values_for_simple_token(category)

            while function_and_args:

                cur_function, args = function_and_args.pop()
                if cur_function in Token.special_functions:
                    result = Utils.special_manipulate_list(cur_function, result, args)
                else:
                    result = Utils.manipulate_list(cur_function, result)
            manipulated_result += result
        self.assertEqual(right_result, manipulated_result)

    def test_get_values_for_complex_function_token(self):
        right_result = ['T41.C0H3N', 'T41.C0HEN', 'T41.COH3N', 'T41.COHEN', 'T4L.C0H3N', 'T4L.C0HEN', 'T4L.COH3N',
                        'T4L.COHEN', 'TA1.C0H3N', 'TA1.C0HEN', 'TA1.COH3N', 'TA1.COHEN', 'TAL.C0H3N', 'TAL.C0HEN',
                        'TAL.COH3N', 'TAL.COHEN', 'DV0R4.T41', 'DV0R4.T4L', 'DV0R4.TA1', 'DV0R4.TAL', 'DV0RA.T41',
                        'DV0RA.T4L', 'DV0RA.TA1', 'DV0RA.TAL', 'DVOR4.T41', 'DVOR4.T4L', 'DVOR4.TA1', 'DVOR4.TAL',
                        'DVORA.T41', 'DVORA.T4L', 'DVORA.TA1', 'DVORA.TAL', 'D4N4.G114D1', 'D4N4.G114DI', 'D4N4.G11AD1',
                        'D4N4.G11ADI', 'D4N4.G1L4D1', 'D4N4.G1L4DI', 'D4N4.G1LAD1', 'D4N4.G1LADI', 'D4N4.GI14D1',
                        'D4N4.GI14DI', 'D4N4.GI1AD1', 'D4N4.GI1ADI', 'D4N4.GIL4D1', 'D4N4.GIL4DI', 'D4N4.GILAD1',
                        'D4N4.GILADI', 'D4NA.G114D1', 'D4NA.G114DI', 'D4NA.G11AD1', 'D4NA.G11ADI', 'D4NA.G1L4D1',
                        'D4NA.G1L4DI', 'D4NA.G1LAD1', 'D4NA.G1LADI', 'D4NA.GI14D1', 'D4NA.GI14DI', 'D4NA.GI1AD1',
                        'D4NA.GI1ADI', 'D4NA.GIL4D1', 'D4NA.GIL4DI', 'D4NA.GILAD1', 'D4NA.GILADI', 'DAN4.G114D1',
                        'DAN4.G114DI', 'DAN4.G11AD1', 'DAN4.G11ADI', 'DAN4.G1L4D1', 'DAN4.G1L4DI', 'DAN4.G1LAD1',
                        'DAN4.G1LADI', 'DAN4.GI14D1', 'DAN4.GI14DI', 'DAN4.GI1AD1', 'DAN4.GI1ADI', 'DAN4.GIL4D1',
                        'DAN4.GIL4DI', 'DAN4.GILAD1', 'DAN4.GILADI', 'DANA.G114D1', 'DANA.G114DI', 'DANA.G11AD1',
                        'DANA.G11ADI', 'DANA.G1L4D1', 'DANA.G1L4DI', 'DANA.G1LAD1', 'DANA.G1LADI', 'DANA.GI14D1',
                        'DANA.GI14DI', 'DANA.GI1AD1', 'DANA.GI1ADI', 'DANA.GIL4D1', 'DANA.GIL4DI', 'DANA.GILAD1',
                        'DANA.GILADI', 'D4V1D.M4N', 'D4V1D.MAN', 'D4VID.M4N', 'D4VID.MAN', 'DAV1D.M4N', 'DAV1D.MAN',
                        'DAVID.M4N', 'DAVID.MAN']

        patterns = Pattern('|replace(upper(leet(names))," ", ".")|')
        tokens = patterns.get_tokens()
        manipulated_result = []
        for token in tokens:
            # function = token.get_function()
            function_and_args = token.get_function_and_args()
            category = token.get_category()
            generator = Generator(patterns, self.profile)
            result = generator.get_values_for_simple_token(category)

            while function_and_args:

                cur_function, args = function_and_args.pop()
                if cur_function in Token.special_functions:
                    result = Utils.special_manipulate_list(cur_function, result, args)
                else:
                    result = Utils.manipulate_list(cur_function, result)
            manipulated_result += result
        self.assertEqual(right_result, manipulated_result)


class testGenerate(unittest.TestCase):
    def setUp(self):
        # profile_file = "tests/default_profile.geney"
        # pattern_file = "tests/default_patterns.pgeney"
        # result_file = "tests/default_result.dic"
        #
        # with open(profile_file, 'r') as f:
        #     profile_as_json = json.load(f)
        #
        # with open(pattern_file, 'r') as f:
        #     data = f.read().splitlines()
        #     patterns = []
        #     for line in data:
        #         if not line.startswith('#') and not line.startswith('//'):
        #             patterns.append(line)
        # with open(result_file, 'r') as f:
        #     self.default_result_list = f.read().splitlines()

        self.default_result_list = [u'tal cohen', u'dvora tal', u'dana giladi', u'david man', u'al', u'vo', u'an',
                                    u'av', u'basketball', u'baske', u'football', u'basketball', 'test', u'a', u'b',
                                    u'c', u'aa', u'ab', u'ac', u'ba', u'bb', u'bc', u'ca', u'cb', u'cc', u'aaa', u'aab',
                                    u'aac', u'aba', u'abb', u'abc', u'aca', u'acb', u'acc', u'baa', u'bab', u'bac',
                                    u'bba', u'bbb', u'bbc', u'bca', u'bcb', u'bcc', u'caa', u'cab', u'cac', u'cba',
                                    u'cbb', u'cbc', u'cca', u'ccb', u'ccc', u'FOOTBALL', u'BASKETBALL', u'aa', u'ab',
                                    u'ac', u'ba', u'bb', u'bc', u'ca', u'cb', u'cc', 'JOHN', 'JOHn', 'JOhN', 'JOhn',
                                    'JoHN', 'JoHn', 'JohN', 'John', 'jOHN', 'jOHn', 'jOhN', 'jOhn', 'joHN', 'joHn',
                                    'johN', 'john', u'Tal Cohen', u'Dvora Tal', u'Dana Giladi', u'David Man',
                                    't41 c0h3n', 't41 c0hen', 't41 coh3n', 't41 cohen', 't4l c0h3n', 't4l c0hen',
                                    't4l coh3n', 't4l cohen', 'ta1 c0h3n', 'ta1 c0hen', 'ta1 coh3n', 'ta1 cohen',
                                    'tal c0h3n', 'tal c0hen', 'tal coh3n', 'tal cohen', 'dv0r4 t41', 'dv0r4 t4l',
                                    'dv0r4 ta1', 'dv0r4 tal', 'dv0ra t41', 'dv0ra t4l', 'dv0ra ta1', 'dv0ra tal',
                                    'dvor4 t41', 'dvor4 t4l', 'dvor4 ta1', 'dvor4 tal', 'dvora t41', 'dvora t4l',
                                    'dvora ta1', 'dvora tal', 'd4n4 g114d1', 'd4n4 g114di', 'd4n4 g11ad1',
                                    'd4n4 g11adi', 'd4n4 g1l4d1', 'd4n4 g1l4di', 'd4n4 g1lad1', 'd4n4 g1ladi',
                                    'd4n4 gi14d1', 'd4n4 gi14di', 'd4n4 gi1ad1', 'd4n4 gi1adi', 'd4n4 gil4d1',
                                    'd4n4 gil4di', 'd4n4 gilad1', 'd4n4 giladi', 'd4na g114d1', 'd4na g114di',
                                    'd4na g11ad1', 'd4na g11adi', 'd4na g1l4d1', 'd4na g1l4di', 'd4na g1lad1',
                                    'd4na g1ladi', 'd4na gi14d1', 'd4na gi14di', 'd4na gi1ad1', 'd4na gi1adi',
                                    'd4na gil4d1', 'd4na gil4di', 'd4na gilad1', 'd4na giladi', 'dan4 g114d1',
                                    'dan4 g114di', 'dan4 g11ad1', 'dan4 g11adi', 'dan4 g1l4d1', 'dan4 g1l4di',
                                    'dan4 g1lad1', 'dan4 g1ladi', 'dan4 gi14d1', 'dan4 gi14di', 'dan4 gi1ad1',
                                    'dan4 gi1adi', 'dan4 gil4d1', 'dan4 gil4di', 'dan4 gilad1', 'dan4 giladi',
                                    'dana g114d1', 'dana g114di', 'dana g11ad1', 'dana g11adi', 'dana g1l4d1',
                                    'dana g1l4di', 'dana g1lad1', 'dana g1ladi', 'dana gi14d1', 'dana gi14di',
                                    'dana gi1ad1', 'dana gi1adi', 'dana gil4d1', 'dana gil4di', 'dana gilad1',
                                    'dana giladi', 'd4v1d m4n', 'd4v1d man', 'd4vid m4n', 'd4vid man', 'dav1d m4n',
                                    'dav1d man', 'david m4n', 'david man', u'talcohen', u'dvoratal', u'danagiladi',
                                    u'davidman', u'tc', u'dt', u'dg', u'dm', u'6512345250', u'5656566450', 'tal.cohen',
                                    'dvora.tal', 'dana.giladi', 'david.man', u'tal testcohen', u'dvortesta tal',
                                    u'danatest giladi', u'davitestd man']

        patterns = ['|names|', '|names[1:3]|', '|hobbies.hobby_A|', '|hobbies.hobby_A[:5]|', '|hobbies|', '|"test"|',
                    '|r"[abc]{1,3}"|', '|upper(hobbies)|', '|lower(r"[ABC]{2}")|', '|scramble("john")|',
                    '|title(names)|', '|leet(names)|', '|strip(names)|', '|initials(names)|', '|reverse(phones)|',
                    '|replace(names, " ", ".")|', '|add(names, "test", 4)|', '|cut(address, " ")|']

        profile_as_json = {
            u'dates': {u'birth_day': u'16/01/1993', u'mom_birth': u'17/03/1974', u'dad_birth': u'03/06/1973'},
            u'phones': {u'target_phone': u'0525432156', u'mom_phone': u'0546656565'},
            u'hobbies': {u'hobby_B': u'football', u'hobby_A': u'basketball'},
            u'names': {u'target_name': u'tal cohen', u'target_son': u'dvora tal', u'target_mother': u'dana giladi',
                       u'target_husband': u'david man'},
            u'address': {u'home': u'5th avenu new york', u'work': u'brooklyn street new york'},
            u'work_phones': {u'work_phone': u'065412345', u'home_phone': u'0773658844'}}

        self.profile = Profile(profile_as_json)
        self.patterns = patterns

    def test_please_generate_for_patterns_and_profile(self):
        result = []
        for pattern in self.patterns:
            pattern = Pattern(pattern)
            geney = Generator(pattern, self.profile)
            words_for_pattern = geney.please_generate()
            words_for_pattern_product = list(itertools.product(*words_for_pattern))
            words_for_pattern_strings = [''.join(tup) for tup in words_for_pattern_product]
            result += words_for_pattern_strings
        print result
        self.assertEqual(self.default_result_list, result)


# TODO check count
# TODO check size

if __name__ == '__main__':
    unittest.main()
