from config import conf
from dataset_utils import fetch_primary_roi_datasets

c = Client(conf.neuprint_URL, conf.dataset_version,conf.api_token)
er = fetch_primary_roi_datasets(client=c)