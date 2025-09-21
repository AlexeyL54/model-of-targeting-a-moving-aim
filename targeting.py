from shared import R, D0, Q0, DELTA_T, Point, Role
from math import sin, cos, pi, sqrt

"""
@brief Обновляет позицию цели, движущейся по круговой окружности
@param aim - объект цели
@param t - текущее время
@return None
"""


def UpdatePointOnCircle(aim: Role, t: float):
    # Угловая скорость: ω = v / r (рад/с)
    omega = aim.velocity / R
    # Параметрические уравнения окружности: x = r*cos(ωt), y = r*sin(ωt)
    x = R * cos(omega * t)
    y = R * sin(omega * t)
    aim.trajectory.append(Point(x, y))


"""
@brief Обновляет позицию цели, движущейся по прямой
@param aim - объект цели
@param t - текущее время
@return None
"""


def UpdatePointOnLine(aim: Role, t: float):
    QR = Q0 * pi / 180
    s = aim.velocity * t
    x = s * cos(QR) + D0
    y = s * sin(QR)
    aim.trajectory.append(Point(x, y))


"""
@brief Обновляет позицию перехватчика, движущегося к цели
@param interceptor - объект перехватчика
@param aim - объект цели
@return None
"""


def updateInterceptorPoint(interceptor: Role, aim: Role):
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
    if aim.trajectory and interceptor.trajectory:
        Q = q * pi / 180
        G = 9.8
        delta_x2 = aim.trajectory[-1].x ** 2 - interceptor.trajectory[-1].x ** 2
        delta_y2 = aim.trajectory[-1].y ** 2 - interceptor.trajectory[-1].y ** 2
        D = sqrt(delta_x2 + delta_y2)
        try:
            n: float = (interceptor.velocity * aim.velocity * sin(Q)) / (G * D)
        except ZeroDivisionError:
            n: float = 0
    else:
        n: float = 0
    return n


def overloadCircleTargeting(aim: Role, interceptor: Role, q: float) -> float:
    if aim.trajectory and interceptor.trajectory:
        Q = q * pi / 180
        G = 9.8
        delta_x2 = aim.trajectory[-1].x ** 2 - interceptor.trajectory[-1].x ** 2
        delta_y2 = aim.trajectory[-1].y ** 2 - interceptor.trajectory[-1].y ** 2
        D = sqrt(delta_x2 + delta_y2)
        try:
            n: float = (interceptor.velocity * aim.velocity * sin(Q)) / (G * D)
        except ZeroDivisionError:
            n: float = 0
    else:
        n: float = 0
    return n
