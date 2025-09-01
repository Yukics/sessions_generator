def replace_dict_value_recurse(obj, key_to_replace, replace_value):
    """
    Recursively replaces all values of the specified key in a nested dictionary or list.

    Args:
        obj (dict or list): The object to process.
        key_to_replace (str): The key whose value should be replaced.
        replace_value: The value to set for the specified key.

    Returns:
        The updated object with replacements applied.
    """
    if isinstance(obj, dict):
        return {k: (replace_value if k == key_to_replace else replace_dict_value_recurse(v, key_to_replace, replace_value))
                for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_dict_value_recurse(item, key_to_replace, replace_value) for item in obj]
    else:
        return obj