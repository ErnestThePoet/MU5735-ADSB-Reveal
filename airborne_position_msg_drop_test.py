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

    ref_pos = pms.adsb.airborne_position(adsb_sequence[0], adsb_sequence[1], 0, 1)

    print(f"C2={ref_pos} D={distance.distance(ref_pos, actual_positions[1]).m:.03f}m")

    for i, msg in enumerate(adsb_sequence[2:]):
        if ignored_msg_indexes and i + 2 in ignored_msg_indexes:
            continue

        ref_pos = pms.adsb.airborne_position_with_ref(msg, ref_pos[0], ref_pos[1])
        print(f"C{i + 3}={ref_pos} D={distance.distance(ref_pos, actual_positions[i + 2]).m:.03f}m")

    print()


decode_pos("No dropped messages")
decode_pos("Drop 1 message", {8})
decode_pos("Drop 2 messages", {7, 8})
decode_pos("Drop 3 messages", {6, 7, 8})
decode_pos("Drop 4 messages", {5, 6, 7, 8})
decode_pos("Drop 7 messages", {2, 3, 4, 5, 6, 7, 8})
