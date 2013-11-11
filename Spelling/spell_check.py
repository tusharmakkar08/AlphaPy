#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  spell_check.py
#  
#  Copyright 2013 tusharmakkar08 <tusharmakkar08@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

""" Importing Modules """

import enchant


import os
import sys    
import termios
import fcntl


"""Function for taking running input"""

def getch():
  """	
	For taking charachter by charachter
  """
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c
        
"""Main code"""


d=enchant.Dict("en_US")


def check_exist(word):
	"""
		Check the existence of the word . Returns True or 
	    False depending on whether word exists or not
	"""
	global d
	return d.check(word)


def spell_correct(word):
	"""
		Suggesting spelling corrections . Returns the list of suggestions 
	"""
	global d
	cor_list=[]
	if(check_exist(word)==False):
		cor_list=d.suggest(word)
	return cor_list


def get_text():
	"""
		Getting running text
	"""
	t=""
	while(1):
		user_inp=getch()
		print user_inp
		if user_inp==" " or user_inp=="\n":
			k=[]
			k=spell_correct(t)
			if k==[]:
				t=""
				continue
			ask_resp(k)
			t=""
			user_inp=""
		t+=user_inp
			
			
def ask_resp(l):
	"""
		Asking for User consent 
	"""
	a=raw_input("Do you think you entered correct word (Y/N) ?\n")
	if a=="N" or a=="n":
		k=1
		print "Enter number of correct suggestion or -1 if suggestion not found ."
		for i in l:
			print "#",k," : ",i
			k+=1
		ting=input()
		if ting==-1:
			tim=raw_input("Enter the desired word\n")
			print tim
			return tim
		else:
			print l[ting-1]
			return l[ting-1]
			
print get_text()
