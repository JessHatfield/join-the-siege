import os

import aiohttp
import asyncio
import time

# URL and file path
url = "https://document-classification-service-260885586204.europe-west2.run.app/classify_file"
file_path = f"../files/drivers_license_1.jpg"


async def send_post_request(session):
    start_time = time.time()
    async with session.post(url, data={'file': open(file_path, 'rb')}) as response:
        data = await response.text()  # Read the response (if needed)
        print(data)
        return time.time() - start_time  # Return the elapsed time


async def main(num_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [send_post_request(session) for _ in range(num_requests)]
        response_times = await asyncio.gather(*tasks)
        average_time = sum(response_times) / num_requests
        print(f"Average Response Time: {average_time:.3f} seconds")


if __name__ == "__main__":
    start_time = time.time()
    num_requests = 100  # Number of requests to send
    asyncio.run(main(num_requests))
    print(f'Script ran in {time.time() - start_time}')
