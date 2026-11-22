from datetime import datetime
from decimal import Decimal
from math import isfinite

FORMAT = "%H:%M:%S"
WEIGHT = 75
HEIGHT = 177
# Коэффициенты и длина шага из учебного задания.
K_1 = 0.035
K_2 = 0.029
STEP_M = 0.65

storage_data = {}



def check_correct_data(data):
    if not isinstance(data, tuple) or len(data) != 2:
        return False
    time, steps = data
    return isinstance(time, str) and bool(time) and type(steps) is int and steps >= 0


def check_correct_time(time):
    try:
        current = datetime.strptime(time, FORMAT).time()
    except ValueError:
        return False
    return not storage_data or current.strftime(FORMAT) > max(storage_data)


def get_step_day(steps):
    return sum(storage_data.values()) + steps


def get_distance(steps):
    return steps * STEP_M / 1000


def get_spent_calories(dist, current_time, *, weight=WEIGHT, height=HEIGHT):
    time = datetime.strptime(current_time, FORMAT).time()
    hours = time.hour + time.minute / 60 + time.second / 3600
    if hours == 0:
        return 0.0
    speed = dist / hours
    return (K_1 * weight + speed ** 2 / height * K_2 * weight) * hours * 60


def get_achievement(dist):
    if dist >= 6.5:
        return "Отличный результат! Цель достигнута."
    if dist >= 3.9:
        return "Неплохо! День был продуктивный"
    if dist >= 2:
        return "Завтра наверстаем!"
    return "Лежать тоже полезно. Главное — участие, а не победа!"


def show_message(time, steps, distance, calories, achievement):
    print(
        f"\nВремя: {time}.\n"
        f"Количество шагов за сегодня: {steps}.\n"
        f"Дистанция составила {Decimal(str(distance)):.2f} км.\n"
        f"Вы сожгли {calories:.2f} ккал.\n"
        f"{achievement}\n"
    )


def accept_package(package, *, weight=WEIGHT, height=HEIGHT):
    if not check_correct_data(package):
        return storage_data

    time, steps = package
    if not check_correct_time(time):
        return storage_data

    time = datetime.strptime(time, FORMAT).strftime(FORMAT)
    total_steps = get_step_day(steps)
    distance = get_distance(total_steps)
    calories = get_spent_calories(distance, time, weight=weight, height=height)
    storage_data[time] = steps
    show_message(time, total_steps, distance, calories, get_achievement(distance))
    return storage_data


def reset_day():
    """Start a new day when the caller detects a date change."""
    storage_data.clear()


def read_positive_number(prompt):
    while True:
        raw_value = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw_value)
        except ValueError:
            print("Введите число, например 75 или 75,5.")
            continue
        if isfinite(value) and value > 0:
            return value
        print("Введите конечное число больше нуля.")


if __name__ == "__main__":
    height = read_positive_number("Введите рост в сантиметрах: ")
    weight = read_positive_number("Введите вес в килограммах: ")
    accept_package(("9:00:00", 1000), weight=weight, height=height)
    accept_package(("09:30:00", 500), weight=weight, height=height)
