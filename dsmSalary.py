from flask import Flask, render_template, url_for, request, redirect

import numpy as np
import skfuzzy as fuzz
# import pandas as pd
from skfuzzy import control as ctrl

import locale

def personalInformation(umur, status_pernikahan, jumlah_tanggungan, jarak_rumah, pendidikan_terakhir):
    age = ctrl.Antecedent(np.arange(0, 60, 5), 'age')
    age['young'] = fuzz.trapmf(age.universe, [0, 0, 25, 30])
    age['middle'] = fuzz.trimf(age.universe, [25, 30, 35])
    age['old'] = fuzz.trapmf(age.universe, [30, 35, 60, 60])

    distance = ctrl.Antecedent(np.arange(0, 105, 5), 'distance')
    distance['near'] = fuzz.trapmf(distance.universe, [0, 0, 10, 20])
    distance['average'] = fuzz.trimf(distance.universe, [10, 20, 30])
    distance['far'] = fuzz.trapmf(distance.universe, [20, 30, 100, 100])

    dependents = ctrl.Antecedent(np.arange(0, 8, 0.5), 'dependents')
    dependents['low'] = fuzz.trapmf(dependents.universe, [0, 0, 1, 3])
    dependents['middle'] = fuzz.trimf(dependents.universe, [1, 3, 5])
    dependents['high'] = fuzz.trapmf(dependents.universe, [3, 5, 8, 8])

    personal = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'personal')
    personal['low'] = fuzz.trapmf(personal.universe, [0, 0, 0.2, 0.5])
    personal['middle'] = fuzz.trimf(personal.universe, [0.2, 0.5, 0.8])
    personal['high'] = fuzz.trapmf(personal.universe, [0.5, 0.8, 1, 1])

    rule_personal_1 = ctrl.Rule(age['young'] & distance['near'] & dependents['low']  , personal['high'])
    rule_personal_2 = ctrl.Rule(age['young'] & distance['near'] & dependents['middle']  , personal['high'])
    rule_personal_3 = ctrl.Rule(age['young'] & distance['near'] & dependents['high']  , personal['middle'])
    rule_personal_4 = ctrl.Rule(age['young'] & distance['average'] & dependents['low']  , personal['high'])
    rule_personal_5 = ctrl.Rule(age['young'] & distance['average'] & dependents['middle']  , personal['middle'])
    rule_personal_6 = ctrl.Rule(age['young'] & distance['average'] & dependents['high']  , personal['middle'])
    rule_personal_7 = ctrl.Rule(age['young'] & distance['far'] & dependents['low']  , personal['middle'])
    rule_personal_8 = ctrl.Rule(age['young'] & distance['far'] & dependents['middle']  , personal['middle'])
    rule_personal_9 = ctrl.Rule(age['young'] & distance['far'] & dependents['high']  , personal['low'])
    rule_personal_10 = ctrl.Rule(age['middle'] & distance['near'] & dependents['low']  , personal['high'])
    rule_personal_11 = ctrl.Rule(age['middle'] & distance['near'] & dependents['middle']  , personal['high'])
    rule_personal_12 = ctrl.Rule(age['middle'] & distance['near'] & dependents['high']  , personal['middle'])
    rule_personal_13 = ctrl.Rule(age['middle'] & distance['average'] & dependents['low']  , personal['high'])
    rule_personal_14 = ctrl.Rule(age['middle'] & distance['average'] & dependents['middle']  , personal['middle'])
    rule_personal_15 = ctrl.Rule(age['middle'] & distance['average'] & dependents['high']  , personal['middle'])
    rule_personal_16 = ctrl.Rule(age['middle'] & distance['far'] & dependents['low']  , personal['middle'])
    rule_personal_17 = ctrl.Rule(age['middle'] & distance['far'] & dependents['middle']  , personal['low'])
    rule_personal_18 = ctrl.Rule(age['middle'] & distance['far'] & dependents['high']  , personal['low'])
    rule_personal_19 = ctrl.Rule(age['old'] & distance['near'] & dependents['low']  , personal['middle'])
    rule_personal_20 = ctrl.Rule(age['old'] & distance['near'] & dependents['middle']  , personal['middle'])
    rule_personal_21 = ctrl.Rule(age['old'] & distance['near'] & dependents['high']  , personal['middle'])
    rule_personal_22 = ctrl.Rule(age['old'] & distance['average'] & dependents['low']  , personal['low'])
    rule_personal_23 = ctrl.Rule(age['old'] & distance['average'] & dependents['middle']  , personal['low'])
    rule_personal_24 = ctrl.Rule(age['old'] & distance['average'] & dependents['high']  , personal['low'])
    rule_personal_25 = ctrl.Rule(age['old'] & distance['far'] & dependents['low']  , personal['low'])
    rule_personal_26 = ctrl.Rule(age['old'] & distance['far'] & dependents['middle']  , personal['low'])
    rule_personal_27 = ctrl.Rule(age['old'] & distance['far'] & dependents['high']  , personal['low'])

    personal_point_ctrl = ctrl.ControlSystem([rule_personal_1, rule_personal_2, rule_personal_3, rule_personal_4, rule_personal_5, 
                                            rule_personal_6, rule_personal_7, rule_personal_8, rule_personal_9, rule_personal_10, 
                                            rule_personal_11, rule_personal_12, rule_personal_13, rule_personal_14, rule_personal_15, 
                                            rule_personal_16, rule_personal_17, rule_personal_18, rule_personal_19, rule_personal_20, 
                                            rule_personal_21, rule_personal_22,rule_personal_23,rule_personal_24,rule_personal_25,
                                            rule_personal_26,rule_personal_27])
    
    personal_point = ctrl.ControlSystemSimulation(personal_point_ctrl)

    personal_point.input['age'] = umur
    personal_point.input['distance'] = jarak_rumah
    personal_point.input['dependents'] = jumlah_tanggungan

    # print("age ",ind, ": ", df['formAge'][ind])
    # print("Distance ", ind, ": ", df['formDistance'][ind])
    # print("dependents ", ind, ": ", df['formDependants'][ind])
    # personal_point.input['formal_edu'] = 0.8
    # personal_point.input['married'] = 1

    # COMPUTE FUZZY
    personal_point.compute()

    # COMBINE WITH NON-FUZZY
    # Marriage Status
    married_status = 0
    # if status_pernikahan == 'Belum menikah':
    #     married_status = 0
    # else:
    #     married_status = 1
    
    # Education
    edu_status = 0
    # if 'SD' in pendidikan_terakhir:
    #     edu_status = 1/7
    # elif  'SMP' in pendidikan_terakhir:
    #     edu_status = 2/7
    # elif 'SMA' in pendidikan_terakhir:
    #     edu_status = 3/7
    # elif 'D3' in pendidikan_terakhir:
    #     edu_status = 4/7
    # elif 'S1' in pendidikan_terakhir:
    #     edu_status = 5/7
    # elif 'S2' in pendidikan_terakhir:
    #     edu_status = 6/7
    # elif 'S3' in pendidikan_terakhir:
    #     edu_status = 1

    married_point = status_pernikahan * 0.007246377
    edu_point = (pendidikan_terakhir / 7) * 0.036231884
    total =( married_point + edu_point + (personal_point.output['personal'] * 0.1231884)) / 0.166666667
    # total = married_point + edu_point + (personal_point.output['personal'])

    WA = (personal_point.output['personal'] * 0.1231884)

    return total

