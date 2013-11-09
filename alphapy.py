#!/usr/local/bin/python

import pygtk
pygtk.require('2.0')
import gtk,vte
#import wx
from Compiler import compiler 

class window():
		
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
		
	def delete_event(self,widget=None,event=None,data=None):
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
	
	def buttn(self,icon,func,tip,expand, fill, padding,text=""):
		"creates buttons"
		hbox=gtk.HBox(False,0)
		image = gtk.Image()
   	        image.set_from_file(icon)
   	        image.show()
   	        hbox.add(image)
   	        lbl=gtk.Label(text)
   	        lbl.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
   	        lbl.modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FFFFFF'))
   	        lbl.modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse('#FFFFFF'))
   	        lbl.show()
   	        hbox.add(lbl)
		button = gtk.Button()
		map = button.get_colormap() 
		color = map.alloc_color("#4D4D4D")

		#copy the current style and replace the background
		style = button.get_style().copy()
		style.bg[gtk.STATE_NORMAL] = color
		style.bg[gtk.STATE_ACTIVE] = color
		style.bg[gtk.STATE_PRELIGHT] = color
		button.props.relief = gtk.RELIEF_NONE

		#set the button's style to the one you created
		button.set_style(style)
		self.tooltips.set_tip(button, tip)
		button.add(hbox)
		hbox.show()
		button.connect("clicked",func)
		self.hbox.pack_start(button, expand, fill, padding)
    		button.show()
		
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
		self.window.set_size_request(1000,700)
		self.window.set_title(self.title)
		self.window.connect("delete_event",self.delete_event)
		self.window.set_border_width(0)
		self.file=''
		#~ open_1=wx.NewId()
		#~ save_1=wx.NewId()
		#~ undo_1=wx.NewId()
		#~ redo_1=wx.NewId()
		#~ find_1=wx.NewId()
		#~ self.Bind(wx.EVT_MENU,self.onopen,id=open_1)
		#~ self.Bind(wx.EVT_MENU,self.onsave,id=save_1)
		#~ self.Bind(wx.EVT_MENU,self.undo,id=undo_1)
		#~ self.Bind(wx.EVT_MENU,self.redo,id=redo_1)
		#~ self.Bind(wx.EVT_MENU,self.search_dialog,id=find_1)
		#~ self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('O'), open_1),
		#~ (wx.ACCEL_CTRL, ord('S'), save_1),
		#~ (wx.ACCEL_CTRL, ord('F'), find_1),
		#~ (wx.ACCEL_CTRL, ord('Z'), undo_1),
		#~ (wx.ACCEL_CTRL, ord('Y'), redo_1)])                                          
		#~ self.SetAcceleratorTable(self.accel_tbl)
		self.hbox = gtk.HBox(False, 0)
		expand=False
		fill=False
		padding=2
		self.file=""
		self.tooltips = gtk.Tooltips()
		
		file_menu = gtk.Menu() 
		# Create the menu items
		
		new_item = gtk.MenuItem("New\t\t\tCTRL+N")
		open_item = gtk.MenuItem("Open\t\t\tCTRL+O")
		save_item = gtk.MenuItem("Save\t\t\tCTRL+S")
		saveas_item = gtk.MenuItem("Save as..\t\tCTRL+SHIFT+S")
		quit_item = gtk.MenuItem("Quit\t\t\tCTRL+Q")
		# Add them to the menu
		file_menu.append(new_item)
		file_menu.append(open_item)
		file_menu.append(saveas_item)
		file_menu.append(save_item)
		file_menu.append(quit_item)
		# Attach the callback functions to the activate signal
		new_item.connect_object("activate", self.new, "file.new")
		open_item.connect_object("activate", self.onopen, "file.open")
		save_item.connect_object("activate", self.onsave, "file.save")
		saveas_item.connect_object("activate", self.saveas, "file.saveas")
		quit_item.connect_object ("activate", self.delete_event, "file.quit")
		# We do need to show menu items
		new_item.show()
		open_item.show()
		save_item.show()
		saveas_item.show()
		quit_item.show()
		file_menu.show()
		
		edit_menu=gtk.Menu()
		cut_item = gtk.MenuItem("Cut\t\t\tCTRL+X")
		copy_item = gtk.MenuItem("Copy\t\t\tCTRL+C")
		paste_item = gtk.MenuItem("Paste\t\t\tCTRL+V")
		undo_item = gtk.MenuItem("Undo\t\t\tCTRL+Z")
		redo_item = gtk.MenuItem("Redo\t\t\tCTRL+Y")
		delete_item = gtk.MenuItem("Delete\t\t\tDEL")
		find_item = gtk.MenuItem("Find\t\t\tCTRL+F")
		
		cut_item.connect_object("activate", self.cut, "edit.cut")
		copy_item.connect_object("activate", self.copy, "edit.copy")
		paste_item.connect_object("activate", self.paste, "edit.paste")
		delete_item.connect_object("activate", self.cut, "edit.delete")
		undo_item.connect_object("activate", self.undo, "edit.undo")
		redo_item.connect_object("activate", self.redo, "edit.redo")
		find_item.connect_object("activate", self.search_dialog, "edit.find")
		
		edit_menu.append(cut_item)
		edit_menu.append(copy_item)
		edit_menu.append(paste_item)
		edit_menu.append(undo_item)
		edit_menu.append(redo_item)
		edit_menu.append(find_item)
		edit_menu.append(delete_item)
		
		cut_item.show()
		copy_item.show()
		paste_item.show()
		undo_item.show()
		redo_item.show()
		delete_item.show()
		find_item.show()
		edit_menu.show()
		
		
		menu_bar = gtk.MenuBar()
		file_item = gtk.MenuItem("File")
		edit_item = gtk.MenuItem("Edit")
		file_item.show()
		edit_item.show()
		file_item.set_submenu(file_menu)
		edit_item.set_submenu(edit_menu)
		menu_bar.append(file_item)
		menu_bar.append(edit_item)
		file_item.set_right_justified(True)
		edit_item.set_right_justified(True)
		
		menu_bar.show()
		
		self.buttn("icons/new.png",self.new,"New file",expand, fill, padding)
		self.buttn("icons/open.png",self.onopen,"Open file",expand, fill, padding," Open")
		self.buttn("icons/save.png",self.onsave,"Save file",expand, fill, padding," Save")
		self.buttn("icons/save as.png",self.saveas,"Save as..",expand, fill, padding)
		self.buttn("icons/undo.png",self.undo,"Undo",expand, fill, padding," Undo")
		self.buttn("icons/redo.png",self.redo,"Redo",expand, fill, padding,'Redo')
		self.buttn("icons/compile.png",self.compiler,"Compile",expand, fill, padding," Compile")
		self.buttn("icons/compile-run.png",self.executor,"Compile and Run",expand, fill, padding)
		self.buttn("icons/cut.png",self.cut,"Cut",expand, fill, padding)
		self.buttn("icons/copy.png",self.copy,"Copy",expand, fill, padding)
		self.buttn("icons/paste.png",self.paste,"Paste",expand, fill, padding)
    		self.buttn("icons/find.png",self.search_dialog,"Find",expand, fill, padding)
    		self.buttn("icons/quit.png",self.delete_event,"Quit",expand, fill, padding)  		
				
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
		
        	vbox.pack_start(menu_bar, False, False, 0)
        	eb = gtk.EventBox()     
		eb.add(self.hbox)
		eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#4D4D4D"))
		vbox.pack_start(eb, False, False, 0)
        	vbox1.pack_start(sw)
        	vbox1.set_border_width(2)
        	vbox.pack_start(vbox1, True, True, 0)
        	
        	
		misc=gtk.Notebook()
		misc.set_tab_pos(gtk.POS_LEFT);
		term  = vte.Terminal();
		pid   = term.fork_command('bash');
		term.set_emulation('xterm')
		term.set_size_request(800,150)
		term.show()
		comp = gtk.TextView()
		comp.set_editable(False)
		self.comp_buff = comp.get_buffer()
		comp.show()
		vtb=gtk.VBox(False,0)
		vtb.pack_start(term, False, False, 0)
		vtb2 = gtk.VBox(False,0)
		vtb2.add(comp)
		vtb2.show()
		
		scrbl=gtk.TextView()
		scrbl_bf=scrbl.get_buffer()
		scrbl_bf.set_text("This space can be used as a scribble/notes area.")
		vtb3=gtk.VBox(False,0)
		vtb3.add(scrbl)
		scrbl.show()
		vtb3.show()		
		ter_lbl=gtk.Label("Terminal")
		comp_lbl = gtk.Label('Compiler')
		scrbl_lbl=gtk.Label("Scribble")
		misc.append_page(vtb,ter_lbl)	
		misc.append_page(vtb2, comp_lbl)
		misc.append_page(vtb3, scrbl_lbl)
		misc.show()
		self.nbook = misc
		self.comp = vtb2
		
		vbox.pack_start(misc, False, False, 4)
		vtb.show()
        	
        	self.status_bar = gtk.Statusbar()      
        	self.textbuffer.connect("notify::cursor-position",self.changestbr);
   	        vbox.pack_start(self.status_bar, False, False, 0)
   	        self.status_bar.show()
   	        self.context_id = self.status_bar.get_context_id("Statusbar example")
   	        self.changestbr(self.window)
		self.window.add(vbox)
		self.hbox.show()
		eb.show()
		vbox1.show()
		vbox.show()
		misc.set_current_page(0)
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
	
	def compiler(self,widget):
		if self.file!='':
			compiler.compile_file(self.file)
			with open(compiler.log_file,'rb') as f:
				l = f.readlines()
				msg = ''.join(l)
				self.comp_buff.set_text(msg)
			self.nbook.set_current_page(self.nbook.page_num(self.comp))
				
	def executor(self, widget):
		if self.file!='':
			compiler.execute(self.file)
			with open(compiler.log_file,'rb') as f:
				l = f.readlines()
				msg = ''.join(l)
				self.comp_buff.set_text(msg)
			self.nbook.set_current_page(self.nbook.page_num(self.comp))
	
	
	def new(self,widget):
		"To open a new file and save the current file"
		if self.change:
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO,"Save before openig new file ?")
			dialog.set_title("WARNING ..")
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				self.onsave(self.window)
		self.textbuffer.set_text("")
		self.file=""
		self.change=0
		self.title="AlphaPy Text Editor"
	   	self.window.set_title(self.title)
		
		
	def onopen(self,widget):
		"To open a file and set the current file"
		if self.change:
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO,"Save before opening new file ?")
			dialog.set_title("WARNING ..")
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				self.onsave(self.window)
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
