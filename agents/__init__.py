from .MainMasterAgent import MainMasterAgent
from .LookUpAgent import LookUpAgent

agents = {
    'MasterAgent':
        {
            'jid': 'spade-sag-puppetmaster@blabber.im',
            'agentClass': MainMasterAgent,
            'params': {}
        },
    'WikiTravelLookUpAgent':
        {
            'jid': 'LookUpAgent1@blabber.im',
            'agentClass': LookUpAgent,
            'params': {'site': 'wikitravel', 'summariser_params': [20, 10, 2.5]}
        },
    'WikipediaLookUpAgent':
        {
            'jid': 'LookUpAgent2@blabber.im',
            'agentClass': LookUpAgent,
            'params': {'site': 'wikipedia', 'summariser_params': [30, 10, 2.5]}
        },
    'GoogleSearchLookupAgent':
        {
            'jid': 'LookUpAgent3@blabber.im',
            'agentClass': LookUpAgent,
            'params': {'summariser_params': [30, 10, 2.5]}
        },
}