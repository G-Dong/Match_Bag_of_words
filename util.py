import sys
from core import util

def load_competency_model(path, No_traits):
    for i in range(No_traits):
        # cell_positive = [i, 1, 2] # col: B
        content_cache_1 = util.read_csv_tag(path, tag='Skilled')[i]
        content_cache_0 = util.read_csv_tag(path, tag='Competence')[i]
        content_cache = content_cache_0 + ' ' + content_cache_1
        #print(content_cache)
    return content_cache
