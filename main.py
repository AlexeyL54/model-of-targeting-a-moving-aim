from dataclasses import dataclass
from math import sin, cos, sqrt, acos
import matplotlib.pyplot as plt


d0 = 2500  # начальное расстояние между целью и перехватчиком (м)
r = 2500  # радиус траектории движения цели (м)
aim_vel = 250  # скорость движения цели (м / c)
interceptor_vel = 400  # скорость движения перехватчика (м / с)
delta_t = 1  # время между корректировкой (с)


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


"""
@brief Обновляет позицию цели, движущейся по круговой окружности
@param aim - объект цели
@param t - текущее время
@return None
"""
def UpdatePointOnCircle(aim: Role, t):
    # Угловая скорость: ω = v / r (рад/с)
    omega = aim.velocity / r
    # Параметрические уравнения окружности: x = r*cos(ωt), y = r*sin(ωt)
    x = r * cos(omega * t)
    y = r * sin(omega * t)
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
        d = interceptor.velocity * delta_t

        # Новая позиция перехватчика: текущая позиция + перемещение по направлению к цели
        next_x = norm_vec_x * d + current_x
        next_y = norm_vec_y * d + current_y

        interceptor.trajectory.append(Point(next_x, next_y))


"""
@brief Отрисовывает текущее состояние системы
@param aim - объект цели
@param interceptor - объект перехватчика
@param i - номер шага итерации
@return None
"""
def draw(aim: Role, interceptor: Role, i: int):
    indent = 50

    if len(interceptor.trajectory) > 1:
        # Отрисовка траектории перехватчика между предыдущей и текущей точками
        line_x = [interceptor.trajectory[i - 1].x, interceptor.trajectory[i].x]
        line_y = [interceptor.trajectory[i - 1].y, interceptor.trajectory[i].y]
        plt.plot(line_x, line_y, color="black", linewidth=1.5)

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
    plt.text(interceptor.trajectory[i].x, interceptor.trajectory[i].y + indent, "П" + str(i))

    # Отрисовка точки цели с меткой
    plt.plot(aim.trajectory[i].x, aim.trajectory[i].y, marker="*", color="red")
    plt.text(aim.trajectory[i].x, aim.trajectory[i].y + indent, "Ц" + str(i))


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
            return -1  # Некорректное значение


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


"""
@brief Основной цикл моделирования погони
@param aim - объект цели
@param interceptor - объект перехватчика
@return None
"""
def Fight(aim: Role, interceptor: Role):
    t = delta_t  # начальное время
    step: int = 0  # счетчик шагов

    # Цикл продолжается до тех пор, пока угол коррекции не станет равным 0
    while correctionAngle(aim, interceptor) != 0:
        updateInterceptorPoint(interceptor, aim)   
        draw(aim, interceptor, step)
        UpdatePointOnCircle(aim, t)

        t += delta_t
        step += 1

    destroy(aim, interceptor)  # Отрисовываем момент поражения


"""
@brief Основная функция программы
@return None
"""
def main():
    # Инициализация цели и перехватчика с начальными позициями
    aim = Role(aim_vel, [Point(d0, 0)])  # Цель начинается на расстоянии d0 по оси X
    interceptor = Role(interceptor_vel, [Point(0, 0)])  # Перехватчик в начале координат
    
    # Запуск моделирования погони
    Fight(aim, interceptor)
    
    # Настройка и сохранение графика
    plt.xlabel("x, М")
    plt.ylabel("y, М")
    plt.savefig("погоня_окружность.pdf")


if __name__ == "__main__":
    main()
