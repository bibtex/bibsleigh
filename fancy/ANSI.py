#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for colourful console output
# 
# The pun in “from ANSI import C” is intended.

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
		return '{}{}{}'.format(self.BOLD, s, self.ENDC)
	def uline(self, s):
		return '{}{}{}'.format(self.ULINE, s, self.ENDC)
	def red(self, s):
		return '{}{}{}'.format(self.RED, s, self.ENDC)
	def green(self, s):
		return '{}{}{}'.format(self.GREEN, s, self.ENDC)
	def yellow(self, s):
		return '{}{}{}'.format(self.YELLOW, s, self.ENDC)
	def blue(self, s):
		return '{}{}{}'.format(self.BLUE, s, self.ENDC)
	def purple(self, s):
		return '{}{}{}'.format(self.PURPLE, s, self.ENDC)

C = colours()
