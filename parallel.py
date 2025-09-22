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
    if aim.trajectory:
        Q = q * pi / 180
        S = aim.velocity * DELTA_T
        x = S * cos(Q) + aim.trajectory[-1].x
        y = S * sin(Q) + aim.trajectory[-1].y
        aim.trajectory.append(Point(x, y))


def updateInterceptorPoint(aim: Role, interceptor: Role):
    q = findQAngle(aim, interceptor)
    phi = asin((aim.velocity * sin(q)) / interceptor.velocity)
    S = interceptor.velocity * DELTA_T
    x = S * cos(phi) + interceptor.trajectory[-1].x
    y = S * sin(phi) + interceptor.trajectory[-1].y
    interceptor.trajectory.append(Point(x, y))


def overloadForParellelConvergence(aim: Role, interceptor: Role, q: float) -> float:
    K = interceptor.velocity / aim.velocity
    n: float = (K * cos(q)) / sqrt(K**2 - sin(q) ** 2)
    return n


def fight(aim: Role, interceptor: Role) -> Flight:
    t = DELTA_T  # начальное время
    step: int = 0  # счетчик шагов
    n: list[float] = []
    distance = D0

    # Цикл продолжается до тех пор, пока угол коррекции не станет равным 0
    while distance > 200:
        distance = distanceBetween(aim.trajectory[-1], interceptor.trajectory[-1])
        draw(aim, interceptor, step)
        updateInterceptorPoint(aim, interceptor)
        UpdatePointOnCircle(aim, t)
        q = findQAngle(aim, interceptor)
        n.append(overloadForParellelConvergence(aim, interceptor, q))

        t += DELTA_T
        step += 1

    flight = Flight(n, step)
    return flight
