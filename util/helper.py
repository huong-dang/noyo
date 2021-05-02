"""Define utility methods that can be used anywhere"""
from uuid import UUID

# Verify if a string is a valid uuid (universally unique identifier)
def is_uuid(string, version=4):
    try:
        uuid_obj = UUID(string, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == string


# Check if 2 dictionaries have the same values for the list of keys passed in
def is_different(dict1, dict2, keys):
    has_changed = False
    for key in keys:
        dict1_val = dict1.get(key, "")
        dict2_val = dict2.get(key, "")
        if dict1_val != dict2_val:
            has_changed = True
            break
    return has_changed
        
