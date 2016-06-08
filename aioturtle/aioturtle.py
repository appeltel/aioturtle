"""
_aioturtle_

asynchronous extension of python turtle module
"""
import sys
import math
import time
import asyncio
import turtle
import warnings
import logging

_TURTLE_FUNCTION_ALIASES = {
    'goto': ('setpos', 'setposition'),
    'back': ('bk', 'backward'),
    'right': ('rt',),
    'left': ('lt',),
    'setheading': ('seth',),
    'forward': ('fd',)
}

_TURTLEPROMPT_HELP = (
    """
    Valid TurtlePrompt Commands:

    -   > [TURTLENAME] [COMMAND] [ARG1] [ARG2] ...
        Sends a command to a turtle by name, either calling function
        or scheduling a coroutine. Ex: "steve fd 100", "steve circle 100 180",
        "steve color red yellow".

    -   > list
        Lists all currently scheduled coroutines.

    -   > new [TURTLENAME]
        Create a new AsyncTurtle with specified name.

    -   > quit
        Exit this program.

    -   > help
        Print this message.        
    """
)


def add_turtle_fcn_aliases(cls):
    """
    Add turtle movement function aliases to
    the attributes of the given class cls.
    """
    for fcn, aliases in _TURTLE_FUNCTION_ALIASES.items():
        for alias in aliases:
            setattr(cls, alias, getattr(cls, fcn))


class AioBaseTurtle(turtle.Turtle):
    """
    _AioBaseTurtle_

    Base class from which to create synchronous and
    asynchronous turtle types. Refactors the animated
    navigation methods in turtle.Turtle to allow
    for more readable subclass methods highlighting the
    differences between functions and coroutines.

    To further simplify the example code and avoid
    issues with separate asyncio and tkinter event loops,
    undo and gui functions are disabled.

    The number of steps to move a given distance is linearized
    so that a turtle will move a number of units equal to its
    speed in each step, unless speed is zero in which case the
    turtle moves instantaneously.
    """

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.messages = []
        super().__init__(**kwargs)

    @property
    def animated(self):
        """
        True if the turtle should be animated for the
        current action, False otherwise
        """
        return self._speed and self.screen._tracing == 1

    @property
    def step_time(self):
        """
        The time in seconds between animated steps
        for this turtle.
        """
        return self.screen._delayvalue * 0.001

    def _calc_move(self, endpoint):
        """
        Given an endpoint, calculate the number of steps and the
        vector delta to travel each step for moving an animated turtle
        to endpoint
        """
        speed = self._speed if self._speed else 1e9
        screen = self.screen
        diff = (endpoint-self._position)
        diffsq = (diff[0]*screen.xscale)**2 + (diff[1]*screen.yscale)**2
        steps = max(1, int(diffsq**0.5 / self._speed))
        delta = diff * (1.0/steps)
        return steps, delta

    def _move_step(self, start, step_num, delta):
        """
        Instantaneously move the turtle one step of vector delta
        and draw line as appropriate, from a move beginning at
        position start. The step_num is the current step in the
        animated move indexed from 1.
        """
        self._position = start + delta * step_num
        top = True if step_num == 1 else False
        if self._drawing:
            self.screen._drawline(
                self.drawingLineItem,
                (start, self._position),
                self._pencolor,
                self._pensize,
                top
            )
        self._update_graphics()

    def _finalize_move(self, end):
        """
        Complete turtle move and drawing at end of animated
        move or perform an instantaneous move.
        """
        if self.animated and self._drawing:
            self.screen._drawline(
                self.drawingLineItem,
                ((0, 0), (0, 0)),
                fill="",
                width=self._pensize
            )
        if self._drawing:
            self.currentLine.append(end)
        if isinstance(self._fillpath, list):
            self._fillpath.append(end)
        self._position = end
        if self._creatingPoly:
            self._poly.append(end)
        if len(self.currentLine) > 42:
            self._newLine()
        self._update_graphics()

    def _update_graphics(self):
        """
        Update the turtle rendering in tk
        """
        screen = self.screen
        if screen._tracing == 0:
            return
        elif screen._tracing == 1:
            self._update_data()
            self._drawturtle()
            screen._update()
        else:
            self._update_data()
            if screen._updatecounter == 0:
                for t in screen.turtles():
                    t._drawturtle()
                screen._update()

    def _calc_rotation(self, angle):
        """
        Given an angle to rotate by, return a tuple consisting of
        the final orientation, number of steps, and angle to
        rotate in each step.
        """
        angle *= self._degreesPerAU
        new_orient = self._orient.rotate(angle)
        speed = self._speed if self._speed else 1e9
        steps = 1 + int(abs(angle) / (3.0*speed))
        delta = 1.0 * angle / steps
        return new_orient, steps, delta

    def _calc_circle(self, radius, extent=None, steps=None):
        """
        Return a tuple consisting of the number of steps (steps),
        step length (step_len), and step rotation (rot_step) given
        circle parameters radius and (optionally) extent and steps.
        """
        if extent is None:
            extent = self._fullcircle
        if steps is None:
            frac = abs(extent)/self._fullcircle
            steps = 1+int(min(11+abs(radius)/6.0, 59.0)*frac)
        rot_step = 1.0 * extent / steps
        step_len = 2.0 * radius * math.sin(
            rot_step*math.pi/360.0*self._degreesPerAU
        )
        if radius < 0:
            step_len, rot_step, = -step_len, -rot_step
        return steps, step_len, rot_step

    def undo(self):
        raise NotImplementedError(
            'For simplicity, undo is intentionally not implemented '
            'in aioturtle'
        )

    def ondrag(self):
        raise NotImplementedError(
            'GUI functions are intentionally not implemented in aioturtle'
        )

    def onrelease(self):
        raise NotImplementedError(
            'GUI functions are intentionally not implemented in aioturtle'
        )

    def onclick(self):
        raise NotImplementedError(
            'GUI functions are intentionally not implemented in aioturtle'
        )

    def _goto(self):
        raise NotImplementedError('Subclass should implement turtle movement')

    def _rotate(self):
        raise NotImplementedError('Subclass should implement turtle movement')


