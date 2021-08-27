# -*- coding: utf-8 -*-
"""
    odktools.resources.resources
    ~~~~~~~~~~~~~~~~~~

    Provides the different helper functions to a pyramid request.

    :copyright: (c) 2017 by QLands Technology Consultants.
    :license: AGPL, see LICENSE for more details.
"""

import arrow
from ago import human

import ushauri.plugins as p

__all__ = ["helper"]


class helper:
    request = None

    def __init__(self, request):
        self.request = request

    # This function will humanize a date using ago
    def humanize_date(self, date):
        return human(date, precision=1)

    def readble_date(self, date):
        ar = arrow.get(date)
        return ar.format("dddd Do of MMMM, YYYY")

    def pluralize(self, noun, size):
        if size == 1:
            return noun
        plural = noun
        # Call connected plugins to see if they have extended or overwrite ushauri pluralize function
        for plugin in p.PluginImplementations(p.IPluralize):
            res = plugin.pluralize(noun, self.request.locale_name)
            if res != "":
                plural = res
        # Will return English pluralization if none of the above happens
        # return pluralize_en(noun)
        return plural
