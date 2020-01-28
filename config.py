#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# This file contains:
# the Webex Auth, Webex URL and Space name
# the Webhook username and password

WEBEX_TEAMS_URL = 'https://api.ciscospark.com/v1'
WEBEX_TEAMS_AUTH = 'Bearer ' + ''
WEBEX_TEAMS_ROOM = ''
WEBEX_BOT_ID = ''

WEBHOOK_URL = 'https://ip_address:5000/webhook'
WEBHOOK_USERNAME = ''
WEBHOOK_PASSWORD = ''
WEBHOOK_AUTH = 'Basic '

DNAC_IP = ''
DNAC_URL = 'https://' + DNAC_IP
DNAC_USER = ''
DNAC_PASS = ''
DNAC_ISSUE = DNAC_URL + '/dna/assurance/issueDetails?issueId='

WEBEX_BOT_TOKEN = ''

PAGERDUTY_INTEGRATION_KEY = ''
PAGERDUTY_EVENTS_URL = 'https://events.pagerduty.com/v2/enqueue'

JIRA_API_KEY = ''
JIRA_URL = 'https://username.atlassian.net'
JIRA_EMAIL = ''
JIRA_PROJECT = ''
JIRA_ISSUES = 'https://username.atlassian.net/projects/..../queues/custom/1/'


IOS_XE_HOST = ''
IOS_XE_USER = ''
IOS_XE_PASS = ''

DNAC_DEVICE_CONFIG = 'dnac_device_config.txt'
DEVICE_RUNNING_CONFIG = 'device_running_config.txt'

