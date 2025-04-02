#CmdUtils is a small terminal library for python 3.8 or newer
#Copyright (C) 2022-2023  Simon Poulet-Alligand | Arma_mainfeer
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#>>-----------Import----------------<<

import datetime
import typing
import time

from .command import Command, InputParameter ,globalCommands
from .key import __key as key
from .__keyboardHandler import keyboardHandler

#>>-----------Constants-------------<<

DEBUG = -1
INFO = 0
WARM = 1
ERROR = 2
CRITICAL = 3
GLOBAL_DEBUG = False
RESET_COLOR = "\033[m"
DEFAULT_COLOR = "\033[38;5;97m"
DEBUG_COLOR = "\033[38;5;240m"
FATAL_COLOR = "\033[38;5;160m"
ERROR_COLOR = "\033[38;5;166m"
WARN_COLOR = "\033[38;5;11m"
INFO_COLOR = "\033[38;5;248m"
INTERNAL_DEBUG = False

#>>-----------Utils------------------<<

def Interrupt(text:str,source:str)-> None:
	log("INPUT", text, source, color=WARN_COLOR,pend="")
	keyboardHandler.getch()
	return

def Input(text:str,source:str) -> str:
	log("INPUT", text, source, color=WARN_COLOR,pend="")
	return keyboardHandler.term_pause(input," : ")

def Validate(text:str,source:str, enterIsYes=False) -> bool:
	log("INPUT", text, source, color=WARN_COLOR,pend="")
	if enterIsYes:
		answer = keyboardHandler.term_pause(input,' [Y/n] : ').casefold()
		return answer == 'Y'.casefold() or answer == 'O'.casefold() or answer == ""
	else:
		answer = keyboardHandler.term_pause(input,' [Y/n] : ').casefold()
		return answer == 'Y'.casefold() or answer == 'O'.casefold()

def Choice(text:str,source:str,choices:list,enterIsNone=False) -> int:
	log("INPUT", text, source, color=WARN_COLOR,pend="")
	print(f"[1/{len(choices)}] : ")
	answer = 0
	for _choice in range(len(choices)):
		print(f"[{_choice+1}] - {choices[_choice]}",end="\n")
	try:
		answer = keyboardHandler.term_pause(input)
		if enterIsNone and answer == "":
			return -1
		else:
			answer = int(answer)
		if answer > len(choices):
			raise ValueError
	except ValueError:
		error("Invalid input....retrying",source)
		return Choice(text,source,choices,enterIsNone)
	return answer -1

def log(level : str, content : str, source : str,color : str ="",pend : str ='\n') -> None:
	now = datetime.datetime.now()
	hour = '{:02d}'.format(now.hour)
	minute = '{:02d}'.format(now.minute)
	second = '{:02d}'.format(now.second)
	template_format = "\r{color}[{hour}:{minute}:{second}][{source}/{level}] {content}\033[m"
	formatted_message = template_format.format(color=color,hour=hour,minute=minute,second=second,level=level,content=content,source=source)
	print(formatted_message,end=pend)

def debug(message : typing.Any, source : str="MAIN") -> None:
	if GLOBAL_DEBUG:
		log("DEBUG", message, source, color=DEBUG_COLOR)

def info(message : typing.Any, source : str="MAIN") -> None:
	log("INFO", message, source, color=INFO_COLOR)

def warn(message : typing.Any, source : str="MAIN") -> None:
	log("WARN", message, source, color=WARN_COLOR)

def error(message : typing.Any, source : str="MAIN") -> None:
	log("ERROR", message, source, color=ERROR_COLOR)

def fatal(message : typing.Any, source : str="MAIN") -> None:
	log("FATAL", message, source, color=FATAL_COLOR)

def toggleGlobalDebug():
	global GLOBAL_DEBUG
	GLOBAL_DEBUG = not GLOBAL_DEBUG

def toggleInternalDebug():
	global INTERNAL_DEBUG
	INTERNAL_DEBUG = not INTERNAL_DEBUG

def formatter(unformatted_str: str) -> str:
	replace_dict = {"%h": "hour", "%m" : "minutes", "%s" : "seconde",}
	return ""

#>>-----------HANDLER------------------<<

