"""door
Usage:
  my2h_transform.py
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

    print('Hello World')


if __name__ == '__main__':
    main()
