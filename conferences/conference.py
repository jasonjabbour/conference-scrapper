from ast import Delete
from re import T
import conference_config
from requests_html import HTMLSession

class Conference(object):
    '''A conference prototype class'''

    def __init__(self, 
                 conference_name: str, 
                 conference_field: str):
        '''Basic constructor of a Conference
        
        Args:
            name: name of the conference
            conference_field: field of the conference (architecture, robotics, ...)
        '''
        self._conference_name = conference_name
        self._conference_field = conference_field

        conference_params = conference_config.ConferencesParameters()
        self._start_year = conference_params.start_year
        self._end_year = conference_params.end_year
        

    def set_keywords(self, keyword_list):
        '''Load list of keywords'''
        if type(keyword_list) is not list:
            raise TypeError('Keywords must be a list of keyword.')

        self._keyword_list = keyword_list
    
    def set_conference_proceedings_webpage(self, proceedings_webpage):
        '''Load Webpage URL containing conference proceedings'''
        self._proceedings_webpage = proceedings_webpage

    def set_conference_start_year(self, start_year):
        self._start_year = start_year

    def set_conference_end_year(self, end_year):
        self._end_year = end_year
    
    def restart_session(self):
        '''Make sure session has been closed from previous runs'''
        session = HTMLSession()
        r = session.get('https://www.google.com/')

        r.close()
        session.close()
        
        del r 
        del session

    def format_year(self, year):
        '''Takes in a conference year and adds 1900 or 2000.
        
        Assumption:
            No conference takes place before 1950
        
        Returns:
            year: int year such as 2012 or 1978
        
        '''
        year = int(year)

        # Assuming we will not have a conference before 1950
        if year < 50:
            year = 2000 + year
        else:
            year = 1900 + year

        return year
    
    def year_within_range(self, year):
        '''Takes in a four digit year and checks
            if the year is within the range of the 
            start and end years
        
        Returns:
            True: if year within range
            False: if year outside of range
        '''

        if (year >= self._start_year) and (year <= self._end_year):
            return True
        
        return False


        


    

        




