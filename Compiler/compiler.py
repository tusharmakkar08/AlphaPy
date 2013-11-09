import subprocess
import shlex
import time
import sys
import os

compile_ret_code = 0		#checking if compilation was successful or not
comp_lang = ['c','cpp','java','py']
log_file = 'Compiler/compile.log'
def get_file_extension(in_file): 	#Finding file extension
	return in_file.split(".")[-1]
	
def compile_file(in_file,  ext = '', out_file=log_file):			#in_file-> source code; out_file-> redirect for STDOUT 
	if ext == '':
		ext = get_file_extension(in_file)
		
	compile_ret_code = -1
	path_temp = in_file.split('/')[:-1]
	path = '/'.join(path_temp)
	fl = in_file.split('/')[-1]
	file_name = fl.split('.')[0]
	object_file = path+'/'+file_name
	
	ccmd = '-Wall -o ' + '"' + object_file + '"  "' + in_file + '"'
	
	if ext == 'c':
		cmd = 'gcc '+ ccmd
		
	elif ext == 'cpp':
		cmd = 'g++ ' + ccmd
		
	elif ext == 'java':
		cmd = 'javac -d ' + '"' + path + '" "' + in_file +'"'
	
	elif ext == 'py':
		cmd = 'python -m py_compile '+ '"' + in_file +'"'
		object_file = in_file	
	lang = ext

	with open(out_file,'wb') as out:
		if cmd == '':
			print >> out, 'The language of the source code is not supported by this editor'
		
		else:
			print >> out, cmd
			p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = out)	
			compile_ret_code = p.wait()
			
			if compile_ret_code == 0:
				print >> out,'Compilation Successful'
			else:
				print >> out, 'Compilation Failed'
				
	return compile_ret_code,object_file,lang				#Return the return code of compilation, name of the object file
	
def execute(obj_file,args = '',lang = '' ,args_file = '.args'): 	#Execute the object file by passing thee necessary details to the run script
														
	ret_code = 1
	if lang == '':
		ext = get_file_extension(obj_file)
		if ext in comp_lang:
			ret_code,obj_file,lang = compile_file(obj_file, ext)   #Compile if necessary
		else:
			lang = ext
			with open(out_file,'wb') as out:
				print >> out,'Compilation Successful'
			ret_code = 0
			
	if ret_code == 0:		
		print 'Compilation Successful, Executing'
		f = open(args_file,'wb')					
		print >> f, obj_file
		print >> f, lang
		print >> f, args
		os.system("gnome-terminal -e 'bash -c \"bash Compiler/run_script.sh " + args_file + "\"'") 	# FIND A BETTER WAY TO INCLUDE ALL THE ARGS IN THIS COMMAND, AND NOT USING A TEMP FILE 
	
	else:
		print 'Compilation errors, check the log file'

#~ def main():
	#~ file1 = os.environ['HOME'] + '/workspace/ADSAProject2/src/dataStructures/Trie.java'
	#~ file2 = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/OS Lab/Lab/cat.c'
	#~ file3 = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/OS Lab/Lab/cat.cpp'
	#~ py_file = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/SP/AlphaPy/alphapy.py'
	#~ rb_file = os.environ['HOME'] + '/Downloads/server.rb'
	#~ sh_file = os.environ['HOME'] + '/start-aomx.sh'
	#~ r_file = os.environ['HOME'] + '/Documents/TUD Internship/Backup/Share64/storm-distributed/Graphs/latency.R'
	#~ arg2 = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/OS Lab/Lab/semaphore.c'

	#~ execute(py_file, 'py')
	#~ execute(rb_file, 'rb')
	#~ execute(sh_file,'sh')
	#~ ret_code, obj_file, lang = compile(file3)
	#~ 
	#~ if ret_code == 0:
	#~ execute(arg2, '')
	
	#print 'complete'
	
#~ main()
