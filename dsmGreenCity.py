import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd


def process(elec_consum, water_consum, air_qual, bl_reg, bl_rth, bl_pop, tr_mot, tr_car, tr_bus, tr_tru, ws_gen, ws_red, ws_han, ws_rec, ws_raw):
    #Distance Electricity Membership Function
    electricity_disc = ctrl.Antecedent(np.arange(0, 2501, 1), "Distance Electricity")
    electricity_disc['Low'] = fuzz.trapmf(electricity_disc.universe, [-750, 0, 750, 1500])
    electricity_disc['High'] = fuzz.trapmf(electricity_disc.universe, [750, 1500, 2501, 2501])

    #Electricity Membership Function
    electricity = ctrl.Consequent(np.arange(0, 2501, 1), "Electricity")
    electricity['Good'] = fuzz.trapmf(electricity.universe, [-750, 0, 750, 1500])
    electricity['Bad'] = fuzz.trapmf(electricity.universe, [750, 1500, 2501, 2501])

    #Electricity Rule Base
    rule1 = ctrl.Rule(electricity_disc['Low'], electricity['Good'])
    rule2 = ctrl.Rule(electricity_disc['High'], electricity['Bad'])

    electricity_ctrl = ctrl.ControlSystem([rule1, rule2])
    electricity_score = ctrl.ControlSystemSimulation(electricity_ctrl)

    electricity_score.input['Distance Electricity'] = elec_consum
    electricity_score.compute()
    electricity_result = round(electricity_score.output['Electricity'], 2)

    #Distance Water Membership Function
    water_disc = ctrl.Antecedent(np.arange(0, 50001, 1), "Distance Water")
    water_disc['Low'] = fuzz.trapmf(water_disc.universe, [-10000, 0, 10000, 25000])
    water_disc['High'] = fuzz.trapmf(water_disc.universe, [10000, 25000, 50001, 50001])

    #Water Membership Function
    water = ctrl.Consequent(np.arange(0, 50001, 1), "Water")
    water['Good'] = fuzz.trapmf(water.universe, [-10000, 0, 10000, 25000])
    water['Bad'] = fuzz.trapmf(water.universe, [10000, 25000, 50001, 50001])

    #Water Rule Base
    rule1 = ctrl.Rule(water_disc['Low'], water['Good'])
    rule2 = ctrl.Rule(water_disc['High'], water['Bad'])

    water_ctrl = ctrl.ControlSystem([rule1, rule2])
    water_score = ctrl.ControlSystemSimulation(water_ctrl)

    water_score.input['Distance Water'] = water_consum
    water_score.compute()
    water_result = round(water_score.output['Water'], 2)

    #Distance Air Membership Function
    air_disc = ctrl.Antecedent(np.arange(0, 301, 1), "Distance Air")
    air_disc['Good'] = fuzz.trapmf(air_disc.universe, [0.0, 0.0, 30, 60])
    air_disc['Average'] = fuzz.trimf(air_disc.universe, [40, 75, 110])
    air_disc['Unhealthy'] = fuzz.trimf(air_disc.universe, [90, 125, 160])
    air_disc['Very Unhealthy'] = fuzz.trimf(air_disc.universe, [140, 175, 210])
    air_disc['Dangerous'] = fuzz.trapmf(air_disc.universe, [190, 240, 301, 301])

    #Air Membership Function
    air = ctrl.Consequent(np.arange(0, 301, 1), "Air")
    air['Good'] = fuzz.trapmf(air.universe, [0.0, 0.0, 30, 60])
    air['Good'] = fuzz.trimf(air.universe, [40, 75, 110])
    air['Bad'] = fuzz.trimf(air.universe, [90, 125, 160])
    air['Bad'] = fuzz.trimf(air.universe, [140, 175, 210])
    air['Bad'] = fuzz.trapmf(air.universe, [190, 240, 301, 301])

    #Air Rule Base
    rule1 = ctrl.Rule(air_disc['Good'], air['Good'])
    rule2 = ctrl.Rule(air_disc['Average'], air['Good'])
    rule3 = ctrl.Rule(air_disc['Unhealthy'], air['Bad'])
    rule4 = ctrl.Rule(air_disc['Very Unhealthy'], air['Bad'])
    rule5 = ctrl.Rule(air_disc['Dangerous'], air['Bad'])

    air_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    air_score = ctrl.ControlSystemSimulation(air_ctrl)

    air_score.input['Distance Air'] = air_qual
    air_score.compute()
    air_result = round(air_score.output['Air'], 2)

    #Region Membership Function
    region = ctrl.Antecedent(np.arange(0, 2001, 1), "Region")
    region['Very Small'] = fuzz.trapmf(region.universe, [0.0, 0.0, 225, 450])
    region['Small'] = fuzz.trimf(region.universe, [425, 650, 875])
    region['Average'] = fuzz.trimf(region.universe, [850, 1075, 1300])
    region['Big'] = fuzz.trimf(region.universe, [1275, 1500, 1725])
    region['Very Big'] = fuzz.trapmf(region.universe, [1700, 1925, 2001, 2001])

    #RTH Membership Function
    rth = ctrl.Antecedent(np.arange(0, 1.01, 1), "RTH")
    rth['Bad'] = fuzz.trapmf(rth.universe, [0.0, 0.0, 0.10, 0.30])
    rth['Average'] = fuzz.trimf(rth.universe, [0.25, 0.45, 0.65])
    rth['Good'] = fuzz.trapmf(rth.universe, [0.60, 0.80, 1.01, 1.01])

    #Population Membership Function
    population = ctrl.Antecedent(np.arange(0, 601, 1), "Population Density")
    population['Low'] = fuzz.trapmf(population.universe, [-150, 0, 150, 300])
    population['High'] = fuzz.trapmf(population.universe, [150, 300, 601, 601])

    #Building Land Membership Function
    buildingland = ctrl.Consequent(np.arange(0, 101, 1), "Building Land")
    buildingland['Bad'] = fuzz.trapmf(buildingland.universe, [-100, 0, 25, 50])
    buildingland['Good'] = fuzz.trapmf(buildingland.universe, [25, 50, 101, 101])

    #Building Land Rule Base
    rule1 = ctrl.Rule(region['Very Small'] & rth['Bad'] & population['Low'], buildingland['Bad'])
    rule2 = ctrl.Rule(region['Very Small'] & rth['Average'] & population['Low'], buildingland['Good'])
    rule3 = ctrl.Rule(region['Very Small'] & rth['Good'] & population['Low'], buildingland['Good'])
    rule4 = ctrl.Rule(region['Very Small'] & rth['Bad'] & population['High'], buildingland['Bad'])
    rule5 = ctrl.Rule(region['Very Small'] & rth['Average'] & population['High'], buildingland['Good'])
    rule6 = ctrl.Rule(region['Very Small'] & rth['Good'] & population['High'], buildingland['Good'])
    rule7 = ctrl.Rule(region['Small'] & rth['Bad'] & population['Low'], buildingland['Bad'])
    rule8 = ctrl.Rule(region['Small'] & rth['Average'] & population['Low'], buildingland['Good'])
    rule9 = ctrl.Rule(region['Small'] & rth['Good'] & population['Low'], buildingland['Good'])
    rule10 = ctrl.Rule(region['Small'] & rth['Bad'] & population['High'], buildingland['Bad'])
    rule11 = ctrl.Rule(region['Small'] & rth['Average'] & population['High'], buildingland['Good'])
    rule12 = ctrl.Rule(region['Small'] & rth['Good'] & population['High'], buildingland['Good'])
    rule13 = ctrl.Rule(region['Average'] & rth['Bad'] & population['Low'], buildingland['Bad'])
    rule14 = ctrl.Rule(region['Average'] & rth['Average'] & population['Low'], buildingland['Good'])
    rule15 = ctrl.Rule(region['Average'] & rth['Good'] & population['Low'], buildingland['Good'])
    rule16 = ctrl.Rule(region['Average'] & rth['Bad'] & population['High'], buildingland['Bad'])
    rule17 = ctrl.Rule(region['Average'] & rth['Average'] & population['High'], buildingland['Good'])
    rule18 = ctrl.Rule(region['Average'] & rth['Good'] & population['High'], buildingland['Good'])
    rule19 = ctrl.Rule(region['Big'] & rth['Bad'] & population['Low'], buildingland['Bad'])
    rule20 = ctrl.Rule(region['Big'] & rth['Average'] & population['Low'], buildingland['Good'])
    rule21 = ctrl.Rule(region['Big'] & rth['Good'] & population['Low'], buildingland['Good'])
    rule22 = ctrl.Rule(region['Big'] & rth['Bad'] & population['High'], buildingland['Bad'])
    rule23 = ctrl.Rule(region['Big'] & rth['Average'] & population['High'], buildingland['Good'])
    rule24 = ctrl.Rule(region['Big'] & rth['Good'] & population['High'], buildingland['Good'])
    rule25 = ctrl.Rule(region['Very Big'] & rth['Bad'] & population['Low'], buildingland['Bad'])
    rule26 = ctrl.Rule(region['Very Big'] & rth['Average'] & population['Low'], buildingland['Good'])
    rule27 = ctrl.Rule(region['Very Big'] & rth['Good'] & population['Low'], buildingland['Good'])
    rule28 = ctrl.Rule(region['Very Big'] & rth['Bad'] & population['High'], buildingland['Bad'])
    rule29 = ctrl.Rule(region['Very Big'] & rth['Average'] & population['High'], buildingland['Good'])
    rule30 = ctrl.Rule(region['Very Big'] & rth['Good'] & population['High'], buildingland['Good'])

    buildingland_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, 
                                            rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30])
    buildingland_score = ctrl.ControlSystemSimulation(buildingland_ctrl)

    buildingland_score.input['Region'] = bl_reg
    buildingland_score.input['RTH'] = bl_rth
    buildingland_score.input['Population Density'] = bl_pop
    buildingland_score.compute()
    buildingland_result = round(buildingland_score.output['Building Land'], 2)

    #Motorcycle Membership Function
    motorcycle = ctrl.Antecedent(np.arange(0, 600001, 1), "Motorcycle")
    motorcycle['Low'] = fuzz.trapmf(motorcycle.universe, [-150000, 0, 150000, 300000])
    motorcycle['High'] = fuzz.trapmf(motorcycle.universe, [150000, 300000, 600001, 600001])

    #Car Membership Function
    car = ctrl.Antecedent(np.arange(0, 120001, 1), "Car")
    car['Low'] = fuzz.trapmf(car.universe, [-30000, 0, 30000, 60000])
    car['High'] = fuzz.trapmf(car.universe, [30000, 60000, 120001, 120001])

    #Bus Membership Function
    bus = ctrl.Antecedent(np.arange(0, 2001, 1), "Bus")
    bus['Low'] = fuzz.trapmf(bus.universe, [-500, 0, 500, 1000])
    bus['High'] = fuzz.trapmf(bus.universe, [500, 1000, 2001, 2001])

    #Truck Membership Function
    truck = ctrl.Antecedent(np.arange(0, 30001, 1), "Truck")
    truck['Low'] = fuzz.trapmf(truck.universe, [-10000, 0, 10000, 20000])
    truck['High'] = fuzz.trapmf(truck.universe, [10000, 20000, 30001, 30001])

    #Transportation Membership Function
    transportation = ctrl.Consequent(np.arange(0, 101, 1), "Transportation")
    transportation['Bad'] = fuzz.trapmf(transportation.universe, [-100, 0, 25, 50])
    transportation['Good'] = fuzz.trapmf(transportation.universe, [25, 50, 101, 101])

    #Transportation Rule Base
    rule1 = ctrl.Rule(motorcycle['Low'] & car['Low'] & bus['Low'] & truck['Low'], transportation['Good'])
    rule2 = ctrl.Rule(motorcycle['Low'] & car['Low'] & bus['Low'] & truck['High'], transportation['Good'])
    rule3 = ctrl.Rule(motorcycle['Low'] & car['Low'] & bus['High'] & truck['Low'], transportation['Good'])
    rule4 = ctrl.Rule(motorcycle['Low'] & car['High'] & bus['Low'] & truck['Low'], transportation['Good'])
    rule5 = ctrl.Rule(motorcycle['High'] & car['Low'] & bus['Low'] & truck['Low'], transportation['Good'])
    rule6 = ctrl.Rule(motorcycle['Low'] & car['Low'] & bus['High'] & truck['High'], transportation['Bad'])
    rule7 = ctrl.Rule(motorcycle['Low'] & car['High'] & bus['Low'] & truck['High'], transportation['Bad'])
    rule8 = ctrl.Rule(motorcycle['Low'] & car['High'] & bus['High'] & truck['Low'], transportation['Bad'])
    rule9 = ctrl.Rule(motorcycle['High'] & car['Low'] & bus['Low'] & truck['High'], transportation['Good'])
    rule10 = ctrl.Rule(motorcycle['High'] & car['Low'] & bus['High'] & truck['Low'], transportation['Good'])
    rule11 = ctrl.Rule(motorcycle['High'] & car['High'] & bus['Low'] & truck['Low'], transportation['Good'])
    rule12 = ctrl.Rule(motorcycle['High'] & car['High'] & bus['High'] & truck['Low'], transportation['Bad'])
    rule13 = ctrl.Rule(motorcycle['High'] & car['High'] & bus['Low'] & truck['High'], transportation['Bad'])
    rule14 = ctrl.Rule(motorcycle['High'] & car['Low'] & bus['High'] & truck['High'], transportation['Bad'])
    rule15 = ctrl.Rule(motorcycle['Low'] & car['High'] & bus['High'] & truck['High'], transportation['Bad'])
    rule16 = ctrl.Rule(motorcycle['High'] & car['High'] & bus['High'] & truck['High'], transportation['Bad'])

    transportation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, 
                                            rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16])
    transportation_score = ctrl.ControlSystemSimulation(transportation_ctrl)

    transportation_score.input['Motorcycle'] = tr_mot
    transportation_score.input['Car'] = tr_car
    transportation_score.input['Bus'] = tr_bus
    transportation_score.input['Truck'] = tr_tru
    transportation_score.compute()
    transportation_result = round(transportation_score.output['Transportation'], 2)

    #Waste Generate Membership Function
    generate = ctrl.Antecedent(np.arange(0, 70001, 1), "Waste Generate")
    generate['Low'] = fuzz.trapmf(generate.universe, [-35000, 0, 17500, 35000])
    generate['High'] = fuzz.trapmf(generate.universe, [17500, 35000, 70001, 70001])

    #Waste Deduct Membership Function
    deduct = ctrl.Antecedent(np.arange(0, 35001, 1), "Waste Deduct")
    deduct['Low'] = fuzz.trapmf(deduct.universe, [-15000, 0, 15000, 30000])
    deduct['High'] = fuzz.trapmf(deduct.universe, [15000, 30000, 35001, 35001])

    #Waste Handle Membership Function
    handle = ctrl.Antecedent(np.arange(0, 160001, 1), "Waste Handle")
    handle['Low'] = fuzz.trapmf(handle.universe, [-160000, 0, 40000, 80000])
    handle['High'] = fuzz.trapmf(handle.universe, [40000, 80000, 160001, 160001])

    #Waste Recycle Membership Function
    recycle = ctrl.Antecedent(np.arange(0, 40001, 1), "Waste Recycle")
    recycle['Low'] = fuzz.trapmf(recycle.universe, [-10000, 0, 10000, 20000])
    recycle['High'] = fuzz.trapmf(recycle.universe, [10000, 20000, 40001, 40001])

    #Waste Raw Membership Function
    raw = ctrl.Antecedent(np.arange(0, 5001, 1), "Waste Raw")
    raw['Low'] = fuzz.trapmf(raw.universe, [-50000, 0, 1000, 3000])
    raw['High'] = fuzz.trapmf(raw.universe, [1000, 3000, 5001, 5001])

    #Waste Membership Function
    waste = ctrl.Consequent(np.arange(0, 101, 1), "Waste")
    waste['Bad'] = fuzz.trapmf(waste.universe, [-100, 0, 25, 50])
    waste['Good'] = fuzz.trapmf(waste.universe, [25, 50, 101, 101])

    #Waste Rule Base
    rule1 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['Low'] & recycle['Low'] & raw['Low'], waste['Bad'])
    rule2 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['Low'] & recycle['Low'] & raw['High'], waste['Bad'])
    rule3 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['Low'] & recycle['High'] & raw['Low'], waste['Good'])
    rule4 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['High'] & recycle['Low'] & raw['Low'], waste['Good'])
    rule5 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['Low'] & recycle['Low'] & raw['Low'], waste['Good'])
    rule6 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['Low'] & recycle['Low'] & raw['Low'], waste['Bad'])
    rule7 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['Low'] & recycle['High'] & raw['High'], waste['Good'])
    rule8 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['High'] & recycle['Low'] & raw['High'], waste['Good'])
    rule9 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['Low'] & recycle['Low'] & raw['High'], waste['Good'])
    rule10 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['Low'] & recycle['Low'] & raw['High'], waste['Bad'])
    rule11 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['High'] & recycle['High'] & raw['Low'], waste['Good'])
    rule12 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['Low'] & recycle['High'] & raw['Low'], waste['Good'])
    rule13 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['Low'] & recycle['High'] & raw['Low'], waste['Bad'])
    rule14 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['High'] & recycle['Low'] & raw['Low'], waste['Good'])
    rule15 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['High'] & recycle['Low'] & raw['Low'], waste['Good'])
    rule16 = ctrl.Rule(generate['High'] & deduct['High'] & handle['Low'] & recycle['Low'] & raw['Low'], waste['Good'])
    rule17 = ctrl.Rule(generate['High'] & deduct['High'] & handle['High'] & recycle['Low'] & raw['Low'], waste['Good'])
    rule18 = ctrl.Rule(generate['High'] & deduct['High'] & handle['Low'] & recycle['High'] & raw['Low'], waste['Good'])
    rule19 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['High'] & recycle['High'] & raw['Low'], waste['Good'])
    rule20 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['High'] & recycle['High'] & raw['Low'], waste['Good'])
    rule21 = ctrl.Rule(generate['High'] & deduct['High'] & handle['Low'] & recycle['Low'] & raw['High'], waste['Good'])
    rule22 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['High'] & recycle['Low'] & raw['High'], waste['Good'])
    rule23 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['High'] & recycle['Low'] & raw['High'], waste['Good'])
    rule24 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['Low'] & recycle['High'] & raw['High'], waste['Good'])
    rule25 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['Low'] & recycle['High'] & raw['High'], waste['Good'])
    rule26 = ctrl.Rule(generate['Low'] & deduct['Low'] & handle['High'] & recycle['High'] & raw['High'], waste['Good'])
    rule27 = ctrl.Rule(generate['High'] & deduct['High'] & handle['High'] & recycle['High'] & raw['Low'], waste['Good'])
    rule28 = ctrl.Rule(generate['High'] & deduct['High'] & handle['High'] & recycle['Low'] & raw['High'], waste['Good'])
    rule29 = ctrl.Rule(generate['High'] & deduct['High'] & handle['Low'] & recycle['High'] & raw['High'], waste['Good'])
    rule30 = ctrl.Rule(generate['High'] & deduct['Low'] & handle['High'] & recycle['High'] & raw['High'], waste['Good'])
    rule31 = ctrl.Rule(generate['Low'] & deduct['High'] & handle['High'] & recycle['High'] & raw['High'], waste['Good'])
    rule32 = ctrl.Rule(generate['High'] & deduct['High'] & handle['High'] & recycle['High'] & raw['High'], waste['Good'])

    waste_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, 
                                    rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30])
    waste_score = ctrl.ControlSystemSimulation(waste_ctrl)

    waste_score.input['Waste Generate'] = ws_gen
    waste_score.input['Waste Deduct'] = ws_red
    waste_score.input['Waste Handle'] = ws_han 
    waste_score.input['Waste Recycle'] = ws_rec
    waste_score.input['Waste Raw'] = ws_raw
    waste_score.compute()
    waste_result = round(waste_score.output['Waste'], 2)

    return electricity_result, water_result, air_result, buildingland_result, transportation_result, waste_result

