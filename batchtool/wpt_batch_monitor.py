__author__ = 'h5m9n3v5v5t1u4f6@igeg.slack.com (Perfomance)'

import argparse
import os

import wpt_batch_lib

def run_monitor(args):
    while True:
        

def main():
    parser = argparse.ArgumentParser(description='')

    # Environment settings
    parser.add_argument('-s', '--server', action='store',
                           default='http://www.webpagetest.org/',
                           help='the wpt server URL')
    parser.add_argument('-f', '--outputdir', action='store',
                           default='./result', help='output directory')
    parser.add_argument('-T', '--testidsdir', action='store',
                           default='./test_ids', help='test ids directory')

    run_monitor(parser.parse_args())


if __name__ == '__main__':
  main()