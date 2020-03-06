"""My2h JOP Transform Utility
Usage:
  my2h_transform.py blocks <myjop_blk_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""


from docopt import docopt


def main():
    '''Entry point'''
    args = docopt(__doc__, version='0.0.1')  # pylint: disable=unused-variable

    if args['blocks']:
        with open(args['<myjop_blk_file>'], encoding='cp1250') as blk_file:
            lines = blk_file.readlines()

        print_next = True
        for line in lines:
            if print_next:
                print(line)
                print_next = False
            if line == '\n':
                print_next = True


if __name__ == '__main__':
    main()
