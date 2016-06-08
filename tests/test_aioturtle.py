"""
Tests for the aioturtle module.

This testing is not as generally comprehensive as I would like,
but serves more as an example of generally testing asyncio
coroutines.
"""
import asyncio
import turtle
import unittest

from aioturtle.aioturtle import (AsyncTurtle,)

class AsyncTurtleTests(unittest.TestCase):
    """
    Tests for the AysncTurtle class
    """
    def setUp(self):
        """
        Ensure a clean event loop and screen for each test.

        Make the delay for the screen 0 for immediate drawing.
        """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        if turtle.Turtle._screen is None:
            turtle.Turtle._screen = turtle.Screen()
        turtle.Turtle._screen.clear()
        turtle.Turtle._screen.delay(delay=0)


    def test_navigation(self):
        """
        Test that a AsyncTurtle ends up in the correct position
        after several concurrent commands in sequence.
        """
        turtle = AsyncTurtle(loop=self.loop)
        tasks = [
            asyncio.ensure_future(turtle.fd(10), loop=self.loop),
            asyncio.ensure_future(turtle.lt(90), loop=self.loop),
            asyncio.ensure_future(turtle.fd(10), loop=self.loop),
            asyncio.ensure_future(turtle.rt(90), loop=self.loop),
            asyncio.ensure_future(turtle.fd(10), loop=self.loop)
        ]
        self.loop.run_until_complete(asyncio.wait(tasks, loop=self.loop))
        self.loop.close()
        self.assertEqual(turtle.pos()[0], 20)
        self.assertEqual(turtle.pos()[1], 10)
