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
                'anio': row[3],  # Assuming you don't need year as an integer
                'cuatrimestre': row[4],
                # ... rest of the dictionary construction
                'profesores': row[11]  # Keep 'profesores' data as a string
            })
    return materias


# Leer los archivos
aulas = leer_aulas('Aulas.csv')
materias = leer_materias('Materias.csv')


def asignar_aulas_y_horarios(aulas, materias):
    asignaciones = []

    for materia in materias:
        asignada = False

        # Intentar asignar aula
        for aula in aulas:
            if aula['capacidad'] >= materia['alumnos_esperados']:
                # Verificar disponibilidad
                available = all(aula['disponibilidad'][dia][hora] for dia, horas in materia['profesores'].items(
                    # Assuming comma-separated list
                ) for hora in horas.split(','))

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


# Asignar aulas y horarios
asignaciones = asignar_aulas_y_horarios(aulas, materias)

# Imprimir asignaciones
for asignacion in asignaciones:
    print(f"Materia: {asignacion['materia']}, Aula: {asignacion['aula']}, Día: {
          asignacion['dia']}, Horas: {asignacion['horas']}")


def guardar_asignaciones(asignaciones, archivo):
    with open(archivo, mode='w', newline='', encoding='ISO-8859-1') as csvfile:
        fieldnames = ['materia', 'aula', 'dia', 'horas']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for asignacion in asignaciones:
            writer.writerow(asignacion)


# Guardar las asignaciones
guardar_asignaciones(asignaciones, 'Asignaciones.csv')
