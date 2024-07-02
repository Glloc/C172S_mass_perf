#Script by Gautier C. for BAA pre-flight prep log


#Todo
#clean up sequencing
#trip fuel + LDG weight to calc
#GUI
#PDF output

from datfile import aircraft_data, coordinates, weight_limits

#This calcs the slope coeffs of the loading graph, y = m * x with m being the coefficient
def calculate_slope(coord_x, coord_y):
    return coord_x / coord_y

def initialize_slopes():
    slopes = {key: calculate_slope(x, y) for key, (x, y) in coordinates.items()}
    for key, slope in slopes.items():
        print(f"Coefficient for {key.replace('_', ' ')} is {slope:.3f}")
    return slopes

def calculate_load_moment(weight, load_type, slopes):
    # Check if the load type is valid
    if load_type not in slopes:
        return "Invalid load type. Valid types are: 'pilot_and_front_passenger', 'fuel', 'rear_passenger', 'baggage_a', 'baggage_b'."
    # Check if the weight exceeds the limit
    if weight > weight_limits[load_type]:
        print("---ATTENTION PILOT--- Weight exceeds the limit of ", weight_limits[load_type], "KG for", load_type.replace('_', ' '))

    # Calculate the load moment
    load_moment = slopes[load_type] * weight
    return load_moment

def get_aircraft_registration():
    return ("LY-" + input("Enter the last 3 letters of aircraft registration (e.g., BAK, FRA): ")).strip().upper()

def get_fuel_data():
    print('####################################')
    print('###  FUEL  ###')
    print('####################################')
    fuel = float(input("Enter trip planned time (in minutes) : "))
    fuel_alt = float(input("Enter planned time to divert to Alternate airport (in minutes) : "))
    return fuel, fuel_alt

def print_fuel_requirements(aircraft_registration, fuel, fuel_alt):
    empty_weight = aircraft_data[aircraft_registration]['empty_weight']
    empty_weight_moment = aircraft_data[aircraft_registration]['empty_weight_moment']
    MTOW = aircraft_data[aircraft_registration]['MTOW']
    print(f"Aircraft {aircraft_registration}: Empty Weight Moment = {empty_weight_moment} kg-mm, MTOW = {MTOW} kg")

    fuel_conso = float(aircraft_data[aircraft_registration]['fuel_conso']) / 60
    print('Required trip litres for ', fuel, ' minutes : ', fuel * fuel_conso, ' L')
    print(f'Required 10% contingency litres for {fuel * 0.1} minutes : {((fuel * fuel_conso * 0.1)):.2f} L')
    print('Required litres for diverting to alternate of ', fuel_alt, ' minutes : ', fuel_alt * fuel_conso, ' L')
    print('Reserve fuel is 1 hour, for : ', fuel_conso * 60, ' L')
    print(f'Total Fuel is {fuel + fuel * 0.1 + fuel_alt + 60} minutes : {((fuel + fuel * 0.1 + fuel_alt + 60) * fuel_conso)} L')

def get_mass_and_cg_data(aircraft_registration, slopes):
    print('####################################')
    print('###  MASS & CG  ###')
    print('####################################')
    empty_weight = aircraft_data[aircraft_registration]['empty_weight']
    empty_weight_moment = aircraft_data[aircraft_registration]['empty_weight_moment']
    MTOW = aircraft_data[aircraft_registration]['MTOW']

    load_types = [
        'pilot_and_front_passenger',
        'fuel',
        'rear_passenger',
        'baggage_a',
        'baggage_b'
    ]

    total_weight = empty_weight
    total_load_moment = empty_weight_moment

    for load_type in load_types:
        weight = float(input(f"Enter the load weight (in kg) for {load_type.replace('_', ' ')}: "))
        load_moment = calculate_load_moment(weight, load_type, slopes)
        print(f"The load moment for {load_type.replace('_', ' ')} with weight {weight} kg is {load_moment:.2f} kg-mm.")
        total_weight += weight
        total_load_moment += load_moment

    return total_weight, total_load_moment, MTOW

def fuel_trip_moment(aircraft_registration, total_weight, total_load_moment, fuel) :
    print('####################################')
    print('###  END of TRIP FUEL & MOMENT  ###')
    print('####################################')
    total_weight -= fuel * fuel_conso * fuel_density


def print_total_weight_and_moment(aircraft_registration, total_weight, total_load_moment, MTOW):
    print('####################################')
    print(f"Aircraft {aircraft_registration}: Empty Weight = {aircraft_data[aircraft_registration]['empty_weight']},")
    print(f"Empty Weight Moment = {aircraft_data[aircraft_registration]['empty_weight_moment']} kg-mm, MTOW = {MTOW} kg")
    print(f"Total weight is {total_weight:.2f} kg.")
    print(f"Total load moment is {total_load_moment:.2f} kg-mm.")
    if total_weight > MTOW:
        print("---ATTENTION PILOT--- Total weight exceeds MTOW! Get your papers in order or DO NOT FLY")

def main():
    slopes = initialize_slopes()
    aircraft_registration = get_aircraft_registration()
    
    if aircraft_registration not in aircraft_data:
        print("Invalid aircraft registration.")
        return
    
    fuel, fuel_alt = get_fuel_data()
    print_fuel_requirements(aircraft_registration, fuel, fuel_alt)
    total_weight, total_load_moment, MTOW = get_mass_and_cg_data(aircraft_registration, slopes)
    print_total_weight_and_moment(aircraft_registration, total_weight, total_load_moment, MTOW)

if __name__ == "__main__":
    main()
