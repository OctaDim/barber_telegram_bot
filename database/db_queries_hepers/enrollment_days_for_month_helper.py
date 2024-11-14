from datetime import timedelta

from database.db_models.work_time_model import WorkTime
from utilities.list_utils import remove_list_duplicates


def get_enrollment_days_helper(slots_records: list[WorkTime],
                               selected_services_duration: timedelta,
                               time_loss_max_limit: int
                               ) -> list[int]:
    if not slots_records:
        return []

    time_loss_max_limit = timedelta(minutes=int(time_loss_max_limit))

    enrollment_days = []
    all_slots_number = len(slots_records)

    for start_index in range(all_slots_number):
        day_of_month = slots_records[start_index].day_of_month
        temp_interval_duration = slots_records[start_index].slot_duration
        slot_time_loss = temp_interval_duration - selected_services_duration

        if temp_interval_duration >= selected_services_duration:
            if slot_time_loss <= time_loss_max_limit:
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
                slot_time_loss = temp_interval_duration - selected_services_duration

                if temp_interval_duration >= selected_services_duration:
                    if slot_time_loss <= time_loss_max_limit:
                        enrollment_days.append(day_of_month)
                    break

    enrollment_days = remove_list_duplicates(enrollment_days)
    return enrollment_days

# ##################### TEST CODE ######################################
# ######################################################################
#
# all_slots_records_by_month = get_slots_from_now_for_month_query(
#     year=2024,
#     month=11,
#     # master_id=1,
#     # masters_ids_list=[1],
#     masters_ids_list=[1, 2, 3],
#     order_by_fields=("master_id", "time_start"),
#     active=True,
#     reserved=False,
#     admin_only=False,
# )
# for record in all_slots_records_by_month:
#     print(f"{record.id}\t\t"
#           f"{record.day_of_month}\t\t"
#           f"{record.master_id}\t\t"
#           # f"{record.active}\t\t"
#           # f"{record.reserved}\t\t"
#           f"{record.time_start}\t\t"
#           f"{record.time_end}\t\t"
#           f"{record.slot_duration}\t\t"
#           f"{record.prior_slot_time_end}\t\t\t\t\t"
#           f"{record.slots_time_continuing}\t\t"
#           # f"{record.master_id_continuing}\t\t"
#           )
# print()
# duration_list = [
#     # timedelta(minutes=0),
#     # timedelta(minutes=5),
#     timedelta(minutes=15),
#     # timedelta(minutes=16),
#     # timedelta(minutes=60),
#     # timedelta(minutes=61),
#     # timedelta(minutes=120),
#     # timedelta(minutes=310),
#     # timedelta(minutes=600),
#     # timedelta(minutes=1400)
# ]
# for duration in duration_list:
#     all_enrollment_days = get_enrollment_days_query_helper(
#         slots_records=all_slots_records_by_month,
#         selected_services_duration=duration,
#         time_loss_max_limit=90)
#     print("##### selected services duration", duration)
#     print("##### all_enrollment_days", all_enrollment_days)
#     print()
# ######################################################################
# ##################### END TEST CODE ##################################
