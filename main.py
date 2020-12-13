import logging
from argparse import ArgumentParser, Namespace
from typing import TextIO
from operator import itemgetter

parser: ArgumentParser = ArgumentParser()
parser.add_argument("--log", default="info")

options: Namespace = parser.parse_args()

level = logging.DEBUG

if options.log.lower() == "info":
    level = logging.INFO

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    level=level)

logger = logging.getLogger(__name__)


def read_input_data(file_name: str) -> tuple[int, list[tuple[int, int]]]:
    f: TextIO = open(file_name)

    puzzle_input: tuple[int, list[tuple[int, int]]] = (int(f.readline().strip()), [])

    for i, bus_id in enumerate(f.readline().split(",")):
        if bus_id.strip() != "x":
            puzzle_input[1].append((i, int(bus_id.strip())))

    return puzzle_input


def erw_eukl_alg(num_1: int, num_2: int) -> tuple[int, int]:
    if num_1 < num_2:
        tmp: int = num_1
        num_1 = num_2
        num_2 = tmp
    a: int = num_1
    b: int = num_2
    qs: list[int] = [a // b]
    r: int = num_1 % num_2
    while r != 0:
        a = b
        b = r
        qs.append(a // b)
        r = a % b
    s: int = 1
    t: int = 0
    tmp: int
    qs.reverse()
    for q in qs:
        tmp = s
        s = t
        t = tmp - q * t
    return s, t


def solution_part_1(file_name: str) -> int:
    timestamp: int
    bus_ids: list[tuple[int, int]]
    (timestamp, bus_ids) = read_input_data(file_name)
    waiting_time: list[(int, int)] = []
    for _, bus_id in bus_ids:
        waiting_time.append(((timestamp % bus_id) - bus_id, bus_id))
    waiting_time.sort(key=itemgetter(0))
    logger.debug(waiting_time)
    return abs(waiting_time[-1][0])*waiting_time[-1][1]


def solution_part_2(file_name: str) -> int:
    timestamp: int
    bus_ids: list[tuple[int, int]]
    (timestamp, bus_ids) = read_input_data(file_name)
    product: int = 1
    for _, bus_id in bus_ids:
        product *= bus_id
    logger.debug(f"Produkt: {product}")
    e: int
    sol: int = 0
    for pos, bus_id in bus_ids:
        s, t = erw_eukl_alg(bus_id, product // bus_id)
        logger.debug(f"s: {s}, t: {t}, goal: {product // bus_id}, test: {s*product // bus_id + t*bus_id}")
        e = s * (product // bus_id)
        sol += -pos*e
    while sol < 0:
        sol += product
    sol %= product
    return sol


if __name__ == '__main__':
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
