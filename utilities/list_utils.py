import re


def get_strs_list_from_env_string(origin_env_string: str) -> list[str]:
    """ Extract list of strings from env (environment) string
    :param origin_env_string: elements separated with commas in one string,
    e.g. "111, 222, 333" or "111,222,333"
    :return: list of strings, e.g. ["111", "222", "333"]
    """
    cleaned_str = re.sub(r"[^0-9,]", "", origin_env_string)
    cleaned_str = re.sub(r",+", ",", cleaned_str)
    cleaned_str = cleaned_str.strip(",")
    extracted_strings_list = cleaned_str.split(",")
    return extracted_strings_list


def convert_str_list_to_int_list(orig_strings_list: list[str]) -> list[int]:
    result_list = []
    for num_string in orig_strings_list:
        try:
            result_list.append(int(num_string))
        except (ValueError, Exception) as exception_error:
            print(f"\tString not converted to integer because"
                  f"\texception_error = {exception_error}\n"
                  f"\tnum_string = '{num_string}'\n"
                  f"\torig_strings_list = {orig_strings_list}\n")
    return result_list


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
