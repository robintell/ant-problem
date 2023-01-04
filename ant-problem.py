
import random
import numpy as np
import scipy.stats


# Adjust this function to specify any closed boundary around the origin.
def is_food_reached(x: int,
                    y: int) -> bool:
    """
    This function returns a boolean specifying whether food has been reached at certain coordinates.
    :param x: Coordinate x
    :param y: Coordinate y
    :return: Boolean specifying whether food has been reached
    """

    return not ((x - 2.5)/30)**2 + ((y - 2.5)/40)**2 < 1


def take_a_step(x: int,
                y: int) -> tuple:
    """
    This function takes input coordinates and returns output coordinates
    after taking a 10 cm step in any random direction.
    :param x: Start x coordinate
    :param y: Start y coordinate
    :return: x, y coordinates after taking a random step
    """

    direction = random.randint(0, 3)
    if direction == 0:
        x += 10
    elif direction == 1:
        x -= 10
    elif direction == 2:
        y += 10
    elif direction == 3:
        y -= 10
    return x, y


def simulate_path() -> int:
    """
    This function takes random steps starting at the anthill (0, 0)
    until food is found and returns the number of steps required.
    :return: number of random steps required
    """

    x = 0
    y = 0
    steps_taken = 0
    while not is_food_reached(x, y):
        steps_taken += 1
        x, y = take_a_step(x, y)
    return steps_taken


def find_confidence_interval(confidence_level: float,
                             results: list) -> tuple:
    """
    This function calculates the confidence interval given
    a list of simulation results and a user-defined confidence level.
    :param confidence_level: User-defined confidence level
    :param results: List of simulation results
    :return: Confidence interval (low & high)
    """

    return scipy.stats.norm.interval(alpha=confidence_level,
                                     loc=np.mean(results),
                                     scale=scipy.stats.sem(results))


def main(confidence_level: float,
         number_of_digits: int):
    """
    This function comes up with an estimate of average time to find food
    located around a closed boundary (defined in is_food_reached)
    around an anthill with coordinates (0, 0),
    for an ant moving 10 cm per second in any random direction.
    :param confidence_level: Confidence level to stop simulation at
    :param number_of_digits: Number of decimal digits required
    """

    simulations_run = 0
    confidence_interval_low = 0
    confidence_interval_high = 0
    results = []

    # We will first run 30 simulations without any statistical calculations since a sample size <= 30 requires
    # student's t distribution to find the confidence interval
    # The while loop breaks as soon as both bounds of the confidence interval yield the same result
    # when rounded to the nearest number of decimal digits required.

    while simulations_run <= 30 or \
            round(confidence_interval_low, number_of_digits) != round(confidence_interval_high, number_of_digits):
        simulations_run += 1
        result = simulate_path()
        results.append(result)
        if simulations_run > 30:
            confidence_interval_low, confidence_interval_high = find_confidence_interval(confidence_level, results)

    print(f'The average time to find food is {round(confidence_interval_low, number_of_digits)} seconds '
          f'with {confidence_level * 100}% confidence.')


if __name__ == '__main__':
    main(confidence_level=0.999,
         number_of_digits=0)
