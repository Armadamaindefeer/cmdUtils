
from typing import Callable , Any

class Command:
	def __init__( self, name: str, function: Callable[...,Any], usage: str, needQuantity: int =-1, maxQuantity: int =-1, minQuantity: int =-1, argument=None) -> None:
		self.call_name = name
		self.function = function
		self.usage = usage
		self.needQuantity = needQuantity # False : no-defined quantity | 1 -> inf : number of arg required to exec func
		self.maxQuantity = maxQuantity # False : no-limit max quantity | 1 -> inf : max number of arg that the func can handle
		self.minQuantity = minQuantity # False : quantity can be anywhere between 0 and MaxQuantity | 1 -> inf : min number of arg that the func can handle
		self.argument = argument

	def __call__(self, *args , **kwds):
		return self.function(*args,**kwds)

	def run_func(self,*args,**kwargs):
		return self.function(*args,**kwargs)
