import aiohttp
from aiohttp.resolver import AsyncResolver


async def http_get(url: str) -> tuple[bool, str]:
    """
    HTTP requests for GET method.

    Args:
        url (str): URL that will be fetched.

    Returns:
        tuple[bool, str]: First item is Error (bool) and second item is Data as string (str).
    """
    resolver = AsyncResolver(nameservers=["1.1.1.1", "1.0.0.1"])
    conn = aiohttp.TCPConnector(resolver=resolver)
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url) as response:
            if not response.ok or response.status != 200:
                return (
                    True,
                    f"Sorry, cannot processing request from URL {url} with status {response.status} and message below:\n\n{await response.text()}",
                )
            return (False, await response.text())
