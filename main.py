import asyncio
import argparse
import sys
import logging
from enum import Enum

from aiopath import AsyncPath
from aioshutil import copyfile


class Level(Enum):
    """Constants for messages levels"""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


def argument_Parser() -> tuple[str]:
    """
    Parse arguments and return folders path
    """
    parser = argparse.ArgumentParser(
        prog="homework",
    )
    parser.add_argument("source", help="Source folder", type=str)
    parser.add_argument("destination", help="Destination folder", type=str)
    try:
        args = parser.parse_args()
    except Exception as e:
        logger(f"Missing requirements arguments. {e}", Level.ERROR)
        sys.exit(1)
    return args.source, args.destination


async def read_folder(source: AsyncPath, dest: AsyncPath):
    """
    Read folder in asynchronous
    """
    try:
        async for file in source.iterdir():
            if await file.is_dir():
                await read_folder(file, dest)
            else:
                await copy_file(file, dest)

    except Exception as e:
        logger(f"Error reading folder {source}: {e}", Level.ERROR)


async def copy_file(file: AsyncPath, dest: AsyncPath):
    try:
        ext = file.suffix[1:] if file.suffix else "temp_folder"
        folder_path = dest / ext
        await folder_path.mkdir(exist_ok=True, parents=True)
        await copyfile(file, folder_path / file.name)
        logger(f"Copied {file.name} successfully", Level.INFO)
    except:
        logger(f"Error during copying file {file.name}", Level.ERROR)


def logger(message, level="") -> None:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        handlers=[logging.FileHandler("program.log"), logging.StreamHandler()],
    )
    match level:
        case Level.ERROR:
            logging.error(message)
        case Level.WARNING:
            logging.warning(message)
        case _:
            logging.info(message)


async def main():
    """
    Main function
    """
    logger("Operation start", Level.INFO)
    paths = argument_Parser()
    source_folder = AsyncPath(paths[0])
    destination_folder = AsyncPath(paths[1])

    if not await source_folder.exists():
        logger("Source path not exist", Level.ERROR)
        return
    if not await destination_folder.exists():
        logger(
            "Destination path not exist. File copies to dist folder in source folder",
            Level.WARNING,
        )
        destination_folder = AsyncPath(f"{paths[0]}/dist")

    await read_folder(source_folder, destination_folder)
    logger("Operation done", Level.INFO)


if __name__ == "__main__":
    asyncio.run(main())
