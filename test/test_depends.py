import asyncio

import pytest

from dagio import depends


@pytest.mark.asyncio
async def test_depends_single_dependency():
    """Test a simple two-element dag with a single dependency

    a -> b
    """

    task_run_order = []

    class TestDag:
        async def task_a(self):
            task_run_order.append("a")

        @depends("task_a")
        async def task_b(self):
            task_run_order.append("b")

    test_dag_object = TestDag()
    await test_dag_object.task_b()

    assert len(task_run_order) == 2
    assert task_run_order[0] == "a"
    assert task_run_order[1] == "b"


@pytest.mark.asyncio
async def test_depends_two_dependencies():
    r"""Test a simple two-element dag with a multiple dependencies

    A
    |
    B   C
     \ /|
      D |
     / \|
    E   F
     \ /
      G
    """

    task_start_order = []
    task_end_order = []

    class TestDag:
        async def task_a(self):
            task_start_order.append("a")
            await asyncio.sleep(0.1)
            task_end_order.append("a")

        @depends("task_a")
        async def task_b(self):
            task_start_order.append("b")
            await asyncio.sleep(0.1)
            task_end_order.append("b")

        async def task_c(self):
            task_start_order.append("c")
            await asyncio.sleep(0.3)
            task_end_order.append("c")

        @depends("task_b", "task_c")
        async def task_d(self):
            task_start_order.append("d")
            await asyncio.sleep(0.1)
            task_end_order.append("d")

        @depends("task_d")
        async def task_e(self):
            task_start_order.append("e")
            await asyncio.sleep(0.1)
            task_end_order.append("e")

        @depends("task_c", "task_d")
        async def task_f(self):
            task_start_order.append("f")
            await asyncio.sleep(0.2)
            task_end_order.append("f")

        @depends("task_e", "task_f")
        async def task_g(self):
            task_start_order.append("g")
            await asyncio.sleep(0.2)
            task_end_order.append("g")

    test_dag_object = TestDag()
    await test_dag_object.task_g()

    assert len(task_start_order) == 7
    assert "a" in task_start_order[:2]
    assert "c" in task_start_order[:2]
    assert task_start_order[2] == "b"
    assert task_start_order[3] == "d"
    assert "e" in task_start_order[4:6]
    assert "f" in task_start_order[4:6]
    assert task_start_order[6] == "g"

    assert len(task_end_order) == 7
    assert task_end_order[0] == "a"
    assert task_end_order[1] == "b"
    assert task_end_order[2] == "c"
    assert task_end_order[3] == "d"
    assert task_end_order[4] == "e"
    assert task_end_order[5] == "f"
    assert task_end_order[6] == "g"
