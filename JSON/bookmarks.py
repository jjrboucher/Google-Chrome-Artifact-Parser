import json
import pandas as pd
from datetime import datetime, timedelta

def convert_webkit_timestamp(webkit_timestamp):
    # WebKit timestamp is in microseconds since January 1, 1601
    base_date = datetime(1601, 1, 1)
    # Convert WebKit time (microseconds) to seconds
    timestamp_in_seconds = webkit_timestamp / 1_000_000
    # Add to base date
    human_readable_date = base_date + timedelta(seconds=timestamp_in_seconds)
    return human_readable_date

def get_chromium_bookmarks(bookmark_path):
    rows = []
    if "Bookmarks.bak" in bookmark_path:
        worksheet = "Bookmark Backups"
    else:
        worksheet = "Bookmarks"

    # Open and load the JSON file
    with open(bookmark_path, 'r', encoding='utf-8') as file:
        bookmarks = json.load(file)

    # Extract bookmarks
    def parse_bookmark_folder(folder, fpath, level=0):
        items = folder.get("children", [])
        for item in items:
            if item.get("type") == "folder":
                rows.append(['folder',
                             fpath,
                             int(item.get('id')),
                             item.get('name'),
                             item.get('date_added'),
                             ""
                    ])

                parse_bookmark_folder(item, fpath + "/" + item.get('name'),  level + 1)
            elif item.get("type") == "url":
                rows.append(['url',
                             fpath,
                             int(item.get('id')),
                             item.get('name'),
                             item.get('date_added'),
                             convert_webkit_timestamp(int(item.get('date_added'))),
                             item.get('url')
                    ])

    # Parse root-level bookmarks
    roots = bookmarks.get("roots", {})

    for root_key, root_folder in roots.items():
        parse_bookmark_folder(root_folder, root_key, 0)

    bookmarks = pd.DataFrame(rows)
    bookmarks.columns = ['Type', 'Folder Path', 'ID', 'Name', 'Date added', 'Converted Date added (UTC)', 'URL']
    bookmarks.sort_values(['Folder Path','Type'], ascending=[True, True], inplace=True)
    return bookmarks, worksheet
