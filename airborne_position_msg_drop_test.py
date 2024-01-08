import math
from geopy import distance
import pyModeS as pms


def cpr_mod(a: float, b: float):
    res = a % b
    if res < 0:
        res += b
    return res


def generate_adsb_sequence(positions: list[tuple[float, float]]):
    MODES_TEMPLATE = f"10001_101_{pms.hex2bin('780DB8')}_{{0}}_000000000000000000000000"
    ADSB_TEMPLATE = "01011_00_0_100101110100_0_{0}_{1}_{2}"

    even = True
    sequence: list[str] = []

    for lat, lon in positions:
        i = 0 if even else 1
        d_lat = 360 / (60 - i)
        yz = math.floor(131072 * cpr_mod(lat, d_lat) / d_lat + 0.5)
        r_lat = d_lat * (yz / 131072 + math.floor(lat / d_lat))

        d_lon = 360 if pms.cprNL(r_lat) - i == 0 else 360 / (pms.cprNL(r_lat) - i)
        xz = math.floor(131072 * cpr_mod(lon, d_lon) / d_lon + 0.5)

        yz = cpr_mod(yz, 131072)
        xz = cpr_mod(xz, 131072)

        modes = pms.bin2hex(MODES_TEMPLATE.format(ADSB_TEMPLATE.format(
            i, bin(int(yz))[2:].zfill(17), bin(int(xz))[2:].zfill(17))))

        modes = modes[:-6] + hex(pms.crc(modes))[2:].upper().zfill(6)

        sequence.append(modes)

        even = not even

    return sequence


actual_positions = [
    (23.34635931557985, 110.8665426944272),
    (23.34625894779067, 110.8676942564005),
    (23.3460993127592, 110.8688379724686),
    (23.34595425581612, 110.8699840542241),
    (23.34581111111111, 110.8711305555556),
    (23.34572208257996, 110.8722959681039),
    (23.34561413057375, 110.8734468947545),
    (23.34548167343178, 110.8745951079078),
    (23.34533321223092, 110.8757400114616),
    (23.34516545838654, 110.8768829102285),
]

adsb_sequence = generate_adsb_sequence(actual_positions)


def decode_pos(test_name: str, ignored_msg_indexes: set[int] = None):
    print(test_name)

    last_even_msg = ""
    last_odd_msg = ""

    start_index = 1
    for i in range(len(adsb_sequence)):
        if ignored_msg_indexes and i in ignored_msg_indexes:
            continue

        if pms.hex2bin(adsb_sequence[i])[53] == "0":
            last_even_msg = adsb_sequence[i]
        else:
            last_odd_msg = adsb_sequence[i]

        start_index = i + 1

        break

    for i in range(start_index, len(adsb_sequence)):
        if ignored_msg_indexes and i in ignored_msg_indexes:
            continue

        if pms.hex2bin(adsb_sequence[i])[53] == "0":
            last_even_msg = adsb_sequence[i]
            if last_odd_msg == "":
                continue
            selected_msg = last_odd_msg
        else:
            last_odd_msg = adsb_sequence[i]
            if last_even_msg == "":
                continue
            selected_msg = last_even_msg

        calculated_pos = pms.adsb.airborne_position(selected_msg, adsb_sequence[i], 0, 1)

        if i == len(adsb_sequence) - 1:
            dist = distance.distance(calculated_pos, actual_positions[i]).m
            print(f"C{i + 1}={calculated_pos} D={dist:.03f}m")
            print()
            return dist


# decode_pos("No dropped messages")

min_dist = 10000
max_dist = 0
min_dist_drop_desc = ""
max_dist_drop_desc = ""

for i in range(1 << 6):
    ignored_msg_indexes: set[int] = set()
    for j in range(6):
        if i & (1 << j):
            ignored_msg_indexes.add(j + 3)

    test_name = "{}" if len(ignored_msg_indexes) == 0 else str(ignored_msg_indexes)

    dist = decode_pos(test_name, ignored_msg_indexes)
    if dist > max_dist:
        max_dist = dist
        max_dist_drop_desc = test_name

    if dist < min_dist:
        min_dist = dist
        min_dist_drop_desc = test_name

print(f"Min dist for C10: {min_dist:.3f}m when dropping {min_dist_drop_desc}")
print(f"Max dist for C10: {max_dist:.3f}m when dropping {max_dist_drop_desc}")
