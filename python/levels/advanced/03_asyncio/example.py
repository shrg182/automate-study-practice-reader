import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay); return name
async def main():
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch(str(i), .01)) for i in range(3)]
    print([task.result() for task in tasks])
if __name__ == "__main__": asyncio.run(main())
