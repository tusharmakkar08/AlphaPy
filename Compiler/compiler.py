import subprocess
import shlex
import time
import sys
import os

compile_ret_code = 0		#checking if compilation was successful or not

def get_file_extension(in_file): 	#Finding file extension
	return in_file.split(".")[-1]
	
def compile(in_file,  ext = '', out_file='compile.log'):			#in_file-> source code; out_file-> redirect for STDOUT 
	
	if ext == '':
		ext = get_file_extension(in_file)
	
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
		
	lang = ext

	if cmd == '':
		print 'The language of the source code is not supported by this editor'
	
	else:
		out = open(out_file,'wb')
		p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = out)	
		compile_ret_code = p.wait()
	
		return compile_ret_code,object_file,lang				#Return the return code of compilation, name of the object file
	
def execute(obj_file,args = '',lang = '' ,args_file = '.args'): 	#Execute the object file by passing thee necessary details to the run script
														
	ret_code = 1
	if lang == '':
		ext = get_file_extension(obj_file)
		if ext == 'c' or ext == 'cpp' or ext == 'java':
			ret_code,obj_file,lang = compile(obj_file, ext)   #Compile if necessary
		else:
			lang = ext
			ret_code = 0
			
	if ret_code == 0:		
		f = open(args_file,'wb')					
		print >> f, obj_file
		print >> f, lang
		print >> f, args
		os.system("gnome-terminal -e 'bash -c \"bash run_script.sh " + args_file + "\"'") 	# FIND A BETTER WAY TO INCLUDE ALL THE ARGS IN THIS COMMAND, AND NOT USING A TEMP FILE 
	
def main():
	file1 = os.environ['HOME'] + '/workspace/ADSAProject2/src/dataStructures/Trie.java'
	file2 = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/OS Lab/Lab/cat.c'
	file3 = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/OS Lab/Lab/cat.cpp'
	py_file = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/SP/AlphaPy/alphapy.py'
	rb_file = os.environ['HOME'] + '/Downloads/server.rb'
	sh_file = os.environ['HOME'] + '/start-aomx.sh'
	r_file = os.environ['HOME'] + '/Documents/TUD Internship/Backup/Share64/storm-distributed/Graphs/latency.R'
	arg2 = os.environ['HOME'] + '/Documents/ebooks/Comp/5th sem/OS Lab/Lab/ipc.c'

	#~ execute(py_file, 'py')
	#~ execute(rb_file, 'rb')
	#~ execute(sh_file,'sh')
	#~ ret_code, obj_file, lang = compile(file3)
	#~ 
	#~ if ret_code == 0:
	execute(r_file,arg2)
	
	#print 'complete'
	
main()
