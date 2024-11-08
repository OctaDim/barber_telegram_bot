from datetime import timedelta

from sqlalchemy import Row

from utilities.list_utils import remove_list_duplicates


def get_available_enrollment_days(slots_records: list[Row],
                                  services_duration: timedelta) -> list[int]:
    if not slots_records:
        return []

    enrollment_days = []
    all_slots_number = len(slots_records)

    for start_index in range(all_slots_number):
        day_of_month = slots_records[start_index].day_of_month
        temp_interval_duration = slots_records[start_index].slot_duration

        if temp_interval_duration >= services_duration:
            enrollment_days.append(day_of_month)
            continue

        for cur_index in range(start_index + 1, all_slots_number):
            cur_slot_time_start = slots_records[cur_index].time_start
            cur_slot_duration = slots_records[cur_index].slot_duration
            prior_slot_time_end = slots_records[cur_index].prior_slot_time_end

            if cur_slot_time_start != prior_slot_time_end:
                break

            if cur_slot_time_start == prior_slot_time_end:
                temp_interval_duration += cur_slot_duration

                if temp_interval_duration >= services_duration:
                    enrollment_days.append(day_of_month)
                    break

    enrollment_days = remove_list_duplicates(enrollment_days)
    return enrollment_days

# ##################### TEST CODE ######################################
# ######################################################################
# year = 2024
# month = 10
# slot_records = get_slots_from_now_for_month(year=year, month=month,
#                                             master_id=None)
# for record in slot_records:
#     print(f"{record.day_of_month}\t\t\t"
#           f"{record.time_start}\t\t\t"
#           f"{record.time_end}\t\t\t"
#           f"{record.slot_duration}\t\t\t"
#           f"{record.continuing}\t\t\t"
#           f"{record.prior_slot_time_end}")
# print()
# duration_list = [
#     # timedelta(minutes=0),
#     # timedelta(minutes=5),
#     # timedelta(minutes=15),
#     # timedelta(minutes=16),
#     # timedelta(minutes=60),
#     # timedelta(minutes=61),
#     # timedelta(minutes=120),
#     timedelta(minutes=310),
#     # timedelta(minutes=600),
#     # timedelta(minutes=1400)
# ]
# for duration in duration_list:
#     all_enrollment_days = get_available_enrollment_days(
#         slots_records=slot_records,
#         services_duration=duration)
#     print("##### selected services duration", duration)
#     print("##### all_enrollment_days", all_enrollment_days)
#     print()
# ######################################################################
# ##################### END TEST CODE ##################################
