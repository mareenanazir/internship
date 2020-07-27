import argparse
import os


def validate_file_path(file_path):
    if os.path.exists(file_path):
        return file_path
    else:
        raise FileNotFoundError


class ArgumentParser:
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('file_path', type=validate_file_path)
        parser.add_argument('-a',
                            help='For a given country, display the ratio of recovered patients over total cases.',
                            type=str)
        parser.add_argument('-b', help='For a given safety measure, display the average death rate around the globe',
                            type=str)
        parser.add_argument('-c', help='Display the efficiencies of 5 mostly adopted safety measures with'
                                       ' respect to the origin.', action='store_true')
        parser.add_argument('-d', help=' Plot a graph for the efficiencies of 5 mostly adopted safety measures with'
                                       ' respect to the origin.', action='store_true')

        args = parser.parse_args()

        if not (args.a or args.b or args.c):
            parser.error('No arguments provided.')

        return args
