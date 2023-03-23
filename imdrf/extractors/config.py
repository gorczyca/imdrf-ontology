import os
import json

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


IMRDF_PATHS_BASE = './imdrf/sources'

ANNEXES_JSON = {
    'a': {
        'file_name': 'annexa_3.json',
        'label': 'Medical Device Problem'
    },
    'b': {
        'file_name': 'annexb_1.json',
        'label': 'Type of Investigation'
    },
    'c': {
        'file_name': 'annexc_1.json',
        'label': 'Investigation Findings'
    },
    'd': {
        'file_name': 'annexd_1.json',
        'label': 'Investigation Conclusion'
    },
    'e': {
        'file_name': 'annexe_1.json',
        'label': 'Health Effects - Clinical Signs and Symptoms or Conditions'
    },
    'f': {
        'file_name': 'annexf_1.json',
        'label': 'Health Effects - Health Impact'
    },
    'g': {
        'file_name': 'annexg_1.json',
        'label': 'Medical Device Component'
    }
}

IMDRF_ALL_JSON_PATH = 'imdrf_all_terms.json'

for annex in ANNEXES_JSON:
    annex_full_path = os.path.join(IMRDF_PATHS_BASE, ANNEXES_JSON[annex]['file_name'])
    ANNEXES_JSON[annex]['json'] = load_json(os.path.join(IMRDF_PATHS_BASE, ANNEXES_JSON[annex]['file_name']))


ALL_IMDRF = load_json(os.path.join(IMRDF_PATHS_BASE, IMDRF_ALL_JSON_PATH))



