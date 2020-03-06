#!/usr/bin/env python3
"""
pre-req::
ansd yum install python3
ansd yum install python-requests

"""
import json
import requests
import base64
import sys
import argparse
import os


def download(server, token, consul_path=""):

    url = server + "/v1/kv/" + consul_path
    params = {"token": token, "recurse": 1}

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception("HTTP code %s on GET %s" % (response.status_code, url))

        return response.json()

    except Exception as e:
        print("ERROR during download:", e, file=sys.stderr)
        exit(1)


def process(downloaded_data):

    result_obj = []

    for obj in downloaded_data:
        try:
            if obj['Key'][-1] == "/":
                continue

            if obj['Value']:
                obj['Value'] = base64.b64decode(obj['Value'])
                obj['Value'] = str(obj['Value'].decode('utf-8'))

            result_obj.append(obj)

        except UnicodeDecodeError as e:
            print("WARNING: bad chars in", obj['Key'], ": ", e, file=sys.stderr)
            obj['Value'] = None
            result_obj.append(obj)

        except Exception as e:
            print ("ERROR during processing:", e, file=sys.stderr)
            exit(1)

    return result_obj


def read_from_file(file_path, consul_path=None):

    try:
        f = open(file_path, "r", encoding="utf-8")
        data = json.load(f).encode('utf-8')
        f.close()

        if consul_path:
            result_obj = []
            for obj in data:
                if consul_path in obj['Key'].decode('utf-8'):
                    result_obj.append(obj)
            data = result_obj

    except Exception as e:
        print ("ERROR reading file:", e, file=sys.stderr)
        exit(1)

    return data


def output(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


def upload(server, token, data):

    params = {"token": token}

    for obj in data:
        try:
            payload = obj['Value']
            url = server + "/v1/kv/" + obj['Key']

            response = requests.put(url, data=payload, params=params)
            if response.status_code != 200:
                raise Exception("HTTP code %s on PUT %s" % (response.status_code, url))

        except Exception as e:
            print ("ERROR uploading:", e, file=sys.stderr)
            exit(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", type=str, choices=["export", "import"], action="store", help="export or import")
    parser.add_argument("--file", "-f", type=str, help="json file to read", metavar='')
    parser.add_argument("--path", "-p", type=str, help="Consul kv path: 'vault/master/something/key'", default="", metavar='')
    parser.add_argument("--server", "-s", type=str, help="Consul server, proto://url:port", default="http://localhost:8500", metavar='')
    parser.add_argument("--token", "-t", type=str, help="Consul ACL token", metavar='')
    args = parser.parse_args()

    if args.token:
        token = args.token
    elif 'CONSUL_HTTP_TOKEN' in os.environ:
        token = os.environ['CONSUL_HTTP_TOKEN']
    else:
        print("Warning: no Consul token provided.", file=sys.stderr)


    if args.action == 'export':
        data = download(args.server, token, args.path)
        data = process(data)
        output(data)

    elif args.action == 'import':
        data = read_from_file(args.file, args.path)
        upload(args.server, token, data)
