from datetime import timedelta

from sqlalchemy import Row


def get_available_enrollment_intervals(
        slots_records: list[Row],
        selected_services_duration: timedelta) -> dict[dict] | dict:
    if not slots_records:
        return {}

    enrollment_intervals = {}
    all_slots_number = len(slots_records)

    for start_index in range(all_slots_number):
        temp_interval_slots = [slots_records[start_index].id]
        first_slot_time_start = slots_records[start_index].time_start
        first_slot_time_end = slots_records[start_index].time_end
        temp_interval_duration = slots_records[start_index].slot_duration

        if temp_interval_duration >= selected_services_duration:
            time_loss = temp_interval_duration - selected_services_duration
            client_time_end = first_slot_time_end - time_loss
            first_slot_id = slots_records[start_index].id

            enrollment_intervals[first_slot_id] = {
                "first slot id": slots_records[start_index].id,
                "all slots ids": temp_interval_slots,
                "slot time start": first_slot_time_start,
                "slot time end": first_slot_time_end,
                "client time end": client_time_end,
                "all slots duration": temp_interval_duration,
                "selected services duration": selected_services_duration,
                "slot time loss": time_loss}
            continue

        for cur_index in range(start_index + 1, all_slots_number):
            temp_interval_slots.append(slots_records[cur_index].id)
            cur_slot_time_start = slots_records[cur_index].time_start
            cur_slot_time_end = slots_records[cur_index].time_end
            cur_slot_duration = slots_records[cur_index].slot_duration
            prior_slot_time_end = slots_records[cur_index].prior_slot_time_end

            if cur_slot_time_start != prior_slot_time_end:
                break

            if cur_slot_time_start == prior_slot_time_end:
                temp_time_start = first_slot_time_start
                temp_time_end = cur_slot_time_end
                temp_interval_duration += cur_slot_duration

                if temp_interval_duration >= selected_services_duration:
                    time_loss = temp_interval_duration - selected_services_duration
                    client_time_end = temp_time_end - time_loss
                    first_slot_id = slots_records[start_index].id

                    enrollment_intervals[first_slot_id] = {
                        "first slot id": slots_records[start_index].id,
                        "all slots ids": temp_interval_slots,
                        "slot time start": temp_time_start,
                        "slot time end": temp_time_end,
                        "client time end": client_time_end,
                        "all slots duration": temp_interval_duration,
                        "selected services duration": selected_services_duration,
                        "slot time loss": time_loss}
                    break

    return enrollment_intervals

# ##################### TEST CODE ######################################
# ######################################################################
# year = 2024
# month = 10
# day = 31
# test_date = datetime(year=year, month=month, day=day)
# slot_records = get_slots_from_now_for_date(required_date=test_date,
#                                            master_id=None)
# for record in slot_records:
#     print(f"{record.id}\t\t"
#           f"{record.day_of_month}\t\t"
#           f"{record.master_id}\t\t"
#           f"{record.active}\t\t"
#           f"{record.reserved}\t\t"
#           f"{record.time_start}\t\t"
#           f"{record.time_end}\t\t"
#           f"{record.slot_duration}\t\t"
#           f"{record.continuing}\t\t"
#           f"{record.prior_slot_time_end}\t\t")
# print()
# duration_list = [
#     timedelta(hours=0, minutes=38),
#     # timedelta(minutes=0),
#     # timedelta(minutes=5),
#     # timedelta(minutes=15),
#     # timedelta(minutes=16),
#     # timedelta(minutes=45),
#     # timedelta(minutes=46),
#     # timedelta(minutes=60),
#     # timedelta(minutes=61),
#     # timedelta(minutes=120),
#     # timedelta(minutes=121),
#     # timedelta(minutes=600),
#     # timedelta(minutes=1440)
# ]
# for duration in duration_list:
#     all_enrollment_intervals = get_available_enrollment_intervals(
#         slots_records=slot_records, selected_services_duration=duration)
#     print("#" * 100)
#     print(f"##### TEST TIME {duration}")
#     print("#" * 100)
#     for available_interval in all_enrollment_intervals:
#         for key, value in available_interval.items():
#             print(key, value)
#         print()
#     print()
# ######################################################################
# ##################### END TEST CODE ##################################
