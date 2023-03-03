from flask import Flask, render_template, url_for, request, redirect

# import numpy as np
# import skfuzzy as fuzz
# # import pandas as pd
# from skfuzzy import control as ctrl

import dsmSalary as modelSalary
import dsmTeam as modelTeam
import dsmGreenCity as modelGreenCity

app = Flask(__name__)

class PersonalInformation:
    def __init__(self, umur, status_pernikahan, jumlah_tanggungan, jarak_rumah, pendidikan_terakhir, total_personal_information):
        self.umur = umur
        self.status_pernikahan = status_pernikahan
        self.jumlah_tanggungan = jumlah_tanggungan
        self.jarak_rumah = jarak_rumah
        self.pendidikan_terakhir = pendidikan_terakhir
        self.total_personal_information = total_personal_information

class Skills:
    def __init__(self, pengetahuan, kemampuan, kecepatan, kualitas, jumlah, total_skills):
        self.pengetahuan = pengetahuan
        self.kemampuan = kemampuan
        self.kecepatan = kecepatan
        self.kualitas = kualitas
        self.jumlah = jumlah
        self.total_skills = total_skills

class Attitude:
    def __init__(self, perilaku, disiplin, kejujuran, tanggung_jawab, total_attitude):
        self.perilaku = perilaku
        self.disiplin = disiplin
        self.kejujuran = kejujuran
        self.tanggung_jawab = tanggung_jawab
        self.total_attitude = total_attitude

class Achievement:
    def __init__(self, pencapaian, pengalaman_bekerja, gaji, level_pekerjaan, total_achievement):
        self.pencapaian = pencapaian
        self.pengalaman_bekerja = pengalaman_bekerja
        self.gaji = gaji
        self.level_pekerjaan = level_pekerjaan
        self.total_achievement = total_achievement

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dsm-salary')
def indexGreg():
    return render_template('gregoryus/index.html')

@app.route('/dsm-salary/result', methods=['POST', 'GET'])
def resultGreg():
    final_result = False
    if request.method == 'POST':
        # PERSONAL INFORMATION
        umur = float(request.form['umur'])
        status_pernikahan = float(request.form['status_pernikahan'])
        jumlah_tanggungan = float(request.form['jumlah_tanggungan'])
        jarak_rumah = float(request.form['jarak_rumah'])
        pendidikan_terakhir = float(request.form['pendidikan_terakhir'])

        married_status = 'Belum Menikah'
        if status_pernikahan == 0:
            married_status = 'Belum Menikah'
        else:
            married_status = 'Sudah Menikah'

        edu_status = 'SD'
        if pendidikan_terakhir == 1:
            edu_status = 'SD'
        elif  pendidikan_terakhir == 2:
            edu_status = 'SMP'
        elif  pendidikan_terakhir == 3:
            edu_status = 'SMA/SMK'
        elif  pendidikan_terakhir == 4:
            edu_status = 'D3'
        elif  pendidikan_terakhir == 5:
            edu_status = 'S1'
        elif  pendidikan_terakhir == 6:
            edu_status = 'S2'
        elif  pendidikan_terakhir == 7:
            edu_status = 'S3'

        total_personal_information = modelSalary.personalInformation(umur, status_pernikahan, jumlah_tanggungan, jarak_rumah, pendidikan_terakhir)
        pi_1 = PersonalInformation(int(umur), married_status, int(jumlah_tanggungan), jarak_rumah, edu_status, total_personal_information)
        

        # # SKILLS
        pengetahuan = float(request.form['pengetahuan'])
        kemampuan = float(request.form['kemampuan'])
        kecepatan = float(request.form['kecepatan'])
        kualitas = float(request.form['kualitas'])
        jumlah = float(request.form['jumlah'])

        total_skills = modelSalary.skills(pengetahuan, kemampuan, kecepatan, kualitas, jumlah)
        s_1 = Skills(pengetahuan, kemampuan, kecepatan, kualitas, jumlah, total_skills)

        # ATTITUDE
        perilaku = float(request.form['perilaku'])
        disiplin = float(request.form['disiplin'])
        kejujuran = float(request.form['kejujuran'])
        tanggung_jawab = float(request.form['tanggung_jawab'])

        total_attitude = modelSalary.attitude(perilaku, disiplin, kejujuran, tanggung_jawab)
        at_1 = Attitude(perilaku, disiplin, kejujuran, tanggung_jawab, total_attitude)

        # ACHIEVEMENT
        pencapaian = float(request.form['pencapaian'])
        pengalaman_bekerja = float(request.form['pengalaman_bekerja'])
        gaji = float(request.form['gaji'])
        level_pekerjaan = float(request.form['level_pekerjaan'])

        position_status = 'Mahasiswa'
        if level_pekerjaan == 1:
            position_status = 'Mahasiswa'
        elif  level_pekerjaan == 2:
            position_status = 'Junior Level'
        elif  level_pekerjaan == 3:
            position_status = 'Middle Level'
        elif  level_pekerjaan == 4:
            position_status = 'Senior Level'
        elif  level_pekerjaan == 5:
            position_status = 'Managerial'

        total_achievement = modelSalary.achievement(pencapaian, pengalaman_bekerja, gaji, level_pekerjaan)
        a_1 = Achievement(int(pencapaian), pengalaman_bekerja, int(gaji), position_status, total_achievement)

        final_salary = modelSalary.fuzzyStageTwo(total_personal_information, total_skills, total_attitude, total_achievement)

        final_result = True

        return render_template('gregoryus/result.html', pi = pi_1, ac = a_1, at = at_1, sk = s_1, final_salary = final_salary)
    else:
        return render_template('gregoryus/index.html')
    
