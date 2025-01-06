import aiohttp


async def http_get(url: str) -> tuple[bool, str]:
    """
    HTTP requests for GET method.

    Args:
        url (str): URL that will be fetched.

    Returns:
        tuple[bool, str]: First item is Error (bool) and second item is Data as string (str).
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.ok or response.status != 200:
                return (
                    True,
                    f"Mohon maaf, tidak dapat mengambil data dari URL {url} karena status {response.status} dengan pesan \n```bash\n{await response.text()}```",
                )
            return (False, await response.text())
