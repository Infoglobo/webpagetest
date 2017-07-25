<h1>BatchTool</h1>

This is an unofficial fork based in official WebPagetest repository [WebPagetest](https://github.com/WPO-Foundation/webpagetest).

Refer to the [original documentation](https://sites.google.com/a/webpagetest.org/docs/advanced-features/webpagetest-batch-processing-command-line-tool) to run the script properly.

<h1>Motivation</h1>

The original code waits in a loop until all the tests submitted are finished. That could result in an infinite loop if any of the tests never completes.

We also wanted to add more command line options and have the test results saved in json format.

<h1>New Behaviour</h1>

We splitted the original wp_batch.py in two scripts with different responsibilities:

<h2>wpt_batch</h2>

Sends a set of urls to a webpagetest server, receives the **test id** associated with each url and saves them as files in  a **test_ids_dir** directory (option --testidsdir), each file is named with the testid received and the URL of webpagetest server used is saved as content of each testid file.

<h2>wpt_batch_monitor</h2>

Listen **test_ids_dir** directory and for each file inside it will request WebPagetest's API to see the status code:
* 1XX - do nothing, will consult it again in next turn
* 2XX - generate a .json file inside **result** directory and remove the file from **test_id_dir**
* 4XX - as it is an error, only remove the file from **test_id_dir**

<h1>New command line options</h1>

<h2>wpt_batch</h2>

* <h3>-f | --outputdir [DIRECTORY]</h3>

Path to a directory... (TODO: remove this option from wpt_batch.py)

* <h3>-T | --testidsdir [DIRECTORY]</h3>

Path to a directory where the testid files are stored. If omitted, defaults to "./testid". 

* <h3>-U | --url [URL_TO_BE_TESTED]</h3>

Sets an URL to be tested

This option is an alternative to **--urlfile**. Both can be used simultaneously, in that case all URLs from the file and from the command line are submitted together.

<pre>
<code>$ python wpt_batch.py -U http://your-url.com</code>
<code>$ python wpt_batch.py --url http://your-url.com</code>
</pre>

* <h3>-M | --mobile</h3> 

Enables the "mobile" test parameter. From webpagetest documentation, what is does is "Set to 1 to have Chrome emulate a mobile browser (screen resolution, UA string, fixed viewport)". See the [documentation](https://sites.google.com/a/webpagetest.org/docs/advanced-features/webpagetest-restful-apis)

<pre>
<code>$ python wpt_batch.py --mobile --url http://your-url.com  </code>
</pre>

<h2>wpt_batch_monitor</h2>

* <h3>-T | --testidsdir [DIRECTORY]</h3>

Path to the directory where wp_batch stores the testid files. The default value is **./testid**.

The script wpt_batch_monitor stays in a loop waiting for new files to appear. Whenever it sees a new **test_id** file, it will request the WePpagetest server to get the test result. 

The URL of the WePpagetest server is extracted from the **test_id** file. 

If a given test completes, the **test_id** file is removed from the **test_ids_dir** and the result is saved as a json file in **--outputdir**

* <h3>-f | --outputdir [DIRECTORY]</h3>
Path to a directory to save the results of the tests completed succesfully. If omitted, defaults to **./result**

<h1>Usage</h1>

This is a basic example on how to setup properly the script to run. You can freely adapt it to suit your needs.

1. Run the monitor script in background to monitor all urls sent to be tested

<pre>
<code>$ python wpt_batch_monitor.py --testidsdir ./test_ids --outputdir ./result &</code>
</pre>

2. Using **crontab**, add lines to call the script, passing the -U arg to inform which url will be tested. Here we will put 3 different urls to be tested, every day, at 2am

<pre>
<code>0 2 * * * /usr/bin/python wpt_batch.py -U http://your-url-1.com</code>
<code>0 2 * * * /usr/bin/python wpt_batch.py -U http://your-url-2.com</code>
<code>0 2 * * * /usr/bin/python wpt_batch.py -U http://your-url-3.com</code>
</pre>
