from neuprint import Client

# Please put the API token into the environment variable NEUPRINT_APPLICATION_CREDENTIALS

client = Client('neuprint.janelia.org', dataset='hemibrain:v1.1')

client.fetch_version()

