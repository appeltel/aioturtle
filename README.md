# aioturtle

Extension of the python standard library turtle module
to move turtles asynchronously using the asyncio
module and the new async/await syntax in python 3.5.

<table><tr>
<td>
![Example aioturtle session](docs/images/snapshot.png)
</td>
<td>
```
$ python -m aioturtle
TurtlePrompt version 0.0.0: Enter "help" for help, "quit" to exit.
aioturtle> victor circle -100
<Task pending coro=<circle() running at /.../aioturtle/aioturtle.py:400>>
aioturtle> guido circle -100
<Task pending coro=<circle() running at /.../aioturtle/aioturtle.py:400>>
aioturtle>
```
</td>
</tr></table>
