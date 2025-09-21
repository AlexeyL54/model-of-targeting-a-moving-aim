from math import sin, cos, pi, sqrt, asin

from shared import (
    D0,
    Q0,
    DELTA_T,
    Point,
    Role,
    angleBetween,
    distanceBetween,
    draw,
)
from targeting import UpdatePointOnCircle


def updateAimPoint(aim: Role, q: float):
    if aim.trajectory:
        Q = q * pi / 180
        S = aim.velocity * DELTA_T
        x = S * cos(Q) + aim.trajectory[-1].x
        y = S * sin(Q) + aim.trajectory[-1].y
        aim.trajectory.append(Point(x, y))


def updateInterceptorPoint(aim: Role, interceptor: Role, q: float):
    if len(aim.trajectory) > 1 and len(interceptor.trajectory) > 1:
        vision_vec_x = interceptor.trajectory[0].x - aim.trajectory[0].x
        vision_vec_y = interceptor.trajectory[0].y - aim.trajectory[0].y

        aim_moving_vec_x = aim.trajectory[-2].x - aim.trajectory[-1].x
        aim_moving_vec_y = aim.trajectory[-2].y - aim.trajectory[-1].y

        vision_vec = Point(vision_vec_x, vision_vec_y)
        aim_moving_vec = Point(aim_moving_vec_x, aim_moving_vec_y)

        q = angleBetween(vision_vec, aim_moving_vec) + (pi / 2)
    else:
        q = Q0

        # Q = q * pi / 180
        phi = asin((aim.velocity * sin(q)) / interceptor.velocity)
        S = interceptor.velocity * DELTA_T
        x = S * cos(phi) + interceptor.trajectory[-1].x
        y = S * sin(phi) + interceptor.trajectory[-1].y
        interceptor.trajectory.append(Point(x, y))


def overloadForParellelConvergence(aim: Role, interceptor: Role, q: float) -> float:
    K = interceptor.velocity / aim.velocity
    n: float = (K * cos(q)) / sqrt(K**2 - sin(q) ** 2)
    return n


def fight(aim: Role, interceptor: Role):
    t = DELTA_T  # начальное время
    step: int = 0  # счетчик шагов
    #  n: list[float]
    q = Q0
    distance = D0

    # Цикл продолжается до тех пор, пока угол коррекции не станет равным 0
    while distance > 200:
        distance = distanceBetween(aim.trajectory[-1], interceptor.trajectory[-1])
        draw(aim, interceptor, step)
        updateInterceptorPoint(aim, interceptor, q)
        # updateAimPoint(aim, q)
        UpdatePointOnCircle(aim, t)

        t += DELTA_T
        step += 1
        q += 8

    return step
