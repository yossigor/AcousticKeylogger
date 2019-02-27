import argparse
import asyncio
from AcousticKeylogger import AcousticKeylogger

parser = argparse.ArgumentParser(description='classification attack')
parser.add_argument('--target_file',required=True)
parser.add_argument('--model_file',required=True)

args = parser.parse_args()


async def main():
    acoustic_keylogger = AcousticKeylogger()
    await acoustic_keylogger.classification_attack(args.target_file,args.model_file)

    

asyncio.run(main())