@app.route('/dsm-team')
def indexMartin():
    return render_template('martin/index.html')
    
@app.route('/dsm-team/result', methods=['POST', 'GET'])
def resultMartin():
    if request.method == 'POST':
        result = list()
        extraversion = float(request.form["extraversion"])
        result.append(extraversion)
        openness_to_experience = float(request.form["ote"])
        result.append(openness_to_experience)
        conscientiousness = float(request.form["conscientiousness"])
        result.append(conscientiousness)
        agreeableness = float(request.form["agreeableness"])
        result.append(agreeableness)
        neuroticism = float(request.form["neuroticism"])
        result.append(neuroticism)
        interpersonal_skills = float(request.form["interpersonal"])
        result.append(interpersonal_skills)
        communication_skills = float(request.form["communication"])
        result.append(communication_skills)
        ability_to_work_independently = float(request.form["independently"])
        result.append(ability_to_work_independently)
        active_listener = float(request.form["listener"])
        result.append(active_listener)
        strong_analytical_problem_solving_skills = float(request.form["analytical"])
        result.append(strong_analytical_problem_solving_skills)
        open_adaptable_to_changes = float(request.form["changes"])
        result.append(open_adaptable_to_changes)
        innovative = float(request.form["innovative"])
        result.append(innovative)
        organization_skills = float(request.form["organization"])
        result.append(organization_skills)
        pay_thorough_acute_attention_to_details = float(request.form["attention"])
        result.append(pay_thorough_acute_attention_to_details)
        fast_learner = float(request.form["learner"])
        result.append(fast_learner)
        team_player = float(request.form["team"])
        result.append(team_player)

        value = []
        value.append(result)
        

        labels, centers, percentage = modelTeam.fuzzyCMeansClustering(value)
        percent = percentage

        if labels[0] == 0:
            labels = "System Analyst"
        elif labels[0] == 1:
            labels = "Software Designer"
        elif labels[0] == 2:
            labels = "Software Developer"
        elif labels[0] == 3:
            labels = "Software Tester"
        elif labels[0] == 4:
            labels = "Software Maintainer"


        system_analyst = "{:.2%}".format(percent[0][0])
        software_designer = "{:.2%}".format(percent[0][1])
        software_developer = "{:.2%}".format(percent[0][2])
        software_tester = "{:.2%}".format(percent[0][3])
        software_maintainer = "{:.2%}".format(percent[0][4])

        return render_template('martin/result.html', percentage =  percent, system_analyst = system_analyst, software_designer = software_designer, software_developer = software_developer, software_tester = software_tester, software_maintainer = software_maintainer, labels = labels)
    else:
        return render_template('martin/index.html')


@app.route('/dsm-greencity', methods=['POST', 'GET'])
def indexJoshua():
    if request.method == "POST":
        elec_consum = float(request.form["electricity"])
        water_consum = float(request.form["water"])
        air_qual = float(request.form["air"])
        bl_reg = float(request.form["region"])
        bl_rth = float(request.form["rth"])
        bl_pop = float(request.form["population"])
        tr_mot = float(request.form["motorcycle"])
        tr_car = float(request.form["car"])
        tr_bus = float(request.form["bus"])
        tr_tru = float(request.form["truck"])
        ws_gen = float(request.form["generate"])
        ws_red = float(request.form["reduce"])
        ws_han = float(request.form["handle"])
        ws_rec = float(request.form["recycle"])
        ws_raw = float(request.form["raw"])

        result1, result2, result3, result4, result5, result6 = modelGreenCity.process(elec_consum, water_consum, air_qual, bl_reg, bl_rth, bl_pop, tr_mot, tr_car, tr_bus, tr_tru, ws_gen, ws_red, ws_han, ws_rec, ws_raw)

        final_result = modelGreenCity.final(result1, result2, result3, result4, result5, result6)

        return render_template('joshua/index.html', final_result = final_result)
    else:
        return render_template('joshua/index.html')

if __name__ == "__main__":
    app.run(debug=True)