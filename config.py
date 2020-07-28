class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
        

conf = AttrDict(
    {
    'api_token':None, #uses envvar if None
    'neuprint_URL':'neuprint.janelia.org',
    'dataset_version' :'hemibrain:v1.0.1',
    'datasets_dir': 'datasets',
    'roi_connections_file': 'roi-connections.csv',
    'neurons_file': 'neurons.csv',
    })

