
import conference_config
import conferences.conference as conference
from conferences import ISCA_conference

ARCHITECTURE_CONFERENCE_LIST = [ISCA_conference.ISCAConference]
KEYWORDS = ['machine learning', 'reinforcement learning', 'deep learning',
            'neural network', 'deep neural network', ' dnn ', ' ml ', ' rl ', ' dnns ']

def main():
    ''''''
    # Default Parameters
    arch_conf_objects = []

    # Get conference parameters
    conference_params = conference_config.ConferencesParameters()

    # Scrap Architecture Conferences
    if conference_params.architecture_conferences: 
        # Initialize All Architecture Conferences
        for arch_conf in ARCHITECTURE_CONFERENCE_LIST:
            # Initialize Architecture Conference Class
            arch_conf_class = arch_conf()
            # Set Keywords to look for
            arch_conf_class.set_keywords(KEYWORDS)
            # Get number of keywords per year
            keywords_per_year = arch_conf_class.get_number_keywords_per_year()
            
            # Save Conference Class
            arch_conf_objects.append(arch_conf_class)


if __name__ == '__main__':
    main()