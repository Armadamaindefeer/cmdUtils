import os

# Thanks for Michel Blancard for the source used here
# You can find original code by following this link https://gist.github.com/michelbl/efda48b19d3e587685e3441a74457024
# 

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import atexit
    import sys
    import termios
    from select import select

class keyboardHandler:
	isSetup = False
	handlerQte = 0
	old_term = []
	new_term = []
	if os.name != 'nt':
		fd = sys.stdin.fileno()
	else:
		fd = 0

	def __init__(self):
		keyboardHandler.handlerQte +=1
		self.set_custom_term()


	def __del__(self):
		keyboardHandler.handlerQte -= 1
		if keyboardHandler.handlerQte == 0:
			self.set_normal_term()

	@classmethod
	def term_pause(cls,func,*args,**kwargs):
		cls.set_normal_term()
		result = func(*args,**kwargs)
		cls.set_custom_term()
		return result


	@classmethod
	def set_custom_term(cls):
		''' Set custom terminal. On Windows this is a no-op.
		'''
		if os.name == 'nt':
			pass
		elif not cls.isSetup:
			# Save the terminal settings
			cls.new_term = termios.tcgetattr(cls.fd)
			cls.old_term = termios.tcgetattr(cls.fd)

			# New terminal setting unbuffered
			cls.new_term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
			termios.tcsetattr(cls.fd, termios.TCSAFLUSH, cls.new_term)
			atexit.register(cls.set_normal_term)
		cls.isSetup = True

	@classmethod
	def set_normal_term(cls):
		''' Resets to normal terminal.  On Windows this is a no-op.
		'''
		if os.name == 'nt':
			pass
		else:
			termios.tcsetattr(cls.fd, termios.TCSAFLUSH, cls.old_term)
		cls.isSetup = False

	@classmethod
	def getch(cls):
		''' return lastest stdin char
		'''
		if not cls.isSetup:
			cls.set_custom_term()

		if os.name == 'nt':
			return msvcrt.getch()
		else: 
			return sys.stdin.read(1)

	@classmethod
	def wgetch(cls):
		''' return lastest stdin utf-8 key
		'''	
		if os.name == "nt":
			return msvcrt.getwch()
		else:

			"""
			#Probable remplacement de l'algorithm sous le doc
			char_test = ["\x1B","\x4F\x5B","\x31\x32\x33\x35\x36","\x30\x31\x33\x34\x35\x37\x38\x39"]
			wide_char_bis = ""
			for i in range(len(char_test)):
				wide_char_bis += self.getch()
				if wide_char_bis[i] != char_test[i]:
					return wide_char_bis
			"""

			wide_char = cls.getch()

			if wide_char[0] not in "\x1B":
				return wide_char

			wide_char += cls.getch()
			if wide_char[1] not in "\x4F\x5B":
				return wide_char

			wide_char += cls.getch()
			if wide_char[2] not in "\x31\x32\x33\x35\x36":
				return wide_char

			wide_char += cls.getch()
			if wide_char[3] not in "\x30\x31\x33\x34\x35\x37\x38\x39":
				return wide_char

			wide_char += cls.getch()
			return wide_char

	@classmethod
	def getche(cls):
		''' take latest inputed char, print it then return it
		'''		
		if os.name == "nt":
			return msvcrt.getche()
		else:
			char = cls.getch()
			print(char,end='')
			return char

	@classmethod
	def wgetche(cls):
		''' take latest inputed utf-8 key, print it then return it
		'''	
		if os.name == "nt":
			return msvcrt.getwche()
		else:
			wchar = cls.wgetch()
			print(wchar,end='')
			return wchar

	@classmethod
	def kbhit(cls):
		''' Returns True if keyboard character was hit, False otherwise.
		'''
		if not keyboardHandler.isSetup:
			cls.set_custom_term()
		if os.name == 'nt':
			return msvcrt.kbhit()
		else:
			dr,_,_ = select([sys.stdin], [], [], 0)
			return dr != []
