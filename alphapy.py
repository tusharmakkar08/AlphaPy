#!/usr/local/bin/python

import pygtk
pygtk.require('2.0')
import gtk,vte
from Compiler import compiler 
from Syntax import syntaxhighlighter
from Spelling import spell_check
import zlib
from Speech import speech

class window():
		
	def search_dialog(self,widget,data=None):
		pg=self.notebook.get_current_page()
		dialog = gtk.Dialog("Find", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
		
		dialog.set_size_request(300,100)
		
		hbox1 = gtk.HBox(False,0)
		hbox2 = gtk.HBox(False,0)
		#~ hbox3 = gtk.HBox(False,0)
		
		self.found = {pg:False}
		self.found1 = {pg:False}
		self.next1 = {pg:False}
		self.prev1 = {pg:False}
		self.count = {pg:0}
		
		label = gtk.Label("Enter String")
		hbox1.pack_start(label)
		label.show()
		
		self.entry= gtk.Entry()
		hbox1.pack_start(self.entry)
		self.entry.show()
		
		button1 = gtk.Button('Previous')
		button1.connect('clicked', self.find_prev)
		button1.show()
		hbox2.pack_start(button1)
		
		button = gtk.Button('Next')
		button.connect('clicked', self.find_next)
		button.show()
		hbox2.pack_start(button)
		
		hbox1.show()
		hbox2.show()
		dialog.vbox.pack_start(hbox1, gtk.TRUE, gtk.TRUE, 0)
		dialog.vbox.pack_start(hbox2, gtk.TRUE, gtk.TRUE, 0)
		
		response = dialog.run()
		dialog.destroy()	
	
	def wrap_dialog(self,widget,data=None):
		pg=self.notebook.get_current_page()
		if self.count[pg]>1:
			self.count[pg] = 0
			self.not_found_dialog(widget)
			return
			
		dialog = gtk.Dialog("Find", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_OK,gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
		dialog.set_size_request(400,100)
		
		hbox1 = gtk.HBox(False,0)
		label = gtk.Label("End of the document reached. Wrap around search?")
		label.show()
		hbox1.pack_start(label)
		hbox1.show()
		
		dialog.vbox.pack_start(hbox1, gtk.TRUE, gtk.TRUE, 0)
		response = dialog.run()
		if response==gtk.RESPONSE_OK:
			self.found[pg] = []
			self.found1[pg] = []
			self.found[pg].append('')
			self.found[pg].append(self.textbuffer[pg].get_start_iter())
			self.found1[pg].append(self.textbuffer[pg].get_end_iter())
			if self.next1[pg]:
				self.find_next(widget)
			elif self.prev1:
				self.find_prev(widget)
			self.next1[pg] = False
			self.prev1[pg] = False
		dialog.destroy()	

	def not_found_dialog(self,widget,data=None):
		dialog = gtk.Dialog("Find", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_OK))	
		dialog.set_size_request(400,100)
		
		hbox1 = gtk.HBox(False,0)
		label = gtk.Label("Input String not Found")
		label.show()
		hbox1.pack_start(label)
		hbox1.show()
		
		dialog.vbox.pack_start(hbox1, gtk.TRUE, gtk.TRUE, 0)
		response = dialog.run()
		dialog.destroy()	

	def replace_dialog(self,widget,data=None):
		pg=self.notebook.get_current_page()
		dialog = gtk.Dialog("Find", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_OK))
		dialog.set_size_request(350,200)
		
		hbox1 = gtk.HBox(False,0)
		hbox2 = gtk.HBox(False,0)
		hbox3 = gtk.HBox(False,0)
		hbox4 = gtk.HBox(False,0)
		hbox5 = gtk.HBox(False,0)
		hbox6 = gtk.HBox(False,0)
		hbox7 = gtk.HBox(False,0)
		hbox8 = gtk.HBox(False,0)
		hbox9 = gtk.HBox(False,0)
		hbox10 = gtk.HBox(False,0)
		
		self.found = {pg:False}
		self.found1 = {pg:False}
		self.next1 = {pg:False}
		self.prev1 = {pg:False}
		self.count = {pg:0}
		
		label = gtk.Label("Enter String")
		hbox1.pack_start(label)
		label.show()
		hbox1.show()
		
		self.entry= gtk.Entry()
		hbox2.pack_start(self.entry)
		self.entry.show()
		hbox2.show()
		
		hbox3.pack_start(hbox1)
		hbox3.pack_start(hbox2)
		hbox3.show()
		
		label = gtk.Label("Enter Replacing String")
		hbox4.pack_start(label)
		label.show()
		hbox4.show()
		
		self.entry1= gtk.Entry()
		hbox5.pack_start(self.entry1)
		self.entry1.show()
		hbox5.show()
		
		hbox6.pack_start(hbox4)
		hbox6.pack_start(hbox5)
		hbox6.show()
		
		button1 = gtk.Button('Next')
		button1.connect('clicked', self.find_next,1)
		button1.show()
		hbox7.pack_start(button1)
		hbox7.show()
		
		button2 = gtk.Button('Previous')
		button2.connect('clicked', self.find_prev)
		button2.show()
		hbox8.pack_start(button2)
		hbox8.show()
		
		button3 = gtk.Button('Replace')
		button3.connect('clicked', self.replace_string)
		button3.show()
		hbox9.pack_start(button3)
		hbox9.show()
		
		hbox10.pack_start(hbox7)
		hbox10.pack_start(hbox8)
		hbox10.pack_start(hbox9)
		hbox10.show()
		
		dialog.vbox.pack_start(hbox3, gtk.TRUE, gtk.TRUE, 0)
		dialog.vbox.pack_start(hbox6, gtk.TRUE, gtk.TRUE, 0)
		dialog.vbox.pack_start(hbox10, gtk.TRUE, gtk.TRUE,0)
		
		response = dialog.run()
		dialog.destroy()	
		
	def delete_event(self,widget=None,event=None,data=None):
		"Quit window"
		f=0
		for i in self.change:
			if i:
				f=1
				break 
		if f:
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO,"All unsaved data will be lost,are you sure ?")
			dialog.set_title("WARNING ..")
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				gtk.main_quit()
			else: return True
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

		button.set_style(style)
		self.tooltips.set_tip(button, tip)
		button.add(hbox)
		hbox.show()
		button.connect("clicked",func)
		self.hbox.pack_start(button, expand, fill, padding)
    		button.show()
    	
    	def create_tab(self, title,d=0):
		#hbox will be used to store a label and button, as notebook tab title
		hbox = gtk.HBox(False, 0)
		label = gtk.Label(title.split('/')[-1])
		hbox.pack_start(label)

		#get a stock close button image
		close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
		image_w, image_h = gtk.icon_size_lookup(gtk.ICON_SIZE_MENU)
		
		#make the close button
		btn = gtk.Button()
		btn.set_relief(gtk.RELIEF_NONE)
		btn.set_focus_on_click(False)
		btn.add(close_image)
		hbox.pack_start(btn, False, False)
		
		#this reduces the size of the button
		style = gtk.RcStyle()
		style.xthickness = 0
		style.ythickness = 0
		btn.modify_style(style)

		hbox.show_all()

		#tab contents
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.textview .append( gtk.TextView())
		self.textview[-1].set_editable(True)
		self.textbuffer .append( self.textview[-1].get_buffer())
		self.insert_event = self.textbuffer[-1].connect("insert-text",self._on_insert)
	        self.delete_event = self.textbuffer[-1].connect("delete-range",self._on_delete)
	        self.change_event = self.textbuffer[-1].connect("changed",self._on_text_changed)
	        if title!='Untitled':
	        	if d:self.textbuffer[-1].set_text(zlib.decompress(open(title,"rb+").read()))
	        	else:self.textbuffer[-1].set_text()

		sw.add(self.textview[-1])
		self.textview[-1].show()
		sw.show()
		self.clipboard=gtk.Clipboard()		
		self.textbuffer[-1].connect("changed",self.changetitle);
		self.widget.append(gtk.VBox(False,10))
		self.widget[-1].pack_start(sw)
        	self.widget[-1].set_border_width(2)
        	self.widget[-1].show()
        	self.file.append(title)
        	self.change+=[0]
        	self.textbuffer[-1].connect("notify::cursor-position",self.changestbr);
		
		#add the tab
		self.notebook.insert_page(self.widget[-1], hbox)
		
		#connect the close button
		btn.connect('clicked', self.on_closetab_button_clicked, self.widget[-1])

	def on_closetab_button_clicked(self, sender, widget):
		"Close a tab"
		pagenum = self.notebook.page_num(widget)
		if self.change[pagenum]==1:
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO,"Do you want to save before close ?")
			dialog.set_title("WARNING ..")
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				self.onsave(self.window)
		
		#and close it
		self.notebook.remove_page(pagenum)
		self.textbuffer.pop(pagenum)
		self.file.pop(pagenum)
		self.change.pop(pagenum)
		self.textview.pop(pagenum)
		self.widget.pop(pagenum)
		
	def __init__(self):
		"Initiate the window,button,etc .."
		self.undo_max = 100	
		self._highlight_strings = []
		self.undos = []
		self.redos = []
		self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(True)
		self.title="AlphaPy Text Editor"
		self.change=[]
		self.window.set_size_request(1000,700)
		self.window.set_title(self.title)
		self.window.connect("delete_event",self.delete_event)
		self.window.set_border_width(0)
		self.textbuffer=[]
		self.textview=[]
		self.file=[]
		self.widget=[]
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
		
		html_menu=gtk.Menu()
		rtf_menu=gtk.Menu()
		export_menu=gtk.Menu()
		
		mono_h = gtk.MenuItem("Monokai")
		manni_h = gtk.MenuItem("Manni")
		rrt_h = gtk.MenuItem("Rrt")
		perldoc_h = gtk.MenuItem("Perldoc")
		borl_h = gtk.MenuItem("Borland")
		clor_h = gtk.MenuItem("Colorful")
		def_h = gtk.MenuItem("Default")
		murphy_h = gtk.MenuItem("Murphy")
		vs_h = gtk.MenuItem("VS")
		trk_h = gtk.MenuItem("Trac")
		tng_h = gtk.MenuItem("Tango")
		frty_h = gtk.MenuItem("Fruity")
		atm_h = gtk.MenuItem("Autumn")
		bw_h = gtk.MenuItem("BW")
		emcs_h = gtk.MenuItem("Emacs")
		vim_h = gtk.MenuItem("Vim")
		psty_h = gtk.MenuItem("Pasty")
		frd_h = gtk.MenuItem("Friendly")
		nat_h = gtk.MenuItem("Native")
		mono_r = gtk.MenuItem("Monokai")
		manni_r = gtk.MenuItem("Manni")
		rrt_r = gtk.MenuItem("Rrt")
		perldoc_r = gtk.MenuItem("Perldoc")
		borl_r = gtk.MenuItem("Borland")
		clor_r = gtk.MenuItem("Colorful")
		def_r = gtk.MenuItem("Default")
		murphy_r = gtk.MenuItem("Murphy")
		vs_r = gtk.MenuItem("VS")
		trk_r = gtk.MenuItem("Trac")
		tng_r = gtk.MenuItem("Tango")
		frty_r = gtk.MenuItem("Fruity")
		atm_r = gtk.MenuItem("Autumn")
		bw_r = gtk.MenuItem("BW")
		emcs_r = gtk.MenuItem("Emacs")
		vim_r = gtk.MenuItem("Vim")
		psty_r = gtk.MenuItem("Pasty")
		frd_r = gtk.MenuItem("Friendly")
		nat_r = gtk.MenuItem("Native")
		
		mono_h.connect_object("activate", self.mono_html, "html.mono")
		manni_h.connect_object("activate", self.manni_html, "html.manni")
		rrt_h.connect_object("activate", self.rrt_html, "html.rrt")
		perldoc_h.connect_object("activate", self.perl_html, "html.perldoc")
		borl_h.connect_object("activate", self.borl_html, "html.borl")
		clor_h.connect_object("activate", self.col_html, "html.clor")
		def_h.connect_object("activate", self.def_html, "html.def")
		murphy_h.connect_object("activate", self.mur_html, "html.murphy")
		vs_h.connect_object("activate", self.vs_html, "html.vs")
		trk_h.connect_object("activate", self.tr_html, "html.trk")
		tng_h.connect_object("activate", self.tan_html, "html.tng")
		frty_h.connect_object("activate", self.fr_html, "html.frty")
		atm_h.connect_object("activate", self.aut_html, "html.atm")
		bw_h.connect_object("activate", self.bw_html, "html.bw")
		emcs_h.connect_object("activate", self.emac_html, "html.emcs")
		vim_h.connect_object("activate", self.vi_html, "html.vim")
		psty_h.connect_object("activate", self.pas_html, "html.psty")
		frd_h.connect_object("activate", self.fri_html, "html.frd")
		nat_h.connect_object("activate", self.nat_html, "html.nat")
		
		mono_r.connect_object("activate", self.mono_rtf, "rtf.mono")
		manni_r.connect_object("activate", self.manni_rtf, "rtf.manni")
		rrt_r.connect_object("activate", self.rrt_rtf, "rtf.rrt")
		perldoc_r.connect_object("activate", self.perl_rtf, "rtf.perldoc")
		borl_r.connect_object("activate", self.borl_rtf, "rtf.borl")
		clor_r.connect_object("activate", self.col_rtf, "rtf.clor")
		def_r.connect_object("activate", self.def_rtf, "rtf.def")
		murphy_r.connect_object("activate", self.mur_rtf, "rtf.murphy")
		vs_r.connect_object("activate", self.vs_rtf, "rtf.vs")
		trk_r.connect_object("activate", self.tr_rtf, "rtf.trk")
		tng_r.connect_object("activate", self.tan_rtf, "rtf.tng")
		frty_r.connect_object("activate", self.fr_rtf, "rtf.frty")
		atm_r.connect_object("activate", self.aut_rtf, "rtf.atm")
		bw_r.connect_object("activate", self.bw_rtf, "rtf.bw")
		emcs_r.connect_object("activate", self.emac_rtf, "rtf.emcs")
		vim_r.connect_object("activate", self.vi_rtf, "rtf.vim")
		psty_r.connect_object("activate", self.pas_rtf, "rtf.psty")
		frd_r.connect_object("activate", self.fri_rtf, "rtf.frd")
		nat_r.connect_object("activate", self.nat_rtf, "rtf.nat")
		
		mono_h.show()
		manni_h.show()
		rrt_h.show()
		perldoc_h.show()
		borl_h.show()
		clor_h.show()
		def_h.show()
		murphy_h.show()
		vs_h.show()
		trk_h.show()
		tng_h.show()
		frty_h.show()
		atm_h.show()
		bw_h.show()
		emcs_h.show()
		vim_h.show()
		psty_h.show()
		frd_h.show()
		nat_h.show()
		
		mono_r.show()
		manni_r.show()
		rrt_r.show()
		perldoc_r.show()
		borl_r.show()
		clor_r.show()
		def_r.show()
		murphy_r.show()
		vs_r.show()
		trk_r.show()
		tng_r.show()
		frty_r.show()
		atm_r.show()
		bw_r.show()
		emcs_r.show()
		vim_r.show()
		psty_r.show()
		frd_r.show()
		nat_r.show()
		
		html_menu.append(mono_h)
		html_menu.append(manni_h)
		html_menu.append(rrt_h)
		html_menu.append(perldoc_h)
		html_menu.append(borl_h)
		html_menu.append(clor_h)
		html_menu.append(def_h)
		html_menu.append(murphy_h)
		html_menu.append(vs_h)
		html_menu.append(trk_h)
		html_menu.append(tng_h)
		html_menu.append(frty_h)
		html_menu.append(atm_h)
		html_menu.append(bw_h)
		html_menu.append(emcs_h)
		html_menu.append(vim_h)
		html_menu.append(psty_h)
		html_menu.append(frd_h)
		html_menu.append(nat_h)
		rtf_menu.append(mono_r)
		rtf_menu.append(manni_r)
		rtf_menu.append(rrt_r)
		rtf_menu.append(perldoc_r)
		rtf_menu.append(borl_r)
		rtf_menu.append(clor_r)
		rtf_menu.append(def_r)
		rtf_menu.append(murphy_r)
		rtf_menu.append(vs_r)
		rtf_menu.append(trk_r)
		rtf_menu.append(tng_r)
		rtf_menu.append(frty_r)
		rtf_menu.append(atm_r)
		rtf_menu.append(bw_r)
		rtf_menu.append(emcs_r)
		rtf_menu.append(vim_r)
		rtf_menu.append(psty_r)
		rtf_menu.append(frd_r)
		rtf_menu.append(nat_r)
		
		html_item=gtk.MenuItem("Export as HTML")
		rtf_item=gtk.MenuItem("Export as RTF")
		html_item.set_submenu(html_menu)
		rtf_item.set_submenu(rtf_menu)
		html_item.show()
		rtf_item.show()
		export_menu.append(html_item)
		export_menu.append(rtf_item)
		html_item.set_right_justified(True)
		rtf_item.set_right_justified(True)
		export_item = gtk.MenuItem("Export")
		export_item.show()
		export_item.set_submenu(export_menu)
		
		
		menu_bar = gtk.MenuBar()
		file_item = gtk.MenuItem("File")
		edit_item = gtk.MenuItem("Edit")
		file_item.show()
		edit_item.show()
		file_item.set_submenu(file_menu)
		edit_item.set_submenu(edit_menu)
		menu_bar.append(file_item)
		menu_bar.append(edit_item)
		menu_bar.append(export_item)
		file_item.set_right_justified(True)
		edit_item.set_right_justified(True)
		
		menu_bar.show()
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
		self.buttn("icons/find_replace.png",self.replace_dialog,"Find & Replace",expand, fill, padding)
		self.buttn("icons/compress.png",self.compr,"Compress",expand, fill, padding,"Compress")
		self.buttn("icons/decompress.png",self.decompr,"Decompress",expand, fill, padding)
		self.buttn("icons/speech.png",self.spee,"Speech",expand, fill, padding,"Speak")  
		self.buttn("icons/quit.png",self.delete_event,"Quit",expand, fill, padding)  		
				
			
		
		
		vbox=gtk.VBox(False,0)
        	vbox.pack_start(menu_bar, False, False, 0)
        	eb = gtk.EventBox()     
		eb.add(self.hbox)
		eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#4D4D4D"))
		vbox.pack_start(eb, False, False, 0)
        	
        	
        	self.notebook=gtk.Notebook()
        	self.notebook.set_tab_pos(gtk.POS_TOP);
        	self.create_tab('Untitled')
        	self.notebook.show()
        	
        	
        	vbox.pack_start(self.notebook, True, True, 0)
        	
		misc=gtk.Notebook()
		misc.set_tab_pos(gtk.POS_LEFT);
		term  = vte.Terminal();
		pid   = term.fork_command('bash');
		term.set_emulation('xterm')
		term.set_size_request(800,150)
		term.show()
		comp = gtk.TextView()
		comp.set_editable(False)
		comp.set_cursor_visible(False)
		self.comp_buff = comp.get_buffer()
		comp.show()
		vtb=gtk.VBox(False,0)
		vtb.pack_start(term, False, False, 0)
		vtb2 = gtk.VBox(False,0)
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.add(comp)
		sw.show()
		vtb2.add(sw)
		vtb2.show()
		
		scrbl=gtk.TextView()
		scrbl_bf=scrbl.get_buffer()
		scrbl_bf.set_text("This space can be used as a scribble/notes area.")
		vtb3=gtk.VBox(False,0)
		vtb3.add(scrbl)
		scrbl.show()
		vtb3.show()
		self.msg=gtk.TextView()
		self.msg_bf=self.msg.get_buffer()
		self.msg.set_editable(False)
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.add(self.msg)
		sw.show()
		vtb4=gtk.VBox(False,0)
		vtb4.add(sw)
		self.msg.show()
		vtb4.show()		
		ter_lbl=gtk.Label("Terminal")
		comp_lbl = gtk.Label('Compiler')
		scrbl_lbl=gtk.Label("Scribble")
		msg_lbl=gtk.Label("Message")
		misc.append_page(vtb,ter_lbl)	
		misc.append_page(vtb2, comp_lbl)
		misc.append_page(vtb3, scrbl_lbl)
		misc.append_page(vtb4, msg_lbl)
		misc.show()
		self.nbook = misc
		self.comp = vtb2
		
		vbox.pack_start(misc, False, False, 4)
		vtb.show()
        	
        	self.status_bar = gtk.Statusbar()      
   	        vbox.pack_start(self.status_bar, False, False, 0)
   	        self.status_bar.show()
   	        self.context_id = self.status_bar.get_context_id("Statusbar example")
   	        self.changestbr(self.window)
		self.window.add(vbox)
		self.hbox.show()
		eb.show()
		vbox.show()
		misc.set_current_page(0)
		self.window.show()
		
	def compr(self,widget):
		"Compress text in current tab"
		pg=self.notebook.get_current_page()
		dialog = gtk.FileChooserDialog("Choose file name",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		filter = gtk.FileFilter()
		filter.set_name("All files")
	   	filter.add_pattern("*")
	 	dialog.add_filter(filter)
	 	response = dialog.run()
	   	if response == gtk.RESPONSE_OK:
	   		file=dialog.get_filename()
	   		out=open(file,"wb+")
	   		out.write((zlib.compress(self.textbuffer[pg].get_text(self.textbuffer[pg].get_start_iter(),self.textbuffer[pg].get_end_iter()))))
			out.close()
	   		print "Compress Succesful"
	   	elif response == gtk.RESPONSE_CANCEL:
	   	       print 'Closed, no files selected'
	   	dialog.destroy()
		
		
	def decompr(self,widget):
		"Compress text in current tab"
		pg=self.notebook.get_current_page()
		dialog = gtk.FileChooserDialog("Open file to decompress",
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
		    file= dialog.get_filename()
		    if file in self.file:return
		    self.create_tab(file ,1)
		elif response == gtk.RESPONSE_CANCEL:
		    print 'Closed, no files selected'
		dialog.destroy()	
	
	def cut(self,widget):
		pg=self.notebook.get_current_page()
		self.textbuffer[pg].cut_clipboard(self.clipboard, True)
	
	def copy(self,widget):
		pg=self.notebook.get_current_page()
		self.textbuffer[pg].copy_clipboard(self.clipboard)
	
	def paste(self,widget):
		pg=self.notebook.get_current_page()
		self.textbuffer[pg].paste_clipboard(self.clipboard,None, True)
	
	
	def changetitle(self,widget,title=None):
		"Change Title when file is temporary"
		pg=self.notebook.get_current_page()
		print self.file,pg,self.widget
		if self.change[pg]==0:
			hbox = gtk.HBox(False, 0)
			print title
			if title is None:
				title=self.file[pg]
			label = gtk.Label('**'+title.split('/')[-1])
			hbox.pack_start(label)

			#get a stock close button image
			close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
			image_w, image_h = gtk.icon_size_lookup(gtk.ICON_SIZE_MENU)
		
			#make the close button
			btn = gtk.Button()
			btn.set_relief(gtk.RELIEF_NONE)
			btn.set_focus_on_click(False)
			btn.add(close_image)
			hbox.pack_start(btn, False, False)
		
			#this reduces the size of the button
			style = gtk.RcStyle()
			style.xthickness = 0
			style.ythickness = 0
			btn.modify_style(style)

			hbox.show_all()
			self.notebook.set_tab_label(self.widget[pg], hbox)
			btn.connect('clicked', self.on_closetab_button_clicked, self.widget[pg])
			self.change[pg]=1
		elif not title is None:
			hbox = gtk.HBox(False, 0)
			label = gtk.Label(title.split('/')[-1])
			hbox.pack_start(label)

			#get a stock close button image
			close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
			image_w, image_h = gtk.icon_size_lookup(gtk.ICON_SIZE_MENU)
		
			#make the close button
			btn = gtk.Button()

			btn.set_relief(gtk.RELIEF_NONE)
			btn.set_focus_on_click(False)
			btn.add(close_image)
			hbox.pack_start(btn, False, False)
		
			#this reduces the size of the button
			style = gtk.RcStyle()
			style.xthickness = 0
			style.ythickness = 0
			btn.modify_style(style)

			hbox.show_all()
			self.notebook.set_tab_label(self.widget[pg], hbox)
			btn.connect('clicked', self.on_closetab_button_clicked, self.widget[pg])
			self.change[pg]=0
		
	def changestbr(self,widget,data=None):
		"Change statusbar values"
		pg=self.notebook.get_current_page()
		cl= 1+self.textbuffer[pg].get_iter_at_mark(self.textbuffer[pg].get_insert()).get_line()
		col=self.textbuffer[pg].get_iter_at_mark(self.textbuffer[pg].get_insert()).get_line_index()
		ln=self.textbuffer[pg].get_line_count()
		ch=self.textbuffer[pg].get_char_count()
		selln=0
		selch=0
		if self.textbuffer[pg].get_selection_bounds()!=():
			st,end=self.textbuffer[pg].get_selection_bounds()
			selln=end.get_line()-st.get_line()+1
			selch=end.get_offset()-st.get_offset()
		data="\t\tline : "+str(cl)+"  col : "+str(col)+"\t\tlines : "+str(ln)+" chars : "+str(ch)+"\tSel : "+str(selln)+" | "+str(selch)
		if self.file[pg]=="Untitled":
			text="New file"+data
		else:
			text=self.file[pg]+data
		self.status_bar.push(self.context_id, text)
		
		
	def undo(self,widget):
		pg=self.notebook.get_current_page()
		if len(self.undos) == 0:
			print "length is "+ str(len(self.undos))
		        return
		print "length is "+str(len(self.undos))
	        self.textview[pg].get_buffer().disconnect(self.delete_event)
	        self.textview[pg].get_buffer().disconnect(self.insert_event)

	        undo = self.undos[-1]
	        redo = self._do_action(undo)
	        self.redos.append(redo)
	        del(self.undos[-1])
	
	        self.insert_event = self.textbuffer[pg].connect("insert-text",self._on_insert)
	        self.delete_event = self.textbuffer[pg].connect("delete-range",self._on_delete)
        
	def _do_action(self, action):
		pg=self.notebook.get_current_page()
	        if action["action"] == "delete":
			start_iter = self.textbuffer[pg].get_iter_at_offset(action["offset"])
			end_iter =  self.textbuffer[pg].get_iter_at_offset(action["offset"] + len(action["text"]))
			self.textbuffer[pg].delete(start_iter, end_iter)
			action["action"] = "insert"
		
		elif action["action"] == "insert":
			start_iter = self.textbuffer[pg].get_iter_at_offset(action["offset"])
			self.textbuffer[pg].insert(start_iter, action["text"])
			action["action"] = "delete"

		return action
	
	def redo(self,widget):
		pg=self.notebook.get_current_page()
		if len(self.redos) == 0:
			return
			
		self.textbuffer[pg].disconnect(self.delete_event)
		self.textbuffer[pg].disconnect(self.insert_event)
		
		redo = self.redos[-1]
		undo = self._do_action(redo)
		self.undos.append(undo)
		del(self.redos[-1])

		self.insert_event = self.textbuffer[pg].connect("insert-text",self._on_insert)
		self.delete_event = self.textbuffer[pg].connect("delete-range",self._on_delete)

	def _on_text_changed(self, buff):
		pg=self.notebook.get_current_page()
		self.textbuffer[pg].disconnect(self.change_event)
		self.change_event = self.textbuffer[pg].connect("changed",self._on_text_changed)

	def _on_insert(self, text_buffer, iter, text, length, data=None):	
		pg=self.notebook.get_current_page()
                print "inserting\n"
		cmd = {"action":"delete","offset":iter.get_offset(),"text":text}
		start = self.textbuffer[pg].get_start_iter()
		end = self.textbuffer[pg].get_end_iter()	
		words = self.textbuffer[pg].get_text(start,end)
		print words[len(words)-1]
		if words!="" and words[len(words)-1]==" ":
			king=spell_check.get_text(words)
			self.msg_bf.insert(self.msg_bf.get_start_iter(),king)
		self._add_undo(cmd)
		self.redos = []
		if text == "\n": 
			cur_line = iter.get_line()
			prev_line_iter = self.textbuffer[pg].get_iter_at_line(cur_line)
			pl_offset = prev_line_iter.get_offset()
			pl_text = self.textbuffer[pg].get_text(prev_line_iter, iter, False)
			if pl_text.strip().find("*") == 0:
				ws = ""
				if not pl_text.startswith("*"):
					ws = (pl_text.split("*")[0])
			

	def _on_delete(self, text_buffer, start_iter, end_iter, data=None):
		pg=self.notebook.get_current_page()
                print "deleting\n"
		text = self.textbuffer[pg].get_text(start_iter,end_iter, False)        
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
		pg=self.notebook.get_current_page()
		if self.file[pg]=="Untitled":
			dialog = gtk.FileChooserDialog("Save..",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			filter = gtk.FileFilter()
			filter.set_name("All files")
	   		filter.add_pattern("*")
	 		dialog.add_filter(filter)
	 		response = dialog.run()
	   		if response == gtk.RESPONSE_OK:
	   			self.file[pg]=dialog.get_filename()
	   			out=open(self.file[pg],"w")
	   			start, end = self.textbuffer[pg].get_bounds()
	   			text = self.textbuffer[pg].get_text(start, end, include_hidden_chars=True)
	   			out.write(text)
	   			self.changetitle(None,self.file[pg])
	   			self.change[pg]=0
	   			print "Save Succesful"
	   	   	elif response == gtk.RESPONSE_CANCEL:
	   		       print 'Closed, no files selected'
	   		dialog.destroy()
	   	else:
	   		out=open(self.file[pg],"w")
	   		start, end = self.textbuffer[pg].get_bounds()
	   		text = self.textbuffer[pg].get_text(start, end, include_hidden_chars=True)
	   		out.write(text)
	   		print "Save Succesful"
   			self.changetitle(None,self.file[pg])
   			self.change[pg]=0
	   		
	
	def saveas(self,widget):
			"Save the file with a different name"
			pg=self.notebook.get_current_page()
			dialog = gtk.FileChooserDialog("Save as..",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			filter = gtk.FileFilter()
			filter.set_name("All files")
	   		filter.add_pattern("*")
	 		dialog.add_filter(filter)
	 		response = dialog.run()
	   		if response == gtk.RESPONSE_OK:
	   			self.file[pg]=dialog.get_filename()
	   			out=open(self.file[pg],"w")
	   			start, end = self.textbuffer[pg].get_bounds()
	   			text = self.textbuffer[pg].get_text(start, end, include_hidden_chars=True)
	   			out.write(text)
	   			self.changetitle(None,self.file[pg])
	   			self.change[pg]=0
	   			print "Save Succesful"
	   	   	elif response == gtk.RESPONSE_CANCEL:
	   		       print 'Closed, no files selected'
	   		dialog.destroy()
	
	def compiler(self,widget):
		pg=self.notebook.get_current_page()
		if self.file[pg]!='Untitled':
			compiler.compile_file(self.file[pg])
			with open(compiler.log_file,'rb') as f:
				l = f.readlines()
				msg = ''.join(l)
				self.comp_buff.set_text(msg)
			self.nbook.set_current_page(self.nbook.page_num(self.comp))
				
	def executor(self, widget):
		pg=self.notebook.get_current_page()
		if self.file!='Untitled':
			compiler.execute(self.file[pg])
			with open(compiler.log_file,'rb') as f:
				l = f.readlines()
				msg = ''.join(l)
				self.comp_buff.set_text(msg)
			self.nbook.set_current_page(self.nbook.page_num(self.comp))
	
	
	def new(self,widget):
		"To open a new file and save the current file"
		#if self.change:
		#	dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL |gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO,"Save before openig new file ?")
		#	dialog.set_title("WARNING ..")
		#	response = dialog.run()
		#	dialog.destroy()
		#	if response == gtk.RESPONSE_YES:
		#		self.onsave(self.window)
		
		self.create_tab('Untitled')
		
		
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
		    file= dialog.get_filename()
		    if file in self.file:return
		    self.create_tab(file)
		elif response == gtk.RESPONSE_CANCEL:
		    print 'Closed, no files selected'
		dialog.destroy()
		
	def find_next(self,widget, data=None):
		pg=self.notebook.get_current_page()
		if pg not in self.found:
			self.found1[pg] = None
			self.found1[pg] = None
		self.found1[pg] = self.found[pg]
		iput = self.entry.get_text()
		if iput=='':
			return
		start_iter = self.found[pg][1] if self.found[pg] else self.textbuffer[pg].get_iter_at_mark(self.textbuffer[pg].get_insert())
		self.found[pg] = start_iter.forward_search(iput,0, None) 
		if self.found[pg]:
			self.count[pg]=0
			self.found1[pg] = self.found[pg]
			match_start,match_end = self.found[pg]
			self.textbuffer[pg].select_range(match_start,match_end)
			self.textview[pg].scroll_to_iter(match_start,0.0)
		elif self.found[pg] == None:
			self.count[pg]+=1
			self.next1[pg] = True
			self.prev1[pg] = False
			self.wrap_dialog(widget)
			
	def find_prev(self,widget,data=None):
		pg=self.notebook.get_current_page()
		if pg not in self.found:
			self.found1[pg] = None
			self.found1[pg] = None
		self.found[pg] = self.found1[pg]
		iput = self.entry.get_text()
		if iput=='':
			return
		start_iter = self.found1[pg][0] if self.found1[pg] else self.textbuffer[pg].get_iter_at_mark(self.textbuffer[pg].get_insert())
		self.found1[pg] = start_iter.backward_search(iput,0, None) 
		if self.found1[pg]:
			self.count[pg]=0
			self.prev1[pg] = True
			self.next1[pg] = False
			self.found[pg] = self.found1[pg]
			match_start,match_end = self.found1[pg]
			self.textbuffer[pg].select_range(match_start,match_end)
			self.textview[pg].scroll_to_iter(match_start,0.0)
			
		elif self.found1[pg] == None:
			self.count[pg]+=1
			self.next1[pg] = False
			self.prev1[pg] = True
			self.wrap_dialog(widget)
	
	def replace_string(self,widget,data=None):
		pg=self.notebook.get_current_page()
		iput = self.entry1.get_text()
		search = self.entry.get_text()
		print iput
		if iput=='':
			return
		if search=='' or not self.found[pg]:
			pos = self.textbuffer[pg].get_iter_at_mark(self.textbuffer[pg].get_insert())
		else:
			self.textbuffer[pg].delete(self.found[pg][0], self.found[pg][1])
			pos = self.found[pg][0]
		self.textbuffer[pg].insert(pos, iput)
		self.found[pg] = False
		self.found1[pg] = False
		self.next1[pg] = False
		self.prev1[pg] = False
		self.count[pg] = False
					
	def mono_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,1)
		syntaxhighlighter.open_html(name)
	
	def manni_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,2)
		syntaxhighlighter.open_html(name)
	
	def rrt_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,3)
		syntaxhighlighter.open_html(name)
	
	def perl_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,4)
		syntaxhighlighter.open_html(name)
	
	def borl_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,5)
		syntaxhighlighter.open_html(name)
	
	def col_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,6)
		syntaxhighlighter.open_html(name)
	
	def def_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,7)
		syntaxhighlighter.open_html(name)
	
	def mur_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,8)
		syntaxhighlighter.open_html(name)
	
	def vs_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,9)
		syntaxhighlighter.open_html(name)
	
	def tr_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,10)
		syntaxhighlighter.open_html(name)
	
	def tan_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,11)
		syntaxhighlighter.open_html(name)
	
	def fr_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,12)
		syntaxhighlighter.open_html(name)
	
	def aut_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,13)
		syntaxhighlighter.open_html(name)
	
	def bw_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,14)
		syntaxhighlighter.open_html(name)
	
	def emac_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,15)
		syntaxhighlighter.open_html(name)
	
	def vi_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,16)
		syntaxhighlighter.open_html(name)
	
	def pas_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,17)
		syntaxhighlighter.open_html(name)
	
	def fri_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,18)
		syntaxhighlighter.open_html(name)
	
	def nat_html(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.html_out(name,19)
		syntaxhighlighter.open_html(name)
	
	def mono_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,1)
		syntaxhighlighter.open_rtf(name)
	
	def manni_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,2)
		syntaxhighlighter.open_rtf(name)
	
	def rrt_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,3)
		syntaxhighlighter.open_rtf(name)
	
	def perl_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,4)
		syntaxhighlighter.open_rtf(name)
	
	def borl_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,5)
		syntaxhighlighter.open_rtf(name)
	
	def col_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,6)
		syntaxhighlighter.rtf_html(name)
	
	def def_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,7)
		syntaxhighlighter.open_rtf(name)
	
	def mur_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,8)
		syntaxhighlighter.open_rtf(name)
	
	def vs_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,9)
		syntaxhighlighter.open_rtf(name)
	
	def tr_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,10)
		syntaxhighlighter.open_rtf(name)
	
	def tan_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,11)
		syntaxhighlighter.open_rtf(name)
	
	def fr_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,12)
		syntaxhighlighter.open_rtf(name)
	
	def aut_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,13)
		syntaxhighlighter.open_rtf(name)
	
	def bw_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,14)
		syntaxhighlighter.open_rtf(name)
	
	def emac_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,15)
		syntaxhighlighter.open_rtf(name)
	
	def vi_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,16)
		syntaxhighlighter.open_rtf(name)
	
	def pas_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,17)
		syntaxhighlighter.open_rtf(name)
	
	def fri_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,18)
		syntaxhighlighter.open_rtf(name)
	
	def nat_rtf(self,widget):
		pg=self.notebook.get_current_page()
		name=self.file[pg]
		syntaxhighlighter.rtf_out(name,19)
		syntaxhighlighter.open_rtf(name)
	
	def spee(self,widget):
		pg=self.notebook.get_current_page()
		text=self.textbuffer[pg].get_text(self.textbuffer[pg].get_start_iter(),self.textbuffer[pg].get_end_iter())
		speech.txt_to_sp(text)
	
	
def main():
	gtk.main()
	return 0

if __name__=="__main__":
	window()
	main()