def skills(pengetahuan, kemampuan, kecepatan, kualitas, jumlah):
    my_skill = ctrl.Antecedent(np.arange(0, 11, 1), 'my_skill')
    my_skill['low'] = fuzz.trapmf(my_skill.universe, [0, 0, 2, 5])
    my_skill['middle'] = fuzz.trimf(my_skill.universe, [2, 5, 8])
    my_skill['high'] = fuzz.trapmf(my_skill.universe, [5, 8, 10, 10])

    knowledge = ctrl.Antecedent(np.arange(0, 11, 1), 'knowledge')
    knowledge['low'] = fuzz.trapmf(knowledge.universe, [0, 0, 2, 5])
    knowledge['middle'] = fuzz.trimf(knowledge.universe, [2, 5, 8])
    knowledge['high'] = fuzz.trapmf(knowledge.universe, [5, 8, 10, 10])

    speed = ctrl.Antecedent(np.arange(0, 120, 1), 'speed')
    speed['fast'] = fuzz.trapmf(speed.universe, [0, 0, 10, 25])
    speed['middle'] = fuzz.trimf(speed.universe, [10, 25, 40])
    speed['slow'] = fuzz.trapmf(speed.universe, [25, 40, 120, 120])

    quantity = ctrl.Antecedent(np.arange(0, 11, 1), 'quantity')
    quantity['low'] = fuzz.trapmf(quantity.universe, [0, 0, 2, 5])
    quantity['middle'] = fuzz.trimf(quantity.universe, [2, 5, 8])
    quantity['high'] = fuzz.trapmf(quantity.universe, [5, 8, 10, 10])

    quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    quality['low'] = fuzz.trapmf(quality.universe, [0, 0, 2, 5])
    quality['middle'] = fuzz.trimf(quality.universe, [2, 5, 8])
    quality['high'] = fuzz.trapmf(quality.universe, [5, 8, 10, 10])

    skill = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'skill')
    skill['low'] = fuzz.trapmf(skill.universe, [0, 0, 0.2, 0.5])
    skill['middle'] = fuzz.trimf(skill.universe, [0.2, 0.5, 0.8])
    skill['high'] = fuzz.trapmf(skill.universe, [0.5, 0.8, 1, 1])

    rule_skill_1 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_2 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_3 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['high'] , skill['low'])
    rule_skill_4 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['low'])
    rule_skill_5 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_6 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_7 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['low'] , skill['low'])
    rule_skill_8 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_9 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['high'] , skill['middle'])
    rule_skill_10 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_11 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_12 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['high'] , skill['low'])
    rule_skill_13 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_14 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_15 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_16 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_17 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_18 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_19 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_20 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_21 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_22 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_23 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_24 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_25 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_26 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_27 = ctrl.Rule(my_skill['low'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_28 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_29 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_30 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['high'] , skill['low'])
    rule_skill_31 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_32 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_33 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_34 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['low'] , skill['low'])
    rule_skill_35 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_36 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_37 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_38 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_39 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_40 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_41 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_42 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_43 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_44 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_45 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_46 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_47 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_48 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_49 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_50 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_51 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_52 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_53 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_54 = ctrl.Rule(my_skill['low'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_55 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_56 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_57 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['high'] , skill['low'])
    rule_skill_58 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['low'])
    rule_skill_59 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_60 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_61 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_62 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_63 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['high'] , skill['middle'])
    rule_skill_64 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_65 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_66 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_67 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_68 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_69 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_70 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_71 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_72 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_73 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['low'] , skill['middle'])
    rule_skill_74 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_75 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_76 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_77 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_78 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_79 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_80 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_81 = ctrl.Rule(my_skill['low'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])

    rule_skill_82 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_83 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_84 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['high'] , skill['low'])
    rule_skill_85 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['low'])
    rule_skill_86 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_87 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_88 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['low'] , skill['low'])
    rule_skill_89 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_90 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['high'] , skill['middle'])
    rule_skill_91 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_92 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_93 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['high'] , skill['low'])
    rule_skill_94 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['low'])
    rule_skill_95 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_96 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_97 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_98 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_99 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_100 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_101 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_102 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_103 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_104 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_105 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_106 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_107 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_108 = ctrl.Rule(my_skill['middle'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_109 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_110 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_111 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_112 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_113 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_114 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_115 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_116 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_117 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_118 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_119 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_120 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_121 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_122 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_123 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_124 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_125 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_126 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_127 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_128 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_129 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_130 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_131 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_132 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_133 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_134 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_135 = ctrl.Rule(my_skill['middle'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_136 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_137 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_138 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_139 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_140 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_141 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_142 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_143 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_144 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_145 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['low'] , skill['middle'])
    rule_skill_146 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_147 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_148 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_149 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_150 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_151 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_152 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_153 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_154 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['low'] , skill['middle'])
    rule_skill_155 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_156 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_157 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_158 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_159 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['high'])
    rule_skill_160 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_161 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_162 = ctrl.Rule(my_skill['middle'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])

    rule_skill_163 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_164 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_165 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['low'] & quantity['high'] , skill['low'])
    rule_skill_166 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_167 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_168 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_169 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_170 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_171 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['slow'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_172 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['low'] , skill['middle'])
    rule_skill_173 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_174 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_175 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_176 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_177 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_178 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_179 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_180 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_181 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_182 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_183 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_184 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['low'])
    rule_skill_185 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_186 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_187 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_188 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_189 = ctrl.Rule(my_skill['high'] & knowledge['low']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_190 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_191 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_192 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_193 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['low'])
    rule_skill_194 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_195 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_196 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_197 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_198 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['slow'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_199 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_200 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_201 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_202 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_203 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_204 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_205 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_206 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_207 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_208 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['low'] , skill['middle'])
    rule_skill_209 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_210 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_211 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_212 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_213 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['high'])
    rule_skill_214 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_215 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_216 = ctrl.Rule(my_skill['high'] & knowledge['middle']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_217 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_218 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_219 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_220 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_221 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_222 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_223 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_224 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['middle'] , skill['middle'])
    rule_skill_225 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['slow'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_226 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_227 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['middle'] , skill['low'])
    rule_skill_228 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_229 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_230 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_231 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_232 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_233 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_234 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['middle'] & quality['high'] & quantity['high'] , skill['high'])
    rule_skill_235 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['low'] , skill['low'])
    rule_skill_236 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['middle'] , skill['middle'])
    rule_skill_237 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['low'] & quantity['high'] , skill['middle'])
    rule_skill_238 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['low'] , skill['middle'])
    rule_skill_239 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['middle'] , skill['middle'])
    rule_skill_240 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['middle'] & quantity['high'] , skill['middle'])
    rule_skill_241 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['low'] , skill['middle'])
    rule_skill_242 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['middle'] , skill['high'])
    rule_skill_243 = ctrl.Rule(my_skill['high'] & knowledge['high']  & speed['fast'] & quality['high'] & quantity['high'] , skill['high'])

    skill_point_ctrl = ctrl.ControlSystem([rule_skill_1, rule_skill_2, rule_skill_3, rule_skill_4, rule_skill_5, rule_skill_6, rule_skill_7,
                                        rule_skill_8, rule_skill_9, rule_skill_10, rule_skill_11, rule_skill_12, rule_skill_13, rule_skill_14, 
                                        rule_skill_15, rule_skill_16, rule_skill_17, rule_skill_18, rule_skill_19, rule_skill_20, rule_skill_21, 
                                        rule_skill_22,rule_skill_23,rule_skill_24,rule_skill_25,rule_skill_26,rule_skill_27,rule_skill_28,
                                        rule_skill_29,rule_skill_30,rule_skill_31,rule_skill_32,rule_skill_33,rule_skill_34,rule_skill_35,
                                        rule_skill_36,rule_skill_37,rule_skill_38,rule_skill_39,rule_skill_40,rule_skill_41,rule_skill_42,
                                        rule_skill_43,rule_skill_44,rule_skill_45,rule_skill_46,rule_skill_47,rule_skill_48,rule_skill_49,
                                        rule_skill_50,rule_skill_51,rule_skill_52,rule_skill_53,rule_skill_54,rule_skill_55,rule_skill_56,
                                        rule_skill_57,rule_skill_58,rule_skill_59,rule_skill_60,rule_skill_61,rule_skill_62,rule_skill_63,
                                        rule_skill_64,rule_skill_65,rule_skill_66,rule_skill_67,rule_skill_68,rule_skill_69,rule_skill_70,
                                        rule_skill_71,rule_skill_72,rule_skill_73,rule_skill_74,rule_skill_75,rule_skill_76,rule_skill_77,
                                        rule_skill_78,rule_skill_79,rule_skill_80,rule_skill_81,rule_skill_82,rule_skill_83,rule_skill_84,
                                        rule_skill_85,rule_skill_86,rule_skill_87,rule_skill_88,rule_skill_89,rule_skill_90,rule_skill_91,
                                        rule_skill_92,rule_skill_93,rule_skill_94,rule_skill_95,rule_skill_96,rule_skill_97,rule_skill_98,
                                        rule_skill_99,rule_skill_100,rule_skill_101,rule_skill_102,rule_skill_103,rule_skill_104,rule_skill_105,
                                        rule_skill_106,rule_skill_107,rule_skill_108,rule_skill_109,rule_skill_110,rule_skill_111,rule_skill_112,
                                        rule_skill_113,rule_skill_114,rule_skill_115,rule_skill_116,rule_skill_117,rule_skill_118,rule_skill_119,
                                        rule_skill_120,rule_skill_121,rule_skill_122,rule_skill_123,rule_skill_124,rule_skill_125,rule_skill_126,
                                        rule_skill_127,rule_skill_128,rule_skill_129,rule_skill_130,rule_skill_131,rule_skill_132,rule_skill_133,
                                        rule_skill_134,rule_skill_135,rule_skill_136,rule_skill_137,rule_skill_138,rule_skill_139,rule_skill_140,
                                        rule_skill_141,rule_skill_142,rule_skill_143,rule_skill_144,rule_skill_145,rule_skill_146,rule_skill_147,
                                        rule_skill_148,rule_skill_149,rule_skill_150,rule_skill_151,rule_skill_152,rule_skill_153,rule_skill_154,
                                        rule_skill_155,rule_skill_156,rule_skill_157,rule_skill_158,rule_skill_159,rule_skill_160,rule_skill_161,
                                        rule_skill_162,rule_skill_163,rule_skill_164,rule_skill_165,rule_skill_166,rule_skill_167,rule_skill_168,
                                        rule_skill_169,rule_skill_170,rule_skill_171,rule_skill_172,rule_skill_173,rule_skill_174,rule_skill_175,
                                        rule_skill_176,rule_skill_177,rule_skill_178,rule_skill_179,rule_skill_180,rule_skill_181,rule_skill_182,
                                        rule_skill_183,rule_skill_184,rule_skill_185,rule_skill_186,rule_skill_187,rule_skill_188,rule_skill_189,
                                        rule_skill_190,rule_skill_191,rule_skill_192,rule_skill_193,rule_skill_194,rule_skill_195,rule_skill_196,
                                        rule_skill_197,rule_skill_198,rule_skill_199,rule_skill_200,rule_skill_201,rule_skill_202,rule_skill_203,
                                        rule_skill_204,rule_skill_205,rule_skill_206,rule_skill_207,rule_skill_208,rule_skill_209,rule_skill_210,
                                        rule_skill_211,rule_skill_212,rule_skill_213,rule_skill_214,rule_skill_215,rule_skill_216,rule_skill_217,
                                        rule_skill_218,rule_skill_219,rule_skill_220,rule_skill_221,rule_skill_222,rule_skill_223,rule_skill_224,
                                        rule_skill_225,rule_skill_226,rule_skill_227,rule_skill_228,rule_skill_229,rule_skill_230,rule_skill_231,
                                        rule_skill_232,rule_skill_233,rule_skill_234,rule_skill_235,rule_skill_236,rule_skill_237,rule_skill_238,
                                        rule_skill_239,rule_skill_240,rule_skill_241,rule_skill_242,rule_skill_243])
    
    skill_point = ctrl.ControlSystemSimulation(skill_point_ctrl)

    knowledge_total = pengetahuan 
    skill_point.input['knowledge'] = knowledge_total

    my_skill_total = kemampuan 
    skill_point.input['my_skill'] = my_skill_total

    skill_point.input['speed'] = kecepatan
    skill_point.input['quantity'] = jumlah 
    skill_point.input['quality'] = kualitas

    # COMPUTE FUZZY
    skill_point.compute()
    total = (skill_point.output['skill'] * 0.33333333) / 0.33333333

    WA = skill_point.output['skill'] * 0.33333333

    return total

