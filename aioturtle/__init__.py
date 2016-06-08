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
import turtle

from .aioturtle import BlockingTurtle, AsyncTurtle, TurtlePrompt, demo


__title__ = 'aioturtle'
__version__ = '0.0.0'
__author__ = 'Eric Appelt'
__license__ = 'None'
__copyright__ = 'Copyright 2016 Eric Appelt'

# I mean, it could change one day, right???
_KNOWN_TURTLES = ('turtle 1.1b- - for Python 3.1   -  4. 5. 2009',)

if turtle._ver not in _KNOWN_TURTLES:
    msg = (
        'aioturtle may not have been tested against the version of the turtle '
        'module packaged with this python distribution.'
    )
    warnings.warn(msg, UserWarning)
