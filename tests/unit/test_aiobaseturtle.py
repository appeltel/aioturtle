"""
_test_aiobaseturtle_

Unit tests for the AioBaseTurtle class methods.
"""
import math
import unittest
import unittest.mock as mock
from turtle import Vec2D

from aioturtle.aioturtle import AioBaseTurtle

class AioBaseTurtleTests(unittest.TestCase):
    """
    Tests for the AioBaseTurtle class

    Trivial property methods are not tested, as well as
    the _finalize_move and _update_graphics methods which
    are comprised of calls to graphics functions.
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

    def test_calc_rotation(self):
        """
        Test the AioBaseTurtle._calc_rotation function
        """
        t = AioBaseTurtle()
        t.speed(speed=2)
        orient, steps, delta = t._calc_rotation(120)
        self.assertEqual(steps, 21)
        self.assertAlmostEqual(delta, 120.0 / 21.0)
        self.assertAlmostEqual(orient[0], math.cos(math.radians(120)))
        self.assertAlmostEqual(orient[1], math.sin(math.radians(120)))

    def test_calc_circle(self):
        """
        Test the AioBaseTurtle._calc_circle function
        """
        t = AioBaseTurtle()
        steps, step_len, rot_step = t._calc_circle(100, extent=180)
        self.assertEqual(steps, 14)
        self.assertAlmostEqual(rot_step, 180.0 / 14.0)
        self.assertAlmostEqual(step_len, 22.3928952207)

    def test_move_step(self):
        """
        Test the AioBaseTurtle._move_step function
        """
        t = AioBaseTurtle()
        t._move_step(Vec2D(-100, 0), 20, Vec2D(10,5))
        self.assertAlmostEqual(t._position[0], 100)
        self.assertAlmostEqual(t._position[1], 100)
        t.screen._drawline.assert_called_once_with(
            t.currentLineItem,
            ((-100.0, 0.0), (100.0, 100.0)), # called with mutable _position
            "black",
            1,
            False
        )
        self.mock_update.assert_called_once_with()
