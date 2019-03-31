# CHROME BOOKMARKS DEDUPE

This tool helps you deduplicate Google Chrome's bookmarks.

## How to use
* export your Google Chrome's bookmarks to an HTML file
* Run:
```bash
$ make venv
$ make run/bookmarks_20_03_2019.html
```

The tool creates the file `output.html` which contains no duplicates and
can be re-imported in Google Chrome.
