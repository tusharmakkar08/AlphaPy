#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  syntaxhighlighter.py
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

import pygments

from pygments import highlight
from pygments.lexers import *
from pygments.formatters import *
from pygments.styles import STYLE_MAP
from pygments.styles import get_all_styles

import os

import webbrowser

"""Main code"""

def guess_lex(code):
	return guess_lexer(code)
	
def guess_lex_file(name,code):
	return guess_lexer_for_filename(name,code)

def Highlight(name):
	k="pygmentize %s"%(name)
	os.system(k)
	
def pref_style():
	styles = list(get_all_styles())
	print "Choose from one of the styles"
	count=1
	for i in styles:
		print count,":",i
		count+=1
	k=input()
	return styles[k-1]

def html_out(name,k):
	"""HTML printed"""
	styles = list(get_all_styles())
	m=styles[k-1]
	print m
	new=""
	for i in name:
		if i==".":
			break
		new+=i
	stri="pygmentize -O full,style="+m+" -o "+new+".html "+name
	print stri
	os.system(stri)

def show_html(name):
	new=""
	for i in name:
		if i==".":
			break
		new+=i
	url=new+".html"
	stri="libreoffice --writer -o %s"%(url)
	os.system(stri)

def open_html(name):
	newt=2 		# open in a new tab, if possible
	new=""
	for i in name:
		if i==".":
			break
		new+=i
	url=new+".html"
	webbrowser.open(url,new=newt)

def rtf_out(name):
	"""Rich text format"""
	m=pref_style()
	new=""
	for i in name:
		if i==".":
			break
		new+=i
	stri="pygmentize -O full,style="+m+" -o "+new+".rtf "+name
	os.system(stri)

def open_rtf(name):
	new=""
	for i in name:
		if i==".":
			break
		new+=i
	url=new+".rtf"
	stri="libreoffice --writer -o %s"%(url)
	os.system(stri)

def copy_clipboard(name,flag):
	"""For directly cutting paste to different pahes like powerpoint etc"""
	new=""
	for i in name:
		if i==".":
			break
		new+=i
	if flag==1:
		stri="xclip -in -selection c "+new+".html"
	else:
		stri="xclip -in -selection c "+new+".rtf"
	os.system(stri)
	
"""Code Testing"""
#t=raw_input("Enter filename\n")
#html_out("test.py",5)
#copy_clipboard(t,1)
#open_rtf(t)
#print pref_style()	
