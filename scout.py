#!/usr/bin/env python

import os
import sys
import optparse
import ConfigParser

try:
    import requests
except ImportError, e:
    print "Please install Python Requests and try again: https://pypi.python.org/pypi/requests/"
    sys.exit(-1)

CONFIG_SAMPLE = """
[user]
username=hudson_user
password=hudson_user_password

[server]
url=hudson_url/hudson/job
"""
def _parse_config(cfile):
    """
    Parses configuration file and returns auth and server information.
    """
    user_cfg = ConfigParser.SafeConfigParser()
    try:
        user_cfg.read(os.path.abspath(os.path.expanduser(cfile)))
    except Exception, e:
        print "Failed to parse configuration file: %s" % str(e)
        sys.exit(-1)

    try:
        username = user_cfg.get('user', 'username')
        password = user_cfg.get('user', 'password')
        server = user_cfg.get('server', 'url')
    except NoOptionError, e:
        print "The configuration file doesn't seem to be properly formatted."
        print "Please make sure to have a configuration file as follows:"
        print CONFIG_SAMPLE
        sys.exit(-1)

    return (username, password, server)
    
    
def fetch_build_data(username, password, server, plan):
    """
    Fetches and returns a dictionary representing certain results from the latest build of a plan.
    """
    
    errors = plan_date = plan_url = plan_status = plan_record = None
    skipped = failed = passed = total = 0
    
    url = "%s/%s/api/json" % (server, plan)
    auth = (username, password)

    plan_r = requests.get(url, auth=auth)

    if plan_r.status_code == 200:
        plan_data = plan_r.json()
        last_build = plan_data['lastCompletedBuild']

        if last_build is None:
            errors = "No builds found for plan %s." % plan
        else:
            url = "%sapi/json" % last_build['url']
            build_r = requests.get(url, auth=auth)
            
            if build_r.status_code == 200:
                try:
                    build_data = build_r.json()
                    results = build_data['actions']

                    # Extract results from build run
                    counts = [x for x in results if type(x) == dict and 'skipCount' in x.keys()]
                    if counts:
                        skipped = counts[0]['skipCount']
                        failed = counts[0]['failCount']
                        total = counts[0]['totalCount']
                        passed = total - skipped - failed
                        plan_date = build_data['id'].split('_')[0]
                        plan_url = build_data['url']
                        plan_status = build_data['result']
                    else:
                        errors = "Could not find results for latest build."
                    
                except Exception, e:
                    errors = "Could not fetch results for latest build: %s" % str(e)
                    pass

    else:
        errors = "Could not fetch report for %s" % plan

    plan_record = {
        'name' : plan,
        'skipped' : skipped,
        'failed' : failed,
        'total' : total,
        'passed' : passed,
        'date' : plan_date,
        'url' : plan_url,
        'status' : plan_status,
        'errors' : errors,
        }

    return plan_record


if __name__ == "__main__":

    description = "Fetches results from Hudson runs."
    usage = "Usage: %prog [--username <username> --password <password> --server <server_url>] [--config <file>] --plan <plan_name>"
    epilog = "Constructive comments and feedback can be sent to Og Maciel <omaciel at ogmaciel dot com>."
    version = "%prog version 0.1"

    p = optparse.OptionParser(usage=usage, description=description, epilog=epilog, version=version)
    p.add_option('-u', '--username', type=str, dest='username', help='Valid Hudson username')
    p.add_option('-p', '--password', type=str, dest='password', help='Valid Hudson password')
    p.add_option('-s', '--server', type=str, dest='server', help='URL to a Hudson server')
    p.add_option('-c', '--config', type=str, dest='config', help='An optional configuration file')
    p.add_option('--plan', type=str, dest='plan', help='The Hudson plan name')

    options, arguments = p.parse_args()

    if options.config:

        if not options.plan:
            print "Please provide a valid plan name."
            sys.exit(-1)

        options.username, options.password, options.server = _parse_config(options.config)
        
    else:
            
        if not options.username or not options.password or not options.plan:
            p.print_help()
            sys.exit(-1)

    result = fetch_build_data(options.username, options.password, options.server, options.plan)
    print result
