from math import ceil

from hypothesis.strategies import builds, text, sampled_from


def string_containing(s, max_size=None, min_size=None, alphabet=None, with_spacing=False):
    part_max_size = (max_size - len(s)) // 2 if max_size else None
    if with_spacing:
        part_max_size -= 1

    part_min_size = ceil((min_size - len(s)) // 2) if min_size else None

    def _gen_str(pre, suf):
        if with_spacing:
            return pre + ' ' + s + ' ' + suf
        else:
            return pre + s + suf

    return builds(_gen_str, text(min_size=part_min_size, max_size=part_max_size, alphabet=alphabet), text(min_size=part_min_size, max_size=part_max_size, alphabet=alphabet))


def string_not_containing(s, max_size=None, min_size=None, alphabet=None, average_size=None):
    return text(min_size=max_size, max_size=min_size, average_size=average_size, alphabet=alphabet).filter(lambda _s: s.lower() not in _s.lower())


def false_values():
    return sampled_from([False, None, '', [], (), {}, 0, 0.0])
