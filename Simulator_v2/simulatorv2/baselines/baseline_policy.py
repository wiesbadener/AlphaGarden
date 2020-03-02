import numpy as np
from simulatorv2.sim_globals import MAX_WATER_LEVEL, PRUNE_DELAY, PRUNE_THRESHOLD


def get_sector_x(sector, garden_rows, sector_rows):
    return (sector % (garden_rows // sector_rows)) * sector_rows


def get_sector_y(sector, garden_cols, sector_cols):
    return (sector // (garden_cols // sector_cols)) * sector_cols


def plant_in_sector(seeds, plant_idx, x_low, x_high, y_low, y_high):
    return np.any(seeds[x_low:x_high, y_low:y_high, plant_idx])


def policy(timestep, state, global_cc_vec, garden_rows, garden_cols, sector, sector_rows,
           sector_cols, step, water_threshold):
    x_low = get_sector_x(sector, garden_rows, sector_rows)
    y_low = get_sector_y(sector, garden_cols, sector_cols)
    x_high, y_high = x_low + sector_rows, y_low + sector_cols
    seeds_and_water = state[1][0]
    seeds = seeds_and_water[:, :, :-1]
    water_grid = seeds_and_water[:, :, -1]
    prob = global_cc_vec / np.sum(global_cc_vec)
    if timestep > PRUNE_DELAY:
        for i in range(len(global_cc_vec)):
            if plant_in_sector(seeds, i, x_low, x_high, y_low, y_high) and \
                    (prob[i] > PRUNE_THRESHOLD / len(global_cc_vec)):
                return [i + 5]
    if np.sum(water_grid) < garden_rows * garden_cols * step * water_threshold:
        sector_water = np.sum(water_grid[x_low:x_high][y_low:y_high])
        irr_policy = 0
        while sector_water < MAX_WATER_LEVEL:
            irr_policy += 1
            sector_water += MAX_WATER_LEVEL / 4
        return [irr_policy]
    return [0]
