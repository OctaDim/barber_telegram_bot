from typing import Union, Sized


def create_paginated_elems(all_elements: Sized,
                           elements_per_page: Union[int, 0, None] = 0,
                           ) -> dict:
    paginated_elements_dict = {}

    if not elements_per_page or not isinstance(all_elements, Sized):
        paginated_elements_dict[1] = all_elements
    else:
        page_number = 1
        for index in range(0, len(all_elements), elements_per_page):
            per_page_slice = all_elements[index: index + elements_per_page]
            paginated_elements_dict[page_number] = per_page_slice
            page_number += 1

    return paginated_elements_dict
