import numpy as np
from logger import Logger, Event
from plant import Plant

class Garden:
    def __init__(self, plants=[], N=50, M=50, step=1, drainage_rate=2, irr_threshold=5, plant_types=[], skip_initial_germination=True):
        # dictionary with plant ids as keys, plant objects as values
        self.plants = {}

        self.N = N
        self.M = M

        # list of plant types the garden will support
        self.plant_types = plant_types

        # Structured array of gridpoints. Each point contains its water levels
        # and set of coordinates of plants that can get water/light from that location.
        # First dimension is horizontal, second is vertical.
        self.grid = np.empty((N, M), dtype=[('water', 'f'), ('nearby', 'O')])

        # Grid for plant growth state representation
        self.plant_grid = np.zeros((N, M, len(plant_types)))

        # Defines the order in which irrigations are applied
        self.locations = []

        # initializes empty lists in grid
        for i in range(N):
            for j in range(M):
                self.grid[i,j]['nearby'] = set()
                self.locations.append((i, j))

        self.plant_locations = {}

        # distance between adjacent points in grid
        self.step = step

        # Drainage rate of water in soil
        self.drainage_rate = drainage_rate

        # amount of grid points away from irrigation point that water will spread to
        self.irr_threshold = irr_threshold

        # Add initial plants to grid
        self.curr_id = 0
        for plant in plants:
            if skip_initial_germination:
                plant.current_stage().skip_to_end()
            self.add_plant(plant)

        self.control_plant = Plant(0, 0, color='gray')
        self.control_plant.id = "Control"
        if skip_initial_germination:
            self.control_plant.current_stage().skip_to_end()

        self.logger = Logger()

    def add_plant(self, plant):
        if (plant.row, plant.col) in self.plant_locations:
            print(f"[Warning] A plant already exists in position ({plant.row, plant.col}). The new one was not planted.")
        else:
            plant.id = self.curr_id
            self.plants[plant.id] = plant
            self.plant_locations[plant.row, plant.col] = True
            self.curr_id += 1
            self.grid[plant.row, plant.col]['nearby'].add(plant.id)

    # Updates plants after one timestep, returns list of plant objects
    # irrigations is list of (location, amount) tuples
    def perform_timestep(self, water_amt=0, irrigations=None):
        if not irrigations:
            # Default to uniform irrigation
            self.reset_water(water_amt)
        else:
            for i in range(len(irrigations)):
                location = (i / self.N, i % self.M)
                self.irrigate(location, irrigations[i])

        self.distribute_light()
        self.distribute_water()
        self.grow_plants()
        self.grow_control_plant()

        return self.plants.values()

    def grow_control_plant(self):
        cp = self.control_plant
        cp.num_sunlight_points = cp.num_grid_points
        cp.water_amt = cp.desired_water_amt()
        self.logger.log(Event.WATER_REQUIRED, "Control", cp.water_amt)

        next_step = self.grow_plant(cp)
        if next_step:
            cp.num_grid_points += next_step * 8

    # Resets all water resource levels to the same amount
    def reset_water(self, water_amt):
        self.grid['water'] = water_amt

    # Updates water levels in grid in response to irrigation, location is (x, y) tuple
    def irrigate(self, location, amount):
        closest_x, closest_y = round(location[0] / self.step), round(location[1] / self.step)
        for i in range(max(0, closest_x - self.irr_threshold), min(self.grid.shape[0], closest_x + self.irr_threshold + 1)):
            for j in range(max(0, closest_y - self.irr_threshold), min(self.grid.shape[1], closest_y + self.irr_threshold + 1)):
                # calculates distance from irrigation location to center of resource cell
                grid_x = i * self.step
                grid_y = j * self.step
                # dist = np.sqrt((location[0] - grid_x)**2 + (location[1] - grid_y)**2)

                # updates water level in resource grid
                self.grid[i,j]['water'] += amount

    def get_water_amounts(self, step=5):
        amounts = []
        for i in range(0, len(self.grid), step):
            for j in range(0, len(self.grid[i]), step):
                water_amt = 0
                for a in range(i, i+step):
                    for b in range(j, j+step):
                        water_amt += self.grid[a, b]['water']
                midpt = (i + step // 2, j + step // 2)
                amounts.append((midpt, water_amt))
        return amounts

    def enumerate_grid(self, coords=False):
        for i in range(0, len(self.grid)):
            for j in range(len(self.grid[i])):
                yield (self.grid[i, j], (i, j)) if coords else self.grid[i, j]

    def distribute_light(self):
        for point in self.enumerate_grid():
            if point['nearby']:
                tallest_id = max(point['nearby'], key=lambda id: self.plants[id].height)
                self.plants[tallest_id].add_sunlight_point()

    def distribute_water(self):
        # Log desired water levels of each plant before distributing
        for plant in self.plants.values():
            self.logger.log(Event.WATER_REQUIRED, plant.id, plant.desired_water_amt())

        for point in self.enumerate_grid():
            if point['nearby']:
                plant_ids = list(point['nearby'])

                while point['water'] > 0 and plant_ids:
                    # Pick a random plant to give water to
                    i = np.random.choice(range(len(plant_ids)))
                    plant = self.plants[plant_ids[i]]

                    # Calculate how much water the plant needs for max growth,
                    # and give as close to that as possible
                    if plant.num_sunlight_points > 0:
                        water_to_absorb = min(point['water'], plant.desired_water_amt() / plant.num_grid_points)
                        plant.water_amt += water_to_absorb
                        point['water'] -= water_to_absorb

                    plant_ids.pop(i)

            # Water evaporation/drainage from soil
            point['water'] = max(0, point['water'] - self.drainage_rate)

    def grow_plants(self):
        for plant in self.plants.values():
            self.grow_plant(plant)
            # if next_step:
            self.update_plant_coverage(plant)

    def grow_plant(self, plant):
        next_step = plant.radius // self.step + 1
        next_line_dist = next_step * self.step

        prev_radius = plant.radius
        upward, outward = plant.amount_to_grow()
        plant.height += upward
        plant.radius += outward
        self.plant_grid[plant.row, plant.col, self.plant_types.index(plant.type)] = plant.radius

        self.logger.log(Event.WATER_ABSORBED, plant.id, plant.water_amt)
        self.logger.log(Event.RADIUS_UPDATED, plant.id, plant.radius)
        self.logger.log(Event.HEIGHT_UPDATED, plant.id, plant.height)

        plant.reset()

        if prev_radius < next_line_dist and plant.radius >= next_line_dist:
            return next_step

    def update_plant_coverage(self, plant):
        for point in self._get_new_points(plant):
            if self.within_radius(point, plant):
                if plant.id not in self.grid[point]['nearby']:
                    plant.num_grid_points += 1
                    self.grid[point]['nearby'].add(plant.id)

    def _get_new_points(self, plant):
        rad_step = int(plant.radius // self.step)
        start_row, end_row = max(0, plant.row - rad_step), min(self.grid.shape[0] - 1, plant.row + rad_step)
        start_col, end_col = max(0, plant.col - rad_step), min(self.grid.shape[1] - 1, plant.col + rad_step)

        for col in range(start_col, end_col + 1):
            yield (start_row, col)
            yield (start_row + 1, col)
            yield (end_row - 1, col)
            yield (end_row, col)
        for row in range(start_row, end_row + 1):
            yield (row, start_col)
            yield (row, start_col + 1)
            yield (row, end_col - 1)
            yield (row, end_col)

    def within_radius(self, grid_pos, plant):
        dist = self.step ** 0.5 * np.linalg.norm((grid_pos[0] - plant.row, grid_pos[1] - plant.col))
        return dist <= plant.radius

    def get_state(self):
        water = np.expand_dims(self.grid['water'], axis=2)
        return np.dstack((self.plant_grid, water))
