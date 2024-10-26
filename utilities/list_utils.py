def empty_list_if_none(orig_list: list | None) -> list:
    result_list = [] if orig_list is None else orig_list
    return result_list


def remove_same_list_elms_by_value(old_list: list,
                                   value_to_remove: int) -> list:
    new_list = [elem for elem in old_list if elem != value_to_remove]
    return new_list


def remove_list_duplicates(orig_list: list) -> list:
    result_list = list(set(orig_list))
    return result_list
