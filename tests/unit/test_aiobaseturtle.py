"""
_test_aiobaseturtle_

Unit tests for the AioBaseTurtle class methods.
"""
import unittest
import unittest.mock as mock
from turtle import Vec2D

from aioturtle.aioturtle import AioBaseTurtle

class AioBaseTurtleTests(unittest.TestCase):
    """
    Tests for the AioBaseTurtle class
    """
    def setUp(self):
        """
        Mock out the tkinter canvas and all graphics
        """
        self.screentype_patcher = mock.patch(
            'turtle._Screen',
            new=mock.Mock
        )
        self.mock_screentype = self.screentype_patcher.start()

        self.screen_patcher = mock.patch('turtle.Turtle._screen')
        self.mock_screen = self.screen_patcher.start()
        self.mock_screen.xscale = 1.0
        self.mock_screen.yscale = 1.0
        self.mock_screen.mode.return_value = 'standard'


        self.update_patcher = mock.patch(
            'aioturtle.aioturtle.AioBaseTurtle._update_graphics'
        )
        self.mock_update = self.update_patcher.start()

    def tearDown(self):
        """
        Restore mocks
        """
        self.screentype_patcher.stop()
        self.screen_patcher.stop()
        self.update_patcher.stop()

    def test_calc_move(self):
        """
        Test the AioBaseTurtle._calc_move function
        """
        t = AioBaseTurtle()
        t.speed(speed=5)
        steps, delta = t._calc_move(Vec2D(0, 100))
        self.assertEqual(steps, 20)
        self.assertAlmostEqual(delta[0], 0.0)
        self.assertAlmostEqual(delta[1], 5.0)
