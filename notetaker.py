#!/usr/bin/env python

from gi.repository import Gtk
import gio
import pango
import sys
import locale
import os
import linecache

NOTES_FOLDER = ""

SELECTED_FILE = ""

model =  Gtk.ListStore(str)

	    
class NoteTaker(Gtk.Window):

	# Initializing main window
	 
	def __init__(self):
                
                # main window for the application
                Gtk.Window.__init__(self)
                
		self.set_title("Note Taker")
		self.set_default_size(800,600)
		self.set_position(Gtk.WindowPosition.CENTER)
		
		self.show()
                self.CheckConfigFile(self)
		
		#statusbar = Gtk.Statusbar()
		toolbar = Gtk.Toolbar()
		hbox = Gtk.HBox(False,0)
		vbox = Gtk.VBox(False,0)
		
		# divide the main window in three containers
		sep2 = Gtk.HSeparator()
	        sep2.set_size_request(-1,10)
	        
	        sep3 = Gtk.HSeparator()
	        sep3.set_size_request(-1,5)
	        
		hbox = self.BrowserViewer()
		vbox.pack_start(toolbar,False,True,0)
		vbox.pack_start(sep2,False,True,0)
		vbox.pack_start(hbox,True,True,0)
		
		
		# toolbar buttons
		button_add = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
		button_add.set_tooltip_text("Add new note")
		button_remove = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
		button_remove.set_tooltip_text("Delete note")
		button_settings = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EXECUTE)
		button_settings.set_tooltip_text("Select notes directory")
                toolbar.insert(button_add, 0)
                toolbar.insert(button_remove, 1)
                toolbar.insert(button_settings, 2)
                button_add.connect("clicked",self.add_button_clicked)
                button_settings.connect("clicked",self.settings_button_clicked)
                button_remove.connect("clicked",self.remove_button_clicked)                
                
                self.add(vbox)
                                
                
        
        def CheckConfigFile(self,widget):
	
		print "Checking config file"
		
		if os.path.isfile("./config"):
			print "Config file exist"
			config = open("./config","r")
			global NOTES_FOLDER
			NOTES_FOLDER = config.read()
			print NOTES_FOLDER
			return 0
			
		else:
			print "Need to create config file"
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            			Gtk.ButtonsType.OK, "Configuration file not found")
        		dialog.format_secondary_text("Please select the directory containg notes (.txt)")
		        dialog.run()
		        dialog.destroy()
		        
	def add_button_clicked(self,widget):
		
		print "Add button is clicked"
		
	
	def remove_button_clicked(self,widget):
		
		print "Remove button is clicked"
		os.remove(NOTES_FOLDER  + model[SELECTED_FILE][0] + '.txt')
		model.remove(SELECTED_FILE)
		print "Selected file is", NOTES_FOLDER  + model[SELECTED_FILE][0] + '.txt'
		
	
	def settings_button_clicked(self,widget):
		
		print "Settings button is clicked"
		filename = self.set_notes_directory()
		
        
        def set_notes_directory(self):
        
		dialog = Gtk.FileChooserDialog("Please notes directory", self,
		    Gtk.FileChooserAction.SELECT_FOLDER,
		    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
		     "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800, 400)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
		    print "Select clicked"
		    print "Folder selected: " + dialog.get_filename()
		    global NOTES_FOLDER
  		    NOTES_FOLDER = dialog.get_filename() + "/"
  		    config = open("./config","w")
  		    config.write(NOTES_FOLDER)
  		    config.close();
  		    
  		    dialog.destroy()	
  		    self.__init__()    	
		 
		elif response == Gtk.ResponseType.CANCEL:
		    print "Cancel clicked"
		    dialog.destroy()
		
		
       
	def main(self):
		self.connect('destroy', Gtk.main_quit)
		self.show_all()
		Gtk.main()
		
	
	class BrowserViewer(Gtk.HBox):
	
		def __init__(self):
		
			Gtk.HBox.__init__(self)
			 
			self.preFileName = preFileName = ""
		
			scw0 = Gtk.ScrolledWindow()
			scw0.set_size_request(150,-1)
		
			#self.model = model =  Gtk.ListStore(str)
				
			view = Gtk.TreeView(model)
		        renderer = Gtk.CellRendererText()
		        column = Gtk.TreeViewColumn("Notes", renderer, text=0)
		        view.append_column(column)
		                        
		        scw0.add(view)
		        
		        select = view.get_selection()
		        select.connect("changed", self.on_tree_selection_changed)
		       
		        sep = Gtk.VSeparator()
			sep.set_size_request(10,-1)
			
		        folder = gio.File(NOTES_FOLDER)
		        
		        scw1 = Gtk.ScrolledWindow()
			
			self.textview  = textview = Gtk.TextView()
		
			self.statusbar= statusbar = Gtk.Statusbar()
		
		
			vboxtext = Gtk.VBox(False,0)
		
			statusbar.push(0,"")
		
			
			textview.set_wrap_mode(Gtk.WrapMode.WORD)
		        textview.set_editable(False)
		        textview.set_cursor_visible(False) 
		        textview.set_justification(Gtk.Justification.LEFT)
		        scw1.add(textview)
		        
		        sep3 = Gtk.HSeparator()
			sep3.set_size_request(-1,10)
		        
		        vboxtext.pack_start(scw1,True,True,0)
		        vboxtext.pack_start(sep3,False,True,0)
		        vboxtext.pack_start(statusbar,False,True,0)
		   
		        self.browse(folder)
		       	
		        
		        self.pack_start(scw0,False,True,0)
		        self.pack_start(sep,False,True,0)
		        self.pack_start(vboxtext,True,True,0)
		        

		def on_tree_selection_changed(self,selection):
		        
		        self.textview.set_editable(True)
		        self.textview.set_cursor_visible(True) 
		        	
			model1,treeiter = selection.get_selected()
		
			if treeiter != None:
				print self.preFileName
				filename = NOTES_FOLDER  + model1[treeiter][0]
				global SELECTED_FILE
				SELECTED_FILE = treeiter
				self.print_file_name(filename)
				self.statusbar.push(0,model1[treeiter][0])
				self.textviewer(filename)

		def print_file_name(self,filename):
		
			fileName, fileExtension = os.path.splitext(filename)
			print  fileName + '       ' + fileExtension
	
		        
		                         
		def browse(self,folder):
		        
		        subdirs = []
			files = []
		        
		      	
		      	infos = folder.enumerate_children('standard::is-hidden,'
					'standard::name,standard::display-name,standard::type,'
					'access::can-execute,standard::size')
		
			for info in infos:
				if info.get_is_hidden():
					continue
				name = info.get_name()
				child = folder.get_child(name)
				display = info.get_display_name()
				sortname = locale.strxfrm(display.decode('utf-8'))
			
				if info.get_file_type() == gio.FILE_TYPE_DIRECTORY:
					subdirs.append((sortname, child, display + '/'))
				else:
					files.append((sortname, child, display))
			
		
			subdirs.sort()
			files.sort()
			model.clear()
		
			#for sortname, child, display in subdirs:
			#	model.append([display])
			for sortname, child, display in files:
			
				fileName, fileExtension = os.path.splitext(display)
				if fileExtension == '.txt' or fileExtension == '.TXT':
					model.append([fileName])
				else:
					continue
				
		 
		def textviewer(self,filename):
		 	
		 	
		 	self.CheckForSaveAndSave()
		 	
		 	self.preFileName = filename
		 	
		 	self.ViewNote(filename)
		 	
		 	
		
		def ViewNote(self,filename):
			
			fin = open(filename+'.txt', "r")
		    	text = fin.read()
		    	fin.close()
		    	
		    	self.textview.set_sensitive(False)
		   	buff = self.textview.get_buffer()
		   	buff.set_text(text)
		    	buff.set_modified(False)
		    	self.textview.set_sensitive(True)
		 
		def CheckForSaveAndSave(self):
		 	
		 	buff = self.textview.get_buffer()
		
			if buff.get_modified():        		
				print "Previous file is not saved ", self.preFileName
				fout = open(self.preFileName+'.txt', "r+")
				fout.seek(0)
	    			fout.truncate()
	    			text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), 0)
				fout.write(text)
		    		buff.set_modified(False)
		    		fout.close()
		    		self.textview.set_sensitive(True)
				
			else:
				print "Everything is saved"	

	
 
if __name__ == '__main__':
	notes = NoteTaker()
	notes.main()
