# -*- coding: utf-8 -*-
import os
import yaml
from re import search
from shutil import copyfile
import subprocess

def read_config_file():
    with open("config.yml", 'r') as confFile:
        config = yaml.load(confFile, Loader=yaml.FullLoader)
    return config


def create_student_dirs(filename):
    print("\nCréation des dossiers pour les étudiants ...")
    config = read_config_file()
    with open(filename, 'r', encoding='utf8') as studentsfile:
        lines = studentsfile.read().splitlines()
        for line in lines:
            student_dir = os.path.join(config['destination'], line)
            if not os.path.isdir(student_dir):
                os.mkdir(student_dir)
    print('Ok.\n')


def copy_final_thesis(config, year):
    print("Copie des mémoires " + year + " en cours ...")
    students_file_name = config['liste_etudiants']
    dest_dir = config['destination']
    thesis_dir = os.path.join(config['dossier_parent'], 'MEMOIRE I5\MEMOIRE-' + str(year))
    if not os.path.isdir(thesis_dir):
        thesis_dir = os.path.join(config['dossier_parent'], 'MEMOIRE I2\MEMOIRE-' + str(year))
        if not os.path.isdir(thesis_dir):
            print("[ERREUR] Dossier des mémoires non trouvé")
            handle_quit(1)
    copy_final_thesis_files(dest_dir, students_file_name, thesis_dir)
    print('Ok.\n')


def copy_final_thesis_files(dest_dir, students_file_name, thesis_dir):
    with open(students_file_name, 'r', encoding='utf8') as students_file:
        students = students_file.read().splitlines()
        for student in students:
            for folder in os.listdir(thesis_dir):
                for file in os.listdir(os.path.join(thesis_dir, folder)):
                    if search(student, file):
                        copyfile(os.path.join(thesis_dir, folder, file), os.path.join(dest_dir, student, file))


def copy_report_card(config, promo, year):
    school_year = str(str(year) + '-' + str(int(year) + 1))
    print("Copie des bulletins des " + promo + " " + school_year + " en cours ...")
    students_file_name = config['liste_etudiants']
    dest_dir = config['destination']
    report_card_dir = ""
    if promo == "I2":
        report_card_dir = os.path.join(config['dossier_parent'], 'BULLETINS', school_year, "I5", "Bulletins annuels définitifs")
        if not os.path.isdir(report_card_dir):
            report_card_dir_not_found = report_card_dir
            report_card_dir = os.path.join(config['dossier_parent'], 'BULLETINS', school_year, "I2", "Bulletins annuels definitifs")
            if not os.path.isdir(report_card_dir):
                print("[ERREUR] Dossier des bulletins I2-I5 non trouvé."
                      "\nChemins testés:\n" +
                      report_card_dir_not_found + "\n" +
                      report_card_dir + "\n")
                handle_quit(1)
    elif promo == "I1":
        report_card_dir = os.path.join(config['dossier_parent'], 'BULLETINS', school_year, "I4", "Definitifs")
        if not os.path.isdir(report_card_dir):
            report_card_dir_not_found = report_card_dir
            report_card_dir = os.path.join(config['dossier_parent'], 'BULLETINS', school_year, "I1", "Definitifs")
            if not os.path.isdir(report_card_dir):
                print("[ERREUR] Dossier des bulletins I1-I4 non trouvé."
                      "\nChemins testés:\n" +
                      report_card_dir_not_found + "\n" +
                      report_card_dir + "\n")
                handle_quit(1)
    elif promo == "B3" or promo == "B2" or promo == "B1":
        report_card_dir = os.path.join(config['dossier_parent'], 'BULLETINS', school_year, promo,
                                       "Definitifs")
        if not os.path.isdir(report_card_dir):
            print("[ERREUR] Dossier des bulletins " + promo + " non trouvé.\nChemin testé:\n" + report_card_dir)
            handle_quit(1)
    else:
        print("[ERREUR] Copie de bulletins : Promotion non reconnue : " + promo)
        handle_quit(1)
    with open(students_file_name, 'r', encoding='utf8') as students_file:
        students = students_file.read().splitlines()
        for student in students:
            for file in os.listdir(report_card_dir):
                if search(student, file):
                    copyfile(os.path.join(report_card_dir, file), os.path.join(dest_dir, student, file))
    print('Ok.\n')


def core(promo, year, config):
    if promo == "I2":
        copy_final_thesis(config, int(year) + 1)
        copy_report_card(config, "I2", year)
        copy_report_card(config, "I1", int(year) - 1)
    elif promo == "B3":
        copy_report_card(config, "B3", year)
        copy_report_card(config, "B2", int(year) - 1)
        copy_report_card(config, "B1", int(year) - 2)
    else:
        print("[ERREUR] Core : Promotion non reconnue : " + promo)
        handle_quit(1)


def handle_quit(code):
    input('\nAppuyez sur une touche pour quitter...')
    exit(code)


def handle_wrong_promo(promo):
    print("[ERREUR] Promotion non reconnue : " + promo)
    handle_quit(1)


if __name__ == '__main__':
    promotion = str(input('Quelle promo souhaitez-vous manipuler ? (Entrer "B3" ou "I2" ) \n-->   '))
    if promotion != "B3" and promotion != "I2":
        handle_wrong_promo(promotion)
    annee_promotion = str(input('\nEntrez l\'année de rentrée de la promotion: (2019, 2018 ...)\n-->   '))
    configFile = read_config_file()
    create_student_dirs(configFile['liste_etudiants'])
    core(promotion, annee_promotion, configFile)
    print("\nYouhou ! Opérations terminées ! :)\n")
    subprocess.Popen(r'explorer "' + configFile['destination'] + '"')
    handle_quit(0)
