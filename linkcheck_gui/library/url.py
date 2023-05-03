# Copyright (C) 2000-2014 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Functions for parsing and matching URL strings.
"""

import requests

from linkcheck import log, LOG_CHECK
from linkcheck.configuration import get_certifi_file, get_system_cert_file


def get_content(url, user=None, password=None, data=None, addheaders=None):
    """Get URL content and info.

    @return: (decoded text content of URL, headers) or
             (None, errmsg) on error.
    @rtype: tuple (String, dict) or (None, String)
    """
    from linkcheck import configuration

    headers = {
        'User-Agent': configuration.UserAgent,
    }
    if addheaders:
        headers.update(addheaders)
    method = 'GET'
    kwargs = dict(headers=headers)
    if user and password:
        kwargs['auth'] = (user, password)
    if data:
        kwargs['data'] = data
        method = 'POST'

    try:
        kwargs["verify"] = get_system_cert_file()
    except ValueError:
        try:
            kwargs["verify"] = get_certifi_file()
        except (ValueError, ImportError):
            pass
    try:
        response = requests.request(method, url, **kwargs)
        return response.text, response.headers
    except (
        requests.exceptions.RequestException,
        requests.exceptions.BaseHTTPError,
    ) as msg:
        log.warn(
            LOG_CHECK,
            ("Could not get content of URL %(url)s: %(msg)s.")
            % {"url": url, "msg": str(msg)},
        )
        return None, str(msg)
