"""
Music server development configuration.

Brett Levenson <brettlev@umich.edu>
"""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'mHxxe\xd6$|\xe67K\xf6[\x9f\xeb\xdd\x949Sn\xb82BV'  # noqa: E501  pylint: disable=line-too-long
SESSION_COOKIE_NAME = 'login'
