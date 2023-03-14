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
