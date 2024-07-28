import csv


def imprimir_claves_csv(archivo):
    with open(archivo, 'r', newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        claves = reader.fieldnames
        print("Claves en el archivo CSV:", claves)


# Imprimir las claves del archivo Materias.csv
imprimir_claves_csv('Materias.csv')
