#coding: utf-8
import logging

from cache_utils.utils import _cache_key, _func_info, _func_type, sanitize_memcached_key
from django.core.cache import get_cache
from django.utils.functional import wraps

logger = logging.getLogger("cache_utils")

def cached(timeout, group=None, backend=None):
    """ Caching decorator. Can be applied to function, method or classmethod.
    Supports bulk cache invalidation and invalidation for exact parameter
    set. Cache keys are human-readable because they are constructed from
    callable's full name and arguments and then sanitized to make
    memcached happy.

    It can be used with or without group_backend. Without group_backend
    bulk invalidation is not supported.

    Wrapped callable gets `invalidate` methods. Call `invalidate` with
    same arguments as function and the result for these arguments will be
    invalidated.
    """

    if group:
        backend_kwargs = {'group': group}
        get_key = _cache_key
    else:
        backend_kwargs = {}
        def get_key(*args, **kwargs):
            return sanitize_memcached_key(_cache_key(*args, **kwargs))

    if backend:
        cache_backend = get_cache(backend)
    else:
        cache_backend = get_cache('default')

    def _cached(func):
        
        #if not key:
        func_type = _func_type(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            full_name(*args)

            # try to get the value from cache
            key = get_key(wrapper._full_name, func_type, args, kwargs)
            value = cache_backend.get(key, **backend_kwargs)
            
            # in case of cache miss recalculate the value and put it to the cache
            if value is None:
                logger.debug("Cache MISS: %s" % key)
                value = func(*args, **kwargs)
                cache_backend.set(key, value, timeout, **backend_kwargs)
                logger.debug("Cache SET: %s" % key)
            else:
                logger.debug("Cache HIT: %s" % key)
            
            return value

        def invalidate(*args, **kwargs):
            """ 
            Invalidates cache result for function called with passed arguments
            """
            if not hasattr(wrapper, '_full_name'):
                return

            key = get_key(wrapper._full_name, 'function', args, kwargs)
            cache_backend.delete(key, **backend_kwargs)
            logger.debug("Cache DELETE: %s" % key)
            
        def force_recalc(*args, **kwargs):
            """
            Forces a call to the function & sets the new value in the cache
            """
            full_name(*args)

            key = get_key(wrapper._full_name, func_type, args, kwargs)
            value = func(*args, **kwargs)
            cache_backend.set(key, value, timeout, **backend_kwargs)
            return value

        def full_name(*args):
            # full name is stored as attribute on first call
            if not hasattr(wrapper, '_full_name'):
                name, _args = _func_info(func, args)
                wrapper._full_name = name
        
        def require_cache(*args, **kwargs):
            """
            Only pull from cache, do not attempt to calculate
            """
            full_name(*args)
            key = get_key(wrapper._full_name, func_type, args, kwargs)
            logger.debug("Require cache %s" % key)
            value = cache_backend.get(key, **backend_kwargs)
            if not value:
                logger.info("Could not find required cache %s" % key)
                raise NoCachedValueException
            return value
        
        wrapper.require_cache = require_cache
        wrapper.invalidate = invalidate
        wrapper.force_recalc = force_recalc
        
        return wrapper
    return _cached


class NoCachedValueException(Exception):
    pass