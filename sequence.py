#Script by Sam Hau for BAA pre-flight prep log // The objective of this script is to sequence the calculations according to the briefing & performance sheet

# sequence.py
from datfile import (
    aircraft_data,
    airports,
    table_tkoff_2550lb,
    table_ROC_2550lb,
    table_ldg_2550lb

)

from mass_balance import (
    initialize_slopes,
    get_aircraft_registration,
    get_fuel_data,
    print_fuel_requirements,
    get_mass_and_cg_data,
    print_total_weight_and_moment,

)

from C172S_perf_code_wind import (
    prepare_takeoff_interpolator,
    prepare_ROC_interpolator,
    prepare_LDG_interpolator,
    get_user_input,
    find_best_runway,
    print_non_wind_corrected_data,
    print_wind_corrected_data,
    adjust_distances_for_headwind,

)

def main_sequence():
    # Mass & CG calculations
    slopes = initialize_slopes()
    aircraft_registration = get_aircraft_registration()

    if aircraft_registration not in aircraft_data:
        print("Invalid aircraft registration.")
        return

    fuel, fuel_alt = get_fuel_data()
    print_fuel_requirements(aircraft_registration, fuel, fuel_alt)

    total_weight, total_weight_post_trip, total_load_moment, total_load_moment_post_trip, MTOW = get_mass_and_cg_data(
        aircraft_registration, slopes, fuel,
        aircraft_data[aircraft_registration]['fuel_conso'],
        aircraft_data[aircraft_registration]['fuel_density']
    )

    print_total_weight_and_moment(aircraft_registration, total_weight, total_weight_post_trip, total_load_moment, total_load_moment_post_trip, MTOW)

    # Performance calculations
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
    main_sequence()