__author__ = 'h5m9n3v5v5t1u4f6@igeg.slack.com (Perfomance)'

import argparse
import os
import logging
from time import sleep

import wpt_batch_lib
    
def get_server_url(filepath):
    file = open(filepath, 'r')
    server_url = file.read().strip()
    file.close()
    return server_url

def run_monitor(options):
    if not os.path.isdir(options.outputdir):
        os.mkdir(options.outputdir)

    while True:
        for test_id in os.listdir(options.testidsdir):
           file_path = os.path.join(options.testidsdir, test_id) 
           server_url = get_server_url(file_path)
           test_status = wpt_batch_lib.CheckStatus(test_id, server_url)
            
           if int(test_status) >= 200:
               os.remove(file_path)
               if test_status == '200':
                   json_result = wpt_batch_lib.GetJSONResult(test_id, server_url)
                   wpt_batch_lib.CreateFile(os.path.join(options.outputdir, test_id + '.json'), json_result)
               else:
                   logging.error('Test failed: test_id[%s] test_status[%s]', test_id, test_status)    

        sleep(10)
        
def main():
    parser = argparse.ArgumentParser(description='')

    # Environment settings
    parser.add_argument('-f', '--outputdir', action='store',
                           default='./result', help='output directory')
    parser.add_argument('-T', '--testidsdir', action='store',
                           default='./test_ids', help='test ids directory')

    run_monitor(parser.parse_args())


if __name__ == '__main__':
  main()