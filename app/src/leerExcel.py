import pandas as pd
import csv
from categorias.Materia import Materia
from categorias.Profesor import Profesor


def leer_excel(nombre_archivo):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(nombre_archivo)

        # Lista para almacenar datos procesados
        processed_data = []

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
                "carrera": carrera,
                "nombre": nombre_materia,
                "año": año,
                "cuatrimestre": cuatrimestre,
                "taxonomia": taxonomia,
                "horas_semanales": horas_semanales,
                "alumnos_esperados": alumnos_esperados,
                "comisiones": comisiones,
                "tipo_clase": tipo_clase,
                "horas_frente_curso": horas_frente_curso,
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

            # Agregar la materia a la lista de datos procesados
            processed_data.append(materia_data)

        # Guardar los datos en un archivo CSV
        with open('materias.csv', 'w', newline='', encoding='utf-8') as csvfile:
            # **Cambiar el orden de los campos**
            fieldnames = ["codigo_guarani", "nombre", "carrera", "año", "cuatrimestre", "taxonomia",
                          "horas_semanales", "alumnos_esperados", "comisiones", "tipo_clase",
                          "horas_frente_curso", "profesores"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for materia in processed_data:
                writer.writerow(materia)

    except Exception as e:
        print(f"Error processing the Excel file: {e}")


if __name__ == "__main__":
    leer_excel(r'etc\dist2cuadH.xlsx')
