from typing import Callable, Any
from enum import IntFlag, auto

class CommandError:
	PARAMETER_NOT_ENOUGH = auto()
	PARAMETER_TOO_MANY = auto()
	PARAMETER_UNKNOWN = auto()

autoComplete_type = Callable[[list[str]],list[str]]

class Shell:
	def __init__(self,input:list[str],global_args:dict[str,Any]=dict()) -> None:
		self._global = global_args
		self.input = input

	def __getitem__(self, key:int) -> str:
		return self.input[key]

	def __len__(self) -> int:
		return len(self.input)

def basicAutoComplete(input:list[str]) -> list[str]:
	return input

class CommandBase:
	def __init__(self,
			syntax:str,
			usage:str = "",
			desc:str = "",
			autoComplete:autoComplete_type = basicAutoComplete
		  ) -> None:
		self.syntax = syntax
		self.desc = desc
		self.usage = usage
		self.autoComplete = autoComplete

	def __call__(self, input:Shell) -> int:
		return 0

class Command(CommandBase):
	def __init__( self, 
			syntax: str,
			handler: Callable[[Shell],Any],
			usage:str = "", 
			desc :str="",
			mandatory:int = 0,
			optional:int = 0,
			autoComplete:autoComplete_type = basicAutoComplete
		) -> None:
		super().__init__(syntax,usage,desc,autoComplete)
		self.handler = handler
		self.mandatory = mandatory
		self.optional = optional

	def __call__(self, shell:Shell) -> int:
		if len(shell) < self.mandatory:
			return CommandError.PARAMETER_NOT_ENOUGH
		if len(shell) > (self.optional + self.mandatory) and self.optional >= 0:
			return CommandError.PARAMETER_TOO_MANY
		self.handler(shell)
		return 0

class CommandDir(CommandBase):
	def __init__( self, 
			syntax: str,
			command_dir:dict[str,CommandBase],
			usage:str = "", 
			desc :str="",
			autoComplete:autoComplete_type = basicAutoComplete
		) -> None:
		super().__init__(syntax,usage,desc,autoComplete) # Change optional and mandatory count
		self.commands = command_dir

	def __call__(self, shell: Shell) -> int:
		if len(shell) == 0:
			return CommandError.PARAMETER_NOT_ENOUGH

		if shell[0] not in self.commands:
			return CommandError.PARAMETER_UNKNOWN
		
		return	self.commands[shell[0]](Shell(shell.input[1:]))

globalCommands:list[Command] = list()

def Register(syntax:str, usage:str, desc:str,mandatory:int=0,optional:int=0,autoComplete:autoComplete_type=basicAutoComplete):
	def __decorator(func:Callable[[Shell],Any]):
		global  globalCommands
		globalCommands += [Command(syntax,func,usage,desc,mandatory,optional,autoComplete)]
		return func
	return __decorator

