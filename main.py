import matplotlib.pyplot as plt
import targeting
import parallel
from shared import (
    Q0,
    D0,
    DELTA_T,
    AIM_VELOCITY,
    INTERCEPTOR_VELOCITY,
    Role,
    Point,
    correctionAngle,
    draw,
    destroy,
)


"""
@brief Основной цикл моделирования погони
@param aim - объект цели
@param interceptor - объект перехватчика
@return None
"""


def fight(aim: Role, interceptor: Role) -> int:
    t = DELTA_T  # начальное время
    step: int = 0  # счетчик шагов
    n: list[float]
    q = Q0

    # Цикл продолжается до тех пор, пока угол коррекции не станет равным 0
    while correctionAngle(aim, interceptor) != 0:
        # targeting.updateInterceptorPoint(interceptor, aim)
        parallel.updateInterceptorPoint(aim, interceptor, q)
        draw(aim, interceptor, step)
        parallel.updateAimPoint(aim, q)
        # targeting.UpdatePointOnCircle(aim, t)
        # targeting.UpdatePointOnLine(aim, t)

        t += DELTA_T
        step += 1
        q += 10

    destroy(aim, interceptor)
    return step


"""
@brief Основная функция программы
@return None
"""


def main():
    # Инициализация цели и перехватчика с начальными позициями для движения

    # Случай, когда цель двигается по окружности
    circle_aim = Role(AIM_VELOCITY, [Point(D0, 0)])
    circle_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)])

    # Случай, когда цель двигается по прямой
    line_aim = circle_aim
    line_interceptor = circle_interceptor

    # Запуск моделирования погони
    steps: int = parallel.fight(circle_aim, circle_interceptor)
    print(f"Цель, двигающаяся по окружности сбита за {steps} шагов")

    # Настройка и сохранение графика
    plt.xlabel("x, М")
    plt.ylabel("y, М")
    plt.savefig("погоня_окружность.pdf")


if __name__ == "__main__":
    main()
