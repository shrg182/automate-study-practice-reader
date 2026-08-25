import asyncio

async def normalize(queue, output):
    while (item := await queue.get()) is not None:
        output.append(str(item).strip()); queue.task_done()
async def main():
    queue = asyncio.Queue(maxsize=2); output = []
    worker = asyncio.create_task(normalize(queue, output))
    for item in [" notes ", " highlights "]: await queue.put(item)
    await queue.put(None); await worker; print(output)
if __name__ == "__main__": asyncio.run(main())
