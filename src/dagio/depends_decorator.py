import asyncio


def depends(*dependencies):
    def outer_wrapped_fn(fn):
        async def inner_wrapped_fn(self):

            # Set up task list if this is the top level node
            top_level_fn = False
            if getattr(self, "__task_list_lock", None) is None:
                self.__task_list_lock = asyncio.Lock()
                self.__task_list = dict()
                top_level_fn = True

            # Start dependencies which have not already been started
            async with self.__task_list_lock:
                for dependency in dependencies:
                    if dependency not in self.__task_list:
                        self.__task_list[dependency] = asyncio.create_task(
                            getattr(self, dependency)()
                        )

            # Wait for dependencies to finish
            for dependency in dependencies:
                await self.__task_list[dependency]

            # Run this function
            await fn(self)

            # Clean up
            if top_level_fn:
                delattr(self, "__task_list_lock")
                delattr(self, "__task_list")

        return inner_wrapped_fn

    return outer_wrapped_fn
