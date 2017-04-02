import sys, queue, threading, tkinter


msg_queue = queue.Queue()


class Root(tkinter.Tk):

	def __init__(self, *args, **kwargs):

		tkinter.Tk.__init__(self, *args, **kwargs)

		self.protocol("WM_DELETE_WINDOW", self.quit)

		self.big_display_string = tkinter.StringVar()
		self.input_string = tkinter.StringVar()

		self.in_messages = tkinter.Label(self, textvariable = self.big_display_string, justify = tkinter.LEFT, anchor = tkinter.NW, width = 80, height = 20)
		self.in_messages.grid(row = 0, column = 0)

		self.out = tkinter.Entry(self, textvariable = self.input_string, width = 80)
		self.out.bind('<Return>', self.deal_with_user_input)
		self.out.grid(row = 1, column = 0)

		threading.Thread(target = stdin_reader, daemon = True).start()

		self.after(20, self.deal_with_stdin)

	def deal_with_user_input(self, event):
		print(self.input_string.get())
		sys.stdout.flush()
		self.input_string.set("")

	def deal_with_stdin(self):
		try:
			msg = msg_queue.get(block = False).strip()
			lines = self.big_display_string.get().split("\n")
			lines.append(msg)
			if len(lines) > 20:
				lines = lines[len(lines) - 20:]
			text_to_show = "\n".join(lines)
			self.big_display_string.set(text_to_show)
		except:
			pass

		self.after(20, self.deal_with_stdin)


def stdin_reader():
	for line in sys.stdin:
		msg_queue.put(line)


if __name__ == "__main__":
	app = Root()
	app.mainloop()
