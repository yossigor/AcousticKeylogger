import argparse
import asyncio
from AcousticKeylogger import AcousticKeylogger

parser = argparse.ArgumentParser(description='write model to disk')
parser.add_argument('--training_folder',required=True)
parser.add_argument('--output',required=True)

args = parser.parse_args()


async def main():
    acoustic_keylogger = AcousticKeylogger()
    await acoustic_keylogger.write_model_to_disk(args.training_folder,args.output)

    

asyncio.run(main())


