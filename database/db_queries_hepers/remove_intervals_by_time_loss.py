import copy
from datetime import timedelta


def remove_intervals_over_time_loss_limit(
        time_loss_max_limit: int,
        enrollment_intervals: dict[dict] | dict) -> dict[dict] | dict:
    """
    Removes intervals by time loss max limit. Removing is executed
    in the origin dictionary passed as link to the original dictionary
    :param time_loss_max_limit: int - Max loss time limit in minutes
    :param enrollment_intervals: dict[dict] | dict - Original list,
    from where intervals will be removed.
    :return: dict[dict] | dict - not necessarily, original dict is edited
    """
    orig_dict_deep_copy = copy.deepcopy(enrollment_intervals)
    time_loss_max_limit = timedelta(minutes=int(time_loss_max_limit))

    for key, value in orig_dict_deep_copy.items():
        slot_time_loss = orig_dict_deep_copy[key].get("slot time loss")
        if slot_time_loss > time_loss_max_limit:
            enrollment_intervals.pop(key)
    return enrollment_intervals
