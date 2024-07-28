import csv

def leer_materias(archivo):
    materias = []
    with open(archivo, 'r', newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            materias.append({
                'codigo_guarani': row['codigo_guarani'],
                'nombre': row['nombre'],
                'carrera': row['carrera'],
                'anio': row['anio'],  # Ajusta esta clave según el resultado de la impresión
                'cuatrimestre': row['cuatrimestre'],  # Ajusta esta clave según el resultado de la impresión
                'profesores': row['profesores'].split(';'),
                'alumnos_esperados': int(row['alumnos_esperados']),  # Ajusta esta clave según el resultado de la impresión
                'horas_frente_curso': int(row['horas_frente_curso']),  # Ajusta esta clave según el resultado de la impresión
                'comisiones': int(row['comisiones'])  # Ajusta esta clave según el resultado de la impresión
            })
    return materias

def leer_aulas(archivo):
    aulas = []
    with open(archivo, 'r', newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            horarios = eval(row['Horarios Disponibles'])
            aulas.append({
                'nombre': row['Nombre del Aula'],
                'capacidad': int(row['Capacidad']),
                'edificio': row['Edificio'],
                'horarios_disponibles': horarios
            })
    return aulas

def escribir_aulas(archivo, aulas):
    with open(archivo, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        fieldnames = ['Nombre del Aula', 'Capacidad', 'Edificio', 'Horarios Disponibles']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for aula in aulas:
            writer.writerow({
                'Nombre del Aula': aula['nombre'],
                'Capacidad': aula['capacidad'],
                'Edificio': aula['edificio'],
                'Horarios Disponibles': str(aula['horarios_disponibles'])
            })

def copiar_archivo_aulas(archivo_origen, archivo_destino):
    with open(archivo_origen, 'r', newline='', encoding='ISO-8859-1') as csvfile_origen, \
         open(archivo_destino, 'w', newline='', encoding='ISO-8859-1') as csvfile_destino:
        reader = csv.reader(csvfile_origen)
        writer = csv.writer(csvfile_destino)
        for row in reader:
            writer.writerow(row)

def reordenar_materias_por_alumnos(materias):
    return sorted(materias, key=lambda x: x['alumnos_esperados'], reverse=True)

def asignar_materias_a_aulas(materias, aulas):
    asignaciones_exitosas = []
    asignaciones_no_exitosas = []
    
    for materia in materias:
        materia_asignada = False
        for profesor in materia['profesores']:
            for aula in aulas:
                for dia, horarios in aula['horarios_disponibles'].items():
                    for i, disponible in enumerate(horarios):
                        if disponible is True:
                            aula['horarios_disponibles'][dia][i] = f"{materia['codigo_guarani']} - {profesor}"
                            asignaciones_exitosas.append({
                                'materia': materia['nombre'],
                                'codigo_guarani': materia['codigo_guarani'],
                                'profesor': profesor,
                                'aula': aula['nombre'],
                                'edificio': aula['edificio'],
                                'dia': dia,
                                'horario': i
                            })
                            materia_asignada = True
                            break
                    if materia_asignada:
                        break
                if materia_asignada:
                    break
            if materia_asignada:
                break
        if not materia_asignada:
            asignaciones_no_exitosas.append({
                'materia': materia['nombre'],
                'codigo_guarani': materia['codigo_guarani'],
                'profesores': materia['profesores']
            })
    
    return asignaciones_exitosas, asignaciones_no_exitosas

def guardar_asignaciones(asignaciones_exitosas, asignaciones_no_exitosas, archivo_exitosas, archivo_no_exitosas):
    with open(archivo_exitosas, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        fieldnames = ['Materia', 'Codigo Guarani', 'Profesor', 'Aula', 'Edificio', 'Dia', 'Horario']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for asignacion in asignaciones_exitosas:
            writer.writerow(asignacion)
    
    with open(archivo_no_exitosas, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        fieldnames = ['Materia', 'Codigo Guarani', 'Profesores']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for asignacion in asignaciones_no_exitosas:
            writer.writerow(asignacion)

# Crear una copia de aulas.csv y nombrarla "sugerencia_asignacion.csv"
copiar_archivo_aulas('aulas.csv', 'sugerencia_asignacion.csv')

# Leer materias y reordenarlas por cantidad de alumnos esperados
materias = leer_materias('Materias.csv')
materias_reordenadas = reordenar_materias_por_alumnos(materias)

# Leer aulas
aulas = leer_aulas('sugerencia_asignacion.csv')

# Asignar materias a aulas
asignaciones_exitosas, asignaciones_no_exitosas = asignar_materias_a_aulas(materias_reordenadas, aulas)

# Guardar asignaciones
guardar_asignaciones(asignaciones_exitosas, asignaciones_no_exitosas, 'Asignaciones_Exitosas.csv', 'Asignaciones_No_Exitosas.csv')

# Actualizar el archivo de aulas con las asignaciones realizadas
escribir_aulas('sugerencia_asignacion.csv', aulas)