class BlockingTurtle(AioBaseTurtle):
    """
    _BlockingTurtle_

    """
    def _goto(self, end):
        """
        Move the turtle to point end in small steps (if animated)
        depending on turtle speed, drawing a line if the pen is down.
        """
        if self.animated:
            start = self._position
            steps, delta = self._calc_move(end)
            for n in range(1, steps):
                time.sleep(self.step_time)
                self._move_step(start, n, delta)

        self._finalize_move(end)

    def _rotate(self, angle):
        """
        Turn the turtle clockwise by angle (degrees), in small
        steps if animated.
        """
        new_orient, steps, delta = self._calc_rotation(angle)
        if self.animated:
            for _ in range(steps):
                self._orient = self._orient.rotate(delta)
                time.sleep(self.step_time)
                self._update_graphics()
        self._orient = new_orient
        self._update_graphics()

    def goto(self, x, y=None):
        __doc__ = turtle.Turtle.goto.__doc__

        if y is None:
            self._goto(turtle.Vec2D(*x))
        else:
            self._goto(turtle.Vec2D(x, y))

    def forward(self, distance):
        __doc__ = turtle.Turtle.forward.__doc__

        ende = self._position + self._orient * distance
        self._goto(ende)

    def back(self, distance):
        __doc__ = turtle.Turtle.back.__doc__

        ende = self._position - self._orient * distance
        self._goto(ende)

    def left(self, angle):
        __doc__ = turtle.Turtle.left.__doc__

        self._rotate(angle)

    def right(self, angle):
        __doc__ = turtle.Turtle.right.__doc__

        self._rotate(-angle)

    def setheading(self, to_angle):
        __doc__ = turtle.Turtle.setheading.__doc__

        angle = (to_angle - self.heading())*self._angleOrient
        full = self._fullcircle
        angle = (angle+full/2.)%full - full/2.
        self._rotate(angle)

    def circle(self, radius, extent=None, steps=None):
        __doc__ = turtle.Turtle.circle.__doc__

        steps, step_len, rot_step = self._calc_circle(radius, extent, steps)

        self._rotate(rot_step * 0.5)
        for idx in range(steps):
            self._goto(self._position + self._orient*step_len)
            self._rotate(rot_step)
        self._rotate(-rot_step * 0.5)

add_turtle_fcn_aliases(BlockingTurtle)


