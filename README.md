Scout
=====

Introduction
------------
**Scout** fetches results from `Jenkins <http://jenkins-ci.org/>`_ runs which can be used to generate reports.

Examples
--------
Assuming you have a valid account for an existing `Jenkins <http://jenkins-ci.org/>`_ server, fetch the results of a plan run:

         python scout.py -u <username> -p <password> -s <url> -p <plan name>
         {'status': u'UNSTABLE', 'skipped': 46, 'url': u'http://<server>/<plan-name>/263/', 'failed': 34, 'passed': 255, 'date': u'2013-04-30', 'total': 335}

One can also pass a configuration file as an argument:

        python scout.py -c <filename> -p <plan name>

The configuration file has the following format:

        [user]
        username=hudson_user
        password=hudson_user_password

        [server]
        url=hudson_url/hudson/job

Installation
------------

Simply clone the repository to your system:

       git clone git://github.com/omaciel/scout.git

Author
------

This software is developed by
`Og Maciel <http://ogmaciel.tumblr.com>`_.