def attitude(perilaku, disiplin, kejujuran,  tanggung_jawab):
    my_attitude = ctrl.Antecedent(np.arange(0, 11, 1), 'my_attitude')
    my_attitude['low'] = fuzz.trapmf(my_attitude.universe, [0, 0, 2, 5])
    my_attitude['middle'] = fuzz.trimf(my_attitude.universe, [2, 5, 8])
    my_attitude['high'] = fuzz.trapmf(my_attitude.universe, [5, 8, 11, 11])

    discipline = ctrl.Antecedent(np.arange(0, 11, 1), 'discipline')
    discipline['low'] = fuzz.trapmf(discipline.universe, [0, 0, 2, 5])
    discipline['middle'] = fuzz.trimf(discipline.universe, [2, 5, 8])
    discipline['high'] = fuzz.trapmf(discipline.universe, [5, 8, 11, 11])

    respond = ctrl.Antecedent(np.arange(0, 11, 1), 'respond')
    respond['low'] = fuzz.trapmf(respond.universe, [0, 0, 2, 5])
    respond['middle'] = fuzz.trimf(respond.universe, [2, 5, 8])
    respond['high'] = fuzz.trapmf(respond.universe, [5, 8, 11, 11])

    honest = ctrl.Antecedent(np.arange(0, 11, 1), 'honest')
    honest['low'] = fuzz.trapmf(honest.universe, [0, 0, 2, 5])
    honest['middle'] = fuzz.trimf(honest.universe, [2, 5, 8])
    honest['high'] = fuzz.trapmf(honest.universe, [5, 8, 11, 11])

    attitude = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'attitude')
    attitude['low'] = fuzz.trapmf(attitude.universe, [0, 0, 0.2, 0.5])
    attitude['middle'] = fuzz.trimf(attitude.universe, [0.2, 0.5, 0.8])
    attitude['high'] = fuzz.trapmf(attitude.universe, [0.5, 0.8, 1.1, 1.1])

    rule_attitude_1 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['low'] & honest['low'] , attitude['low'])
    rule_attitude_2 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['low'] & honest['middle'] , attitude['low'])
    rule_attitude_3 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['low'] & honest['high'] , attitude['low'])
    rule_attitude_4 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['middle'] & honest['low'] , attitude['low'])
    rule_attitude_5 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['middle'] & honest['middle'] , attitude['low'])
    rule_attitude_6 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['middle'] & honest['high'] , attitude['middle'])
    rule_attitude_7 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['high'] & honest['low'] , attitude['low'])
    rule_attitude_8 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_9 = ctrl.Rule(my_attitude['low'] & discipline['low'] & respond['high'] & honest['high'] , attitude['middle'])
    rule_attitude_10 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['low'] & honest['low'] , attitude['low'])
    rule_attitude_11 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['low'] & honest['middle'] , attitude['middle'])
    rule_attitude_12 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['low'] & honest['high'] , attitude['middle'])
    rule_attitude_13 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['middle'] & honest['low'] , attitude['low'])
    rule_attitude_14 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['middle'] & honest['middle'] , attitude['middle'])
    rule_attitude_15 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['middle'] & honest['high'] , attitude['middle'])
    rule_attitude_16 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['high'] & honest['low'] , attitude['low'])
    rule_attitude_17 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_18 = ctrl.Rule(my_attitude['low'] & discipline['middle'] & respond['high'] & honest['high'] , attitude['high'])
    rule_attitude_19 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['low'] & honest['low'] , attitude['low'])
    rule_attitude_20 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['low'] & honest['middle'] , attitude['middle'])
    rule_attitude_21 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['low'] & honest['high'] , attitude['middle'])
    rule_attitude_22 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['middle'] & honest['low'] , attitude['middle'])
    rule_attitude_23 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['middle'] & honest['middle'] , attitude['middle'])
    rule_attitude_24 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['middle'] & honest['high'] , attitude['middle'])
    rule_attitude_25 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['high'] & honest['low'] , attitude['middle'])
    rule_attitude_26 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_27 = ctrl.Rule(my_attitude['low'] & discipline['high'] & respond['high'] & honest['high'] , attitude['high'])

    rule_attitude_28 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['low'] & honest['low'] , attitude['low'])
    rule_attitude_29 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['low'] & honest['middle'] , attitude['low'])
    rule_attitude_30 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['low'] & honest['high'] , attitude['middle'])
    rule_attitude_31 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['middle'] & honest['low'] , attitude['low'])
    rule_attitude_32 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['middle'] & honest['middle'] , attitude['middle'])
    rule_attitude_33 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['middle'] & honest['high'] , attitude['middle'])
    rule_attitude_34 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['high'] & honest['low'] , attitude['low'])
    rule_attitude_35 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_36 = ctrl.Rule(my_attitude['middle'] & discipline['low'] & respond['high'] & honest['high'] , attitude['middle'])
    rule_attitude_37 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['low'] & honest['low'] , attitude['low'])
    rule_attitude_38 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['low'] & honest['middle'] , attitude['middle'])
    rule_attitude_39 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['low'] & honest['high'] , attitude['middle'])
    rule_attitude_40 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['middle'] & honest['low'] , attitude['low'])
    rule_attitude_41 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['middle'] & honest['middle'] , attitude['middle'])
    rule_attitude_42 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['middle'] & honest['high'] , attitude['middle'])
    rule_attitude_43 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['high'] & honest['low'] , attitude['middle'])
    rule_attitude_44 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_45 = ctrl.Rule(my_attitude['middle'] & discipline['middle'] & respond['high'] & honest['high'] , attitude['high'])
    rule_attitude_46 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['low'] & honest['low'] , attitude['middle'])
    rule_attitude_47 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['low'] & honest['middle'] , attitude['middle'])
    rule_attitude_48 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['low'] & honest['high'] , attitude['high'])
    rule_attitude_49 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['middle'] & honest['low'] , attitude['middle'])
    rule_attitude_50 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['middle'] & honest['middle'] , attitude['middle'])
    rule_attitude_51 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['middle'] & honest['high'] , attitude['high'])
    rule_attitude_52 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['high'] & honest['low'] , attitude['middle'])
    rule_attitude_53 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_54 = ctrl.Rule(my_attitude['middle'] & discipline['high'] & respond['high'] & honest['high'] , attitude['high'])

    rule_attitude_55 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['low'] & honest['low'] , attitude['low'])
    rule_attitude_56 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['low'] & honest['middle'] , attitude['low'])
    rule_attitude_57 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['low'] & honest['high'] , attitude['middle'])
    rule_attitude_58 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['middle'] & honest['low'] , attitude['low'])
    rule_attitude_59 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['middle'] & honest['middle'] , attitude['middle'])
    rule_attitude_60 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['middle'] & honest['high'] , attitude['middle'])
    rule_attitude_61 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['high'] & honest['low'] , attitude['low'])
    rule_attitude_62 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_63 = ctrl.Rule(my_attitude['high'] & discipline['low'] & respond['high'] & honest['high'] , attitude['middle'])
    rule_attitude_64 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['low'] & honest['low'] , attitude['low'])
    rule_attitude_65 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['low'] & honest['middle'] , attitude['middle'])
    rule_attitude_66 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['low'] & honest['high'] , attitude['high'])
    rule_attitude_67 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['middle'] & honest['low'] , attitude['middle'])
    rule_attitude_68 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['middle'] & honest['middle'] , attitude['middle'])
    rule_attitude_69 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['middle'] & honest['high'] , attitude['high'])
    rule_attitude_70 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['high'] & honest['low'] , attitude['middle'])
    rule_attitude_71 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['high'] & honest['middle'] , attitude['middle'])
    rule_attitude_72 = ctrl.Rule(my_attitude['high'] & discipline['middle'] & respond['high'] & honest['high'] , attitude['high'])
    rule_attitude_73 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['low'] & honest['low'] , attitude['middle'])
    rule_attitude_74 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['low'] & honest['middle'] , attitude['middle'])
    rule_attitude_75 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['low'] & honest['high'] , attitude['high'])
    rule_attitude_76 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['middle'] & honest['low'] , attitude['middle'])
    rule_attitude_77 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['middle'] & honest['middle'] , attitude['high'])
    rule_attitude_78 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['middle'] & honest['high'] , attitude['high'])
    rule_attitude_79 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['high'] & honest['low'] , attitude['middle'])
    rule_attitude_80 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['high'] & honest['middle'] , attitude['high'])
    rule_attitude_81 = ctrl.Rule(my_attitude['high'] & discipline['high'] & respond['high'] & honest['high'] , attitude['high'])

    attitude_point_ctrl = ctrl.ControlSystem([rule_attitude_1, rule_attitude_2, rule_attitude_3, rule_attitude_4, rule_attitude_5, 
                                            rule_attitude_6, rule_attitude_7, rule_attitude_8, rule_attitude_9, rule_attitude_10, 
                                            rule_attitude_11, rule_attitude_12, rule_attitude_13, rule_attitude_14, rule_attitude_15, 
                                            rule_attitude_16, rule_attitude_17, rule_attitude_18, rule_attitude_19, rule_attitude_20, 
                                            rule_attitude_21, rule_attitude_22,rule_attitude_23,rule_attitude_24,rule_attitude_25,
                                            rule_attitude_26,rule_attitude_27,rule_attitude_28,rule_attitude_29,rule_attitude_30,
                                            rule_attitude_31,rule_attitude_32,rule_attitude_33,rule_attitude_34,rule_attitude_35,
                                            rule_attitude_36,rule_attitude_37,rule_attitude_38,rule_attitude_39,rule_attitude_40,
                                            rule_attitude_41,rule_attitude_42,rule_attitude_43,rule_attitude_44,rule_attitude_45,
                                            rule_attitude_46,rule_attitude_47,rule_attitude_48,rule_attitude_49,rule_attitude_50,
                                            rule_attitude_51,rule_attitude_52,rule_attitude_53,rule_attitude_54,rule_attitude_55,
                                            rule_attitude_56,rule_attitude_57,rule_attitude_58,rule_attitude_59,rule_attitude_60,
                                            rule_attitude_61,rule_attitude_62,rule_attitude_63,rule_attitude_64,rule_attitude_65,
                                            rule_attitude_66,rule_attitude_67,rule_attitude_68,rule_attitude_69,rule_attitude_70,
                                            rule_attitude_71,rule_attitude_72,rule_attitude_73,rule_attitude_74,rule_attitude_75,
                                            rule_attitude_76,rule_attitude_77,rule_attitude_78,rule_attitude_79,rule_attitude_80,
                                            rule_attitude_81])
    
    attitude_point = ctrl.ControlSystemSimulation(attitude_point_ctrl)

    attitude_point.input['my_attitude'] = perilaku 
    attitude_point.input['discipline'] = disiplin 
    attitude_point.input['respond'] = tanggung_jawab 
    attitude_point.input['honest'] = kejujuran 

    # COMPUTE FUZZY
    attitude_point.compute()

    # total = position_point + (achievment_point.output['achievment'] * 0.15942029)
    total = (attitude_point.output['attitude'] * 0.289855072) / 0.289855072

    return total

