import asyncio
from AcousticKeylogger import AcousticKeylogger 

async def main():
    for i in range(1):
        acoustic_keylogger = AcousticKeylogger()
        await acoustic_keylogger.hello()

    

asyncio.run(main())
