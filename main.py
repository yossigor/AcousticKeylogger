import asyncio
from AcousticKeylogger import AcousticKeylogger 

async def main():
    keyloggers = []
    for i in range(5):
         keyloggers.append(AcousticKeylogger())
    for i in range(len(keyloggers)):
        asyncio.create_task(keyloggers[i].hello())
    

asyncio.run(main())
