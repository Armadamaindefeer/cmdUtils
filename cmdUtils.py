#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#v1.0.1[pre-released]
#CmdUtils is a small terminal library for python 3.8 or newer
#Copyright (C) 2023  Simon Poulet-Alligand | Arma_mainfeer
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
import time
from typing import Callable , Any, Union

from readchar import readchar as getch, readkey as wgetch, key

from command import Command
from forbidden_key import forbidden_key

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
INTERNAL_DEBUG = True

#>>-----------Utils------------------<<

def validate(message : str) -> bool:
	log("WARN", message, "MAIN", color=WARN_COLOR,pend="" )
	answer = input(' [Y/n]\n')
	return answer == 'Y' or answer == 'y' or answer == 'o' or answer == 'O' or answer == ""

def log(level : str, content : str, source : str,color : str ="",pend : str ='\n') -> None:
	now = datetime.datetime.now()
	hour = '{:02d}'.format(now.hour)
	minute = '{:02d}'.format(now.minute)
	second = '{:02d}'.format(now.second)
	template_format = "\r{color}[{hour}:{minute}:{second}][{source}/{level}] {content}\033[m"
	formatted_message = template_format.format(color=color,hour=hour,minute=minute,second=second,level=level,content=content,source=source)
	print(formatted_message,end=pend)

def debug(message : Any, source : str="MAIN") -> None:
	if GLOBAL_DEBUG:
		log("DEBUG", message, source, color=DEBUG_COLOR)

def info(message : Any, source : str="MAIN") -> None:
	log("INFO", message, source, color=INFO_COLOR)

def warn(message : Any, source : str="MAIN") -> None:
	log("WARN", message, source, color=WARN_COLOR)

def error(message : Any, source : str="MAIN") -> None:
	log("ERROR", message, source, color=ERROR_COLOR)

def fatal(message : Any, source : str="MAIN") -> None:
	log("FATAL", message, source, color=FATAL_COLOR)

def toggleGlobalDebug():
	global GLOBAL_DEBUG
	GLOBAL_DEBUG = not GLOBAL_DEBUG

def formatter(unformatted_str: str) -> str:
	replace_dict = {"%h": "hour", "%m" : "minutes", "%s" : "seconde",}
	return ""

#>>-----------HANDLER------------------<<