class CmdHandler:
	def __init__(self, source: str, debug: bool = False, command_char: str = "" ) -> None:
		self.cmd_history = [""]
		self.cmd_latest_index = 0
		self.source = source
		self.format = ""
		self.isDebug = debug
		self.command_char = command_char
		self.command_char_mode = True if command_char != "" else False
		self.cmd_list:dict[str,Command] = dict()
		self.__default_callback = Command("print", print, "print TEXT ...","lorem ipsum", minQuantity=1)
		self.kb = keyboardHandler()
		for command in globalCommands:
			self.add_command(command)

	def debug(self, message: str) -> None:
		if self.isDebug or GLOBAL_DEBUG:
			log("DEBUG", message, self.source, color=DEBUG_COLOR)

	def _internal_debug(self, message: str) -> None:
		if INTERNAL_DEBUG:
			log("DEBUG",message,"CMD_HANDLER", color=DEBUG_COLOR)

	def info(self, message: typing.Any) -> None:
		info(message, self.source)

	def warn(self, message: typing.Any) -> None:
		warn(message, self.source)

	def error(self, message: typing.Any) -> None:
		error(message, self.source)

	def fatal(self, message: typing.Any) -> None:
		fatal(message, self.source)

	def add_multiple_command(self,commands : set | list | tuple):
		for command in commands:
			self.add_command(command)

	def add_command(self,command : Command):
		#Remove runtime type check, done at compile time
		if type(command) == Command:
			self.cmd_list[command.call_name] = command
		else:
			self.warn(f"Unrecognized commands format for {command} of type {type(command)}")

	def getAvailableToken(self,values:list[str],buffer:str):
		token_set = {token[:len(buffer)+1] for token in values if token.startswith(buffer)}
		if len(token_set) > 1 or len(token_set) == 0:
			return buffer
		else:
			returnToken = token_set.pop()
			available_value = [value for value in values if value.startswith(returnToken)]
			if len(available_value) == 1:
				return available_value[0] + " "
			else:
				return self.getAvailableToken(values,returnToken)

	def autoComplete(self,char_buffer:str,values:list[str]) ->str:

		display_token = [token for token in values if token.startswith(char_buffer)]
		if len(display_token) > 1 and len(display_token) <= 60:
			print("\r",end="")
			for i,value in enumerate(display_token,1):
				terminator = "\n" if i % 6 == 0 else "\t"
				print(value,end=terminator)
			print()

		return self.getAvailableToken(values,char_buffer)


	def custom_input(self):
		__char_buffer = self.cmd_history[-1]
		__current_index = len(self.cmd_history) -1
		__cursor_retreat = 1
		print(f"\r$> {__char_buffer}",end=" \x1b[2K")
		while True:
			second = True
			if self.kb.kbhit() and second :
				second = not second
				__temp = self.kb.wgetch()
				if __temp in key.forbidden_key:
					if INTERNAL_DEBUG:
						self._internal_debug(f"Forbidden key triggered with : {[hex(ord(char)) for char in __temp]}")
					continue
				match __temp:
					case key.BACKSPACE:
						if __cursor_retreat <= len(__char_buffer) and len(__char_buffer) > 0:
							FirstHalf = __char_buffer[:len(__char_buffer) - __cursor_retreat +1][:-1]
							SecondHalf = __char_buffer[len(FirstHalf)+1::]
							__char_buffer = FirstHalf + SecondHalf				
					case key.SUPPR:
						if __cursor_retreat <= len(__char_buffer) and len(__char_buffer) > 0:
							FirstHalf = __char_buffer[:len(__char_buffer) - __cursor_retreat +2][:-1]
							SecondHalf = __char_buffer[len(FirstHalf)+1::]
							__char_buffer = FirstHalf + SecondHalf
							__cursor_retreat -= 1 if __cursor_retreat > 1 else 0 	
					case key.ENTER :
						if __char_buffer.strip() != "":
							self.cmd_history[-1] = __char_buffer
							self.cmd_history += [""]
							__current_index = len(self.cmd_history)-1
							__output__ = __char_buffer
							__char_buffer = ""
							return __output__
					#Remplacer debug key par auto complétion
					case key.F2:
						if INTERNAL_DEBUG:
							self._internal_debug(f"Input log current index : {__current_index}/{len(self.cmd_history)-1}")
							self._internal_debug(f"Commands log history : {self.cmd_history}")
							self._internal_debug(f"Char buffer text : \"{__char_buffer}\", {[hex(ord(char)) for char in __char_buffer]}")
							self._internal_debug(f"Char buffer size : {len(__char_buffer)}")
							self._internal_debug(f"Cursor retreat : {__cursor_retreat}")
					case key.TAB:
						available_command = list(self.cmd_list.keys())
						token_metadata,token = self.parser(__char_buffer)
						self._internal_debug(f"Tokens : {token}")

						if token_metadata["isCommand"] and len(token) > 0:
							if token[0] in available_command:
								__char_buffer = self.cmd_list[token[0]].auto_completion(token)
							elif len(token) == 2 and not (token[0] == "" or token[0] == " ") and not (token[1] == " "):
								token[0] = self.autoComplete(token[0],available_command)
								__char_buffer = token[0]

					case key.UP:
						if __current_index == len(self.cmd_history)-1:
							self.cmd_history[-1] =  __char_buffer
						if __current_index > 0:
							__cursor_retreat = 0

						__current_index -= 1 if __current_index != 0 else 0
						__char_buffer = self.cmd_history[__current_index]
					case key.DOWN:
						if __current_index != len(self.cmd_history)-1:
							__current_index += 1
							__char_buffer = self.cmd_history[__current_index]
							__cursor_retreat = 1
					case key.LEFT:
						if __cursor_retreat <= len(__char_buffer):
							__cursor_retreat += 1
					case key.RIGHT:
						if __cursor_retreat > 1:
							__cursor_retreat -= 1
					case key.CTRL_C:
						self._internal_debug(f"Catch and Rise again KeyboardInterrupt")
						raise KeyboardInterrupt
					case _:
						FirstHalf = __char_buffer[:len(__char_buffer) -__cursor_retreat + 1]
						SecondHalf = __char_buffer[len(FirstHalf)::]
						__char_buffer = FirstHalf + __temp + SecondHalf
	
				__cursor_retreat = 1 if __cursor_retreat-1 > len(__char_buffer) else __cursor_retreat
				print(f"\r$> {__char_buffer} \033[{__cursor_retreat}D",end=" \x1b[2K")
			time.sleep(0.0005)

	def parser(self, _to_parse: str) -> tuple[dict,list[str]]:
		input_metadata = {"isCommand" : False}
		#Détermine si l'input est une commande
		if self.command_char_mode and _to_parse.startswith(self.command_char):
			input_metadata["isCommand"] = True
			_to_parse = _to_parse.replace(self.command_char,"",1)
		elif not self.command_char_mode:
			input_metadata["isCommand"] = True


		__input_parameter = []
		_bracket = False
		_skip_next = False
		temp = ""
		for i,char in enumerate(_to_parse):
			if _skip_next:
				temp += char
				_skip_next = False
			elif char == "\\":
				temp += char
				_skip_next = True
			elif char == "\"":
				_bracket = not _bracket
			elif _bracket:
				temp += char
			elif char == " ":
				__input_parameter += [temp]
				temp = ""
			else:
				temp += char
			
			if i == len(_to_parse) -1:
				__input_parameter += [temp]

		while len(__input_parameter) > 0 and __input_parameter[-1] == "":
			__input_parameter = __input_parameter[:-1]

		endSpacing = ""

		if len(_to_parse) > 0 and _to_parse.endswith(" "):
			for char in _to_parse[::-1]:
				if char != " ":
					break
				else:
					endSpacing += " "

		__input_parameter += [endSpacing]
		return (input_metadata, __input_parameter)

	def check_func_input(self, parameter_input: list[str], commandsObject: Command) -> bool:
		if commandsObject.needQuantity <= -1:
			if commandsObject.maxQuantity >= 0 and len(parameter_input) > commandsObject.maxQuantity:
				self.warn(f"Too many parameter for function : {commandsObject.call_name}")
				return False
			elif commandsObject.minQuantity >= 0 and len(parameter_input) < commandsObject.minQuantity:
				self.warn(f"Not enough parameter for function : {commandsObject.call_name}")
				return False
		elif len(parameter_input) != commandsObject.needQuantity:
			self.warn(f"Incorrect input quantity for function : {commandsObject.call_name} ")
			return False
		return True


	#Command_unit -> [{"isCommand" : value},[command_name/parameter, parameter ...]]
	#Commands_list -> [Command_unit,Command_unit,...]
	def handle_input(self, text_input: str | None = None):
		input_user_ = self.custom_input() if text_input == None else text_input
		input_metadata, input_parameter = self.parser(input_user_)
		command_name = input_parameter[0]

		if command_name == "":
			print("\r",end="")
			return

		elif input_metadata["isCommand"] == False and self.command_char_mode:
			self._internal_debug(f"passing args to defaut callback with input :{input_parameter}")
			self.__default_callback(InputParameter(dict(),[*input_parameter]))
			return

		elif not command_name in self.cmd_list:
			self.warn(f"Unrecognized commands : {command_name}")
			return

		elif not self.check_func_input(input_parameter[1::][:-1], self.cmd_list[command_name]):
			self.warn(self.cmd_list[command_name].usage)
			return

		else:
			self._internal_debug(f"Launching command \'{command_name}\' with parameters : {input_parameter[1::][:-1]}")
			self.cmd_list[command_name](InputParameter(dict(),[*input_parameter[1::][:-1]]))
