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

# Importing modules

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

def upload(name,content):
	gauth = GoogleAuth()
	drive = GoogleDrive(gauth)
	file1 = drive.CreateFile({'title': name})  
	file1.SetContentString(content) 
	file1.Upload()

def get_name():
	gauth = GoogleAuth()
	drive = GoogleDrive(gauth)
	file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	k=""
	for file1 in file_list:
		k+='%s\n'%(file1['title'])
	return k
		
def test1():
	get_name()

def test2():
	k=raw_input("Enter name of file\n")
	l=raw_input("Enter content of file\n")
	upload(k,l)
	
#test2()
