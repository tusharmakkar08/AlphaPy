#!/usr/local/bin/python

import pygtk
pygtk.require('2.0')
import gtk
import search

class window:
	
	def search_dialog(self,widget,data=None):
		dialog = gtk.Dialog("Find", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
		
		dialog.set_size_request(300,100)
		
		hbox1 = gtk.HBox(False,0)
		hbox2 = gtk.HBox(False,0)
		
		label = gtk.Label("Enter String")
		hbox1.pack_start(label)
		label.show()
		
		self.entry= gtk.Entry()
		hbox1.pack_start(self.entry)
		self.entry.show()
		
		button = gtk.Button('Find Next')
		button.connect('clicked', self.find_next)
		button.show()
		hbox2.pack_start(button)
		
		#~ button = gtk.Button('Find Previous')
		#~ #button.connect('clicked', self.find_prev)
		#~ button.show()
		#~ hbox2.pack_start(button)
		
		hbox1.show()
		hbox2.show()
		dialog.vbox.pack_start(hbox1, gtk.TRUE, gtk.TRUE, 0)
		dialog.vbox.pack_start(hbox2, gtk.TRUE, gtk.TRUE, 0)
		
		response = dialog.run()
		dialog.destroy()	
		
	def delete_event(self,widget,event,data=None):
		"Quit window"
		if self.change:
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO,"Save before quit ?")
			dialog.set_title("WARNING ..")
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				self.onsave(self.window)
			elif response == gtk.RESPONSE_NO:
				gtk.main_quit()
			else: return True
			return False
		else:
			gtk.main_quit()
			return False
		
	def __init__(self):
		"Initiate the window,button,etc .."
		self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(True)
		self.title="AlphaPy Text Editor"
		self.change=0
		self.window.set_title(self.title)
		self.window.connect("delete_event",self.delete_event)
		self.window.set_border_width(1)
		self.window.set_size_request(800,700)
		hbox = gtk.HBox(False, 0)
		expand=False
		fill=False
		padding=2
		self.file=""
		self.tooltips = gtk.Tooltips()
		
		image = gtk.Image()
   	        image.set_from_file("icons/open.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Open file")
		button.add(image)
		button.connect("clicked",self.onopen)
		hbox.pack_start(button, expand, fill, padding)
    		button.show()
		
		image = gtk.Image()
   	        image.set_from_file("icons/save.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Save file")
		button.add(image)
		button.connect("clicked",self.onsave)
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()
    		
    		image = gtk.Image()
   	        image.set_from_file("icons/save as.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Save as..")
		button.add(image)
		button.connect("clicked",self.saveas)
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()
    		
		image = gtk.Image()
   	        image.set_from_file("icons/cut.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Cut")
		button.add(image)
		button.connect("clicked",self.cut)
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()
		
		image = gtk.Image()
   	        image.set_from_file("icons/copy.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Copy")
		button.add(image)
		button.connect("clicked",self.copy)
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()
    		
    		image = gtk.Image()
   	        image.set_from_file("icons/paste.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Paste")
		button.add(image)
		button.connect("clicked",self.paste)
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()  
    		
    		image = gtk.Image()
   	        image.set_from_file("icons/find.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Find")
		button.add(image)
		button.connect("clicked", self.search_dialog)			#Set Handler for searching.
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()    		
		
		image = gtk.Image()
   	        image.set_from_file("icons/quit.png")
   	        image.show()
		self.button = gtk.Button()
		self.tooltips.set_tip(self.button, "Quit")
		self.button.add(image)
		self.button.connect("clicked",self.delete_event,None)
    		hbox.pack_start(self.button, expand, fill, padding)
		self.button.show()
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.textview = gtk.TextView()
		self.textview.set_editable(True)
		self.textbuffer = self.textview.get_buffer()
		sw.add(self.textview)
		self.textview.show()
		sw.show()
		self.clipboard=gtk.Clipboard()		
		self.textbuffer.connect("changed",self.changetitle);
		
		
		vbox=gtk.VBox(False,0)
		vbox1=gtk.VBox(False,10)
		vbox.pack_start(hbox, False, False, 0)
        	vbox1.pack_start(sw)
        	vbox1.set_border_width(2)
        	vbox.pack_start(vbox1, True, True, 0)
        	self.status_bar = gtk.Statusbar()      
        	self.textbuffer.connect("notify::cursor-position",self.changestbr);
   	        vbox.pack_start(self.status_bar, False, False, 0)
   	        self.status_bar.show()
   	        self.context_id = self.status_bar.get_context_id("Statusbar example")
		self.window.add(vbox)
		hbox.show()
		vbox1.show()
		vbox.show()
		self.window.show()

	def cut(self,widget):
		self.textbuffer.cut_clipboard(self.clipboard, True)
	
	def copy(self,widget):
		self.textbuffer.copy_clipboard(self.clipboard)
	
	def paste(self,widget):
		self.textbuffer.paste_clipboard(self.clipboard,None, True)
	
	
	def changetitle(self,widget):
		"Change Title when file is temporary"
		if self.change==0:
			self.title="**"+self.title
			self.window.set_title(self.title)
			self.change=1
		
	def changestbr(self,widget,data=None):
		"Change statusbar values"
		cl= 1+self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert()).get_line()
		col=self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert()).get_line_index()
		ln=self.textbuffer.get_line_count()
		ch=self.textbuffer.get_char_count()
		selln=0
		selch=0
		if self.textbuffer.get_selection_bounds()!=():
			st,end=self.textbuffer.get_selection_bounds()
			selln=end.get_line()-st.get_line()+1
			selch=end.get_offset()-st.get_offset()
		data="\t\tline : "+str(cl)+"  col : "+str(col)+"\t\tlines : "+str(ln)+" chars : "+str(ch)+"\tSel : "+str(selln)+" | "+str(selch)
		if self.file=="":
			text="New file"+data
		else:
			text=self.file+data
		self.status_bar.push(self.context_id, text)
		
		
	def onsave(self,widget):
		"To save a file and set th file parameter if it is a new file or just overwrite"
		if self.file=="":
			dialog = gtk.FileChooserDialog("Save..",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			filter = gtk.FileFilter()
			filter.set_name("All files")
	   		filter.add_pattern("*")
	 		dialog.add_filter(filter)
	 		response = dialog.run()
	   		if response == gtk.RESPONSE_OK:
	   			self.file=dialog.get_filename()
	   			out=open(self.file,"w")
	   			start, end = self.textbuffer.get_bounds()
	   			text = self.textbuffer.get_text(start, end, include_hidden_chars=True)
	   			out.write(text)
	   			self.title=self.file+" - AlphaPy Text Editor"
	   			self.window.set_title(self.title)
	   			self.change=0
	   			print "Save Succesful"
	   	   	elif response == gtk.RESPONSE_CANCEL:
	   		       print 'Closed, no files selected'
	   		dialog.destroy()
	   	else:
	   		out=open(self.file,"w")
	   		start, end = self.textbuffer.get_bounds()
	   		text = self.textbuffer.get_text(start, end, include_hidden_chars=True)
	   		out.write(text)
	   		print "Save Succesful"
   			self.title=self.file+" - AlphaPy Text Editor"
   			self.window.set_title(self.title)
   			self.change=0
	   		
	
	def saveas(self,widget):
			"Save the file with a different name"
			dialog = gtk.FileChooserDialog("Save as..",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			filter = gtk.FileFilter()
			filter.set_name("All files")
	   		filter.add_pattern("*")
	 		dialog.add_filter(filter)
	 		response = dialog.run()
	   		if response == gtk.RESPONSE_OK:
	   			self.file=dialog.get_filename()
	   			out=open(self.file,"w")
	   			start, end = self.textbuffer.get_bounds()
	   			text = self.textbuffer.get_text(start, end, include_hidden_chars=True)
	   			out.write(text)
	   			self.title=self.file+" - AlphaPy Text Editor"
	   			self.window.set_title(self.title)
	   			self.change=0
	   			print "Save Succesful"
	   	   	elif response == gtk.RESPONSE_CANCEL:
	   		       print 'Closed, no files selected'
	   		dialog.destroy()
	
		
		
	def onopen(self,widget):
		"To open a file and set the current file"
		dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
		    self.file= dialog.get_filename()
		    self.textbuffer.set_text(open(self.file,"r+").read())
		    self.title=self.file+" - AlphaPy Text Editor"
		    self.window.set_title(self.title)
		    self.change=0
		elif response == gtk.RESPONSE_CANCEL:
		    print 'Closed, no files selected'
		dialog.destroy()
		
	def find_next(self,widget, data=None):
		
		iput = self.entry.get_text()
		print '\n' + iput
		if iput == '':
			print 'Invalid search input'
		else:
			startiter = self.textbuffer.get_start_iter()
			
			if type(startiter) is None:
				print 'Input file is empty'
			
			else:
				try:
					match_start, match_end = startiter.forward_search(iput, gtk.TEXT_SEARCH_TEXT_ONLY)
				except:
					print 'String not found'
					return 
					
				if type(match_start) is not None and type(match_end) is not None:
					
					line_start = match_start.get_line() + 1
					line_end = match_end.get_line() + 1
					line_start_offset = match_start.get_line_index()
					line_end_offset = match_end.get_line_index()
					
					print 'start_offset:' + str(match_start.get_offset()) + ' end_offset:' + str(match_end.get_offset())
					print 'line_start:' + str(line_start) + ' line_end:' + str(line_end)
					print 'line_start_offset:' + str(line_start_offset) + ' line_end_offset:' + str(line_end_offset)
				
				else:
					print 'String not found'
	
def main():
	gtk.main()
	return 0

if __name__=="__main__":
	window()
	main()
