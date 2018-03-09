"""Class Performance"""


from datetime import datetime


class Log(object):
    """Class Log"""
    def __init__(self, user_name, page, method, content):
        self._time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self._user_name = user_name
        self._page = page
        self._method = method
        self._content = content

    def set_user_name(self, user_name):
        self._user_name = user_name

    def set_page(self, page):
        self._page = page

    def set_method(self, method):
        self._method = method

    def set_content(self, content):
        self._content = content

    @property
    def get_user_name(self):
        return self._user_name

    @property
    def get_page(self):
        return self._page

    @property
    def get_time(self):
        return self._time

    @property
    def get_method(self):
        return self._method

    @property
    def get_content(self):
        return self._content
