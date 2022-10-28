import attr

@attr.s
class ConferencesParameters():
    '''List of Conference Related Parameters'''
    start_year = attr.ib(type=int, default=2000)
    end_year = attr.ib(type=int, default=2022)
    architecture_conferences = attr.ib(type=bool, default=True)
