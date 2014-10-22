# -*- coding: utf-8 -*-

"""
tests.restaurants_test
~~~~~~~~~~~~~~~

This module tests retreiving restaurants from ordr.in.
"""

import os
import unittest
import simplejson as json
from time import sleep
from hashlib import sha256
from random import randrange
from silently.frontend import create_app
from silently.api import ordrin
from requests import HTTPError
from flask_login import login_user, current_user

class SilentlyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(settings_override={'CACHE_TYPE': 'null'})

    def test_get_restaurants(self):
        """Tests for the presence of the test entry in a restaurant list."""
        address = {'number': '375',
                   'street': 'Noe St',
                   'city': 'San Francisco',
                   'zip': '94114'}

        with self.app.app_context():
            restaurants = ordrin.get_restaurants(address)

        # Ordr.in returns a test entry as the first item in the list when
        # when hitting their testing servers.
        entry = restaurants[0]
        self.assertEquals(entry['na'], 'Test Merchant 20130315')
        self.assertEquals(entry['id'], 23917)

    def test_get_details(self):
        """Tests the menu for the test entry."""
        restaurant_id = 23917
        with self.app.app_context():
            details = ordrin.get_details(restaurant_id)

        self.assertEquals(details['name'], 'Test Merchant 20130315',
                'Check restaurant name on test details.')
        self.assertEquals(details['id'], restaurant_id,
                'Check restaurant id on test details.')
        self.assertTrue(details['delivers'], 'Check delivery flag on test entry.')
        self.assertTrue(details['allows_asap'],
                'Check asap flag on test details.')
        self.assertAlmostEqual(details['location'][0], 42.825685,
                'Check latitude on test details.')
        self.assertAlmostEqual(details['location'][1], -73.879458,
                'Check longitude on test details.')
        self.assertEquals(details['partner'], 'delivery.com',
                'Check delivery partner on test details.')
        self.assertEquals(details['address'], '123 FAKE ST',
                'Check address on test details.')
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
