#! python3
import argparse


def prompt():
    parser = argparse.ArgumentParser(
        description="A simple serverless function transformer,\
        and a simple way to call function in other language.")

    parser.add_argument("filePath",
                        nargs='*', metavar="file_Pame", type=str,
                        help="The file containing function to be exposed.")

    args = parser.parse_args()

    if not args.filePath:
        print("No file path provided")
    print(args.filePath)
