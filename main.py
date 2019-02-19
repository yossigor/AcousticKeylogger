import asyncio
from AcousticKeylogger import AcousticKeylogger 

async def main():
    acoustic_keylogger = AcousticKeylogger()
    await acoustic_keylogger.hello()

asyncio.run(main())
