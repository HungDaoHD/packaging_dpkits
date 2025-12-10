# # Import all public names from submodules
# from .converter.converter import *
# from .metadata.metadata import *

# import sys
# import inspect

# module = sys.modules[__name__]



# # Automatically collect all classes defined in dpkits2.*
# __all__ = [
#     name
#     for name, obj in inspect.getmembers(module)
#     if inspect.isclass(obj)
#     and obj.__module__.startswith(module.__name__)
#     and not name.startswith("_")  # ignore private
# ]
