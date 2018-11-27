# -*- coding: utf-8 -*-
"""
abstract: A implement of local cache
by zyp
"""
import hashlib
from time import time


_mem_caches = {}


def cache(expire=7200, key="", max_len=300000):
    """
    Mem cache to python dict by key
    :param int expire: seconds
    :param str key: md5 base key
    :param int max_len: the max length of cached value
    """

    def wrapper(func):
        def mem_wrapped_func(*args, **kwargs):
            now = time()
            if key:
                c = key
            else:
                c = repr(func)
            k = key_gen(c, *args, **kwargs)

            value = _mem_caches.get(k, None)
            if _valid_cache(value, now):
                return value["value"]
            else:
                val = func(*args, **kwargs)
                if isinstance(val, unicode):
                    val = val.encode('utf8')
                assert len(str(val)) <= max_len
                _mem_caches[k] = {"value": val, "expire": now + expire}

                return val

        return mem_wrapped_func

    return wrapper


def key_gen(key, *args, **kwargs):
    """
    generate hash key
    """
    code = hashlib.md5()

    code.update(str(key))
    code.update("".join(sorted(map(str, args))))
    code.update("".join(sorted(map(str, kwargs.items()))))

    return code.hexdigest()


def _valid_cache(value, now):
    """
    valid if expired
    """
    if value:
        if value["expire"] > now:
            return True
        else:
            return False
    else:
        return False
