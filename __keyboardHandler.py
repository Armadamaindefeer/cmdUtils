import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    from select import select

class keyboardHandler:
	def __init__(self):
		self.old_term = []

		if os.name == 'nt':
			pass
		else:
		# Save the terminal settings
			self.fd = sys.stdin.fileno()
			self.new_term = termios.tcgetattr(self.fd)
			self.old_term = termios.tcgetattr(self.fd)

			# New terminal setting unbuffered
			self.new_term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

	def set_normal_term(self):
		''' Resets to normal terminal.  On Windows this is a no-op.
		'''
		if os.name == 'nt':
			pass
		else:
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


	def getch(self):
		''' return lastest stdin char
		'''
		if os.name == 'nt':
			return msvcrt.getch().decode('utf-8')
		else:
			__temp = sys.stdin.read(1)
			#print(__temp)
			return __temp

	def b_wgetch(self):
		''' return lastest stdin utf-8 key (unused)
		'''
		if os.name == "nt":
			return msvcrt.getwch().decode('utf-8')
		else:
			wide_char = self.getch()
			wide_char_ord  = ord(wide_char)
			if (wide_char_ord & 0b1000_0000) == 0b0 or (wide_char_ord < 256):
				pass
			else:
				for i in range(2,9):
					if wide_char_ord & (0b1111_1111 << (8 - i) & 0b1111_1111) == (0b1111_1111 << (9 - i) & 0b1111_1111):
						for _ in range(i-2):
							wide_char += self.getch()

			return wide_char

	def wgetch(self):
		''' return lastest stdin utf-8 key
		'''		
		if os.name == "nt":
			return msvcrt.getwch.decode('utf-8')
		else:
			wide_char = self.getch()

			if wide_char[0] != "\x1B":
				return wide_char

			wide_char += self.getch()
			if wide_char[1] not in "\x4F\x5B":
				return wide_char

			wide_char += self.getch()
			if wide_char[2] not in "\x31\x32\x33\x35\x36":
				return wide_char

			wide_char += self.getch()
			if wide_char[3] not in "\x30\x31\x33\x34\x35\x37\x38\x39":
				return wide_char

			wide_char += self.getch()
			return wide_char

	def getche(self):
		''' take latest inputed char, print it then return it
		'''		
		if os.name == "nt":
			return msvcrt.getche().decode("utf-8")
		else:
			char = self.getch()
			print(char,end='')
			return char

	def wgetche(self):
		''' take latest inputed utf-8 key, print it then return it
		'''	
		if os.name == "nt":
			return msvcrt.getwche().decode("utf-8")
		else:
			wchar = self.wgetch()
			print(wchar,end='')
			return wchar

	def kbhit(self):
		''' Returns True if keyboard character was hit, False otherwise.
		'''
		if os.name == 'nt':
			return msvcrt.kbhit()
		else:
			dr,_,_ = select([sys.stdin], [], [], 0)
			return dr != []

	def __del__(self):
		self.set_normal_term()
