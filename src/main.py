import argparse
import logging

from src.analysis import distribution

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="CLI to run statistics on lifters. All generated graphs are placed under the graphs directory.")
parser.add_argument('-d', '--distribution', action='store_true', help='Graphs distributions of lifters. Graphs are placed under the graphs/distributions directory')

if __name__ == "__main__":
    args = parser.parse_args()
    logger.debug("args: %s", args)
    if args.distribution:
        logger.info("Going into distribution main()")
        distribution.main()
