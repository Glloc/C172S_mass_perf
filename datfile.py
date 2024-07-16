#Data of airports and POH 

print('heellooo')

import numpy as np

# Define the airport data
airports = {
    'LEDA': {
        'elevation': 1152,
        'runways': 
            [
            {'heading': 133, 'length': 8202},
            {'heading': 313, 'length': 8202}
            ]
    },
    'LEHC': {
        'elevation': 1768,
        'runways': 
            [
            {'heading': 120, 'length': 6890},
            {'heading': 300, 'length': 6890}
            ]
    },
    'LERS': {
        'elevation': 233,
        'runways': 
            [
            {'heading': 70, 'length': 8068},
            {'heading': 250, 'length': 8068}
            ]
    },
    'LELL': {
        'elevation': 485,
        'runways': 
            [
            {'heading': 130, 'length': 3444},
            {'heading': 310, 'length': 3444}
            ]
    }
}

#Units = AC_Registration: KG, KG, KG, Litres, KG:L
aircraft_data = {
    'LY-BAK': {'empty_weight_moment': 782, 'empty_weight': 785, 'MTOW': 1157, 'fuel_conso': 36, 'fuel_density': 0.72},
    'LY-FTK': {'empty_weight_moment': 823.33, 'empty_weight': 776.1, 'MTOW': 1157, 'fuel_conso': 36, 'fuel_density': 0.72},
    'LY-FTG': {'empty_weight_moment': 823.48, 'empty_weight': 774.3, 'MTOW': 1157, 'fuel_conso': 36, 'fuel_density': 0.72},
    'LY-FTA': {'empty_weight_moment': 807.73, 'empty_weight': 788.8, 'MTOW': 1157, 'fuel_conso': 36, 'fuel_density': 0.72},
    'LY-FTF': {'empty_weight_moment': 833.69, 'empty_weight': 783.35, 'MTOW': 1157, 'fuel_conso': 36, 'fuel_density': 0.72},
    'LY-FTX': {'empty_weight_moment': 821, 'empty_weight': 782, 'MTOW': 1157, 'fuel_conso': 36, 'fuel_density': 0.72},
    'OO-JDH': {'empty_weight_moment': 839, 'empty_weight': 781, 'MTOW': 1157, 'fuel_conso': 36, 'fuel_density': 0.72},
    'LY-BGV': {'empty_weight_moment': 825.06, 'empty_weight': 780.4, 'MTOW': 1100, 'fuel_conso': 36, 'fuel_density': 0.72}
    #'LY-MEP': {'empty_weight_moment': 395, 'empty_weight': 868, 'MTOW': 1230, 'fuel_conso': 34, 'fuel_density': 0.72},

}

# Mass and balance coordinates of the loading diagram
coordinates = {
    'pilot_and_front_passenger': (188, 200),
    'fuel': (184, 152),
    'rear_passenger': (338, 182),
    'baggage_a': (120, 55),
    'baggage_b': (70, 23)
}

# Weight limits for each load type
weight_limits = {
    'pilot_and_front_passenger': 205,
    'fuel': 154,
    'rear_passenger': 182,
    'baggage_a': 54.4,
    'baggage_b': 22.7
}

table_tkoff_2550lb = np.array(
    #Format is [Pres Alt (ft), Temperature (C), Ground roll (ft), Dist to clear 50ft (ft)]
    [
    [[0, 0, 860, 1465],
    [1000, 0, 940, 1600],
    [2000, 0, 1025, 1755],
    [3000, 0, 1125, 1925],
    [4000, 0, 1235, 2120],
    [5000, 0, 1355, 2345],
    [6000, 0, 1495, 2605],
    [7000, 0, 1645, 2910],
    [8000, 0, 1820, 3265]],

    [[0, 10, 925, 1575],
     [1000, 10, 1010, 1720],
     [2000, 10, 1110, 1890],
     [3000, 10, 1215, 2080],
     [4000, 10, 1335, 2295],
     [5000, 10, 1465, 2545],
     [6000, 10, 1615, 2830],
     [7000, 10, 1785, 3170],
     [8000, 10, 1970, 3575]],

    [[0, 20, 995, 1690],
     [1000, 20, 1090, 1850],
     [2000, 20, 1195, 2035],
     [3000, 20, 1310, 2240],
     [4000, 20, 1440, 2480],
     [5000, 20, 1585, 2755],
     [6000, 20, 1745, 3075],
     [7000, 20, 1920, 3440],
     [8000, 20, 2120, 3880]],

    [[0, 30, 1070, 1810],
     [1000, 30, 1170, 1990],
     [2000, 30, 1285, 2190],
     [3000, 30, 1410, 2420],
     [4000, 30, 1550, 2685],
     [5000, 30, 1705, 2975],
     [6000, 30, 1875, 3320],
     [7000, 30, 2065, 3730],
     [8000, 30, 2280, 4225]],

    [[0, 40, 1150, 1945],
     [1000, 40, 1260, 2135],
     [2000, 40, 1380, 2355],
     [3000, 40, 1515, 2605],
     [4000, 40, 1660, 2880],
     [5000, 40, 1825, 3205],
     [6000, 40, 2010, 3585],
     [7000, 40, 2215, 4045],
     [8000, 40, 2450, 4615]]
    ])

