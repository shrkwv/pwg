#!/usr/bin/env python
from __future__ import unicode_literals

from Token import Token

class Pattern:

    def __init__(self, pattern):
        self.pattern = pattern

    def get_tokens(self):
        """
        return all tokens for the pattern as list.
        """
        tokens = []
        tokens_as_string = self.pattern.split("|")[1:-1]
        for token_as_string in tokens_as_string:
            token = Token(token_as_string)
            tokens.append(token)
        return tokens
