import targeting
import parallel
from shared import AIM_VELOCITY, INTERCEPTOR_VELOCITY, D0, Point, Role, saveFig


def main():
    # Случай, когда цель двигается по окружности
    circle_aim = Role(AIM_VELOCITY, [Point(D0, 0)])
    circle_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)])

    # Случай, когда цель двигается по прямой
    line_aim = Role(AIM_VELOCITY, [Point(D0, 0)])
    line_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)])

    # Метод параллельного сближения
    parallel_aim = Role(AIM_VELOCITY, [Point(D0, 0)])
    parallel_interceptor = Role(INTERCEPTOR_VELOCITY, [Point(0, 0)])

    # Запуск моделирования погони
    circle_flight = targeting.circleFight(circle_aim, circle_interceptor)
    saveFig("img/погоня_по_окружности.pdf")
    print(f"Погоня по окружности завершилась через {circle_flight.steps} шагов")

    line_flight = targeting.lineFight(line_aim, line_interceptor)
    saveFig("img/погоня_по_прямой.pdf")
    print(f"Погоня по прямой завершилась через {line_flight.steps} шагов")

    parallel_flight = parallel.fight(parallel_aim, parallel_interceptor)
    saveFig("img/параллельное_сближение.pdf")
    print(
        f"Погоня методом параллельного сближения завершилась через {parallel_flight.steps} шагов"
    )


if __name__ == "__main__":
    main()
