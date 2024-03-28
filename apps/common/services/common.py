from decimal import Decimal


def remove_exponent_from_decimal(num: Decimal) -> Decimal:
    if not isinstance(num, Decimal):
        return num

    return num.to_integral() if num == num.to_integral() else num.normalize()
