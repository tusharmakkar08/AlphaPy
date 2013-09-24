import pygtk
pygtk.require('2.0')
import gtk

class window:
	def delete_event(self,widget,event,data=None):
		gtk.main_quit()
		return False
	def __init__(self):
		self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(True)
		self.window.set_title("AlphaPy Text Editor")
		self.window.connect("delete_event",self.delete_event)
		self.window.set_border_width(1)
		self.window.set_size_request(500,400)
		hbox = gtk.HBox(False, 0)
		expand=False
		fill=False
		padding=0
		
		button = gtk.Button("Open")
		button.connect("clicked",self.onopen)
		hbox.pack_start(button, expand, fill, padding)
    		button.show()
		
		button = gtk.Button("Save")
		button.connect("clicked",self.onsave)
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()
    		
		button = gtk.Button("Cut")
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()
		
		button = gtk.Button("Copy")
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()
    		
    		button = gtk.Button("Paste")
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()  
    		
    		button = gtk.Button("Find")
    		hbox.pack_start(button, expand, fill, padding)
    		button.show()    		
		
		self.button=gtk.Button("Quit")
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
		
		vbox=gtk.VBox(False,0)
		vbox1=gtk.VBox(False,10)
		vbox.pack_start(hbox, False, False, 0)
        	vbox1.pack_start(sw)
        	vbox1.set_border_width(2)
        	vbox.pack_start(vbox1, True, True, 0)
		self.window.add(vbox)
		hbox.show()
		vbox1.show()
		vbox.show()
		self.window.show()
	def onsave(self,widget):
		dialog = gtk.FileChooserDialog("Save..",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		filter = gtk.FileFilter()
		filter.set_name("All files")
   		filter.add_pattern("*")
 		dialog.add_filter(filter)
 		response = dialog.run()
   		if response == gtk.RESPONSE_OK:
   			fl=dialog.get_filename()
   			out=open(fl,"w")
   			start, end = self.textbuffer.get_bounds()
   			text = self.textbuffer.get_text(start, end, include_hidden_chars=True)
   			out.write(text)
   			print "Save Succesful"
   	   	elif response == gtk.RESPONSE_CANCEL:
   		       print 'Closed, no files selected'
   		dialog.destroy()
		#print "saved"
	def onopen(self,widget):
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
		    fl= dialog.get_filename()
		    self.textbuffer.set_text(open(fl,"r+").read())
		elif response == gtk.RESPONSE_CANCEL:
		    print 'Closed, no files selected'
		dialog.destroy()
	
def main():
	gtk.main()
	return 0

if __name__=="__main__":
	window()
	main()
