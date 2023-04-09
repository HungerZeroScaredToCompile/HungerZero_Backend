from django.test import TestCase
from urls import urlpatterns
# Create your tests here.

for url in urlpatterns:
    if isinstance(url, str):
        print(f"This is a string URL pattern: {url}")
    elif isinstance(url, tuple):
        print(f"This is a tuple URL pattern: {url}")
    else:
        print("Unknown URL pattern")

def flatten(lst):
    """Flatten a list of nested lists/tuples."""
    for item in lst:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

def is_string_or_tuple(obj):
    """Check if an object is a string or tuple."""
    return isinstance(obj, str) or isinstance(obj, tuple)

def check_urlpatterns(urlpatterns):
    """Check if all URL patterns have unique names."""
    names = []
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            # Recursively check nested URL patterns
            check_urlpatterns(pattern.url_patterns)
        else:
            name = pattern.name
            if is_string_or_tuple(name):
                if isinstance(name, str):
                    # Check if name is already used
                    if name in names:
                        raise Exception(f'Duplicate URL pattern name: {name}')
                    names.append(name)
                elif isinstance(name, tuple):
                    # Check if any of the names are already used
                    if any(n in names for n in name):
                        raise Exception(f'Duplicate URL pattern name: {name}')
                    names.extend(name)