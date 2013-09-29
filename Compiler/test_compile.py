import subprocess
import shlex
import time
import sys
import os

compile_ret_code = 0		#checking if compilation was successful or not

def compile(in_file, out_file='compile.log'):			#in_file-> source code; out_file-> redirect for STDOUT 
	
	ext = in_file.split(".")[-1]
	path_temp = in_file.split('/')[:-1]
	path = '/'.join(path_temp)
	fl = in_file.split('/')[-1]
	file_name = fl.split('.')[0]
	object_file = path+'/'+file_name
	
	ccmd = '-Wall -o ' + '"' + object_file + '"  "' + in_file + '"'
	
	if ext == 'c':
		cmd = 'gcc '+ ccmd
		lang = 'c'
		
	elif ext == 'c++':
		cmd = 'g++ ' + ccmd
		lang = 'c++'
		
	elif ext == 'java':
		cmd = 'javac -d ' + '"' + path + '" "' + in_file +'"'
		lang = 'java'
		
	print cmd
	out = open(out_file,'wb')
	p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = out)	
	compile_ret_code = p.wait()
	
	return compile_ret_code,object_file,lang				#Return the return code of compilation, name of the object file
	
def execute(obj_file,lang,arg_list=[]):
	
	args = ' '.join(arg_list)
	
	if lang == 'c' or lang == 'c++':
		cmd = '"' + obj_file + '" ' + args
	
	print(cmd)	
	os.system("gnome-terminal -e 'bash -c \"bash run_script.sh\"'")
	
def main():
	file1 = '/workspace/ADSAProject2/src/dataStructures/Trie.java'
	file2 = '/Documents/ebooks/Comp/5th sem/OS Lab/Lab/fcfs.c'
	
	ret_code, obj_file, lang = compile(os.environ['HOME']+file2)
	
	if ret_code == 0:
		execute(obj_file, lang)
	
	print 'complete'
	
main()
