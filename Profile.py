#!/usr/bin/env python
class Profile:

    def __init__(self, profile):
        self.profile = profile

    def get_values_for_category(self, category):
        """
        get all values for the required category
        """
        values = []
        try:
            values = self.profile[category].values()
        except:
            pass
            #TODO
        return values

    def get_value_for_field(self, category, field):
        """
        get specific value for field in category.
        """
        value = []
        try:
            value.append(self.profile[category][field])
        except:
            pass
            #TODO
        return value
