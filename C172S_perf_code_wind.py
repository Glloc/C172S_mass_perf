#Script by Gautier C. for BAA pre-flight prep log


#Add to the GUI / PDF
#converting to meters as well 
import scipy
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import math

from datfile import table_tkoff_2550lb
from datfile import table_ROC_2550lb
from datfile import table_ldg_2550lb
from datfile import airports

def prepare_takeoff_interpolator(data):
    pres_altitudes = sorted(set(row[0] for temp_table in data for row in temp_table))
    temperatures = sorted(set(row[1] for temp_table in data for row in temp_table))
    ground_rolls = np.zeros((len(pres_altitudes), len(temperatures)))
    dist_to_clear_50fts = np.zeros((len(pres_altitudes), len(temperatures)))

    for i, pres_alt in enumerate(pres_altitudes):
        for j, temp in enumerate(temperatures):
            for temp_table in data:
                for row in temp_table:
                    if row[0] == pres_alt and row[1] == temp:
                        ground_rolls[i, j] = row[2]
                        dist_to_clear_50fts[i, j] = row[3]

    f_ground_roll = RegularGridInterpolator((pres_altitudes, temperatures), ground_rolls)
    f_dist_to_clear_50ft = RegularGridInterpolator((pres_altitudes, temperatures), dist_to_clear_50fts)

    return f_ground_roll, f_dist_to_clear_50ft


def prepare_ROC_interpolator(data):
    pres_altitudes = sorted(set(row[0] for temp_table in data for row in temp_table))
    temperatures = sorted(set(row[2] for temp_table in data for row in temp_table))
    climb_speeds = np.zeros((len(pres_altitudes), len(temperatures)))
    ROCs = np.zeros((len(pres_altitudes), len(temperatures)))

    for i, pres_alt in enumerate(pres_altitudes):
        for j, temp in enumerate(temperatures):
            for temp_table in data:
                for row in temp_table:
                    if row[0] == pres_alt and row[2] == temp:
                        climb_speeds[i, j] = row[1]
                        ROCs[i, j] = row[3]

    f_climb_speed = RegularGridInterpolator((pres_altitudes, temperatures), climb_speeds)
    f_ROC = RegularGridInterpolator((pres_altitudes, temperatures), ROCs)

    return f_climb_speed, f_ROC

def prepare_LDG_interpolator(data):
    pres_altitudes = sorted(set(row[0] for temp_table in data for row in temp_table))
    temperatures = sorted(set(row[1] for temp_table in data for row in temp_table))
    ground_rolls = np.zeros((len(pres_altitudes), len(temperatures)))
    dist_to_clear_50fts = np.zeros((len(pres_altitudes), len(temperatures)))

    for i, pres_alt in enumerate(pres_altitudes):
        for j, temp in enumerate(temperatures):
            for temp_table in data:
                for row in temp_table:
                    if row[0] == pres_alt and row[1] == temp:
                        ground_rolls[i, j] = row[2]
                        dist_to_clear_50fts[i, j] = row[3]

    f_ldg_ground_roll = RegularGridInterpolator((pres_altitudes, temperatures), ground_rolls)
    f_ldg_dist_to_clear_50ft = RegularGridInterpolator((pres_altitudes, temperatures), dist_to_clear_50fts)
    return f_ldg_ground_roll, f_ldg_dist_to_clear_50ft


def calculate_wind_components(wind_direction, wind_speed, runway_heading):
    angle = math.radians(wind_direction - runway_heading)
    headwind = wind_speed * math.cos(angle)
    crosswind = wind_speed * math.sin(angle)
    return headwind, crosswind


def adjust_distances_for_headwind(dist, headwind):
    return dist * (1 - (headwind / 9) * 0.1)


def get_user_input():
    temperature = float(input("Enter the temperature (°C): "))
    airport_code = input("Enter the ICAO code of the airport in upper case: ").upper()

    if airport_code not in airports:
        print("Invalid airport code.")
        exit()

    wind = input("Take wind into account? If NO enter 'N', if YES enter wind format 36020: ")
    wind_direction, wind_speed = 0, 0

    if wind.upper() != 'N':
        try:
            wind_direction = int(wind[:3])
            wind_speed = int(wind[3:])
            print(f"Wind direction: {wind_direction} degrees")
            print(f"Wind speed: {wind_speed} knots")
        except ValueError:
            print("Invalid wind format. Please enter a valid wind format (e.g., 36020) or 'N'.")
            wind_direction, wind_speed = 0, 0

    return temperature, airport_code, wind_direction, wind_speed


def find_best_runway(airport, wind_direction, wind_speed):
    best_runway = None
    best_headwind = -float('inf')
    best_crosswind = 0

    for runway in airport['runways']:
        headwind, crosswind = calculate_wind_components(wind_direction, wind_speed, runway['heading'])
        if headwind > best_headwind:
            best_headwind = headwind
            best_crosswind = crosswind
            best_runway = runway

    if best_runway is None:
        print("No suitable runway found.")
        exit()

    return best_runway, best_headwind, best_crosswind


