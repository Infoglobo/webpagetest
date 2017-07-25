<h1>BatchTool</h1>

This is an unofficial fork based in official WebPagetest repository [WebPagetest](https://github.com/WPO-Foundation/webpagetest).

Refer to the [original documentation](https://sites.google.com/a/webpagetest.org/docs/advanced-features/webpagetest-batch-processing-command-line-tool) to run the script properly.

<h1>Motivations</h1>

The original code had some drawbacks - it waits all the urls being tested to end before you can run it again and the .txt file is the only input available to insert new urls.

With these points in mind, we made some modfications in the original code to solve them.

<h1>New Features</h1>

We separated the wpt_batch's responsabilities in two:

<h2>wpt_batch</h2>

Send the url to WebPagetest's API, receive the **test id** related to the url and save it as a filename in **test_ids_dir** directory.

<h2>wpt_batch_monitor</h2>

Listen **test_ids_dir** directory and for each file inside it will request WebPagetest's API to see the status code:
* 1XX - do nothing, will consult it again in next turn
* 2XX - generate a .json file inside **result** directory and remove the file from **test_id_dir**
* 4XX - as it is an error, only remove the file from **test_id_dir**

To allow this behaviour, some modifications had been made, adding new command line options:

<h2>Provide one single URL instead of a .txt file (-U, --url)</h2>

It's an alternative to **--urlfile** option, it will only add new urls to be tested.

<pre>
<code>$ python wpt_batch.py -U http://your-url.com</code>
<code>$ python wpt_batch.py --url http://your-url.com</code>
</pre>

<h2>Set the test to run in an mobile environment (-M, --mobile)</h2>
Build a profile to simulate an mobile 3G connection.
<pre>
<code>$ python wpt_batch.py -U http://your-url.com -M</code>
<code>$ python wpt_batch.py --url http://your-url.com --mobile</code>
</pre>

<h1>Usage</h1>

This is a basic example on how to setup properly the script to run. You can freely adapt it to suit your needs.

1. Run the monitor script to monitor all urls sent to be tested

<pre>
<code>$ python wpt_batch_monitor.py</code>
</pre>

2. Using **crontab**, add lines to call the script, passing the -U arg to inform which url will be tested. Here we will put 3 different urls to be tested, every day, at 2am

<pre>
<code>0 2 * * * /usr/bin/python wpt_batch.py -U http://your-url-1.com</code>
<code>0 2 * * * /usr/bin/python wpt_batch.py -U http://your-url-2.com</code>
<code>0 2 * * * /usr/bin/python wpt_batch.py -U http://your-url-3.com</code>
</pre>