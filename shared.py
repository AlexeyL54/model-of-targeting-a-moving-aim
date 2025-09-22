from math import sqrt, acos
import matplotlib.pyplot as plt
from dataclasses import dataclass

D0 = 2500  # начальное расстояние между целью и перехватчиком (м)
Y0 = 0  #  начальное расстояние между целью по оси Y (м)
R = 2500  # радиус траектории движения цели (м)
AIM_VELOCITY = 250  # скорость движения цели (м / c)
INTERCEPTOR_VELOCITY = 400  # скорость движения перехватчика (м / с)
DELTA_T = 1  # время между корректировкой (с)
Q0 = 90  # начальный угол ракурса цели


"""Класс для представления точки в 2D пространстве"""


@dataclass
class Point:
    x: float
    y: float


"""Класс для представления роли (цели или перехватчика)"""


@dataclass
class Role:
    velocity: float
    trajectory: list[Point]


@dataclass
class Flight:
    n: list[float]
    steps: int


def draw(aim: Role, interceptor: Role, i: int):
    indent = 50  # отступ для букв от точек

    if len(interceptor.trajectory) > 1:
        # Отрисовка траектории перехватчика между предыдущей и текущей точками
        line_x = [interceptor.trajectory[i - 1].x, interceptor.trajectory[i].x]
        line_y = [interceptor.trajectory[i - 1].y, interceptor.trajectory[i].y]
        plt.plot(line_x, line_y, color="black", linewidth=1.5)

    if aim.trajectory and interceptor.trajectory:
        # Отрисовка линии визирования (перехватчик-цель)
        line_x = [interceptor.trajectory[-1].x, aim.trajectory[-1].x]
        line_y = [interceptor.trajectory[-1].y, aim.trajectory[-1].y]
        plt.plot(line_x, line_y, color="black", linewidth=0.5)

    # Отрисовка точки перехватчика с меткой
    plt.plot(
        interceptor.trajectory[i].x,
        interceptor.trajectory[i].y,
        marker=".",
        color="black",
    )
    plt.text(
        interceptor.trajectory[i].x, interceptor.trajectory[i].y + indent, "П" + str(i)
    )

    # Отрисовка точки цели с меткой
    plt.plot(aim.trajectory[i].x, aim.trajectory[i].y, marker="*", color="red")
    plt.text(aim.trajectory[i].x, aim.trajectory[i].y + indent, "Ц" + str(i))


def angleBetween(vec1: Point, vec2: Point) -> float:
    vec1_len = sqrt(vec1.x**2 + vec1.y**2)
    vec2_len = sqrt(vec2.x**2 + vec2.y**2)
    try:
        cos_angle = (vec1.x * vec2.x + vec1.y * vec2.y) / (vec1_len * vec2_len)
    except ZeroDivisionError:
        cos_angle = 0
    return acos(cos_angle)


"""
@brief Вычисляет угол коррекции между направлением на цель и направлением движения перехватчика
@param aim - объект цели
@param interceptor - объект перехватчика
@return Угол коррекции в радианах или -1 при ошибке
"""


def correctionAngle(aim: Role, interceptor: Role):
    if len(interceptor.trajectory) > 1:
        # Вектор от предыдущей позиции перехватчика к текущей позиции цели
        d_vec_x = aim.trajectory[-1].x - interceptor.trajectory[-2].x
        d_vec_y = aim.trajectory[-1].y - interceptor.trajectory[-2].y

        # Вектор перемещения перехватчика (от предыдущей к текущей позиции)
        inter_vec_x = interceptor.trajectory[-1].x - interceptor.trajectory[-2].x
        inter_vec_y = interceptor.trajectory[-1].y - interceptor.trajectory[-2].y

        # Длины векторов
        d_vec_len = sqrt(d_vec_x**2 + d_vec_y**2)
        inter_vec_len = sqrt(inter_vec_x**2 + inter_vec_y**2)

        # Косинус угла между векторами через скалярное произведение: cosθ = (a·b)/(|a||b|)
        cos_corr_angle = ((d_vec_x * inter_vec_x) + (d_vec_y * inter_vec_y)) / (
            d_vec_len * inter_vec_len
        )

        # Проверка корректности значения косинуса (должен быть в диапазоне [-1, 1])
        if cos_corr_angle >= -1 and cos_corr_angle <= 1:
            return round(acos(cos_corr_angle), 1)  # Возвращаем угол в радианах
        else:
            return -1


"""
@brief Отрисовывает линию поражения цели
@param aim - объект цели
@param interceptor - объект перехватчика
@return None
"""


def destroy(aim: Role, interceptor: Role):
    # Отрисовка линии от предпоследней позиции перехватчика к предпоследней позиции цели
    line_x = [interceptor.trajectory[-2].x, aim.trajectory[-2].x]
    line_y = [interceptor.trajectory[-2].y, aim.trajectory[-2].y]
    plt.plot(line_x, line_y, color="black", linewidth="1.5")
    plt.plot(aim.trajectory[-2].x, aim.trajectory[-2].y, color="orange", marker="X")


def distanceBetween(p1: Point, p2: Point) -> float:
    delta_x = p2.x - p1.x
    delta_y = p2.y - p2.y
    return sqrt(delta_x**2 + delta_y**2)


def makeVector(p1: Point, p2: Point) -> Point:
    x = p2.x - p1.x
    y = p2.y - p1.x
    return Point(x, y)


def findQAngle(aim: Role, interceptor: Role):
    if len(interceptor.trajectory) > 1 and len(aim.trajectory) > 1:
        vision_vec = makeVector(interceptor.trajectory[-1], aim.trajectory[-1])
        aim_moving_vec = makeVector(aim.trajectory[-2], aim.trajectory[-1])
        q = angleBetween(vision_vec, aim_moving_vec)
    else:
        q = Q0
    return q


def saveFig(path: str):
    # Настройка и сохранение графика
    plt.xlabel("x, М")
    plt.ylabel("y, М")
    plt.savefig(path)
    plt.clf()
