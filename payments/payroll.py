async def salary(count):
    x_one = 1500
    x_other = 750
    if count >= 2:
        point = count - 1
        sum_of_point = point * x_other
        sum_start = x_one
        return float(sum_of_point + sum_start)
    else:
        return x_one
