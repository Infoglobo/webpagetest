#!/usr/bin/python2.6
#
# Copyright 2011 Google Inc. All Rights Reserved.

"""A library to support batch processing of WebPageTest tests.

This module provides a set of APIs for batch processing of
WebPageTest tests. A complete test cycle typically consists of
test submission, checking test status, test result download, etc.

A sample usage of this library can be found in wpt_batch.py.
"""

__author__ = 'zhaoq@google.com (Qi Zhao)'

import re
import logging
import urllib
import os
from xml.dom import minidom

def CreateFile(filepath, content=''):
  file = open(filepath, "w")
  file.write(content)
  file.close() 

def __LoadEntity(url, urlopen=urllib.urlopen):
  """A helper function to load an entity such as an URL.

  Args:
    url: the URL to load
    urlopen: the callable to be used to load the url

  Returns:
    The response message
  """
  response = urlopen(url)
  return response


def ImportUrls(url_filename):
  """Load the URLS in the file into memory.

  Args:
    url_filename: the file name of the list of URLs

  Returns:
    The list of URLS
  """
  url_list = []
  for line in open(url_filename, 'rb'):
    # Remove newline and trailing whitespaces
    url = line.rstrip(' \r\n')
    if url:
      url_list.append(url)
  return url_list

def GetXmlNodeValue(xml, node_name):
    dom = minidom.parseString(xml)
    nodes = dom.getElementsByTagName(node_name)
    return nodes[0].firstChild.wholeText

def SubmitBatch(url_list, test_params, testidsdir, server_url='http://www.webpagetest.org/',
                urlopen=urllib.urlopen):
  """Submit the tests to WebPageTest server.

  Args:
    url_list: the list of interested URLs
    test_params: the user-configured test parameters
    server_url: the URL of the WebPageTest server
    urlopen: the callable to be used to load the request

  Returns:
    A dictionary which maps a WPT test id to its URL if submission
    is successful.
  """
  id_url_dict = {}
  for url in url_list:
    test_params['url'] = url
    request = server_url + 'runtest.php?%s' % urllib.urlencode(test_params)
    response = __LoadEntity(request, urlopen)
    return_code = response.getcode()
    if return_code == 200:
      response_xml = response.read()
      status = GetXmlNodeValue(response_xml, 'statusCode')
      if status == '200':
        test_id = GetXmlNodeValue(response_xml, 'testId')
        id_url_dict[test_id] = url
        CreateFile(os.path.join(testidsdir, test_id), server_url)
      else:
        error_message = GetXmlNodeValue(response_xml, 'statusText')
        logging.error('url[%s] status[%s] message[%s]', request, status, error_message)
  return id_url_dict

def CheckStatus(test_id, server_url, urlopen=urllib.urlopen):
  wpt_url = server_url + 'testStatus.php?f=xml&test=' + test_id
  response = __LoadEntity(wpt_url, urlopen)
  response_xml = response.read()
  if response.getcode() == 200:
      status_code = GetXmlNodeValue(response_xml, 'statusCode')
      return status_code
  else: 
      error_message = GetXmlNodeValue(response_xml, 'statusText')
      logging.error('CheckStatus failed: url[%s] status[%s] message[%s]', wpt_url, status, error_message)
      return None
  

def CheckBatchStatus(test_ids, server_url='http://www.webpagetest.org/', urlopen=urllib.urlopen):
  """Check the status of tests.

  Args:
    test_ids: the list of interested test ids
    server_url: the URL of the WebPageTest server
    urlopen: the callable to be used to load the request

  Returns:
    A dictionary where key is the test id and content is its status.
  """
  id_status_dict = {}
  for test_id in test_ids:
    status_code = CheckStatus(test_id, urlopen)
    if status_code:
      id_status_dict[test_id] = status_code
    
  return id_status_dict

def GetJSONResult(test_id, server_url='http://www.webpagetest.org/', urlopen=urllib.urlopen):
  wpt_url = server_url + 'jsonResult.php?test=' + test_id
  response = __LoadEntity(wpt_url, urlopen)
  if response.getcode() == 200:
    return response.read()
  return None

def GetXMLResult(test_ids, server_url='http://www.webpagetest.org/', urlopen=urllib.urlopen):
  """Obtain the test result in XML format.

  Args:
    test_ids: the list of interested test ids
    server_url: the URL of WebPageTest server
    urlopen: the callable to be used to load the request

  Returns:
    A dictionary where the key is test id and the value is a DOM object of the
    test result.
  """
  id_dom_dict = {}
  for test_id in test_ids:
    request = server_url + 'xmlResult/' + test_id + '/'
    response = __LoadEntity(request, urlopen)
    if response.getcode() == 200:
      dom = minidom.parseString(response.read())
      id_dom_dict[test_id] = dom
  return id_dom_dict
