from math import sin, cos, pi, sqrt, asin

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
from targeting import UpdatePointOnCircle


def updateAimPoint(aim: Role, q: float):
    """
    Обновляет позицию цели на основе угла курса.

    Args:
        aim (Role): Объект цели, чья траектория обновляется
        q (float): Угол курса в градусах
    """
    if aim.trajectory:
        Q = q * pi / 180
        S = aim.velocity * DELTA_T
        x = S * cos(Q) + aim.trajectory[-1].x
        y = S * sin(Q) + aim.trajectory[-1].y
        aim.trajectory.append(Point(x, y))


def updateInterceptorPoint(aim: Role, interceptor: Role):
    """
    Обновляет позицию перехватчика для движения к цели.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика, чья траектория обновляется
    """
    q = findQAngle(aim, interceptor)
    phi = asin((aim.velocity * sin(q)) / interceptor.velocity)
    S = interceptor.velocity * DELTA_T
    x = S * cos(phi) + interceptor.trajectory[-1].x
    y = S * sin(phi) + interceptor.trajectory[-1].y
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


def fight(aim: Role, interceptor: Role) -> Flight:
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
    flight = Flight([], 0, [], [], [], [])
    distance = D0

    # Цикл продолжается до тех пор, пока угол коррекции не станет равным 0
    while distance > 200:
        distance = distanceBetween(aim.trajectory[-1], interceptor.trajectory[-1])
        draw(aim, interceptor, step)
        updateInterceptorPoint(aim, interceptor)
        UpdatePointOnCircle(aim, t)
        qi = findQAngle(aim, interceptor)

        flight.n.append(overloadForParellelConvergence(aim, interceptor, qi))
        flight.d.append(distance)
        flight.q.append(qi)
        flight.t.append(t)
        t += DELTA_T
        step += 1

    flight.steps = step
    return flight
