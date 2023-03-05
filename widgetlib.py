#!/bin/python3
""" Part of extpad - Widgets"""
from deps import *

class CNotebook(ttk.Notebook): # With "CustomNotebook" and TNotebook
	__initialized = False
	def __init__(self, *args, **kwargs):
		self.style = ttk.Style()
		self.clr_bg = "#b7b7b7"
		self.clr_tw = "#ffffff"
		if not self.__initialized:
			self.__initialize_custom_style()
			self.__inititialized = True

		kwargs["style"] = "CNotebook"
		ttk.Notebook.__init__(self, *args, **kwargs)

		self._active = None

		self.bind("<ButtonPress-1>", self.on_close_press, True)
		self.bind("<ButtonRelease-1>", self.on_close_release)

	def on_close_press(self, event):
		element = self.identify(event.x, event.y)

		if "close" in element:
			index = self.index("@%d,%d" % (event.x, event.y))
			self.state(['pressed'])
			self._active = index
			return "break"

	def on_close_release(self, event):
		if not self.instate(['pressed']):
			return

		element =  self.identify(event.x, event.y)
		if "close" not in element:
			# user moved the mouse off of the close button
			return

		index = self.index("@%d,%d" % (event.x, event.y))

		if self._active == index:
			self.event_generate("<<NotebookTabClosed>>", x=index)

		self.state(["!pressed"])
		self._active = None

	def __initialize_custom_style(self):
		style = self.style
		self.img_close_raw = \
"""#define tmp1_width 16
#define tmp1_height 16
static unsigned char tmp1_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x08, 0x38, 0x1c, 0x70, 0x0e,
   0xe0, 0x06, 0xc0, 0x01, 0x80, 0x03, 0x60, 0x07, 0x70, 0x0e, 0x38, 0x1c,
   0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };"""
		self.img_file_raw = \
"""#define open16_width 16
#define open16_height 16
static unsigned char open16_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xf8, 0x0f, 0x04, 0x1c, 0x04, 0x3c, 0xf4, 0x3c,
   0x04, 0x20, 0xf4, 0x27, 0x04, 0x20, 0xf4, 0x27, 0x04, 0x20, 0xf4, 0x27,
   0x04, 0x20, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };"""
		self.img_close = tk.Image("bitmap", "img_close", data = self.img_close_raw, foreground = "steelblue")
		self.img_close_act = tk.Image("bitmap", "img_close_act", data=self.img_close_raw, foreground="lightsteelblue")
		self.img_close_pr = tk.Image("bitmap", "img_close_pr", data=self.img_close_raw, foreground="darkslateblue")

		style.theme_settings(style.theme_use(), {
			   "CNotebook": {
				"layout": [
					("CNotebook.client", {"sticky": "nswe"})
				]
			}, "CNotebook.Tab": {
				"layout": [
					("CNotebook.tab", {"sticky": "nswe", "children": [
						("CNotebook.focus", {"side": "top", "sticky": "nswe", "children": [
							("CNotebook.padding", {"side": "top", "sticky": "nswe", "children": [
									("CNotebook.label", {"side": "left", "sticky": ''}),
									("CNotebook.close", {"side": "left", "sticky": ''}),
							]})
						]})
					]})
				]
			}
		})
		style.element_create(
			"close", "image", "img_close",
			("active", "pressed", "!disabled", "img_close_pr"),
			("active", "!disabled", "img_close_act"), 
			border=8, sticky=""
		)

class InfoFrame(ttk.Frame): # Frame to info`rmation
	def __init__(self, ikw, *args, **kwargs):
		def grc(row, column): return {"row": row, "column": column}
		self.style = ttk.Style()
		self.ikw = ikw
		ttk.Frame.__init__(self, *args, **kwargs)

		self.text = tk.Text(master=self, bd=0, highlightthickness=0, wrap="none")
		self.text.insert("end", self.ikw.setdefault("text_ph"))
		self.SCY = ttk.Scrollbar(master=self, orient="vertical", command=self.text.yview)
		self.SCX = ttk.Scrollbar(master=self, orient="horizontal", command=self.text.xview)
		self.text.config(yscrollcommand=self.SCY.set, xscrollcommand=self.SCX.set)
		self.SCY.grid(sticky="nswe", column=1)
		self.SCX.grid(sticky="nswe", row=1)
		self.grip = ttk.Sizegrip(master=self, style="ghost.TSizegrip")
		self.grip.grid(sticky="nswe", row=1, column=1)
		self.text.grid(sticky="nswe", row=0)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

class IFrame(ttk.Frame):
	def __init__(self, ikw, *args, **kwargs):
		self.style = ttk.Style()
		self.ikw = ikw
		self.id = self.ikw.setdefault("fid", ["note", -1])
		super().__init__(*args, **kwargs)

class NBFrame(ttk.Frame): # nFrame back-end
	def __init__(self, ikw, *args, **kwargs):
		def grc(row, column): return {"row": row, "column": column}
		self.style = ttk.Style()
		self.ikw = ikw
		self.id = ikw.setdefault("fid", ["note", -1])
		super().__init__(*args, **kwargs)

		nText = tk.Text(self, bd=0, highlightthickness=0, wrap="none", undo=True)
		nSBX = ttk.Scrollbar(self, command=nText.xview, orient="horizontal")
		nSBY = ttk.Scrollbar(self, command=nText.yview, orient="vertical")
		nText.config(xscrollcommand=nSBX.set, yscrollcommand=nSBY.set)
		nText.insert("1.0", self.ikw.setdefault("text", ""))
		nText.edit_reset()
		nText.edit_modified(0)
		b3bind = self.ikw.setdefault('b3bind')
		if b3bind: nText.bind("<Button-3>", b3bind)
		# Grid controls
		nSBX.grid(column=0, row=1, sticky="nsew")
		nSBY.grid(column=1, row=0, sticky="nsew")
		nText.grid(column=0, row=0, sticky="nsew")
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)