from math import sin, cos, sqrt

from shared import (
    D0,
    DELTA_T,
    Flight,
    Point,
    Role,
    distanceBetween,
    draw,
    findQAngle,
)
from targeting import UpdatePointOnLine, UpdatePointOnCircle


def updateInterceptorPoint(aim: Role, interceptor: Role, t):
    """
    Обновляет позицию перехватчика для движения к цели.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика, чья траектория обновляется
    """
    s = interceptor.velocity * t
    y = (aim.trajectory[-1].y - aim.trajectory[-2].y) + interceptor.trajectory[-1].y
    x = sqrt(abs(s**2 - y**2))  # + interceptor.trajectory[-1].x
    interceptor.trajectory.append(Point(x, y))


def overloadForParellelConvergence(aim: Role, interceptor: Role, q: float) -> float:
    """
    Вычисляет необходимую перегрузку для параллельного сближения.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика
        q (float): Угол между векторами скорости цели и перехватчика

    Returns:
        float: Значение необходимой перегрузки
    """
    K = interceptor.velocity / aim.velocity
    n: float = abs((K * cos(q)) / sqrt(K**2 - sin(q) ** 2))
    return n


def fight(aim: Role, interceptor: Role, center: Point, start: Point, d: int) -> Flight:
    """
    Моделирует процесс перехвата цели параллельным сближением.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика

    Returns:
        Flight: Объект с данными о полете (траектория, перегрузки, расстояния и т.д.)
    """
    t = DELTA_T  # начальное время
    step: int = 0  # счетчик шагов
    flight = Flight([], 0, [], [], [0], [])
    distance = D0

    # Пока расстояние между целью и перехватчиком больше 200 м
    while distance > d:
        distance = distanceBetween(aim.trajectory[-1], interceptor.trajectory[-1])
        draw(aim, interceptor, step)
        UpdatePointOnCircle(aim, t, center, start)
        updateInterceptorPoint(aim, interceptor, t)
        qi = findQAngle(aim, interceptor)

        flight.n.append(overloadForParellelConvergence(aim, interceptor, qi))
        flight.d.append(distance)
        flight.q.append(qi)
        flight.t.append(t)
        t += DELTA_T
        step += 1

    flight.steps = step
    return flight


def lineFight(aim: Role, interceptor: Role, d: int) -> Flight:
    """
    Моделирует процесс перехвата цели параллельным сближением.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика

    Returns:
        Flight: Объект с данными о полете (траектория, перегрузки, расстояния и т.д.)
    """
    t = DELTA_T  # начальное время
    step: int = 0  # счетчик шагов
    flight = Flight([], 0, [], [], [0], [])
    distance = D0

    # Пока расстояние между целью и перехватчиком больше 200 м
    while distance > d:
        distance = distanceBetween(aim.trajectory[-1], interceptor.trajectory[-1])
        draw(aim, interceptor, step)
        UpdatePointOnLine(aim, t)
        updateInterceptorPoint(aim, interceptor, t)
        qi = findQAngle(aim, interceptor)

        flight.n.append(overloadForParellelConvergence(aim, interceptor, qi))
        flight.d.append(distance)
        flight.q.append(qi)
        flight.t.append(t)
        t += DELTA_T
        step += 1

    flight.steps = step
    return flight
