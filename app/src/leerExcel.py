import pandas as pd
import csv
from categorias.Materia import Materia
from categorias.Profesor import Profesor


def leer_excel(nombre_archivo):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(nombre_archivo)

        # Listas para almacenar datos procesados
        profesores_data = []
        carrera_data = []

        # Procesar cada fila del DataFrame
        for index, row in df.iterrows():
            codigo_guarani = row['Código Guaraní']
            nombre_materia = row['Materia']
            año = row['Año']
            cuatrimestre = row['Cuatrimestre']
            taxonomia = row['Taxonomía']
            horas_semanales = row['Horas Semanales']
            alumnos_esperados = row['Alumnos Esperados']
            comisiones = row['Comisiones']
            tipo_clase = row['Tipo de clase']
            horas_frente_curso = row['Horas frente al curso']
            carrera = row['Carrera']  # Nueva columna para la carrera

            dni_profesor = row['DNI Docente']
            apellido_profesor = row['Apellido Docente']
            nombre_profesor = row['Nombre Docente']
            condicion_profesor = row['Condición']
            categoria_profesor = row['Categoría']
            dedicacion_profesor = row['Dedicación']
            horarios_disponibles = row['Horarios Disponibles']

            # Crear un diccionario para almacenar datos de la materia
            materia_data = {
                "codigo_guarani": codigo_guarani,
                "nombre": nombre_materia,
                "año": año,
                "cuatrimestre": cuatrimestre,
                "taxonomia": taxonomia,
                "horas_semanales": horas_semanales,
                "alumnos_esperados": alumnos_esperados,
                "comisiones": comisiones,
                "tipo_clase": tipo_clase,
                "horas_frente_curso": horas_frente_curso,
                "carrera": carrera,
                "profesores": []
            }

            # Crear un diccionario para almacenar datos del profesor
            profesor_data = {
                "apellido": apellido_profesor,
                "nombre": nombre_profesor,
                "condicion": condicion_profesor,
                "categoria": categoria_profesor
            }

            # Agregar profesor a la materia
            materia_data["profesores"].append(profesor_data)

            # Procesar datos para profesores.csv
            profesores_data_row = {
                "dni": dni_profesor,
                "apellido": apellido_profesor,
                "nombre": nombre_profesor,
                "condicion": condicion_profesor,
                "categoria": categoria_profesor,
                "dedicacion": dedicacion_profesor,
                "horarios_disponibles": horarios_disponibles
            }
            profesores_data.append(profesores_data_row)

            # Procesar datos para carrera.csv
            carrera_data_row = {
                "codigo_guarani": codigo_guarani,
                "carrera": carrera
            }
            carrera_data.append(carrera_data_row)

        # Guardar datos en archivos CSV separados
        save_data_to_csv("profesores.csv", profesores_data)
        save_data_to_csv("carrera.csv", carrera_data)

    except Exception as e:
        print(f"Error processing the Excel file: {e}")


def save_data_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    leer_excel(r'etc\dist2cuadH.xlsx')
