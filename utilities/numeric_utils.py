def number_or_str_to_integer(number_or_str_number: int | float | str,
                             positive: bool = False) -> int | None:
    if number_or_str_number is None:
        return int(0)

    try:
        number_or_str_number = str(number_or_str_number).strip()
        number_or_str_number = number_or_str_number.replace(",", ".")

        intermediate_float_number = float(number_or_str_number)

        integer_number = int(intermediate_float_number)
        integer_number = abs(integer_number) if positive else integer_number

    except (TypeError, ValueError) as error:
        print(f"\tERROR INFO: {error}")

    else:
        return integer_number


def number_or_str_to_float(number_or_str_number: int | float | str,
                           positive: bool = False) -> float | None:
    if number_or_str_number is None:
        return float(0)

    try:
        number_or_str_number = str(number_or_str_number).strip()
        number_or_str_number = number_or_str_number.replace(",", ".")

        float_number = float(number_or_str_number)
        float_number = abs(float_number) if positive else float_number

    except (TypeError, ValueError) as error:
        print(f"\tERROR INFO: {error}")

    else:
        return float_number
