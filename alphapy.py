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
		button = gtk.Button("Save")
		expand=False
		fill=False
		padding=0
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
		textview = gtk.TextView()
		textbuffer = textview.get_buffer()
		sw.add(textview)
		textview.show()
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
def main():
	gtk.main()
	return 0

if __name__=="__main__":
	window()
	main()
