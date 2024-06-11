import pandas as pd
from categorias.Materia import Materia
from categorias.Profesor import Profesor


def leer_excel(nombre_archivo):
    # Leer el archivo Excel
    df = pd.read_excel(nombre_archivo)

    # Lista para almacenar materias y profesores
    materias = []
    profesores = {}

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

        dni_profesor = row['DNI Docente']
        apellido_profesor = row['Apellido Docente']
        nombre_profesor = row['Nombre Docente']
        condicion_profesor = row['Condición']
        categoria_profesor = row['Categoría']
        dedicacion_profesor = row['Dedicación']

        # Crear un profesor
        profesor = Profesor(dni_profesor, apellido_profesor, nombre_profesor,
                            condicion_profesor, categoria_profesor, dedicacion_profesor, [])

        # Si el profesor aún no está en la lista, agregarlo
        if dni_profesor not in profesores:
            profesores[dni_profesor] = profesor

        # Agregar la materia al profesor
        profesores[dni_profesor].materias.append(
            {'nombre': nombre_materia, 'codigo_guarani': codigo_guarani})

        # Crear una materia y asignar los profesores
        materia = Materia(codigo_guarani, nombre_materia, año, cuatrimestre, taxonomia,
                          horas_semanales, alumnos_esperados, comisiones, tipo_clase, horas_frente_curso, [])
        materia.profesores.append(profesor.to_dict())

        # Agregar materia a la lista de materias
        materias.append(materia)

    # Guardar los datos en archivos CSV y JSON
    df_materias = pd.DataFrame([materia.to_dict() for materia in materias])
    df_profesores = pd.DataFrame([profesor.to_dict()
                                 for profesor in profesores.values()])

    df_materias.to_csv('materias.csv', index=False)
    df_profesores.to_csv('profesores.csv', index=False)

    df_materias.to_json('materias.json', orient='records')
    df_profesores.to_json('profesores.json', orient='records')


if __name__ == "__main__":
    leer_excel('etc\dist2cuad.xlsx')
