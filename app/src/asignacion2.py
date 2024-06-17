import csv
import ast

# Función para leer el archivo de aulas


def leer_aulas(archivo):
    aulas = []
    with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            aulas.append({
                'nombre': row[0],
                'capacidad': int(row[1]),
                'edificio': row[2],
                'disponibilidad': ast.literal_eval(row[3])
            })
    return aulas


# Función para leer el archivo de materias


def leer_materias(archivo):
    materias = []
    with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            materias.append({
                'codigo_guarani': row[0],
                'nombre': row[1],
                'carrera': row[2],
                'anio': row[3],
                'cuatrimestre': row[4],
                'profesores': None,  # Inicializar como None para manejar datos faltantes
                'alumnos_esperados': row[7],
            })

            # Validar y procesar la información de profesores
            try:
                profesores_value = row[11].strip()
                if profesores_value:  # Si no está vacío
                    profesores_data = ast.literal_eval(
                        profesores_value)  # Convierte a diccionario
                    if isinstance(profesores_data, dict) and all(key in profesores_data for key in ['dia', 'horas']):
                        materias[-1]['profesores'] = profesores_data
                    else:
                        print(f"Error: 'profesores' en la materia {
                              materias[-1]['nombre']} no tiene la estructura correcta")
                else:
                    print(f"Error: 'profesores' en la materia {
                          materias[-1]['nombre']} no es un diccionario válido")

            except (SyntaxError, ValueError):
                print(f"Error: 'profesores' en la materia {
                      materias[-1]['nombre']} no es un diccionario válido")

    return materias


# Leer los archivos
aulas = leer_aulas('Aulas.csv')
materias = leer_materias('Materias.csv')


# Función para asignar aulas y horarios

def asignar_aulas_y_horarios(aulas, materias):
    asignaciones = []

    for materia in materias:
        asignada = False

        # Intentar asignar aula
        for aula in aulas:
            if materia['alumnos_esperados'] <= aula['capacidad']:
                available = all(aula['disponibilidad'][dia][hora] for dia, horas in materia['profesores'].items()
                                for hora in horas.split(','))

                if available:
                    # Asignar aula y marcar horarios como ocupados
                    asignaciones.append({
                        'materia': materia['nombre'],
                        'aula': aula['nombre'],
                        'dia': dia,
                        'horas': horas
                    })
                    for hora in horas.split(','):
                        aula['disponibilidad'][dia][hora] = False
                    asignada = True
                    break

        if not asignada:
            print(f"No se pudo asignar aula para la materia {
                  materia['nombre']}")

    return asignaciones


# Función para guardar las asignaciones


def guardar_asignaciones(asignaciones, archivo):
    with open(archivo, mode='w', newline='', encoding='ISO-8859-1') as csvfile:
        fieldnames = ['materia', 'aula', 'dia', 'horas']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for asignacion in asignaciones:
            writer.writerow(asignacion)


# Asignar aulas y horarios
asignaciones = asignar_aulas_y_horarios(aulas, materias)