def final(electricity_final, water_final, air_final, buildingland_final, transportation_final, waste_final):
    #Electricity Membership Function
    electricity = ctrl.Antecedent(np.arange(0, 101, 1), "Electricity")
    electricity['Bad'] = fuzz.trapmf(electricity.universe, [0, 0, 25, 50])
    electricity['Good'] = fuzz.trapmf(electricity.universe, [25, 50, 101, 101])

    #Water Membership Function
    water = ctrl.Antecedent(np.arange(0, 101, 1), "Water")
    water['Bad'] = fuzz.trapmf(water.universe, [0, 0, 25, 50])
    water['Good'] = fuzz.trapmf(water.universe, [25, 50, 101, 101])

    #Air Membership Function
    air = ctrl.Antecedent(np.arange(0, 101, 1), "Air")
    air['Good'] = fuzz.trapmf(air.universe, [0, 0, 25, 50])
    air['Bad'] = fuzz.trapmf(air.universe, [25, 50, 101, 101])

    #Building Land Membership Function
    buildingland = ctrl.Antecedent(np.arange(0, 101, 1), "Building Land")
    buildingland['Bad'] = fuzz.trapmf(buildingland.universe, [0, 0, 25, 50])
    buildingland['Good'] = fuzz.trapmf(buildingland.universe, [25, 50, 101, 101])

    #Transportation Membership Function
    transportation = ctrl.Antecedent(np.arange(0, 101, 1), "Transportation")
    transportation['Bad'] = fuzz.trapmf(transportation.universe, [0, 0, 25, 50])
    transportation['Good'] = fuzz.trapmf(transportation.universe, [25, 50, 101, 101])

    #Waste Membership Function
    waste = ctrl.Antecedent(np.arange(0, 101, 1), "Waste")
    waste['Bad'] = fuzz.trapmf(waste.universe, [0, 0, 25, 50])
    waste['Good'] = fuzz.trapmf(waste.universe, [25, 50, 101, 101])

    #Green City Membership Function
    greencity = ctrl.Consequent(np.arange(0, 101, 1), "Green City")
    greencity['Bad'] = fuzz.trapmf(greencity.universe, [0, 0, 25, 50])
    greencity['Good'] = fuzz.trapmf(greencity.universe, [25, 50, 101, 101])

    #Green City Rule Base
    rule1 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule2 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule3 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule4 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule5 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule6 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule7 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule8 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule9 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule10 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule11 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule12 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule13 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule14 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Bad'])
    rule15 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule16 = ctrl.Rule(electricity['Good'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Bad'])
    rule17 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule18 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule19 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule20 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule21 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule22 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule23 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule24 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule25 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule26 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule27 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule28 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule29 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule30 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Bad'])
    rule31 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule32 = ctrl.Rule(electricity['Good'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Bad'])
    rule33 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule34 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule35 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule36 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule37 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule38 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule39 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule40 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule41 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule42 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule43 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule44 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule45 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule46 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Bad'])
    rule47 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule48 = ctrl.Rule(electricity['Bad'] & water['Good'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Bad'])
    rule49 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule50 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule51 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule52 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule53 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule54 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule55 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule56 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Good'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule57 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule58 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Good'] & waste['Bad'], greencity['Good'])
    rule59 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule60 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Good'] & transportation['Bad'] & waste['Bad'], greencity['Good'])
    rule61 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Good'], greencity['Good'])
    rule62 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Good'] & waste['Bad'], greencity['Bad'])
    rule63 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Good'], greencity['Good'])
    rule64 = ctrl.Rule(electricity['Bad'] & water['Bad'] & air['Bad'] & buildingland['Bad'] & transportation['Bad'] & waste['Bad'], greencity['Bad'])

    greencity_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, 
                                        rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, 
                                        rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, 
                                        rule49, rule50, rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60, rule61, rule62, rule63, rule64])
    greencity_score = ctrl.ControlSystemSimulation(greencity_ctrl)

    greencity_score.input['Electricity'] = electricity_final
    greencity_score.input['Water'] = water_final
    greencity_score.input['Air'] = air_final
    greencity_score.input['Building Land'] = buildingland_final
    greencity_score.input['Transportation'] = transportation_final
    greencity_score.input['Waste'] = waste_final
    greencity_score.compute()
    greencity_result = round(greencity_score.output['Green City'], 2)
    return greencity_result