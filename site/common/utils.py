import random
from re import L

from django.db.models import QuerySet


def random_sample_queryset(queryset: QuerySet, samples: int):
    """
    Returns a list of `number` instances, or fewer if the total number of instances
    in the queryset is <= `number`.
    """
    total: int = queryset.count()
    to_show: int = min(total, samples)
    sample_indexes = random.sample(range(0, total), to_show)
    sample = []
    for i in range(to_show):
        sample.append(queryset[sample_indexes[i]])
    return sample


def comma_seperate_list(list):
    if not list:
        return ""
    elif len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return " og ".join(list)
    else:
        return f"{', '.join(list[:-1])}, og {list[-1]}"
