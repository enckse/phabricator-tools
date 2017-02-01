#!/usr/bin/python
"""provide tasking helpers."""

import argparse
import conduit


def _process(factory, project, file_name, skip, title):
    """process the tasking request."""
    u = factory.create(conduit.User).query()[conduit.DATA_FIELD]
    skips = []
    user_set = []
    if skip is not None:
        skips = skip.split(",")
    for user in u:
        phid = user['phid']
        roles = user['fields']['roles']
        if "disabled" in roles or 'agent' in roles:
            continue
        user_name = user['fields']["userName"]
        if user_name in skips:
            continue
        user_set.append(phid)
    with open(file_name, 'r') as f:
        contents = f.read()
        m = factory.create(conduit.Maniphest)
        for u in user_set:
            m.create(title, contents, u, project)


def main():
    """main entry."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--token", type=str, required=True)
    parser.add_argument("--project", type=str, required=True)
    parser.add_argument("--skip", type=str)
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--title", type=str, required=True)
    args = parser.parse_args()
    factory = conduit.Factory()
    factory.token = args.token
    factory.host = args.host
    _process(factory, args.project, args.file, args.skip, args.title)

if __name__ == '__main__':
    main()
