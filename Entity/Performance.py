import re
from bs4 import BeautifulSoup


class Performance(object):
    def __init__(self, dept_name, date, project1=0, project2='', project3='', project4='', project5=''):
        self._dept_name = dept_name
        self._date = date
        self._project_1 = project1
        self._project_2 = project2
        self._project_3 = project3
        self._project_4 = project4
        self._project_5 = project5

    def set_dept_name(self, dept_name):
        self._dept_name = dept_name

    def set_date(self, date):
        self._date = date

    def set_project_1(self, project_1):
        self._project_1 = project_1

    def set_project_2(self, project_2):
        self._project_2 = float(project_2)

    def set_project_3(self, project_3):
        self._project_3 = project_3

    def set_project_4(self, project_4):
        self._project_4 = project_4

    def set_project_5(self, project_5):
        self._project_5 = project_5

    @property
    def get_dept_name(self):
        return self._dept_name

    @property
    def get_date(self):
        return self._date

    @property
    def get_project_1(self):
        return self._project_1

    @property
    def get_project_2(self):
        return self._project_2

    @property
    def get_project_3(self):
        return self._project_3

    @property
    def get_project_4(self):
        return self._project_4

    @property
    def get_project_5(self):
        return self._project_5
