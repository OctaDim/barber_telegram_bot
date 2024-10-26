from datetime import timedelta, datetime

from aiogram.fsm.context import FSMContext


async def get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from: FSMContext | dict
) -> dict:
    if isinstance(fsm_state_or_dict_from, FSMContext):
        # if state was passed as FSMContext obj getting dictionary from it
        state_data = await fsm_state_or_dict_from.get_data()
    else:
        # if state argument was passed as dictionary, dictionary used
        state_data = fsm_state_or_dict_from

        state_data = state_data if state_data is not None else {}

    return state_data


async def get_valid_list_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> list:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    valid_list = state_data.get(fsm_state_literal_key)
    valid_list = valid_list if valid_list is not None else []
    return valid_list


async def get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> dict:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    valid_dict = state_data.get(fsm_state_literal_key)
    valid_dict = valid_dict if valid_dict is not None else {}
    return valid_dict


async def get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> timedelta:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    valid_timedelta = state_data.get(fsm_state_literal_key)
    if valid_timedelta is None:
        valid_timedelta = timedelta(0)
    return valid_timedelta


async def get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> float:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    valid_float = state_data.get(fsm_state_literal_key)
    valid_float = valid_float if valid_float is not None else float()
    return valid_float


async def get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> int:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    valid_int = state_data.get(fsm_state_literal_key)
    valid_int = valid_int if valid_int is not None else int()
    return valid_int


async def get_valid_datetime_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> datetime:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    valid_datetime = state_data.get(fsm_state_literal_key)
    if valid_datetime is None:
        valid_datetime = datetime.now()
    return valid_datetime
