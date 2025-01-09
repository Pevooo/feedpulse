import warnings
import functools

def deprecated(message="This function or class is deprecated and may be removed in future versions."):
    def decorator(func_or_class):
        @functools.wraps(func_or_class)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func_or_class.__name__}: {message}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func_or_class(*args, **kwargs)
        return wrapper
    return decorator
