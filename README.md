Scout
=====

Introduction
------------
**Scout** fetches results from [Jenkins] (http://jenkins-ci.org/) runs which can be used to generate reports.

Examples
--------
Assuming you have a valid account for an existing [Jenkins] (http://jenkins-ci.org/) server, fetch the results of a plan run:

```bash
$ python scout.py -u <username> -p <password> -s <url> --plan <plan name>
{'name': 'plan-name', 'errors': None, 'status': u'UNSTABLE', 'skipped': 46, 'url': u'http://<server>/<plan-name>/263/', 'failed': 34, 'passed': 255, 'date': u'2013-04-30', 'total': 335}
```

One can also pass a configuration file as an argument:

```bash
$ python scout.py -c <filename> --plan <plan name>
```

The configuration file has the following format:

```
[user]
username=jenkins_user
password=jenkins_user_password

[server]
url=jenkins_url/jenkins/job
```

You can also use **python** and use the data returned to create different outputs:

```python
from scout import *

data = fetch_build_data("username", "password", "http://my.jenkins.com/job", "project-cli")

print "|| || %(date)s || %(passed)s || %(skipped)s || %(failed)s || %(total)s || %(url)s || ||" % data

|| || 2013-05-03 || 257 || 46 || 32 || 335 || http://jenkins.rhq.lab.eng.bos.redhat.com:8080/jenkins/job/katello-gui/277/ || ||
```

Installation
------------

Simply clone the repository to your system:

```bash
$ git clone git://github.com/omaciel/scout.git
```

Author
------

This software is developed by
[Og Maciel] (http://ogmaciel.tumblr.com>).
