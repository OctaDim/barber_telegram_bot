from aiogram.fsm.state import StatesGroup, State


class EnrolledCategoriesState(StatesGroup):
    selected_category_id = State()  # for containing int
    current_page_number_of_categories = State()  # for containing int
    paginated_categories_records = State()  # for containing dict[list]
