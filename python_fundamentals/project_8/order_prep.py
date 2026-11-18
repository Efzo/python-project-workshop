import argparse
import asyncio
from time import perf_counter


ORDERS = [("A", 0.4), ("B", 0.2), ("C", 0.3)]


async def prepare(order, seconds, stations):
    async with stations:
        print(f"Preparing {order}")
        try:
            await asyncio.sleep(seconds)
        except asyncio.CancelledError:
            print(f"Cancelled {order}")
            raise
        print(f"Finished {order}")
        return order


async def run_orders(limit):
    stations = asyncio.Semaphore(limit)
    start = perf_counter()
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(prepare(order, seconds, stations))
            for order, seconds in ORDERS
        ]
    completed = ", ".join(task.result() for task in tasks)
    print(f"Completed: {completed} in {perf_counter() - start:.2f} s")


def main():
    parser = argparse.ArgumentParser(description="Simulate concurrent order prep.")
    parser.add_argument("--stations", type=int, default=2)
    args = parser.parse_args()
    if args.stations < 1:
        parser.error("--stations must be at least 1")
    asyncio.run(run_orders(args.stations))


if __name__ == "__main__":
    main()
