import asyncio
import argparse
import sys
from aiopath import AsyncPath
from aioshutil import copyfile


def ArgumentParser():
    """
    Parse arguments and return folders path
    """
    parser = argparse.ArgumentParser(
        prog="homework",
    )
    parser.add_argument("source_folder")
    parser.add_argument("destination_folder")
    try:
        args = vars(parser.parse_args())
        return args["source_folder"], args["destination_folder"]
    except SystemExit:
        print("Missing required arguments or invalid input")
        sys.exit()


# async def read_folder(path):
#     try:
#         for file in await path:
#             try:
#                 pass
#             except:
#                 pass
#     except:
#         pass


async def copy_file():
    pass


def logger():
    pass


async def main():
    paths = ArgumentParser()
    print(paths)


if __name__ == "__main__":
    asyncio.run(main())
