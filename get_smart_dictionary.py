import argparse
import asyncio
from AcousticKeylogger import AcousticKeylogger

parser = argparse.ArgumentParser(description='classification attack')
parser.add_argument('--passwords_recordings_folder',required=True)
parser.add_argument('--dictionary_output',required=True)
parser.add_argument('--model_file',required=True)

args = parser.parse_args()


async def main():
    acoustic_keylogger = AcousticKeylogger()
    await acoustic_keylogger.get_smart_dictionary(args.passwords_recordings_folder
    ,args.dictionary_output,args.model_file)

    

asyncio.run(main())


