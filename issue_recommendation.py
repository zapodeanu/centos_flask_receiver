#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


Copyright (c) 2020 Cisco and/or its affiliates.

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
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"



import requests
import json
import time
import urllib3
import utils
import dnac_apis
import jira_apis
import dnac_apis
import difflib

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

from config import DNAC_URL, DNAC_PASS, DNAC_USER, DNAC_IP, DNAC_ISSUE
from config import DNAC_DEVICE_CONFIG, DEVICE_RUNNING_CONFIG

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data: data to pretty print
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def compare_configs(cfg1, cfg2):
    """
    This function, using the unified diff function, will compare two config files and identify the changes.
    '+' or '-' will be prepended in front of the lines with changes
    :param cfg1: old configuration file path and filename
    :param cfg2: new configuration file path and filename
    :return: text with the configuration lines that changed. The return will include the configuration for the sections
    that include the changes
    """

    # open the old and new configuration files
    f1 = open(cfg1, 'r')
    old_cfg = f1.readlines()
    f1.close()

    f2 = open(cfg2, 'r')
    new_cfg = f2.readlines()
    f2.close()

    # compare the two specified config files {cfg1} and {cfg2}
    d = difflib.unified_diff(old_cfg, new_cfg, n=9)

    # create a diff_list that will include all the lines that changed
    # create a diff_output string that will collect the generator output from the unified_diff function
    diff_list = []
    diff_output = ''

    for line in d:
        diff_output += line
        if line.find('Current configuration') == -1:
            if line.find('Last configuration change') == -1:
                if (line.find('+++') == -1) and (line.find('---') == -1):
                    if (line.find('-!') == -1) and (line.find('+!') == -1):
                        if line.startswith('+'):
                            diff_list.append('\n' + line)
                        elif line.startswith('-'):
                            diff_list.append('\n' + line)

    # process the diff_output to select only the sections between '!' characters for the sections that changed,
    # replace the empty '+' or '-' lines with space
    diff_output = diff_output.replace('+!', '!')
    diff_output = diff_output.replace('-!', '!')
    diff_output_list = diff_output.split('!')

    all_changes = []

    for changes in diff_list:
        for config_changes in diff_output_list:
            if changes in config_changes:
                if config_changes not in all_changes:
                    all_changes.append(config_changes)

    # create a config_text string with all the sections that include changes
    config_text = ''
    for items in all_changes:
        config_text += items

    return config_text


def save_configs(device_id):
    """
    This function will save the running config of the device and the last Cisco DNA Center saved configuration to files
    :param device_id: Cisco DNA Center {device_id}
    :return: saved files with the configs
    """

    # get the Cisco DNA Center Auth token
    dnac_auth = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)

    # get the device name for the {device_id}
    device_name = dnac_apis.get_device_info(device_id, dnac_auth)
    print('\nDevice Name: ', device_name)

    # get the running config of the device
    device_1 = dnac_apis.get_output_command_runner('show running-config', device_id, dnac_auth)
    device_config_1 = device_1.replace('show running-config', '')
    device_run_config = device_config_1.replace('\n' + device_name + '#', '\n')

    # save the running config to file

    f_temp = open(DEVICE_RUNNING_CONFIG, 'w')
    f_temp.write(device_run_config)
    f_temp.seek(0)  # reset the file pointer to 0
    f_temp.close()

    # get the last know Cisco DNA Center device config
    dnac_device_config = dnac_apis.get_device_config(device_id, dnac_auth)

    # save the Cisco DNA Center config to file

    f_temp = open(DNAC_DEVICE_CONFIG, 'w')
    f_temp.write(dnac_device_config)
    f_temp.seek(0)  # reset the file pointer to 0
    f_temp.close()


def builder(issue_id):
    """
    This function will collect the Assurance issue details, identify the recommended actions and execute the commands (if any)
    It will create a text file with the output of all the details and commands
    :param issue_id
    :return: issue_details
    """
    # obtain the Cisco DNA Center auth
    issue_list = []

    dnac_auth = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
    issue_complete = dnac_apis.get_issue_enrichment_details(issue_id, dnac_auth)

    # start to collect relevant information from the issue details, create a list with the output, for each suggested action

    issue_info = issue_complete['issueSummary'] + '\n\n'
    issue_info += utils.convert_html_to_text(issue_complete['issueDescription']) + '\n\n'

    issue_list.append(str(issue_info) + '\n\n')

    issue_list.append('The following troubleshooting steps have been recommended by Cisco DNA Center Assurance.\n' +
                      'The Suggested steps and CLI commands have been executed using REST APIs.\n' +
                      'For more details visit the Cisco DNA Center Issue details \n' +
                      DNAC_ISSUE + issue_id
                      )

    device_mngmnt_ip = issue_complete['issueEntityValue']
    device_info = dnac_apis.get_device_info_ip(device_mngmnt_ip, dnac_auth)
    device_id = device_info['id']

    # save the configs for the Cisco DNA Center {device_id}
    save_configs(device_id)

    # check if any device configuration changes from the last saved Cisco DNA Center configuration

    config_diff = compare_configs(DNAC_DEVICE_CONFIG, DEVICE_RUNNING_CONFIG)

    if config_diff == '':
        config_diff_comment = '\nThere are no configurations changes on the device: ' + device_info['hostname']

    else:
        config_diff_comment = '\nThe diff between the Cisco DNA Center saved config and device running config is: \n' + config_diff

    # append the config diff info
    print(config_diff_comment)
    issue_list.append('\n\n' + config_diff_comment + '\n')

    # select suggested actions

    suggested_actions = issue_complete['suggestedActions']
    for action in suggested_actions:
        action_info = 'Cisco DNA Center Suggested Action\n\n' + action['message'] + '\n\n'
        if 'steps' in action:
            steps_list = action['steps']
            action_info += 'Steps:' + '\n\n'
            for step in steps_list:
                device_hostname = dnac_apis.get_device_info(step['entityId'], dnac_auth)
                action_info += step['description'] + '\n\n'
                action_info += 'Device: ' + device_hostname + '\n'
                command_ouput = dnac_apis.get_output_command_runner(step['command'], step['entityId'], dnac_auth)
                action_info += command_ouput + '\n\n'
                print(action_info)
        issue_list.append(action_info)

    # return the list with the commands and steps
    return issue_list

