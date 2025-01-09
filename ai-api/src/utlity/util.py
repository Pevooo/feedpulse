import warnings
import functools


def deprecated(
    message: str = "This functionality is deprecated and will be removed in a future version.",
):
    def decorator(func_or_class):
        if isinstance(func_or_class, type):
            original_init = func_or_class.__init__

            @functools.wraps(original_init)
            def new_init(self, *args, **kwargs):
                warnings.warn(
                    f"{func_or_class.__name__} is deprecated: {message}",
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                original_init(self, *args, **kwargs)

            func_or_class.__init__ = new_init
            return func_or_class

        else:

            @functools.wraps(func_or_class)
            def wrapped(*args, **kwargs):
                warnings.warn(
                    f"{func_or_class.__name__} is deprecated: {message}",
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                return func_or_class(*args, **kwargs)

            return wrapped

    return decorator
