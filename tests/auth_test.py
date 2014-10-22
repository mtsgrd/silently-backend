# -*- coding: utf-8 -*-

"""
tests.auth_test
~~~~~~~~~~~~~~~

This module tests authentication against ordr.in.
"""

import os
import unittest
import simplejson as json
from hashlib import sha256
from random import randrange
from silently.frontend import create_app
from requests import HTTPError
from flask_login import login_user, current_user

class SilentlyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.account = cls._new_account()

    def tearDown(self):
        pass

    @classmethod
    def _new_account(cls):
        """Generates random account details.
        
        When we create a new user against the ordrin test servers it
        persists. Therefore we need a new user id for each test we run.
        """
        randint = randrange(1e6, 1e7-1)
        return {'email': str(randint) + '@testing.com',
                'password': 'HelloWorld-' + str(randint),
                'firstname': 'Mattias',
                'lastname': 'Granlund'}

    def test_1_register(self):
        """Registers a new account on the test servers.

        We can pass the entire account dict to the API since it only looks for
        username and password.
        """
        res = self.client.post('/auth/register', data=self.account)
        data = json.loads(res.data)
        self.assertEqual(self.account['email'], data.get('email'),
                'Email mismatch.')
        self.assertEqual(sha256(self.account['password']).hexdigest(),
                data.get('password'), 'Password mismatch.')
        self.assertEqual(self.account['firstname'], data.get('firstname'),
                'Firstname mismatch.')
        self.assertEqual(self.account['lastname'], data.get('lastname'),
                'Lastname mismatch.')


    def test_2_sign_in(self):
        """Tests that the newly registered account matches the input."""
        # Retrieve account we created in test #1
        res = self.client.post('/auth/login', data=self.account)
        data = json.loads(res.data)
        self.assertEqual(self.account['email'], data.get('email'), 'Email mismatch.')
        self.assertEqual(sha256(self.account['password']).hexdigest(),
                data.get('password'), 'Password mismatch.')
        self.assertEqual(self.account['firstname'], data.get('firstname'),
                'Firstname mismatch.')
        self.assertEqual(self.account['lastname'], data.get('lastname'),
                'Last name mismatch.')

    def test_3_create_invalid_account(self):
        """Tries to register previously registered account."""
        try:
            res = self.client.post('/auth/register', data=self.account)
            self.assertTrue(False, 'Unauthorized exception expected.')
        except HTTPError as err:
            self.assertEqual(err.response.status_code, 401,
                    'Unauthorized status expected.')

    def test_get_invalid_account(self):
        """Tests that a bogus account returns an error."""
        # Retrieve account we created in test #1
        invalid_account = self._new_account()
        try:
            res = self.client.post('/auth/login', data=invalid_account)
            self.assertTrue(False, 'Unauthorized exception expected.')
        except HTTPError as err:
            self.assertEqual(err.response.status_code, 401,
                    'Unauthorized status expected.')

    def test_bad_forms(self):
        """Tests that a bad form data returns errors."""

        # Testing the login form.
        bad_account = {'email': 'a@c', 'password': 'abc'}
        res = self.client.post('/auth/login', data=bad_account)
        data = json.loads(res.data)
        self.assertIn('errors', data, 'Form errors expected.')
        self.assertIn('email', data['errors'], 'Short email allowed.')
        self.assertIn('password', data['errors'], 'Short password allowed.')

        bad_account = {'email': 'a' * 257, 'password': 'a' * 257}
        res = self.client.post('/auth/login', data=bad_account)
        data = json.loads(res.data)
        self.assertIn('errors', data, 'Form errors expected.')
        self.assertIn('email', data['errors'], 'Long email allowed.')
        self.assertIn('password', data['errors'], 'Long password allowed.')

        # Testing the register form.
        bad_account = {'email': 'abc@def.com', 'password': 'abcd',
                'firstname': '', 'lastname': ''}
        res = self.client.post('/auth/register', data=bad_account)
        data = json.loads(res.data)
        self.assertIn('errors', data, 'Form errors expected.')
        self.assertIn('firstname', data['errors'], 'Short firstname allowed.')
        self.assertIn('lastname', data['errors'], 'Short lastname allowed.')

        bad_account = {'email': 'abc@def.com', 'password': 'abcd',
                'firstname': 'a' * 61, 'lastname': 'a' * 61}
        res = self.client.post('/auth/register', data=bad_account)
        data = json.loads(res.data)
        self.assertIn('errors', data, 'Form errors expected.')
        self.assertIn('firstname', data['errors'], 'Long firstname allowed.')
        self.assertIn('lastname', data['errors'], 'Long lastname allowed.')

if __name__ == '__main__':
    unittest.main()
