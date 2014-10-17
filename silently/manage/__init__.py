# -*- coding: utf-8 -*-

from flask_script import Option
from flask_script import Command

class HelloWorld(Command):
    option_list = (
            Option('--verbose', '-v', dest='verbose', default=False),
            )

    def run(self, verbose):
        print "Hello World"
        if verbose:
            print "How are you?"
