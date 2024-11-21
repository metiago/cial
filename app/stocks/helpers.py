import logging

import aiohttp
from werkzeug.exceptions import NotFound


async def fetch_data(url, headers, response_type):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 401 or response.status == 403:
                error_message = f"HTTP error occurred: {response.status} - {await response.text()}"
                logging.error(error_message)
                raise aiohttp.ClientResponseError(
                    status=response.status,
                    message=error_message,
                )
            if response.status == 404:
                logging.warning(f"Resource not found (404) for URL: {url}")
                raise NotFound(f"Resource not found (404) for URL: {url}")

            try:
                if response_type == 'json':
                    return await response.json()
                elif response_type == 'text':
                    return await response.text()
                else:
                    raise ValueError("Invalid response type specified. Use 'json' or 'text'.")
            except Exception as e:
                logging.exception(f"Failed to parse response for URL: {url}")
                raise
