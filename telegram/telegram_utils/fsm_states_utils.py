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
        fsm_state_or_state_dict: FSMContext | dict,
        fsm_state_literal_key: str
) -> list:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_state_dict)

    interim_list = state_data.get(fsm_state_literal_key)
    valid_list = [] if interim_list is None else interim_list
    return valid_list


async def get_valid_dict_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> dict:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    interim_dict = state_data.get(fsm_state_literal_key)
    valid_dict = {} if interim_dict is None else interim_dict
    # valid_dict = valid_dict if valid_dict is not None else {}
    return valid_dict


async def get_valid_timedelta_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> timedelta:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    interim_timedelta = state_data.get(fsm_state_literal_key)
    if interim_timedelta is None:
        valid_timedelta = timedelta(0)
    else:
        valid_timedelta = interim_timedelta

    return valid_timedelta


async def get_valid_float_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> float:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    interim_float = state_data.get(fsm_state_literal_key)
    valid_float = float() if interim_float is None else interim_float
    # valid_float = valid_float if valid_float is not None else float()
    return valid_float


async def get_valid_int_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> int:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    interim_int = state_data.get(fsm_state_literal_key)
    valid_int = int() if interim_int is None else interim_int
    # valid_int = valid_int if valid_int is not None else int()
    return valid_int


async def get_valid_datetime_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> datetime:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    interim_datetime = state_data.get(fsm_state_literal_key)
    if interim_datetime is None:
        valid_datetime = datetime.now()
    else:
        valid_datetime = interim_datetime

    return valid_datetime


async def get_valid_str_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> str:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    interim_str = state_data.get(fsm_state_literal_key)
    valid_str = "" if interim_str is None else interim_str
    return valid_str


async def get_valid_bool_by_fsm_state_key(
        fsm_state_or_dict_from: FSMContext | dict,
        fsm_state_literal_key: str
) -> bool:
    state_data = await get_valid_state_data_from_fsm_state(
        fsm_state_or_dict_from)

    interim_bool = state_data.get(fsm_state_literal_key)
    valid_bool = False if interim_bool is None else interim_bool
    return valid_bool