class CmdHandler:
	def __init__(self, cmd_list: Union[list,set], source: str, debug: bool = False, command_char: str = "" ) -> None:
		self.cmd_history = [""]
		self.cmd_latest_index = 0
		self.source = source
		self.format = ""
		self.isDebug = debug
		self.command_char = command_char
		self.cmd_list = {}
		self.__default_callback = Command("print", print, "lorem ipsum", minQuantity=1)
		for command in cmd_list:
			self.add_command(command)

	def debug(self, message: str) -> None:
		if self.isDebug or GLOBAL_DEBUG:
			log("DEBUG", message, self.source, color=DEBUG_COLOR)

	def _internal_debug(self, message: str) -> None:
		if INTERNAL_DEBUG:
			log("DEBUG",message,self.source, color=DEBUG_COLOR)

	def info(self, message: Any) -> None:
		info(message, self.source)

	def warn(self, message: Any) -> None:
		warn(message, self.source)

	def error(self, message: Any) -> None:
		error(message, self.source)

	def fatal(self, message: Any) -> None:
		fatal(message, self.source)

	def add_command(self,command : Command, name:str = ""):
		if type(command) == Command: 
			self.cmd_list[command.call_name] = command
		else:
			self.warn(f"Unrecognized commands format for{command} of type {type(command)}")

	def custom_input(self):
		#TODO implement cursor
		#TODO lire stdin uniquement changement/toucher presser
		__char_buffer = self.cmd_history[-1]
		__current_index = len(self.cmd_history) -1
		while True:
			print(f"\r$> {__char_buffer}",end=" \x1b[2K")
			__temp = wgetch()

			#Skip des caractère pouvant broke le programme
			if __temp in forbidden_key:
				pass

			#Suppression du caractère sur la gauche
			elif __temp == key.BACKSPACE:
				__char_buffer = __char_buffer[:-1]

			#Validation de la commande
			elif __temp == key.ENTER:
				if __char_buffer.strip() != "":
					self.cmd_history[-1] = __char_buffer
					self.cmd_history += [""]
					__current_index = len(self.cmd_history)-1
					__output__ = __char_buffer
					__char_buffer = ""
					return __output__
				else:
					pass

			#Debug controller (disabled via forbidden key)
			#Sera remplacer par l'autocomplétion
			elif __temp == key.TAB:
				self.info(__current_index)
				self.info(self.cmd_history)

			#Action de remonter l'historique
			elif __temp == key.UP:
				if __current_index == 0:
					pass
				elif __current_index == len(self.cmd_history)-1:
					self.cmd_history[-1] =  __char_buffer
					__current_index -= 1
					__char_buffer = self.cmd_history[__current_index]
				else:
					__current_index -= 1
					__char_buffer = self.cmd_history[__current_index]

			#Action de descendre l'historique
			elif __temp == key.DOWN:
				if __current_index == len(self.cmd_history)-1:
					pass
				else:
					__current_index += 1
					__char_buffer = self.cmd_history[__current_index]
				pass

			#Skip les champs vides -- checker l'utilité de la commande
			#elif __temp == 0:
			#	pass

			elif __temp == key.CTRL_C:
				raise KeyboardInterrupt

			else:
				__char_buffer += __temp

	def parser(self, _to_parse: str):
		input_metadata = {"isCommand" : False}
		#Détermine si l'input est une commande
		if _to_parse.startswith(self.command_char):
			input_metadata["isCommand"] = True
			_to_parse = _to_parse.replace(self.command_char,"",1)
		
		__input_parameter = []
		_bracket = False
		_skip_next = False
		temp = ""
		for i in _to_parse:
			if _skip_next:
				temp += i
				_skip_next = False
			elif i == "\\":
				temp += i
				_skip_next = True
			elif i == "\"":
				_bracket = not _bracket
			elif _bracket:
				temp += i
			elif i == " ":
				__input_parameter += [temp]
				temp = ""
			else:
				temp += i
		__input_parameter += [temp]
		return [input_metadata, __input_parameter]

	def check_func_input(self, parameter_input: list[str], commandsObject: Command) -> bool:
		if commandsObject.needQuantity <= -1:
			if commandsObject.maxQuantity >= 0 and len(parameter_input) > commandsObject.maxQuantity:
				self.warn(f"Too many parameter for function : {commandsObject.call_name}")
				return False
			elif commandsObject.minQuantity >= 0 and len(parameter_input) < commandsObject.minQuantity:
				self.warn(f"Not enough parameter for function : {commandsObject.call_name}")
				return False
		elif len(parameter_input) != commandsObject.needQuantity:
			print(parameter_input)
			print(len(parameter_input))
			self.warn(f"Incorrect input quantity for function : {commandsObject.call_name} ")
			return False
		return True


	#Command_unit -> [{"isCommand" : value},[command_name/parameter, parameter ...]]
	#Commands_list -> [Command_unit,Command_unit,...]
	def handle_input(self, text_input: Union[str,None]=None):
		input_user_ = self.custom_input() if text_input == None else text_input
		input_metadata, input_parameter = self.parser(input_user_)
		command_name = input_parameter[0]

		if command_name == "":
			print("\r")
			return

		elif input_metadata["isCommand"] == False and self.command_char == "":
			self._internal_debug(f"passing args to defaut callback with input :{input_parameter}")
			self.__default_callback(*input_parameter)
			return

		elif not command_name in self.cmd_list:
			self.warn(f"Unrecognized commands : {command_name}")
			return

		elif not self.check_func_input(input_parameter[1::], self.cmd_list[command_name]):
			self.warn(self.cmd_list[command_name].usage)
			return

		else:
			self._internal_debug(f"Launching command \"{command_name}\" with parameters : {input_parameter[1::]}")
			self.cmd_list[command_name](*input_parameter[1::])
