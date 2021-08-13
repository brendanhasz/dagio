# dagio: Asynchronous I/O - with DAGs!

[![Version Badge](https://img.shields.io/pypi/v/dagio)](https://pypi.org/project/dagio/)
[![Test Status](https://github.com/brendanhasz/dagio/workflows/tests/badge.svg)](https://github.com/brendanhasz/probflow/actions?query=branch%3Amaster)


`dagio` is an embarassingly simple Python package for running directed acyclic
graphs of asynchronous I/O operations.  It is built using and to be used with
Python's built-in [`asyncio`](https://docs.python.org/3/library/asyncio.html)
module, and provides a _veeeery_ thin layer of functionality on top of it.
:sweat_smile:

* Git repository: https://github.com/brendanhasz/dagio
* Bug reports: https://github.com/brendanhasz/dagio/issues


## Getting Started

Suppose you have a set of potentially long-running I/O tasks (e.g. hit a web
service, query a database, read a large file from disk, etc), where some of the
tasks depend on other tasks having finished.  That is, you've got a directed
acyclic graph (DAG) of tasks, where non-interdependent tasks can be run
asynchronously.

For example, if you've got a task `G` which depends on `E` and `F`, but `E`
depends on `D`, and `F` depends on both `C` and `D`, etc:

```
A
|
B   C
 \ /|
  D |
 / \|
E   F
 \ /
  G
```

Coding that up using raw `asyncio` might look something like this:

```python
import asyncio


class MyDag:

    async def task_a(self):
        # does task a stuff...

    async def task_b(self):
        # does task b stuff...

    async def task_c(self):
        # does task c stuff...

    async def task_d(self):
        # does task d stuff...

    async def task_e(self):
        # does task e stuff...

    async def task_f(self):
        # does task f stuff...

    async def task_g(self):
        # does task g stuff...


async def run():

    obj = MyDag() 

    task_a = asyncio.create_task(obj.task_a())
    task_c = asyncio.create_task(obj.task_c())

    await task_a

    await obj.task_b()

    await task_c

    await obj.task_d()

    task_e = asyncio.create_task(obj.task_e())
    task_f = asyncio.create_task(obj.task_f())

    await task_e
    await task_f

    await obj.task_g()


asyncio.run(run())
```

Which is... _fine_, I guess :roll_eyes:  But, you have to be careful about what
task you start before what other task, and which tasks can safely be run
asynchronously vs those which can't. And then you have to type out all that
logic and ordering manually!  With the confusing `asyncio` API!  So: a lot of
thought has to go into it, especially for complex DAGs.

And thinking is hard!  Less thinking! :fist:

With `dagio`, you just use the `depends` decorator to specify what methods any
other given method depends on, and it'll figure everything out for you, and run
them in the correct order, asynchronously where possible:

```python
import asyncio
from dagio import depends


class MyDag:

    async def task_a(self):
        # does task a stuff...

    @depends("task_a")
    async def task_b(self):
        # does task b stuff...

    async def task_c(self):
        # does task c stuff...

    @depends("task_b", "task_c")
    async def task_d(self):
        # does task d stuff...

    @depends("task_d")
    async def task_e(self):
        # does task e stuff...

    @depends("task_c", "task_d")
    async def task_f(self):
        # does task f stuff...

    @depends("task_e", "task_f")
    async def task_g(self):
        # does task g stuff...


async def run():
    obj = MyDag() 
    await obj.task_g()


asyncio.run(run())
```

Note that:

1) Each task in your DAG has to be a method of the same class
2) Task methods must be `async` methods
3) Calling a task method decorated with `depends` runs that task _and all its dependencies_
4) Task methods should not take arguments nor return values.  You can handle
   inter-task communication using object attributes (e.g. `self._task_a_output = ...`).
   If you need a lock, you can set up an [`asyncio.Lock`](https://docs.python.org/3/library/asyncio-sync.html#lock)
   in your class's `__init__`.

That's it.  That's all this package does.


## Installation

```
pip install dagio
```


## Support

Post bug reports, feature requests, and tutorial requests in [GitHub
issues](https://github.com/brendanhasz/dagio).


## Contributing

[Pull requests](https://github.com/brendanhasz/dagio/pulls) are totally
welcome! Any contribution would be appreciated, from things as minor as fixing
typos to things as major as adding new functionality. :smile:


## Why the name, dagio?

It's for making DAGs of IO operations. DAG IO. Technically it's _asynchronous_
DAG-based I/O, and the name `adagio` would have been siiiick, but it was
[already taken](https://pypi.org/project/adagio/)! :sob:
