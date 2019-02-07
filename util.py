import sys
from core import util


def load_competency_model(path, no_traits):
    """
    :param path: path of competency model raw documents
    :param no_traits: The total number of traits in the competency model
    :return: sorted documents
    This function is specific tailored according to the Competency Model 2018 October version.
    """
    for i in range(no_traits):
    # cell_positive = [i, 1, 2]
    # col: B
        content_cache_1 = util.read_csv_tag(path, tag='Skilled')[i]
        content_cache_0 = util.read_csv_tag(path, tag='Competence')[i]
        content_cache = content_cache_0 + ' ' + content_cache_1
    #print(content_cache)
    return content_cache
