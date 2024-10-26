from datetime import timedelta
import copy


def remove_intervals_over_time_loss_limit(
        time_loss_max_limit: int,
        enrollment_intervals: list[dict]) -> None:
    """
    Removes intervals by time loss max limit. Removing is executed
    in the origin list passed as argument
    :param time_loss_max_limit: int - Max loss time limit in minutes
    :param enrollment_intervals: list[dict] - Original list, from where
    intervals will be removed.
    :return: None
    """
    orig_list_deep_copy = copy.deepcopy(enrollment_intervals)
    time_loss = timedelta(minutes=int(time_loss_max_limit))

    for index in range(len(orig_list_deep_copy) - 1, -1, -1):
        if orig_list_deep_copy[index].get("slot time loss") >= time_loss:
            enrollment_intervals.pop(index)
    return None
