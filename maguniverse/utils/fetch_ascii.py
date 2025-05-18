# -*- coding: utf-8 -*-
"""
fetch_ascii.py
-----------

Utilities for resolving data paths and fetching ASCII tables, with
CAPTCHA handling for remote downloads.
"""

import os
import sys
import webbrowser

import requests

from maguniverse import __parent_dir__ as sys_parent


def get_default_data_paths(file_path, file_url):
    """
    Determine whether a local data file exists under the repository parent.

    Parameters
    ----------
    file_path : str
        Relative path (within the repository) to the expected local file.
    file_url : str
        URL to fetch the file if the local copy is absent.

    Returns
    -------
    tuple
        (local_path, file_url), where `local_path` is the joined path
        under `sys_parent` if it exists, otherwise None.
    """
    if file_path is not None:
        complete_path = os.path.join(sys_parent, file_path)
        if not os.path.exists(complete_path):
            complete_path = None
    else: complete_path = file_path
    return complete_path, file_url


def get_ascii(file_path=None, file_url=None, save_path=None, fmt='txt'):
    """
    Fetch an ASCII table from a local file or remote URL, with CAPTCHA support.

    Parameters
    ----------
    file_path : str or None
        Path to a local ASCII file. If provided, the file is read directly.
    file_url : str or None
        URL of the ASCII resource. Used only if `file_path` is None.
    save_path : str or None
        If provided (and fmt == 'txt'), the fetched text is written here.
    fmt : {'txt'}, optional
        Output format. Only 'txt' (raw text) is supported.

    Returns
    -------
    str
        The raw ASCII text.

    Raises
    ------
    ValueError
        If neither `file_path` nor `file_url` is provided.
    SystemExit
        After prompting and opening a browser when CAPTCHA is detected.
    """
    if file_path is None and file_url is None:
        raise ValueError("Either file_path or file_url must be provided.")
    if file_path is not None:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    # Remote fetch
    session = requests.Session()
    headers = {'User-Agent': 'python-requests/2.x'}

    def fetch():
        if not isinstance(file_url, str) or not file_url:
            raise ValueError("file_url must be a non-empty string when fetching remotely.")
        resp = session.get(file_url, headers=headers,
                           allow_redirects=True, timeout=10)
        resp.raise_for_status()
        return resp

    if not isinstance(file_url, str) or not file_url:
        raise ValueError("file_url must be a non-empty string when fetching remotely.")
    response = fetch()
    text = response.text

    # CAPTCHA detection
    if '<div class="h-captcha"' in text \
       or 'We apologize for the inconvenience' in text:
        print("\nA CAPTCHA is required to access the content.")
        print("Opening the URL in your default browser; please complete"
              " the CAPTCHA there.")
        webbrowser.open(file_url)
        sys.exit(
            "\nRequest aborted due to human-verification requirement.\n"
            "Please download the ASCII file manually, save it locally, and "
            "then re-run get_ascii() on your local copy."
        )

    # Save if requested
    if save_path and fmt == 'txt':
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(text)

    return text
