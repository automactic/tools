import argparse

from .joiner import GoProFileJoiner

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input path of the dir containing gopro mp4 files.')
    parser.add_argument('output', type=str, help='Output path of the dir to write joined mp4 files.')
    args = parser.parse_args()

    joiner = GoProFileJoiner(args.input, args.output)
    joiner.process()
