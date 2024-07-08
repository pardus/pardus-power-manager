cache_fn = {}
def cached(func):
    def wrapper(*args, **kwargs):
        if func in cache_fn:
            return cache_fn[func]
        else:
            ret = func(*args, **kwargs)
            cache_fn[func] = ret
            return ret
    return wrapper
