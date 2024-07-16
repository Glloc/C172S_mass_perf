# GUI application using the customtkinter module
import customtkinter as ctk
import tkinter as tk


# Sets the appearance of the window
# Supported modes : Light, Dark, System
# "System" sets the appearance mode to
# the appearance mode of the system
ctk.set_appearance_mode("dark")
# Sets the color of the widgets in the window
# Supported themes : green, dark-blue, blue   
ctk.set_default_color_theme("dark-blue")
# Dimensions of the window
appWidth, appHeight = 1200, 800

def get_aircraft_registration(aircraft_registration_input):
    if aircraft_registration_input.startswith("LY-"):
        return aircraft_registration_input
    else :
        return f"LY-{aircraft_registration_input}"

from datfile import (
    aircraft_data,
    airports,
    table_tkoff_2550lb,
    table_ROC_2550lb,
    table_ldg_2550lb,
    info_wind,
    info_temp
)
from mass_balance import (
    initialize_slopes,
    calculate_load_moment,
)
from C172S_perf_code_wind import (
    prepare_takeoff_interpolator,
    prepare_ROC_interpolator,
    prepare_LDG_interpolator,
    find_best_runway,
    print_non_wind_corrected_data,
    print_wind_corrected_data,
    adjust_distances_for_headwind
)
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("BAA Performance Calculations")
        self.geometry("1280x840")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Aircraft Info Frame
        self.aircraftFrame = ctk.CTkFrame(self)
        self.aircraftFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.aircraftHeader = ctk.CTkLabel(self.aircraftFrame, text="Aircraft Information", font=("Arial", 16, "bold"))
        self.aircraftHeader.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.aircraftLabel = ctk.CTkLabel(self.aircraftFrame, text="Aircraft Registration")
        self.aircraftLabel.grid(row=1, column=0, padx=20, pady=10, sticky="e")

        aircraft_options = ['Select Aircraft', "LY-FTG", "LY-BAK", 'LY-FTK', 'LY-FTA', 'LY-FTF', 'LY-FTX', 'OO-JDH', 'LY-BGV']
        self.aircraftSelection = ctk.CTkComboBox(self.aircraftFrame, values=aircraft_options)
        self.aircraftSelection.set("Select Aircraft")
        self.aircraftSelection.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.airportLabel = ctk.CTkLabel(self.aircraftFrame, text="Airport Registration")
        self.airportLabel.grid(row=2, column=0, padx=20, pady=10, sticky="e")

        airport_options = ['Select Airport', 'LEDA', 'LEHC', 'LERS', 'LELL']
        self.airportSelection = ctk.CTkComboBox(self.aircraftFrame, values=airport_options)
        self.airportSelection.set("Select Airport")
        self.airportSelection.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.fuelLabel = ctk.CTkLabel(self.aircraftFrame, text="Enter trip planned time (in minutes):")
        self.fuelLabel.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.fuelEntry = ctk.CTkEntry(self.aircraftFrame, placeholder_text="90")
        self.fuelEntry.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        self.fuelaltLabel = ctk.CTkLabel(self.aircraftFrame, text="Enter planned time to divert to Alternate airport (in minutes):")
        self.fuelaltLabel.grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self.fuelaltEntry = ctk.CTkEntry(self.aircraftFrame, placeholder_text="45")
        self.fuelaltEntry.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        # Output Frame
        self.outputFrame = ctk.CTkFrame(self)
        self.outputFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.outputBox = ctk.CTkTextbox(self.outputFrame, width=600, height=400)
        self.outputBox.grid(row=0, column=0, padx=20, pady=20)

        # Performance Info Frame
        self.performanceFrame = ctk.CTkFrame(self)
        self.performanceFrame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.performanceHeader = ctk.CTkLabel(self.performanceFrame, text="Performance Information", font=("Arial", 16, "bold"))
        self.performanceHeader.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.tempLabel = ctk.CTkLabel(self.performanceFrame, text="Enter the temperature (°C):")
        self.tempLabel.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.tempEntry = ctk.CTkEntry(self.performanceFrame, placeholder_text="0")
        self.tempEntry.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.winddLabel = ctk.CTkLabel(self.performanceFrame, text="Enter Wind direction (degrees):")
        self.winddLabel.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.winddEntry = ctk.CTkEntry(self.performanceFrame, placeholder_text="0")
        self.winddEntry.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.windLabel = ctk.CTkLabel(self.performanceFrame, text="Enter Wind Speed (KT):")
        self.windLabel.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.windEntry = ctk.CTkEntry(self.performanceFrame, placeholder_text="0")
        self.windEntry.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        # Load Info Frame
        self.loadFrame = ctk.CTkFrame(self)
        self.loadFrame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.loadHeader = ctk.CTkLabel(self.loadFrame, text="Load Information", font=("Arial", 16, "bold"))
        self.loadHeader.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.frontLabel = ctk.CTkLabel(self.loadFrame, text="Enter the load weight (in kg) for pilot and front passenger:")
        self.frontLabel.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.frontEntry = ctk.CTkEntry(self.loadFrame, placeholder_text="150")
        self.frontEntry.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.rearLabel = ctk.CTkLabel(self.loadFrame, text="Enter the load weight (in kg) for rear passengers:")
        self.rearLabel.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.rearEntry = ctk.CTkEntry(self.loadFrame, placeholder_text="0")
        self.rearEntry.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.fuelmLabel = ctk.CTkLabel(self.loadFrame, text="Enter the load weight (in kg) for fuel:")
        self.fuelmLabel.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.fuelmEntry = ctk.CTkEntry(self.loadFrame, placeholder_text="153")
        self.fuelmEntry.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        self.bagaLabel = ctk.CTkLabel(self.loadFrame, text="Enter the load weight (in kg) for baggage A:")
        self.bagaLabel.grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self.bagaEntry = ctk.CTkEntry(self.loadFrame, placeholder_text="0")
        self.bagaEntry.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        self.bagbLabel = ctk.CTkLabel(self.loadFrame, text="Enter the load weight (in kg) for baggage B:")
        self.bagbLabel.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self.bagbEntry = ctk.CTkEntry(self.loadFrame, placeholder_text="0")
        self.bagbEntry.grid(row=5, column=1, padx=20, pady=10, sticky="w")

        # Button to Trigger Calculation
        self.calculateButton = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.calculateButton.grid(row=2, column=0, columnspan=2, pady=20)


    def submit(self):
            aircraft_registration = get_aircraft_registration(self.aircraftSelection.get())
            output_text = (f"Aircraft Registration: {aircraft_registration}\n")
            if aircraft_registration not in aircraft_data:
                output_text = ("Invalid aircraft registration.")
            

            # Mass & CG calculations
            slopes = initialize_slopes()


            fuel = float(self.fuelEntry.get())
            fuel_alt = float(self.fuelaltEntry.get())
            output_text += ('####################################\n')
            output_text += ('###  FUEL  ###\n')
            output_text += ('####################################\n')
            empty_weight = aircraft_data[aircraft_registration]['empty_weight']
            empty_weight_moment = aircraft_data[aircraft_registration]['empty_weight_moment']
            MTOW = aircraft_data[aircraft_registration]['MTOW']
            output_text += (f"Aircraft {aircraft_registration}: Empty Weight Moment = {empty_weight_moment} kg-mm, MTOW = {MTOW} kg\n")

            fuel_conso = float(aircraft_data[aircraft_registration]['fuel_conso']) / 60
            total_fuel_time = fuel + fuel * 0.1 + fuel_alt + 60
            output_text += (f'Required trip litres for {fuel} minutes : {(fuel * fuel_conso):.2f} L or {(fuel * fuel_conso / 3.785):.2f} gal (US):\n')
            output_text += (f'Required 10% contingency litres for {fuel * 0.1} minutes : {((fuel * fuel_conso * 0.1)):.2f} L\n')
            output_text += (f"Required litres for diverting to alternate of {fuel_alt} minutes: {fuel_alt * fuel_conso} L \n")
            output_text += (f'Reserve fuel is 1 hour, for : {fuel_conso * 60} L\n')
            output_text += (f'Total Fuel is {total_fuel_time:.2f} minutes : {(total_fuel_time * fuel_conso):.2f} L or {((total_fuel_time * fuel_conso) / 3.785):.2f} gal (US)\n')

            output_text += ('####################################\n')
            output_text += ('###  MASS & CG  ###\n')
            output_text += ('####################################\n')


            load_types = [
                'pilot_and_front_passenger',
                'fuel',
                'rear_passenger',
                'baggage_a',
                'baggage_b'
            ]

            total_weight = empty_weight
            total_load_moment = empty_weight_moment
            total_weight_post_trip = empty_weight
            total_load_moment_post_trip = empty_weight_moment
            fuel_conso = aircraft_data[aircraft_registration]['fuel_conso']
            fuel_dens = aircraft_data[aircraft_registration]['fuel_density']

            for load_type in load_types:
                if load_type == 'pilot_and_front_passenger' :
                    weight = float(self.frontEntry.get())
                if load_type == 'fuel' :
                    weight = float(self.fuelmEntry.get())
                if load_type == 'rear_passenger' :
                    weight = float(self.rearEntry.get())
                if load_type == 'baggage_a' :
                    weight = float(self.bagaEntry.get())
                if load_type == 'baggage_b' :
                    weight = float(self.bagbEntry.get())             
                load_moment = calculate_load_moment(weight, load_type, slopes)
                
                print(f"The load moment for {load_type.replace('_', ' ')} with weight {weight} kg is {load_moment:.2f} kg-mm.")
                output_text += (f"The load moment for {load_type.replace('_', ' ')} with weight {weight} kg is {load_moment:.2f} kg-mm. \n")
                
                total_weight += weight
                total_load_moment += load_moment

                if load_type == 'fuel' :
                    weight_fuel_post_trip = weight - (fuel/60) * fuel_conso * fuel_dens 
                    load_moment_fuel_post_trip = calculate_load_moment(weight_fuel_post_trip, 'fuel', slopes)
                    total_weight_post_trip += weight_fuel_post_trip
                    total_load_moment_post_trip += load_moment_fuel_post_trip
                else : 
                    total_weight_post_trip += weight
                    total_load_moment_post_trip += load_moment

            output_text += ('####################################\n')
            output_text += (f"Aircraft {aircraft_registration}: Empty Weight = {aircraft_data[aircraft_registration]['empty_weight']}, \n")
            output_text += (f"Empty Weight Moment = {aircraft_data[aircraft_registration]['empty_weight_moment']} kg-mm, MTOW = {MTOW} kg\n")
            output_text += (f"Total Weight is {total_weight:.2f} kg.\n")
            output_text += (f"Total load moment is {total_load_moment:.2f} kg-mm.\n")
            output_text += (f"Landing Weight is {total_weight_post_trip:.2f} kg.\n")
            output_text += (f"Landing Load Moment is {total_load_moment_post_trip:.2f} kg-mm.\n")
            if total_weight > MTOW:
                output_text += ("---ATTENTION PILOT--- Total weight exceeds MTOW! Get your papers in order or DO NOT FLY\n")
    


            # Performance calculations
            f_ground_roll, f_dist_to_clear_50ft = prepare_takeoff_interpolator(table_tkoff_2550lb)
            f_climb_speed, f_ROC = prepare_ROC_interpolator(table_ROC_2550lb)
            f_ldg_ground_roll, f_ldg_dist_to_clear_50ft = prepare_LDG_interpolator(table_ldg_2550lb)


            temperature = float(self.tempEntry.get())
            airport_code = self.airportSelection.get()
            wind_direction = float(self.winddEntry.get())
            wind_speed = float(self.windEntry.get())


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


            output_text += ("################################\n")
            output_text += (f"Runway INFO : {airport_code}\n")
            output_text += ("################################\n")
            output_text += (f"Elevation: {airport['elevation']} ft\n")
            output_text += (f"Best runway heading: {best_runway['heading']}\n")
            output_text += (f"Best runway length: {best_runway['length']} ft / {(best_runway['length'])*0.3048} m\n")
            output_text += ("################################\n")
            output_text += ("Non-Wind corrected distances\n")
            output_text += ("################################\n")
            output_text += (f"T/O Ground roll: {ground_roll:.2f} ft\n")
            output_text += (f"T/O Distance (x1.25): {dist_to_clear_50ft:.2f} ft\n")
            output_text += (f"Rate of Climb: {ROC:.2f} fpm at Climb Speed: {climb_speed:.2f} KIAS\n")
            output_text += (f"Landing ground roll: {ldg_ground_roll:.2f} ft\n")
            output_text += (f"Landing Distance (x1.42): {ldg_dist_to_clear_50ft:.2f} ft\n")
            output_text += ("################################\n")
            output_text += ("##########  ~WIND~  ############\n")
            output_text += ("################################\n")
            output_text += (f"Headwind component: {best_headwind:.2f} knots\n")
            output_text += (f"Crosswind component: {abs(best_crosswind):.2f} knots\n")
            output_text += (f"Adjusted T/O ground roll: {adjusted_ground_roll:.2f} feet\n")
            output_text += (f"Adjusted T/O Distance to clear 50ft (x1.25): {adjusted_dist_to_clear_50ft:.2f} feet\n")
            output_text += (f"Rate of Climb: {ROC:.2f} fpm at Climb Speed: {climb_speed:.2f} KIAS\n")
            output_text += (f"Adjusted landing ground roll: {adjusted_ldg_ground_roll:.2f} feet\n")
            output_text += (f"Adjusted landing distance to clear 50ft (x1.42): {adjusted_ldg_dist_to_clear_50ft:.2f} feet\n")

            if best_headwind > 15 or abs(best_crosswind) > 8:
                print(info_wind)
                output_text += (info_wind + "\n")

            if temperature > 35:
                print(info_temp)
                output_text += (info_temp + "\n")


            self.outputBox.insert("end", output_text)
            return



if __name__ == "__main__":
    app = App()
    app.mainloop()