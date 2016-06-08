"""
aioturtle aysncio turtle library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

aioturtle is an extension to the python standard library
"turtle" which provides an AsyncTurtle class to use with
asyncio in which movement and rotation methods are
coroutines rather than fuctions. A rudimentary REPL
is provided in order to send asynchronous instructions to
turtles.

TODO: Provide example usage

:copyright: (c) 2016 by Eric Appelt
:license: None
"""

__title__ = 'aioturtle'
__version__ = '0.0.0'
__author__ = 'Eric Appelt'
__license__ = 'None'
__copyright__ = 'Copyright 2016 Eric Appelt'

from .aioturtle import BlockingTurtle, AsyncTurtle, TurtlePrompt, demo
