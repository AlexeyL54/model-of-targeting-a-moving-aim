from scipy.interpolate import interp1d
import targeting
import parallel
from shared import (
    AIM_VELOCITY,
    INTERCEPTOR_VELOCITY,
    D0,
    R,
    Point,
    Role,
    saveFig,
    saveFlightData,
)
import matplotlib.pyplot as plt
import numpy as np
from math import pi


def main():
    # Случай, когда цель двигается по окружности
    circle_aim = Role(AIM_VELOCITY, [Point(D0, 0)], 30, 0)
    circle_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)], -120, 50)
    circle_center = Point(0, 0)
    start_on_circle = Point(0, 0)

    away_circle_aim = Role(-AIM_VELOCITY, [Point(D0, 0)], -50, 50)
    away_circle_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)], -150, 50)
    away_circle_center = Point(D0 + R, 0)
    away_start_on_circle = Point(pi, pi)

    # Случай, когда цель двигается по прямой
    line_aim = Role(AIM_VELOCITY, [Point(D0, 0)], 0, 0)
    line_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)], -120, 30)

    # Метод параллельного сближения
    parallel_aim = Role(AIM_VELOCITY, [Point(D0, 0)], 0, 20)
    parallel_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)], -120, 20)

    away_parallel_aim = Role(-AIM_VELOCITY, [Point(D0, 0)], 0, 20)
    away_parallel_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)], -120, 20)

    line_parallel_aim = Role(AIM_VELOCITY, [Point(D0, 0)], 0, 0)
    line_parallel_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)], -120, 30)

    # Запуск моделирования погони
    # ======================================================================================================
    circle_flight = targeting.circleFight(
        circle_aim, circle_interceptor, circle_center, start_on_circle, 1
    )
    saveFig("img/погоня_по_окружности.pdf", "x, М", "y, М")
    t_dense = np.linspace(min(circle_flight.t), max(circle_flight.t), 300)
    func = interp1d(circle_flight.t, circle_flight.n, kind="cubic", bounds_error=False)
    plt.plot(t_dense, func(t_dense))
    saveFig(
        "img/перегрузки_при_погоне_по_окружности.pdf", "время, сек", "перегрузка, G"
    )
    print(f"Погоня по окружности завершилась через {circle_flight.steps} шагов")
    saveFlightData("img/погоня_по_окружности.txt", circle_flight)

    # ======================================================================================================
    circle_flight = targeting.circleFight(
        away_circle_aim,
        away_circle_interceptor,
        away_circle_center,
        away_start_on_circle,
        1,
    )
    saveFig("img/погоня_по_окружности_от_нас.pdf", "x, М", "y, М")
    t_dense = np.linspace(min(circle_flight.t), max(circle_flight.t), 300)
    circle_flight.n[-1] = 0
    func = interp1d(circle_flight.t, circle_flight.n, kind="cubic", bounds_error=False)
    plt.plot(t_dense, func(t_dense))
    saveFig(
        "img/перегрузки_при_погоне_по_окружности_от_нас.pdf",
        "время, сек",
        "перегрузка, G",
    )
    print(f"Погоня по окружности от нас завершилась через {circle_flight.steps} шагов")
    saveFlightData("img/погоня_по_окружности_от_нас.txt", circle_flight)

    # ======================================================================================================
    line_flight = targeting.lineFight(line_aim, line_interceptor, 1)
    saveFig("img/погоня_по_прямой.pdf", "x, М", "y, М")
    t_dense = np.linspace(min(line_flight.t), max(line_flight.t), 300)
    func = interp1d(line_flight.t, line_flight.n, kind="cubic", bounds_error=False)
    plt.plot(t_dense, func(t_dense))
    saveFig("img/перегрузки_при_погоне_по_прямой.pdf", "время, сек", "перегрузка, G")
    print(f"Погоня по прямой завершилась через {line_flight.steps} шагов")
    saveFlightData("img/погоня_по_прямой.txt", line_flight)

    # ======================================================================================================
    parallel_flight = parallel.fight(
        parallel_aim, parallel_interceptor, circle_center, start_on_circle, 150
    )
    saveFig("img/параллельное_сближение.pdf", "x, М", "y, М")
    t_dense = np.linspace(min(parallel_flight.t), max(parallel_flight.t), 300)
    func = interp1d(
        parallel_flight.t, parallel_flight.n, kind="cubic", bounds_error=False
    )
    plt.plot(t_dense, func(t_dense))
    saveFig(
        "img/перегрузки_при_параллельном_сближении.pdf", "время, сек", "перегрузка, G"
    )
    print(
        f"Погоня методом параллельного сближения завершилась через {parallel_flight.steps} шагов"
    )
    saveFlightData("img/параллельное_сближение.txt", parallel_flight)

    # ======================================================================================================
    parallel_flight_away = parallel.fight(
        away_parallel_aim,
        away_parallel_interceptor,
        away_circle_center,
        away_start_on_circle,
        100,
    )
    saveFig("img/параллельное_сближение_от_нас.pdf", "x, М", "y, М")
    t_dense = np.linspace(min(parallel_flight_away.t), max(parallel_flight_away.t), 300)
    func = interp1d(
        parallel_flight_away.t,
        parallel_flight_away.n,
        kind="cubic",
        bounds_error=False,
    )
    plt.plot(t_dense, func(t_dense))
    saveFig(
        "img/перегрузки_при_параллельном_сближении_от_нас.pdf",
        "время, сек",
        "перегрузка, G",
    )
    print(
        f"Погоня методом параллельного сближения от нас завершилась через {parallel_flight_away.steps} шагов"
    )
    saveFlightData("img/параллельное_сближение_от_нас.txt", parallel_flight_away)

    # ======================================================================================================
    parallel_line_flight = parallel.lineFight(
        line_parallel_aim, line_parallel_interceptor, 20
    )
    saveFig("img/параллельное_сближение_по_прямой.pdf", "x, М", "y, М")
    t_dense = np.linspace(min(parallel_line_flight.t), max(parallel_line_flight.t), 300)
    func = interp1d(
        parallel_line_flight.t, parallel_line_flight.n, kind="cubic", bounds_error=False
    )
    plt.plot(t_dense, func(t_dense))
    saveFig(
        "img/перегрузки_при_параллельном_сближении_по_прямой.pdf",
        "время, сек",
        "перегрузка, G",
    )
    print(
        f"Погоня при пареллельном сближении по прямой завершилась через {parallel_line_flight.steps} шагов"
    )
    saveFlightData("img/параллельное_сближение_по_прямой.txt", parallel_line_flight)


if __name__ == "__main__":
    main()
