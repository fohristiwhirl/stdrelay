import sys, queue, threading, tkinter

msg_queue = queue.Queue()

class Root(tkinter.Tk):

	def __init__(self, *args, **kwargs):

		tkinter.Tk.__init__(self, *args, **kwargs)

		self.protocol("WM_DELETE_WINDOW", self.quit)

		self.in_messages = tkinter.Label(self, text = "...messages here...", justify = tkinter.LEFT, width = 80)
		self.in_messages.pack()

		self.outvar = tkinter.StringVar()

		self.out = tkinter.Entry(self, textvariable = self.outvar, width = 80)
		self.out.bind('<Return>', self.deal_with_user_input)
		self.out.pack()

		threading.Thread(target = stdin_reader, daemon = True).start()

		self.after(20, self.deal_with_stdin)

	def deal_with_user_input(self, event):
		print(self.outvar.get())
		self.outvar.set("")

	def deal_with_stdin(self):
		try:
			foo = msg_queue.get(block = False).strip()
			self.in_messages.config(text = foo)
		except:
			pass

		self.after(20, self.deal_with_stdin)



def stdin_reader():
	for line in sys.stdin:
		msg_queue.put(line)


if __name__ == "__main__":
	app = Root()
	app.mainloop()
