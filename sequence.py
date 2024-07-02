#Script by Sam Hau for BAA pre-flight prep log // The objective of this script is to sequence the calculations according to the briefing & performance sheet

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from datfile import table_tkoff_2550lb, table_ROC_2550lb, table_ldg_2550lb, airports, aircraft_data, coordinates, weight_limits
from mass_balance import calculate_slope, calculate_load_moment
from C172S_perf_code_wind import prepare_takeoff_interpolator, prepare_ROC_interpolator, prepare_LDG_interpolator, calculate_wind_components, adjust_distances_for_headwind 

# Step 1: Fuel Calculations
def fuel_calculations():
    fuel = float(input("Enter trip planned time (in minutes) : "))
    fuel_alt = float(input("Enter planned time to divert to Alternate airport (in minutes) : "))
    return fuel, fuel_alt

# Step 2: Mass and Balance Calculations
def mass_balance_calculations(aircraft_registration, fuel, fuel_alt):
    empty_weight = aircraft_data[aircraft_registration]['empty_weight']
    empty_weight_moment = aircraft_data[aircraft_registration]['empty_weight_moment']
    MTOW = aircraft_data[aircraft_registration]['MTOW']
    
    fuel_weight = fuel * weight_limits['fuel']  # Assuming weight per minute for simplicity
    fuel_moment = calculate_load_moment(fuel_weight, 'fuel')
    
    total_weight = empty_weight + fuel_weight
    total_moment = empty_weight_moment + fuel_moment
    
    print(f"Empty Weight: {empty_weight}, Fuel Weight: {fuel_weight}")
    print(f"Empty Weight Moment: {empty_weight_moment}, Fuel Moment: {fuel_moment}")
    print(f"Total Weight: {total_weight}, Total Moment: {total_moment}, MTOW: {MTOW}")
    
    return total_weight, total_moment, MTOW

# Function to prepare the interpolator (used in performance_calculations)
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

# Step 3: Performance Calculations
def performance_calculations(total_weight):
    if total_weight < 1157:
        airport = input("Enter airport code: ")
        temperature = float(input("Enter temperature (Â°C): "))
        
        pres_altitude = airports[airport]['pressure_altitude']
        print(f"Using performance table for 2550 lbs.")
        
        f_ground_roll, f_dist_to_clear_50ft = prepare_takeoff_interpolator(table_tkoff_2550lb)
        
        takeoff_performance_ground_roll = f_ground_roll((pres_altitude, temperature))
        takeoff_performance_clear_50ft = f_dist_to_clear_50ft((pres_altitude, temperature))
        
        print(f"Takeoff Performance Ground Roll: {takeoff_performance_ground_roll} ft")
        print(f"Takeoff Performance Distance to Clear 50 ft: {takeoff_performance_clear_50ft} ft")
        return takeoff_performance_ground_roll, takeoff_performance_clear_50ft
    else:
        print("Weight exceeds 1157 kg. Performance calculation for heavier weights not implemented.")
        return None, None

# Main function
def main():
    fuel, fuel_alt = fuel_calculations()
    
    aircraft_registration = ("LY-" + input("Enter the last 3 letters of aircraft registration (e.g., BAK, FRA): ")).strip().upper()
    if aircraft_registration not in aircraft_data:
        print("Invalid aircraft registration.")
        return
    
    total_weight, total_moment, MTOW = mass_balance_calculations(aircraft_registration, fuel, fuel_alt)
    
    takeoff_performance_ground_roll, takeoff_performance_clear_50ft = performance_calculations(total_weight)
    if takeoff_performance_ground_roll and takeoff_performance_clear_50ft:
        print("Takeoff Performance Ground Roll:", takeoff_performance_ground_roll)
        print("Takeoff Performance Distance to Clear 50 ft:", takeoff_performance_clear_50ft)

if __name__ == "__main__":
    main()