class AsyncTurtle(AioBaseTurtle):
    """
    _AsyncTurtle_

    """
    def __init__(self, loop=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.lock = asyncio.Lock(loop=self.loop)
        super().__init__(**kwargs)

    async def _goto(self, end):
        """
        Move the turtle to point end in small steps (if animated)
        depending on turtle speed, drawing a line if the pen is down.
        """
        if self.animated:
            start = self._position
            steps, delta = self._calc_move(end)
            for n in range(1, steps):
                await asyncio.sleep(self.step_time, loop=self.loop)
                self._move_step(start, n, delta)

        self._finalize_move(end)

    async def _rotate(self, angle):
        """
        Turn the turtle clockwise by angle (degrees), in small
        steps if animated.
        """
        new_orient, steps, delta = self._calc_rotation(angle)
        if self.animated:
            for _ in range(steps):
                self._orient = self._orient.rotate(delta)
                await asyncio.sleep(self.step_time, loop=self.loop)
                self._update_graphics()
        self._orient = new_orient
        self._update_graphics()

    async def goto(self, x, y=None):
        __doc__ = turtle.Turtle.goto.__doc__

        with (await self.lock):
            if y is None:
                await self._goto(turtle.Vec2D(*x))
            else:
                await self._goto(turtle.Vec2D(x, y))

    async def forward(self, distance):
        __doc__ = turtle.Turtle.forward.__doc__

        with (await self.lock):
            ende = self._position + self._orient * distance
            await self._goto(ende)

    async def back(self, distance):
        __doc__ = turtle.Turtle.back.__doc__

        with (await self.lock):
            ende = self._position - self._orient * distance
            await self._goto(ende)

    async def left(self, angle):
        __doc__ = turtle.Turtle.left.__doc__

        with (await self.lock):
            await self._rotate(angle)

    async def right(self, angle):
        __doc__ = turtle.Turtle.right.__doc__

        with (await self.lock):
            await self._rotate(-angle)

    async def setheading(self, to_angle):
        __doc__ = turtle.Turtle.setheading.__doc__

        with (await self.lock):
            angle = (to_angle - self.heading())*self._angleOrient
            full = self._fullcircle
            angle = (angle+full/2.)%full - full/2.
            await self._rotate(angle)

    async def circle(self, radius, extent=None, steps=None):
        __doc__ = turtle.Turtle.circle.__doc__

        with (await self.lock):
            steps, dist, rot_step = self._calc_circle(radius, extent, steps)

            await self._rotate(rot_step * 0.5)
            for idx in range(steps):
                await self._goto(self._position + self._orient*dist)
                await self._rotate(rot_step)
            await self._rotate(-rot_step * 0.5)

add_turtle_fcn_aliases(AsyncTurtle)


class TurtlePrompt:
    """
    Interactive prompt for issuing commands to AsyncTurtles
    """
    def __init__(self, version=None):
        """
        Read from STDIN, either get the Screen singleton or
        create it, and prepare Queue.
        """
        self.version = version
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=self.loop)
        self.loop.add_reader(sys.stdin, self.entry)
        if turtle.Turtle._screen is None:
            turtle.Turtle._screen = turtle.Screen()
        self.screen = turtle.Turtle._screen

    def entry(self):
        """
        Callback for STDIN entries
        """
        asyncio.ensure_future(
            self.queue.put(sys.stdin.readline()),
            loop=self.loop
        )

    async def run(self):
        """
        Retrieve command strings from the Queue and parse them
        """
        if self.version:
            welcome = (
                'TurtlePrompt version {0}: Enter "help" for help, '
                '"quit" to exit.'.format(self.version)
            )
        else:
            welcome = 'TurtlePrompt: Enter "help" for help, "quit" to exit.'
        print(welcome)

        while True:
            print('aioturtle> ', end='', flush=True)
            command = await self.queue.get()
            try:
                command = command.split()
                if not command:
                    continue
                elif command[0] == 'quit':
                    return
                elif command[0] == 'new':
                    AsyncTurtle(name=command[1])
                elif command[0] == 'list':
                    for task in asyncio.Task.all_tasks(loop=self.loop):
                        print(task)
                elif command[0] == 'help':
                    print(_TURTLEPROMPT_HELP)
                else:
                    self.command_turtle(command)
            except Exception as e:
                logging.exception(e)

    def command_turtle(self, command_list):
        """
        Interpret a command string as a function or coroutine to
        run on the given turtle. Print the return value of the
        function if not none or the Task if a couroutine. 
        """
        turtle_name = command_list[0]
        turtle = self.get_turtle(turtle_name)

        command = getattr(turtle, command_list[1])
        args = [self._convert_arg(x) for x in command_list[2:]]

        logging.debug(
            'Running command {0} on turtle {1}'
            .format(command, turtle)
        )
        if asyncio.iscoroutinefunction(command):
            result = asyncio.ensure_future(command(*args), loop=self.loop)
        else:
            result = command(*args)
        if result is not None:
            print(result)

    def get_turtle(self, name):
        for turtle in self.screen._turtles:
            if turtle.name == name:
                return turtle
        raise Exception('Turtle {0} not found.'.format(name))

    def _convert_arg(self, arg):
        try:
            return int(arg)
        except ValueError:
            pass
        try:
            return float(arg)
        except ValueError:
            pass
        return arg

def demo(version=None):
    """
    Demonstration of aioturtle capabilities.
    """
    loop = asyncio.get_event_loop()
    turtle_names = ['guido', 'nikolay', 'victor', 'andrew']

    pets = [AsyncTurtle(name=turtle_names[idx]) for idx in range(4)]

    # move turtles to corners of 200 unit box centered at origin to start
    for idx, pet  in enumerate(pets):
        pet.up()
        x_sign = -1 if (idx//2)%2 else 1
        y_sign = -1 if idx%2 else 1  
        loop.run_until_complete(pet.goto(100*x_sign - 100, 100*y_sign))

    pets[0].color('#800000', '#ff0000')
    pets[1].color('#008000', '#00ff00')
    pets[2].color('#000080', '#0000ff')
    pets[3].color('#000000', '#606060')

    for pet in pets:
        pet.down()
        pet.write(pet.name, font=("Arial", 16, "italic"), align="left")

    tasks = [pet.forward(70) for pet in pets]
    loop.run_until_complete(asyncio.wait(tasks)) 

    for pet in pets:
        pet.speed(speed=1)

    prompt = TurtlePrompt(version=version)
    loop.run_until_complete(prompt.run())