def print_non_wind_corrected_data(airport_code, best_runway, ground_roll, dist_to_clear_50ft, climb_speed, ROC, ldg_ground_roll, ldg_dist_to_clear_50ft):
    # Fetch airport data based on airport code
    airport = airports[airport_code]

    # Print relevant information
    print()
    print(f"################################")
    print(f"Runway INFO : {airport_code}")
    print(f"################################")
    print(f"Elevation: {airport['elevation']} ft")
    print(f"Best runway heading: {best_runway['heading']} ")
    print(f"Best runway length: {best_runway['length']} ft / {(best_runway['length'])*0.3048} m ")
    print()
    print(f"################################")
    print(f"Non-Wind corrected distances")
    print(f"################################")
    # Output non-wind-corrected distances
    print(f"T/O Ground roll: {ground_roll:.2f} ft")
    print(f"T/O Distance (x1.25): {dist_to_clear_50ft:.2f} ft")
    print(f"Rate of Climb: {ROC:.2f} fpm at Climb Speed: {climb_speed:.2f} KIAS")
    print(f"Landing ground roll: {ldg_ground_roll:.2f} ft")
    print(f"Landing Distance (x1.42): {ldg_dist_to_clear_50ft:.2f} ft")


def print_wind_corrected_data(best_headwind, best_crosswind, adjusted_ground_roll, adjusted_dist_to_clear_50ft, ROC, climb_speed, adjusted_ldg_ground_roll, adjusted_ldg_dist_to_clear_50ft, temperature):
    print()
    print(f"################################")
    print(f"##########  ~WIND~  ############")
    print(f"################################")
    print(f"Headwind component: {best_headwind:.2f} knots")
    print(f"Crosswind component: {abs(best_crosswind):.2f} knots")
    print(f"Adjusted T/O ground roll: {adjusted_ground_roll:.2f} feet")
    print(f"Adjusted T/O Distance to clear 50ft (x1.25): {adjusted_dist_to_clear_50ft:.2f} feet")
    print(f"Rate of Climb: {ROC:.2f} fpm at Climb Speed: {climb_speed:.2f} KIAS")
    print(f"Adjusted landing ground roll: {adjusted_ldg_ground_roll:.2f} feet")
    print(f"Adjusted landing distance to clear 50ft (x1.42): {adjusted_ldg_dist_to_clear_50ft:.2f} feet")

    if best_headwind > 15 or abs(best_crosswind) > 8:
        info = """
Wind Limitations:

If flying dual (Phase 1 and 2):
- Max wind speed: 25 KT
- Max crosswind: 12 KT 

If flying dual in Phase 3, 4, or 5:
- Max wind speed: 35 KT
- Max crosswind: 15 KT

If flying solo for the first time:
- Max wind speed: 10 KT
- Max crosswind: 7 KT

If flying solo (Phase 1 and 2):
- Max wind speed: 15 KT
- Max crosswind: 6 KT 

If flying solo in Phase 3, 4, or 5:
- Max wind speed: 25 KT
- Max crosswind: 12 KT

Refer to wind limitations in 1.19.19 in operations manual in briefing room.
        """
        print(info)

    if temperature > 35:
        print('---ATTENTION PILOT --- ')
        print('It is getting pretty hot in here, and its not because of you! Check weather reports')
        print('Confirm that temperature DOES NOT go above the 38C limit!')


def main():
    f_ground_roll, f_dist_to_clear_50ft = prepare_takeoff_interpolator(table_tkoff_2550lb)
    f_climb_speed, f_ROC = prepare_ROC_interpolator(table_ROC_2550lb)
    f_ldg_ground_roll, f_ldg_dist_to_clear_50ft = prepare_LDG_interpolator(table_ldg_2550lb)

    temperature, airport_code, wind_direction, wind_speed = get_user_input()

    airport = airports[airport_code]
    best_runway, best_headwind, best_crosswind = find_best_runway(airport, wind_direction, wind_speed)

    indicated_altitude = airports[airport_code]['elevation']

    ground_roll = f_ground_roll((indicated_altitude, temperature))
    dist_to_clear_50ft = f_dist_to_clear_50ft((indicated_altitude, temperature)) * 1.25

    climb_speed = f_climb_speed((indicated_altitude, temperature))
    ROC = f_ROC((indicated_altitude, temperature))

    ldg_ground_roll = f_ldg_ground_roll((indicated_altitude, temperature))
    ldg_dist_to_clear_50ft = f_ldg_dist_to_clear_50ft((indicated_altitude, temperature)) * 1.42

    print_non_wind_corrected_data(airport_code, best_runway, ground_roll, dist_to_clear_50ft, climb_speed, ROC, ldg_ground_roll, ldg_dist_to_clear_50ft)

    adjusted_ground_roll = adjust_distances_for_headwind(ground_roll, best_headwind)
    adjusted_dist_to_clear_50ft = adjust_distances_for_headwind(dist_to_clear_50ft, best_headwind)
    adjusted_ldg_ground_roll = adjust_distances_for_headwind(ldg_ground_roll, best_headwind)
    adjusted_ldg_dist_to_clear_50ft = adjust_distances_for_headwind(ldg_dist_to_clear_50ft, best_headwind)

    print_wind_corrected_data(best_headwind, best_crosswind, adjusted_ground_roll, adjusted_dist_to_clear_50ft, ROC, climb_speed, adjusted_ldg_ground_roll, adjusted_ldg_dist_to_clear_50ft, temperature)


if __name__ == "__main__":
    main()
