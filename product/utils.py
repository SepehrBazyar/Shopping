def readable(price: int) -> str:
    """
    Make Read Able Number for Show Prices in Template Pages
    """

    digits, answer = str(price), []
    for digit in range(len(digits) - 1, -1, -3):
        result = ""
        if int(digits[digit - 2]) >= 0: result += digits[digit - 2]
        if int(digits[digit - 1]) >= 0: result += digits[digit - 1]
        if int(digits[digit]) >= 0: result += digits[digit]
        answer.append(result)
    return '/'.join(answer[::-1])
