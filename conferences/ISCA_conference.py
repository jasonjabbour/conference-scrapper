'''ISCA Conference'''

from conferences import conference
from requests_html import HTMLSession
import re

ALL_PROCEEDINGS_URL = 'https://dl.acm.org/conference/isca/proceedings'

class ISCAConference(conference.Conference):
    '''ISCA Conference Class'''

    def __init__(self):
        '''Constructs an ISCA Conference Class'''

        name = 'ISCA'
        field = 'Architecture'

        super(ISCAConference, self).__init__(
            conference_name=name, 
            conference_field=field)
    
    def get_URL_of_each_proceeding(self):
        '''Using a URL that containts the URL of proceedings
            for every year, return a list of all potention
            proceeding urls

            Returns:
                proceedings_url_list: a list of unordered URL strings 

            Example:
                ['https://dl.acm.org/doi/proceedings/10.1145/800053', ...]
        '''
        proceedings_url_dict = {}

        try: 
            
            #Make sure you are starting a clean session
            self.restart_session()

            # Start HTML Session
            session = HTMLSession()

            # Read Proceedings Page
            r = session.get(ALL_PROCEEDINGS_URL)

            # Execute Javascript on page
            r.html.render(sleep=5, timeout=30)

            # Get the proceedings listed
            proceeding_listings = r.html.find('.show-more-items ul li a') #js--showMore

            # Look through all potential proceedings
            for listing in proceeding_listings:
                try:
                    # Try to get a URL listed
                    proceeding_link = listing.absolute_links
                    # Try to get the title of the proceeding
                    proceeding_title = listing.full_text

                    # Check if text is an ISCA proceeding
                    if ('ISCA \'' in proceeding_title) and ('Proceedings of the ' in proceeding_title):
                        # Check if URL exists
                        if (len(proceeding_link) == 1):
                            # Get link from set
                            proceeding_link = list(proceeding_link)[0]
                            # Check if URL in correct format
                            if 'https://dl.acm.org/doi/proceedings' in proceeding_link:
                                #Get the year of the proceeding
                                year = re.search('ISCA \'\d{2}:', proceeding_title)
                                # Clean year
                                year = year[0].strip('ISCA \'').strip(':')
                                # Format year
                                year = self.format_year(year)

                                if year not in proceedings_url_dict:
                                    if self.year_within_range(year):
                                        proceedings_url_dict[year] = proceeding_link
                                else:
                                    print('Duplicate Year found:', year)
                except:
                    pass
            
            # Check if dictionary is empty
            if not len(proceedings_url_dict) == 0:
                print(f'Gathered {self._conference_name} proceedings.')
            else:
                print(f'Unable to gather {self._conference_name} proceedings.')

            print(proceedings_url_dict)

        except Exception as err:
            print('Unable to gather potention proceeding URLs for ISCA:', err)
        finally:
            #Close session
            r.close()
            session.close()

        return proceedings_url_dict


    def get_number_keywords_per_year(self):
        '''Returns the number of keyword counts for each year 
            in the structure of a dictionary

        Returns:

        '''

        keywords_per_year = {}

        proceedings_url_dict = self.get_URL_of_each_proceeding()

        try:
            # Start HTML Session
            session = HTMLSession()

            for year in proceedings_url_dict:
                try: 
                    # Read Proceedings Page
                    r = session.get(proceedings_url_dict[year])

                    # Execute Javascript on page
                    r.html.render(sleep=5, timeout=20)

                    # Find the paper title and header
                    paper_titles = r.html.find('.issue-item__content div h5 a')
                    paper_headers = r.html.find('.issue-item__content div div p')
                    
                    # Check if javascript executed correctly
                    if len(paper_titles) < 0:
                        print(f'Unable to read page: {proceedings_url_dict[year]}')

                    # Number of paper titles and headers must be equal to zip 
                    assert len(paper_titles) == len(paper_headers), 'Mismatched number of paper titles and headers'

                    for paper_title, paper_header in zip(paper_titles, paper_headers):
                        for keyword in self._keyword_list:
                            if (keyword.lower() in paper_title.full_text.lower()) or (keyword in paper_header.full_text.lower()):
                                print(keyword)
                except Exception as err:
                    print(f'Error when scraping {year} proceedings: {err}')


        except Exception as err:
            print(err)
        finally:
            #Close session
            r.close()
            session.close()



