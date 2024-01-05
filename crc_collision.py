import pyModeS as pms

# When calculating CRC, AP should be all zeros
df5_2101_template = "00101_{0}_0001001110000_000000000000000000000000"
df5_0463_template = "00101_{0}_0010101010110_000000000000000000000000"

collision_values: dict[str, list[str]] = {}

fs_dr_um_valid_values: list[str] = []

for fs in map(lambda x: bin(x)[2:].zfill(3), range(0, 1 << 3)):
    for dr in ("00000", "00001", "00100", "00101"):
        for um in map(lambda x: bin(x)[2:].zfill(6), range(0, 1 << 6)):
            fs_dr_um_valid_values.append(fs + dr + um)

for fs_dr_um_2101 in fs_dr_um_valid_values:
    df5_2101_template_hex = pms.bin2hex(df5_2101_template.format(fs_dr_um_2101))
    crc_df5_2101 = pms.crc(df5_2101_template_hex)

    for fs_dr_um_0463 in map(lambda x: bin(x)[2:].zfill(14), range(0, 1 << 14)):
        df5_0463_template_hex = pms.bin2hex(df5_0463_template.format(fs_dr_um_0463))
        crc_df5_0463 = pms.crc(df5_0463_template_hex)

        if crc_df5_0463 == crc_df5_2101:
            if fs_dr_um_2101 in collision_values:
                collision_values[fs_dr_um_2101].append(fs_dr_um_0463)
            else:
                collision_values[fs_dr_um_2101] = [fs_dr_um_0463]

if len(collision_values) == 0:
    print("No collision")
else:
    for fs_dr_um_2101 in collision_values:
        print(f"Collisions with 2101 where FS,DR,UM={fs_dr_um_2101}:")
        for fs_dr_um_0463 in collision_values[fs_dr_um_2101]:
            print(f"    {fs_dr_um_0463}")
