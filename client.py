import aiohttp
import asyncio

url = 'https://4c1f-34-125-82-134.ngrok-free.app'


async def get_average_temperature():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(f"{url}/average") as response:
                    if response.status == 200:
                        data = await response.json()
                        average_temp = data.get("average_temperature")
                        print(f"Average Temperature: {average_temp}")
                    else:
                        print(f"Failed to fetch average temperature: {response.status}")
            except Exception as e:
                print(f"Error fetching average temperature: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(get_average_temperature())