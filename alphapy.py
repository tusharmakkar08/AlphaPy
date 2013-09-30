#!/usr/local/bin/python

import pygtk
pygtk.require('2.0')
import gtk

class window ():
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
		self.undo_max = 100	
		self._highlight_strings = []
		self.undos = []
		self.redos = []
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
   	        image.set_from_file("icons/undo.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Undo")
		button.add(image)
		button.connect("clicked",self.undo)
		hbox.pack_start(button, expand, fill, padding)
    		button.show()

		image = gtk.Image()
   	        image.set_from_file("icons/redo.png")
   	        image.show()
		button = gtk.Button()
		self.tooltips.set_tip(button, "Redo")
		button.add(image)
		button.connect("clicked",self.redo)
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
		self.insert_event = self.textview.get_buffer().connect("insert-text",self._on_insert)
	        self.delete_event = self.textview.get_buffer().connect("delete-range",self._on_delete)
	        self.change_event = self.textview.get_buffer().connect("changed",self._on_text_changed)

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
		
		
	def undo(self,widget):
		if len(self.undos) == 0:
			print "length is "+ str(len(self.undos))
		        return
		print "length is "+str(len(self.undos))
	        self.textview.get_buffer().disconnect(self.delete_event)
	        self.textview.get_buffer().disconnect(self.insert_event)

	        undo = self.undos[-1]
	        redo = self._do_action(undo)
	        self.redos.append(redo)
	        del(self.undos[-1])
	
	        self.insert_event = self.textview.get_buffer().connect("insert-text",self._on_insert)
	        self.delete_event = self.textview.get_buffer().connect("delete-range",self._on_delete)
        
	def _do_action(self, action):
	        if action["action"] == "delete":
			start_iter = self.textview.get_buffer().get_iter_at_offset(action["offset"])
			end_iter =  self.textview.get_buffer().get_iter_at_offset(action["offset"] + len(action["text"]))
			self.textview.get_buffer().delete(start_iter, end_iter)
			action["action"] = "insert"
		
		elif action["action"] == "insert":
			start_iter = self.textview.get_buffer().get_iter_at_offset(action["offset"])
			self.textview.get_buffer().insert(start_iter, action["text"])
			action["action"] = "delete"

		return action
	
	def redo(self,widget):
		if len(self.redos) == 0:
			return
			
		self.textview.get_buffer().disconnect(self.delete_event)
		self.textview.get_buffer().disconnect(self.insert_event)
		
		redo = self.redos[-1]
		undo = self._do_action(redo)
		self.undos.append(undo)
		del(self.redos[-1])

		self.insert_event = self.textview.get_buffer().connect("insert-text",self._on_insert)
		self.delete_event = self.textview.get_buffer().connect("delete-range",self._on_delete)

	def _on_text_changed(self, buff):
		self.textview.get_buffer().disconnect(self.change_event)
		self.change_event = self.textview.get_buffer().connect("changed",self._on_text_changed)

	def _on_insert(self, text_buffer, iter, text, length, data=None):	
                print "inserting\n"
		cmd = {"action":"delete","offset":iter.get_offset(),"text":text}

		self._add_undo(cmd)
		self.redos = []
		if text == "\n": 
			cur_line = iter.get_line()
			prev_line_iter = self.textview.get_buffer().get_iter_at_line(cur_line)
			pl_offset = prev_line_iter.get_offset()
			pl_text = self.textview.get_buffer().get_text(prev_line_iter, iter, False)
			if pl_text.strip().find("*") == 0:
				ws = ""
				if not pl_text.startswith("*"):
					ws = (pl_text.split("*")[0])

	def _on_delete(self, text_buffer, start_iter, end_iter, data=None):
                print "deleting\n"
		text = self.textview.get_buffer().get_text(start_iter,end_iter, False)        
		cmd = {"action":"insert","offset":start_iter.get_offset(),"text":text}
		self._add_undo(cmd)

	def _add_undo(self, cmd):
		#delete the oldest undo if undo maximum is in effect
                print "adding to undo list\n"
		if self.undo_max is not None and len(self.undos) >= self.undo_max:
			del(self.undos[0])
		self.undos.append(cmd)		

	
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
	
def main():
	gtk.main()
	return 0

if __name__=="__main__":
	window()
	main()
