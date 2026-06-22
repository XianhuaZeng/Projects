# Script Name : PharmaSUGProceedings.py
# Author      : Xianhua Zeng
# Created     : 22th May 2024
# Version     : 0.5
# Description : Python script to download PharmaSUG Proceedings
#               Supports both interactive mode and CLI mode (--year)

import requests, urllib3
from bs4 import BeautifulSoup
from os import path, rename, makedirs
from re import match, sub
from colorama import init, Fore
import unicodedata
import datetime
import argparse
import sys
init(autoreset=True)

LEXJANSEN_URL   = 'https://www.lexjansen.com/pharmasug/'
PHARMASUG_BASE  = 'https://www.pharmasug.org'
PROCEEDINGS_URL = 'https://www.pharmasug.org/conferences/pharmasug-{year}-us/conference-proceedings/'

def sanitize_filename(name, max_len=120):
    """Remove emojis, unsafe filesystem characters, and trim to max length."""
    # Strip emojis and non-printable unicode (So=Symbol/other, Cs=Surrogate, Co=Private, Cn=Unassigned)
    cleaned = ''.join(c for c in name if unicodedata.category(c) not in ('So', 'Cs', 'Co', 'Cn'))
    # Remove filesystem-unsafe chars and known problem chars (ellipsis, registered, etc.)
    cleaned = sub(r'[\\/:\*\?"<>\|®…]', '', cleaned)
    return cleaned.strip()[:max_len]

def download_proceedings(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(Fore.RED + f"Failed to access page (HTTP {response.status_code}): {url}")
        return False

    html_content = response.content
    soup  = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)

    pdf_sect        = [link['href'][1:] for link in links if match(r'#\w{2}', link['href'])]
    pdf_sect_titles = [link.text        for link in links if match(r'#\w{2}', link['href'])]
    sect_dict       = dict(zip(pdf_sect, pdf_sect_titles))

    pdf_links  = [link['href'] for link in links if link['href'].endswith('.pdf')]
    pdf_titles = [
        match(r'.+-(\w+-\w+)\.pdf', link['href']).group(1).replace('-', '_') + ' ' + link.text
        for link in links if link['href'].endswith('.pdf')
    ]
    pdf_dict = dict(zip(pdf_links, pdf_titles))

    if not pdf_links:
        print(Fore.RED + f"No PDF links found. The proceedings for this year may not be available yet, or the URL is incorrect: {url}")
        return False

    total = len(pdf_links)
    for i, href in enumerate(pdf_links, 1):
        pdf_url = f'{PHARMASUG_BASE}{href}'
        try:
            pdf_response = requests.get(pdf_url, verify=False)
            if pdf_response.status_code != 404:
                directory_name = sect_dict[href.split('/')[-2]]
                if not path.exists(directory_name):
                    makedirs(directory_name)
                filename = path.join(directory_name, href.split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(pdf_response.content)
                print(Fore.GREEN + f"[{i}/{total}] Downloaded {filename.split(chr(92))[-1]}")
                new_name = sanitize_filename(pdf_dict[href]) + '.pdf'
                new_path = path.join(directory_name, new_name)
                try:
                    rename(filename, new_path)
                    print(Fore.GREEN + f"[{i}/{total}] Renamed to {new_name}")
                except Exception as e:
                    print(Fore.RED + str(e))
            else:
                print(Fore.RED + f"[{i}/{total}] Error 404 - File Not Found: {href.split('/')[-1]}")
        except Exception as e:
            print(Fore.RED + str(e))

    return True

def validate_year(year_str):
    """Validate year string. Returns (True, int_year) or (False, error_message)."""
    if not match(r'^\d{4}$', year_str):
        return False, 'Invalid year. Please enter a 4-digit year.'
    year = int(year_str)
    if year > datetime.datetime.now().year:
        return False, 'Future conference. Please enter a valid year.'
    if 1997 <= year <= 2010:
        return False, f'To access proceedings from 1997 to 2010, please download them from {LEXJANSEN_URL}'
    if not match(r'20[1-9][1-9]', year_str):
        return False, 'Invalid year. Please enter a valid year (2011 or later).'
    return True, year

def run_interactive():
    """Interactive mode: prompt user to enter year."""
    while True:
        year_str = input("Please enter the conference year (e.g., 2024) and press Enter: ")
        ok, result = validate_year(year_str)
        if not ok:
            print(Fore.RED + result)
        else:
            print('Process start...')
            url = PROCEEDINGS_URL.format(year=year_str)
            if download_proceedings(url):
                print(Fore.GREEN + 'Process complete!')
            break

def run_cli(year_str):
    """CLI mode: year provided via --year argument."""
    ok, result = validate_year(year_str)
    if not ok:
        print(Fore.RED + result)
        sys.exit(1)
    print('Process start...')
    url = PROCEEDINGS_URL.format(year=year_str)
    if download_proceedings(url):
        print(Fore.GREEN + 'Process complete!')
    else:
        sys.exit(1)

def is_jupyter():
    """Detect if running inside a Jupyter / IPython kernel."""
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False

def main():
    # In Jupyter, sys.argv contains kernel arguments that confuse argparse,
    # so skip CLI parsing and go straight to interactive mode.
    if is_jupyter():
        run_interactive()
        return

    parser = argparse.ArgumentParser(
        description='Download PharmaSUG conference proceedings.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python PharmaSUGProceedings.py

  CLI mode:
    python PharmaSUGProceedings.py --year 2024
    python PharmaSUGProceedings.py -y 2023
        """
    )
    parser.add_argument(
        '-y', '--year',
        type=str,
        metavar='YEAR',
        help='Conference year (e.g., 2024). If omitted, interactive mode is launched.'
    )
    args = parser.parse_args()

    if args.year:
        run_cli(args.year)
    else:
        run_interactive()
        input("Press enter to exit.")

if __name__ == '__main__':
    main()

#EOC