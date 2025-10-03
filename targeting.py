from shared import (
    R,
    D0,
    Q0,
    DELTA_T,
    Flight,
    Point,
    Role,
    draw,
    correctionAngle,
    findQAngle,
    distanceBetween,
)
from math import sin, cos, pi, sqrt, isclose


def UpdatePointOnCircle(aim: Role, t: float, center: Point, start: Point):
    """
    Обновляет позицию цели, движущейся по круговой траектории.

    Args:
        aim (Role): Объект цели
        t (float): Текущее время
    """
    # Угловая скорость: ω = v / r (рад/с)
    omega = aim.velocity / R
    # Параметрические уравнения окружности: x = r*cos(ωt), y = r*sin(ωt)
    x = R * cos(omega * t + start.x) + center.x
    y = R * sin(omega * t + start.y) + center.y
    aim.trajectory.append(Point(x, y))


def UpdatePointOnLine(aim: Role, t: float):
    """
    Обновляет позицию цели, движущейся по прямой траектории.

    Args:
        aim (Role): Объект цели
        t (float): Текущее время
    """
    QR = Q0 * pi / 180
    s = aim.velocity * t
    x = s * cos(QR) + D0
    y = s * sin(QR)
    aim.trajectory.append(Point(x, y))


def updateInterceptorPoint(interceptor: Role, aim: Role):
    """
    Обновляет позицию перехватчика, движущегося по направлению к цели.

    Args:
        interceptor (Role): Объект перехватчика
        aim (Role): Объект цели
    """
    if interceptor.trajectory and aim.trajectory:
        current_x = interceptor.trajectory[-1].x
        current_y = interceptor.trajectory[-1].y

        # Вектор направления от перехватчика к цели
        vec_x = aim.trajectory[-1].x - current_x
        vec_y = aim.trajectory[-1].y - current_y

        # Длина вектора (расстояние до цели)
        vec_len = sqrt(vec_x**2 + vec_y**2)

        # Нормализация вектора (получение единичного вектора направления)
        norm_vec_x = vec_x / vec_len
        norm_vec_y = vec_y / vec_len

        # Расстояние, которое пролетит перехватчик за время delta_t
        d = interceptor.velocity * DELTA_T

        # Новая позиция перехватчика: текущая позиция + перемещение по направлению к цели
        next_x = norm_vec_x * d + current_x
        next_y = norm_vec_y * d + current_y

        interceptor.trajectory.append(Point(next_x, next_y))


def overloadLineTargeting(aim: Role, interceptor: Role, q: float) -> float:
    """
    Вычисляет необходимую перегрузку для перехвата цели, движущейся по прямой.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика
        q (float): Угол между векторами скорости цели и перехватчика

    Returns:
        float: Значение необходимой перегрузки
    """
    if aim.trajectory and interceptor.trajectory:
        Q = q * pi / 180
        G = 9.8
        delta_x2 = aim.trajectory[-1].x ** 2 - interceptor.trajectory[-1].x ** 2
        delta_y2 = aim.trajectory[-1].y ** 2 - interceptor.trajectory[-1].y ** 2
        D = sqrt(abs(delta_x2 + delta_y2))
        try:
            n: float = (interceptor.velocity * aim.velocity * sin(Q)) / (G * D)
        except ZeroDivisionError:
            n: float = 0
    else:
        n: float = 0
    return n


def overloadCircleTargeting(aim: Role, interceptor: Role, q: float) -> float:
    """
    Вычисляет необходимую перегрузку для перехвата цели, движущейся по окружности.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика
        q (float): Угол между векторами скорости цели и перехватчика

    Returns:
        float: Значение необходимой перегрузки
    """
    n: float = 0
    if aim.trajectory and interceptor.trajectory:
        Q = q * pi / 180
        G = 9.8
        delta_x = aim.trajectory[-1].x - interceptor.trajectory[-1].x
        delta_y = aim.trajectory[-1].y - interceptor.trajectory[-1].y
        D = sqrt(delta_x**2 + delta_y**2)
        try:
            n: float = (interceptor.velocity * abs(aim.velocity) * sin(Q)) / (G * D)
        except ZeroDivisionError:
            n: float = interceptor.velocity**2 / (G * R)
    return n


def circleFight(
    aim: Role, interceptor: Role, center: Point, start: Point, pres: int
) -> Flight:
    """
    Моделирует процесс перехвата цели, движущейся по круговой траектории.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика

    Returns:
        Flight: Объект с данными о полете (траектория, перегрузки, расстояния и т.д.)
    """
    flight = Flight([], 0, [], [], [], [])
    t = DELTA_T  # начальное время
    step: int = 0  # счетчик шагов
    distance = D0
    s = interceptor.velocity * DELTA_T

    # Цикл продолжается до тех пор, пока угол коррекции не станет равным 0
    while True:
        draw(aim, interceptor, step)
        distance = distanceBetween(aim.trajectory[-1], interceptor.trajectory[-1])
        UpdatePointOnCircle(aim, t, center, start)
        updateInterceptorPoint(interceptor, aim)
        qi = findQAngle(aim, interceptor)

        flight.n.append(overloadCircleTargeting(aim, interceptor, qi))
        flight.d.append(distance)
        flight.q.append(qi)
        flight.t.append(t)
        t += DELTA_T
        step += 1
        if correctionAngle(aim, interceptor, pres) == 0 and distance < s:
            break

    flight.steps = step
    return flight


def lineFight(aim: Role, interceptor: Role, pres) -> Flight:
    """
    Моделирует процесс перехвата цели, движущейся по прямой траектории.

    Args:
        aim (Role): Объект цели
        interceptor (Role): Объект перехватчика

    Returns:
        Flight: Объект с данными о полете (траектория, перегрузки, расстояния и т.д.)
    """
    flight = Flight([], 0, [], [], [], [])
    t = DELTA_T  # начальное время
    step: int = 0  # счетчик шагов
    distance = D0
    s = interceptor.velocity * DELTA_T

    # Цикл продолжается до тех пор, пока угол коррекции не станет равным 0
    while True:
        draw(aim, interceptor, step)
        distance = distanceBetween(aim.trajectory[-1], interceptor.trajectory[-1])
        UpdatePointOnLine(aim, t)
        updateInterceptorPoint(interceptor, aim)
        qi = findQAngle(aim, interceptor)

        flight.n.append(overloadLineTargeting(aim, interceptor, qi))
        flight.d.append(distance)
        flight.q.append(qi)
        flight.t.append(t)
        t += DELTA_T
        step += 1
        if correctionAngle(aim, interceptor, pres) == 0 and distance < s:
            break

    flight.steps = step
    return flight
