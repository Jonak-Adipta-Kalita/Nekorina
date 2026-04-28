import asyncio

from nekosbest import Client


async def main() -> None:
    client = Client()
    try:
        single = await client.get_image("hug")
        print(single)
        multiple = await client.get_image("hug", 3)
        print(multiple)
    finally:
        await client.close()


asyncio.run(main())
