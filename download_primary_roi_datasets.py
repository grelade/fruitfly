from neuprint import Client

from config import conf
from dataset_utils import fetch_primary_roi_datasets, fetch_adjacency


c = Client(conf.neuprint_URL, conf.dataset_version,conf.api_token)
_ = fetch_primary_roi_datasets(client=c)

_,_ = fetch_adjacency(rois=[],client=c,include_nonprimary=False,prefix='noncropped_traced_2')