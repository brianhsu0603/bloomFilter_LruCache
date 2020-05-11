
def lru_cache(max_size):
  
    cache = {}
    cache_keys = []

    def wrap(func):
        def wrapped_func(*args):
            if args in cache:
                del cache_keys[cache_keys.index(args)]
                cache_keys.append(args)
                return cache[args]

            retval = func(*args)

            # Add to the cache and set as most-recently-used
            cache[args] = retval
            cache_keys.append(args)

            if len(cache_keys) > max_size:
                del cache[cache_keys[0]]
                del cache_keys[0]

            return retval
        return wrapped_func
    return wrap