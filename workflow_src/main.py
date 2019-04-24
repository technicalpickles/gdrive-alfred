import sys
import uuid
import json
import argparse

import search
from workflow_version_utils import *

# Settings
MAX_ALFRED_ITEMS = 20

# Have to look in local folder - CI will pip install these locally
sys.path.insert(0, "pylib_dist")

def action_search(query):
    """Returns a list of alfred items."""
    return search.search(query)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", help="Action", default="search", choices=["search"])
    parser.add_argument("--query", help="Query if searching")
    args = parser.parse_args()

    items = []

    # Add Update item at the top
    workflowUpdateAlfredItem = getWorkflowUpdateAlfredItem()
    if workflowUpdateAlfredItem:
        items.append(workflowUpdateAlfredItem)

    # Magic "version" argument
    if args.query != None and "version" in args.query:
        items.append({
            "title": "Current workflow version: %s" % getCurrentVersion(),
        })

    # Action items
    if args.action == "search" and args.query != None:
        items += action_search(args.query)

    # Add UUIDs so we can record easily what was chosen when
    for item in items:
        if "arg" in item:
            item["arg"] = "%s|%s" % (uuid.uuid4().hex, item["arg"])

    # Print for Alfred
    # See https://www.alfredapp.com/help/workflows/inputs/script-filter/json/ for format
    print(json.dumps({"items": items}, indent = 4))

if __name__ == '__main__':
    main()
