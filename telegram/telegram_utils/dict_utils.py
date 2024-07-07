def empty_dict_if_none(original_dict: dict | None) -> dict:
    result_dict = {} if original_dict is None else original_dict
    return result_dict
