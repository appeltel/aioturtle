# aioturtle

Extension of the python standard library turtle module
to move turtles asynchronously using the asyncio
module and the new async/await syntax in python 3.5.

The purpose of this package is to provide a toy enviornment
to learn and play with the asyncio library and new 
python coroutine syntax. While this can be easily achieved by
creating coroutines that simply call `asyncio.sleep(...)` and
print messages to the screen, I find that being able to watch
animated turtles move about the screen is a more satisfying
way to learn asyncio using a toy model.

<table><tr>
<td>
<pre>
$ python -m aioturtle

TurtlePrompt version 0.0.0: Enter "help"
for help, "quit" to exit.

aioturtle&gt; victor circle -100

&lt;Task pending coro=&lt;circle() running
at /.../aioturtle/aioturtle.py:400&gt;&gt;

aioturtle&gt; guido circle -100

&lt;Task pending coro=&lt;circle() running
at /.../aioturtle/aioturtle.py:400&gt;&gt;

aioturtle&gt; █
</pre>
</td>
<td>
<img src="docs/images/snapshot.png" alt="Example aioturtle session" />
</td>
</tr></table>

## Introduction

## Disclaimer

This package essentially ignores the TCL/TK GUI event loop and treats
the TK Canvas object as something that updates and draws effectively
instantaneously. The "IO" delays from the moving turtles are created
artificially by `await asyncio.sleep(...)` statements within the
turtle movement coroutines, although canvas delays may contribute to
the actual wall clock times elapsed between moves.

All GUI functionality is disabled in the turtle classes provided in
this package. Turtles can be managed interactively by the
`TurtlePrompt` class or by user created command line interfaces.
