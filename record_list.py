#!/usr/bin/python3

import json
import os
import sys
import requests

import hetzner_dns_helpers as helpers


def record_list(hetzner_dns_token=None, zone_id=None, zone_name=None):
    """
    Get list of all records.
    https://dns.hetzner.com/api-docs/#operation/GetRecords

    - Lookups can be performed using 'zone_name' or 'zone_id'.

    - If no 'zone_name' or 'zone_id' is given, all records will be returned.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token
    """

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if zone_id is None and os.environ.get('ZONE_ID'):
        # get zone_id from environment variable
        zone_id = os.environ['ZONE_ID']

    if zone_name is None and os.environ.get('ZONE_NAME'):
        # get zone_name from environment variable
        zone_name = os.environ['ZONE_NAME']

    # if (domain) name exists, use it to obtain the zone
    if (zone_name or 'ZONE_NAME' in os.environ):
        from zone_list import zone_list

        # get list of zones
        response_dict = zone_list()

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching zone
        dns_zones = response_dict['zones']
        for zone in dns_zones:
            if zone['name'] == zone_name:
                zone_id = zone['id']
                break

        # if no matching zone found, halt and notify of error
        if zone_id is None:
            error_message = "record not found"  # fixme: is this message right?

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)

    # get zone_id from environment variable
    if zone_id is None:
        zone_id = os.environ.get('ZONE_ID')

    try:
        # build params dict
        params = {}
        if zone_id:
            params['zone_id'] = zone_id

        # get response
        response = requests.get(url='https://dns.hetzner.com/api/v1/records',
                                params=params,
                                headers={'Auth-API-Token': hetzner_dns_token})

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        if __name__ == '__main__':
            # when running via the terminal, print output to console then exit
            print(decoded_response)
            sys.exit(0)  # exit successfully

        return response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == '__main__':
    record_list()
