'''
Created on Jul 2, 2010

@author: catapult
'''
from cx_Freeze import setup, Executable
setup(executables = [Executable("WeatheredStone.py"),Executable("StoneServer.py")])
