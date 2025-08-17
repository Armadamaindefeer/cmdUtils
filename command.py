# A CLI manager for python 
# Copyright (C) 2022-2025 Simon Alligand | Arma_mainfeer
# contact : simon.alligand@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import typing


class InputParameter:
	def __init__(self,global_args:dict[str,typing.Any],input:list[str]) -> None:
		self._global = global_args
		self.input = input

	def __getitem__(self, key:int) -> str:
		return self.input[key]

	def __len__(self) -> int:
		return len(self.input)


class Command:
	def __init__( self, name: str, function: typing.Callable[[InputParameter],typing.Any],usage: str, desc :str,needQuantity: int =-1, maxQuantity: int =-1, minQuantity: int =-1, argument=None, auto_completion_func = lambda x: "".join([text+ ("" if text.endswith(" ") else "") for text in x])) -> None:
		self.call_name = name
		self.function = function
		self.desc = desc
		self.usage = usage
		self.needQuantity = needQuantity # False : no-defined quantity | 1 -> inf : number of arg required to exec func
		self.maxQuantity = maxQuantity # False : no-limit max quantity | 1 -> inf : max number of arg that the func can handle
		self.minQuantity = minQuantity # False : quantity can be anywhere between 0 and MaxQuantity | 1 -> inf : min number of arg that the func can handle
		self.auto_completion = auto_completion_func
		self.argument = argument

	def __call__(self, input:InputParameter):
		return self.function(input)

globalCommands:list[Command] = list()

def Wrapper(name: str, usage: str, desc:str,needQuantity: int =-1, maxQuantity: int =-1, minQuantity: int =-1, argument=None, auto_completion_func = lambda x: "".join([text+ ("" if text.endswith(" ") else "") for text in x])):
	def __wrapped_wrapper(func:typing.Callable[[InputParameter],typing.Any]):			
		global globalCommands
		def __wrapped_func(*args,**kwargs):
			try:
				func(*args,**kwargs)
			except KeyboardInterrupt:
				return print()
		globalCommands += [Command(name,__wrapped_func,usage,desc,needQuantity,maxQuantity,minQuantity,argument,auto_completion_func)]
		return func
	return __wrapped_wrapper