table_ROC_2550lb= np.array(
    #Format is [Pres Alt (ft), Climb Speed (KIAS), Temperature (C), Rate of Climb (fpm)]
    [
    [[0, 74, -20, 855],
    [2000, 73, -20, 760],
    [4000, 73, -20, 685],
    [6000, 73, -20, 575],
    [8000, 72, -20, 465],
    [10000, 72, -20, 360],
    [12000, 72, -20, 255]],

    [[0, 74, 0, 785],
     [2000, 73, 0, 695],
     [4000, 73, 0, 620],
     [6000, 73, 0, 515],
     [8000, 72, 0, 405],
     [10000, 72, 0, 300],
     [12000, 72, 0, 195]],

    [[0, 74, 20, 710],
     [2000, 73, 20, 625],
     [4000, 73, 20, 555],
     [6000, 73, 20, 450],
     [8000, 72, 20, 345],
     [10000, 72, 20, 240],
     [12000, 72, 20, 135]],

    [[0, 74, 40, 645],
     [2000, 73, 40, 560],
     [4000, 73, 40, 495],
     [6000, 73, 40, 390],
     [8000, 72, 40, 285],
     [10000, 72, 40, 180],
     [12000, 72, 40, 0]]
    ])

table_ldg_2550lb = np.array(
    # Format is [Pres Alt (ft), Temperature (C), Ground roll (ft), Dist to clear 50ft (ft)]
    [
    [[0, 0, 545, 1290],
   [1000, 0, 565, 1320],
   [2000, 0, 585, 1355],
   [3000, 0, 610, 1385],
   [4000, 0, 630, 1425],
   [5000, 0, 655, 1460],
   [6000, 0, 680, 1500],
   [7000, 0, 705, 1545],
   [8000, 0, 735, 1585]],

  [[0, 10, 565, 1320],
   [1000, 10, 585, 1350],
   [2000, 10, 610, 1385],
   [3000, 10, 630, 1425],
   [4000, 10, 655, 1460],
   [5000, 10, 680, 1500],
   [6000, 10, 705, 1540],
   [7000, 10, 730, 1585],
   [8000, 10, 760, 1630]],

  [[0, 20, 585, 1350],
   [1000, 20, 605, 1385],
   [2000, 20, 630, 1420],
   [3000, 20, 655, 1460],
   [4000, 20, 675, 1495],
   [5000, 20, 705, 1535],
   [6000, 20, 730, 1580],
   [7000, 20, 760, 1625],
   [8000, 20, 790, 1670]],

  [[0, 30, 605, 1380],
   [1000, 30, 625, 1420],
   [2000, 30, 650, 1455],
   [3000, 30, 675, 1495],
   [4000, 30, 700, 1535],
   [5000, 30, 725, 1575],
   [6000, 30, 755, 1620],
   [7000, 30, 785, 1665],
   [8000, 30, 815, 1715]],

  [[0, 40, 625, 1415],
   [1000, 40, 650, 1450],
   [2000, 40, 670, 1490],
   [3000, 40, 695, 1530],
   [4000, 40, 725, 1570],
   [5000, 40, 750, 1615],
   [6000, 40, 780, 1660],
   [7000, 40, 810, 1705],
   [8000, 40, 840, 1755]]
    ])


info_wind = """
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


info_temp = """
---ATTENTION PILOT ---
It is getting pretty hot in here, and its not because of you! Check weather reports
Confirm that temperature DOES NOT go above the 38C limit!
"""