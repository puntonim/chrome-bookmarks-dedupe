"""

- using beautifulsoup of the html parser in the std library is not an option because they produce html invalid for
chrome.
"""
import re

import click


@click.command()
@click.argument('input_file', type=click.File('r'))
def main(input_file):
    hrefs_found = []
    deleted_count = 0
    output_lines = []

    for line in input_file.readlines():
        # Remove all duplicated <a> tags.
        href = find_href(line)
        if href and href in hrefs_found:
            # Delete the node.
            deleted_count += 1
            continue

        if href and href not in hrefs_found:
            hrefs_found.append(href)
        output_lines.append(line)
    click.echo('Duplicated bookmarks deleted: {}'.format(deleted_count))

    # remove folders left empty.
    remove_empty_folders(output_lines)

    # Write the output file.
    with open('output.html', 'w') as output_file:
        output_file.writelines(output_lines)


HREF_REGEX = re.compile('<DT><A HREF="(?P<href>[^ \t\n\r\f\v"]+)".*</A>')


def find_href(line):
    """
    Format:
        <DT><A HREF="https://its.cern.ch/..." ADD_DATE="1519160256" ICON="...">Jira</A>
    """
    try:
        return HREF_REGEX.search(line).group('href')
    except AttributeError:
        return None


def remove_empty_folders(lines):
    """
    Format:
        <DT><H3 ADD_DATE="1513706853" LAST_MODIFIED="1513706853">Unibg</H3>
        <DL><p>
        </DL><p>
    """
    deleted_count = 0
    DT_REGEX = re.compile(r'<DT><H3.*</H3>')
    DLO_REGEX = re.compile(r'[\t\n\r\f\v]*<DL><p>[\t\n\r\f\v]*')
    DLC_REGEX = re.compile(r'[\t\n\r\f\v]*</DL><p>[\t\n\r\f\v]*')

    while True:
        deleted_in_curr_loop = 0
        i = 0
        while i < len(lines)-2:
            if 'HREF' in lines[i] or not DT_REGEX.search(lines[i]):
                pass
            else:
                if DT_REGEX.search(lines[i]) and DLO_REGEX.search(lines[i+1]) and DLC_REGEX.search(lines[i+2]):
                    # Lines to be deleted.
                    del lines[i]
                    del lines[i]
                    del lines[i]
                    deleted_in_curr_loop += 1
                    break
                else:
                    pass
            i += 1
        deleted_count += deleted_in_curr_loop
        click.echo('Empty folders deleted so far: {}'.format(deleted_count))
        if deleted_in_curr_loop == 0:
            break


if __name__ == '__main__':
    click.echo('** DEDUPLICATE GOOGLE CHROME BOOKMARKS **\n')
    main()