def achievement(pencapaian, pengalaman, gaji, posisi):
    my_achievment = ctrl.Antecedent(np.arange(0, 11, 1), 'my_achievment')
    my_achievment['low'] = fuzz.trapmf(my_achievment.universe, [0, 0, 2, 5])
    my_achievment['middle'] = fuzz.trimf(my_achievment.universe, [2, 5, 8])
    my_achievment['high'] = fuzz.trapmf(my_achievment.universe, [5, 8, 10, 10])

    salary_now = ctrl.Antecedent(np.arange(0, 500, 10), 'salary_now')
    salary_now['low'] = fuzz.trapmf(salary_now.universe, [0, 0, 60, 130])
    salary_now['middle'] = fuzz.trimf(salary_now.universe, [60, 130, 200])
    salary_now['high'] = fuzz.trapmf(salary_now.universe, [130, 200, 500, 500])

    my_experience = ctrl.Antecedent(np.arange(0, 49, 1), 'my_experience')
    my_experience['low'] = fuzz.trapmf(my_experience.universe, [0, 0, 4, 8])
    my_experience['middle'] = fuzz.trimf(my_experience.universe, [4, 8, 12])
    my_experience['high'] = fuzz.trapmf(my_experience.universe, [8, 12, 48, 48])

    achievment = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'achievment')
    achievment['low'] = fuzz.trapmf(achievment.universe, [0, 0, 0.2, 0.5])
    achievment['middle'] = fuzz.trimf(achievment.universe, [0.2, 0.5, 0.8])
    achievment['high'] = fuzz.trapmf(achievment.universe, [0.5, 0.8, 1, 1])

    rule_achievement_1 = ctrl.Rule(my_achievment['low'] & salary_now['low'] & my_experience['low']  , achievment['low'])
    rule_achievement_2 = ctrl.Rule(my_achievment['low'] & salary_now['low'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_3 = ctrl.Rule(my_achievment['low'] & salary_now['low'] & my_experience['high']  , achievment['high'])
    rule_achievement_4 = ctrl.Rule(my_achievment['low'] & salary_now['middle'] & my_experience['low']  , achievment['low'])
    rule_achievement_5 = ctrl.Rule(my_achievment['low'] & salary_now['middle'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_6 = ctrl.Rule(my_achievment['low'] & salary_now['middle'] & my_experience['high']  , achievment['high'])
    rule_achievement_7 = ctrl.Rule(my_achievment['low'] & salary_now['high'] & my_experience['low']  , achievment['middle'])
    rule_achievement_8 = ctrl.Rule(my_achievment['low'] & salary_now['high'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_9 = ctrl.Rule(my_achievment['low'] & salary_now['high'] & my_experience['high']  , achievment['high'])
    rule_achievement_10 = ctrl.Rule(my_achievment['middle'] & salary_now['low'] & my_experience['low']  , achievment['low'])
    rule_achievement_11 = ctrl.Rule(my_achievment['middle'] & salary_now['low'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_12 = ctrl.Rule(my_achievment['middle'] & salary_now['low'] & my_experience['high']  , achievment['high'])
    rule_achievement_13 = ctrl.Rule(my_achievment['middle'] & salary_now['middle'] & my_experience['low']  , achievment['low'])
    rule_achievement_14 = ctrl.Rule(my_achievment['middle'] & salary_now['middle'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_15 = ctrl.Rule(my_achievment['middle'] & salary_now['middle'] & my_experience['high']  , achievment['high'])
    rule_achievement_16 = ctrl.Rule(my_achievment['middle'] & salary_now['high'] & my_experience['low']  , achievment['middle'])
    rule_achievement_17 = ctrl.Rule(my_achievment['middle'] & salary_now['high'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_18 = ctrl.Rule(my_achievment['middle'] & salary_now['high'] & my_experience['high']  , achievment['high'])
    rule_achievement_19 = ctrl.Rule(my_achievment['high'] & salary_now['low'] & my_experience['low']  , achievment['low'])
    rule_achievement_20 = ctrl.Rule(my_achievment['high'] & salary_now['low'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_21 = ctrl.Rule(my_achievment['high'] & salary_now['low'] & my_experience['high']  , achievment['high'])
    rule_achievement_22 = ctrl.Rule(my_achievment['high'] & salary_now['middle'] & my_experience['low']  , achievment['low'])
    rule_achievement_23 = ctrl.Rule(my_achievment['high'] & salary_now['middle'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_24 = ctrl.Rule(my_achievment['high'] & salary_now['middle'] & my_experience['high']  , achievment['high'])
    rule_achievement_25 = ctrl.Rule(my_achievment['high'] & salary_now['high'] & my_experience['low']  , achievment['middle'])
    rule_achievement_26 = ctrl.Rule(my_achievment['high'] & salary_now['high'] & my_experience['middle']  , achievment['middle'])
    rule_achievement_27 = ctrl.Rule(my_achievment['high'] & salary_now['high'] & my_experience['high']  , achievment['high'])

    achievment_point_ctrl = ctrl.ControlSystem([rule_achievement_1, rule_achievement_2, rule_achievement_3, rule_achievement_4, 
                                                rule_achievement_5, rule_achievement_6, rule_achievement_7, rule_achievement_8,
                                                rule_achievement_9, rule_achievement_10, rule_achievement_11, rule_achievement_12, 
                                                rule_achievement_13, rule_achievement_14, rule_achievement_15, rule_achievement_16, 
                                                rule_achievement_17, rule_achievement_18, rule_achievement_19, rule_achievement_20, 
                                                rule_achievement_21, rule_achievement_22,rule_achievement_23,rule_achievement_24,
                                                rule_achievement_25,rule_achievement_26,rule_achievement_27])
                                                
    achievment_point = ctrl.ControlSystemSimulation(achievment_point_ctrl)

    # if '-' in pencapaian:
    #     result = 0
    #     achievment_point.input['my_achievment'] = 0
    # else:
    #     result = pencapaian.split(',')
    #     achievment_point.input['my_achievment'] = len(result)
    
    achievment_point.input['my_achievment'] = pencapaian
    achievment_point.input['salary_now'] = gaji / 100000 
    achievment_point.input['my_experience'] = pengalaman

    # COMPUTE FUZZY
    achievment_point.compute()

    # COMBINE WITH NON-FUZZY
    # Education
    position_status = 0
    # if 'mahasiswa' in posisi.lower():
    #     position_status = 1/5
    # elif  'junior' in posisi.lower():
    #     position_status = 2/5
    # elif 'mid' in posisi.lower() or 'middle' in posisi.lower() or 'specialist' in posisi.lower() or 'software' in posisi.lower():
    #     position_status = 3/5
    # elif 'senior' in posisi.lower():
    #     position_status = 4/5
    # elif 'manager' in posisi.lower() or 'lead' in posisi.lower():
    #     position_status = 1
    # # elif 'pimpinan' in df['formPosition'][ind].lower():
    # #   position_status = 1
    # else:
    #     position_status = 2/5

    position_point = (posisi / 5) * 0.050724638
    total = (position_point + (achievment_point.output['achievment'] * 0.15942029)) / 0.210144928

    WA = (achievment_point.output['achievment'] * 0.15942029)

    return total

def fuzzyStageTwo(total_pi, total_skills, total_attitude, total_achievement):
    personal_cat = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'personal_cat')
    personal_cat['low'] = fuzz.trapmf(personal_cat.universe, [0, 0, 0.2, 0.5])
    personal_cat['middle'] = fuzz.trimf(personal_cat.universe, [0.2, 0.5, 0.8])
    personal_cat['high'] = fuzz.trapmf(personal_cat.universe, [0.5, 0.8, 1, 1])

    skill_cat = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'skill_cat')
    skill_cat['low'] = fuzz.trapmf(skill_cat.universe, [0, 0, 0.2, 0.5])
    skill_cat['middle'] = fuzz.trimf(skill_cat.universe, [0.2, 0.5, 0.8])
    skill_cat['high'] = fuzz.trapmf(skill_cat.universe, [0.5, 0.8, 1, 1])


    attitude_cat = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'attitude_cat')
    attitude_cat['low'] = fuzz.trapmf(attitude_cat.universe, [0, 0, 0.2, 0.5])
    attitude_cat['middle'] = fuzz.trimf(attitude_cat.universe, [0.2, 0.5, 0.8])
    attitude_cat['high'] = fuzz.trapmf(attitude_cat.universe, [0.5, 0.8, 1, 1])

    achievment_cat = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'achievment_cat')
    achievment_cat['low'] = fuzz.trapmf(achievment_cat.universe, [0, 0, 0.2, 0.5])
    achievment_cat['middle'] = fuzz.trimf(achievment_cat.universe, [0.2, 0.5, 0.8])
    achievment_cat['high'] = fuzz.trapmf(achievment_cat.universe, [0.5, 0.8, 1, 1])

    salary = ctrl.Consequent(np.arange(0, 35, 1), 'salary')
    salary['low'] = fuzz.trapmf(salary.universe, [0, 0, 4, 12])
    salary['middle'] = fuzz.trimf(salary.universe, [3, 12, 20])
    salary['high'] = fuzz.trapmf(salary.universe, [12, 20, 35, 35])

    rule_salary_1 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['low'] , salary['low'])
    rule_salary_2 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['middle'] , salary['low'])
    rule_salary_3 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['high'] , salary['low'])
    rule_salary_4 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['low'] , salary['low'])
    rule_salary_5 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['low'])
    rule_salary_6 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['high'] , salary['low'])
    rule_salary_7 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['low'] , salary['low'])
    rule_salary_8 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['middle'] , salary['low'])
    rule_salary_9 = ctrl.Rule(personal_cat['low'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['high'] , salary['low'])
    rule_salary_10 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['low'] , salary['low'])
    rule_salary_11 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_12 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['high'] , salary['middle'])
    rule_salary_13 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['low'] , salary['middle'])
    rule_salary_14 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_15 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['high'] , salary['middle'])
    rule_salary_16 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['low'] , salary['middle'])
    rule_salary_17 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_18 = ctrl.Rule(personal_cat['low'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['high'] , salary['middle'])
    rule_salary_19 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['low'] , salary['middle'])
    rule_salary_20 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_21 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['high'] , salary['middle'])
    rule_salary_22 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['low'] , salary['middle'])
    rule_salary_23 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['high'])
    rule_salary_24 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['high'] , salary['high'])
    rule_salary_25 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['low'] , salary['high'])
    rule_salary_26 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['middle'] , salary['high'])
    rule_salary_27 = ctrl.Rule(personal_cat['low'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['high'] , salary['high'])

    rule_salary_28 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['low'] , salary['low'])
    rule_salary_29 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['middle'] , salary['low'])
    rule_salary_30 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['high'] , salary['low'])
    rule_salary_31 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['low'] , salary['low'])
    rule_salary_32 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['low'])
    rule_salary_33 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['high'] , salary['low'])
    rule_salary_34 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['low'] , salary['low'])
    rule_salary_35 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['middle'] , salary['low'])
    rule_salary_36 = ctrl.Rule(personal_cat['middle'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['high'] , salary['low'])
    rule_salary_37 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['low'] , salary['low'])
    rule_salary_38 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_39 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['high'] , salary['middle'])
    rule_salary_40 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['low'] , salary['middle'])
    rule_salary_41 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_42 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['high'] , salary['middle'])
    rule_salary_43 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['low'] , salary['middle'])
    rule_salary_44 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_45 = ctrl.Rule(personal_cat['middle'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['high'] , salary['middle'])
    rule_salary_46 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['low'] , salary['middle'])
    rule_salary_47 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['middle'] , salary['high'])
    rule_salary_48 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['high'] , salary['high'])
    rule_salary_49 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['low'] , salary['high'])
    rule_salary_50 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['high'])
    rule_salary_51 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['high'] , salary['high'])
    rule_salary_52 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['low'] , salary['high'])
    rule_salary_53 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['middle'] , salary['high'])
    rule_salary_54 = ctrl.Rule(personal_cat['middle'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['high'] , salary['high'])

    rule_salary_55 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['low'] , salary['low'])
    rule_salary_56 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['middle'] , salary['low'])
    rule_salary_57 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['low'] & achievment_cat['high'] , salary['low'])
    rule_salary_58 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['low'] , salary['low'])
    rule_salary_59 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['low'])
    rule_salary_60 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['middle'] & achievment_cat['high'] , salary['low'])
    rule_salary_61 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['low'] , salary['low'])
    rule_salary_62 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['middle'] , salary['low'])
    rule_salary_63 = ctrl.Rule(personal_cat['high'] & skill_cat['low'] & attitude_cat['high'] & achievment_cat['high'] , salary['low'])
    rule_salary_64 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['low'] , salary['low'])
    rule_salary_65 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_66 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['low'] & achievment_cat['high'] , salary['middle'])
    rule_salary_67 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['low'] , salary['middle'])
    rule_salary_68 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_69 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['middle'] & achievment_cat['high'] , salary['middle'])
    rule_salary_70 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['low'] , salary['middle'])
    rule_salary_71 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['middle'] , salary['middle'])
    rule_salary_72 = ctrl.Rule(personal_cat['high'] & skill_cat['middle'] & attitude_cat['high'] & achievment_cat['high'] , salary['middle'])
    rule_salary_73 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['low'] , salary['middle'])
    rule_salary_74 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['middle'] , salary['high'])
    rule_salary_75 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['low'] & achievment_cat['high'] , salary['high'])
    rule_salary_76 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['low'] , salary['high'])
    rule_salary_77 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['middle'] , salary['high'])
    rule_salary_78 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['middle'] & achievment_cat['high'] , salary['high'])
    rule_salary_79 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['low'] , salary['high'])
    rule_salary_80 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['middle'] , salary['high'])
    rule_salary_81 = ctrl.Rule(personal_cat['high'] & skill_cat['high'] & attitude_cat['high'] & achievment_cat['high'] , salary['high'])

    salary_point_ctrl = ctrl.ControlSystem([rule_salary_1, rule_salary_2, rule_salary_3, rule_salary_4, rule_salary_5, 
                                            rule_salary_6, rule_salary_7, rule_salary_8, rule_salary_9, rule_salary_10, 
                                            rule_salary_11, rule_salary_12, rule_salary_13, rule_salary_14, rule_salary_15, 
                                            rule_salary_16, rule_salary_17, rule_salary_18, rule_salary_19, rule_salary_20, 
                                            rule_salary_21, rule_salary_22,rule_salary_23,rule_salary_24,rule_salary_25,
                                            rule_salary_26,rule_salary_27,rule_salary_28,rule_salary_29,rule_salary_30,
                                            rule_salary_31,rule_salary_32,rule_salary_33,rule_salary_34,rule_salary_35,
                                            rule_salary_36,rule_salary_37,rule_salary_38,rule_salary_39,rule_salary_40,
                                            rule_salary_41,rule_salary_42,rule_salary_43,rule_salary_44,rule_salary_45,
                                            rule_salary_46,rule_salary_47,rule_salary_48,rule_salary_49,rule_salary_50,
                                            rule_salary_51,rule_salary_52,rule_salary_53,rule_salary_54,rule_salary_55,
                                            rule_salary_56,rule_salary_57,rule_salary_58,rule_salary_59,rule_salary_60,
                                            rule_salary_61,rule_salary_62,rule_salary_63,rule_salary_64,rule_salary_65,
                                            rule_salary_66,rule_salary_67,rule_salary_68,rule_salary_69,rule_salary_70,
                                            rule_salary_71,rule_salary_72,rule_salary_73,rule_salary_74,rule_salary_75,
                                            rule_salary_76,rule_salary_77,rule_salary_78,rule_salary_79,rule_salary_80,
                                            rule_salary_81])
                                            
    salary_point = ctrl.ControlSystemSimulation(salary_point_ctrl)

    salary_point.input['personal_cat'] = total_pi
    salary_point.input['skill_cat'] = total_skills
    salary_point.input['attitude_cat'] = total_attitude
    salary_point.input['achievment_cat'] = total_achievement

    # COMPUTE FUZZY
    salary_point.compute()

    # total = position_point + (achievment_point.output['achievment'] * 0.15942029)
    total = salary_point.output['salary'] * 1000000

    return rupiah_format(total)
    # return round(total, 2)

def rupiah_format(angka, with_prefix=False, desimal=2):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah