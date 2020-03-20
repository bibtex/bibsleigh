#!/c/Users/vadim/AppData/Local/Programs/Python/Python37-32/python
# -*- coding: utf-8 -*-
#
# a module for colourful console output
#
# The pun in “from ANSI import C” is intended.

def colour(c, s):
	return '{}{}{}'.format(c, s, '\033[0m')

class colours:
	def __init__(self):
		pass
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	ULINE = '\033[4m'
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	BLUE = '\033[94m'
	PURPLE = '\033[95m'
	def bold(self, s):
		return colour(self.BOLD, s)
	def uline(self, s):
		return colour(self.ULINE, s)
	def red(self, s):
		return colour(self.RED, s)
	def green(self, s):
		return colour(self.GREEN, s)
	def yellow(self, s):
		return colour(self.YELLOW, s)
	def blue(self, s):
		return colour(self.BLUE, s)
	def purple(self, s):
		return colour(self.PURPLE, s)

C = colours()
