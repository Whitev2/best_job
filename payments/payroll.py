from DataBase.base import User

user = User()


async def salary(telegram_id: str, count):
    car_mass = await user.get_car_mass(telegram_id)
    sum_start = 0
    x_other = 0
    if car_mass[0][0] == '2.5':
        sum_start = 1500
        x_other = 750
    elif car_mass[0][0] == '5':
        sum_start = 1500
        x_other = 750
    elif car_mass[0][0] == '10':
        sum_start = 1500
        x_other = 750

    if count >= 2:
        point = count - 1
        sum_of_point = point * x_other
        return float(sum_of_point + sum_start)
    else:
        return sum_start
