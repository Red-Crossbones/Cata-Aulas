import csv
import ast
import sys
from collections import defaultdict

# Configurar la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='ISO-8859-1')


def leer_aulas(archivo):
    aulas = []
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar encabezado
            for row in reader:
                if len(row) >= 4:
                    try:
                        capacidad = int(row[1]) if row[1].isdigit() else 0
                        disponibilidad = ast.literal_eval(
                            row[3]) if row[3] else []
                        aulas.append({
                            'nombre': row[0],
                            'capacidad': capacidad,
                            'edificio': row[2],
                            'disponibilidad': disponibilidad
                        })
                    except (ValueError, SyntaxError):
                        print(f"Error: Valor inválido en la fila {
                              row} del archivo {archivo}")
                else:
                    print(f"Error: Fila con menos de 4 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error as e:
        print(f"Error: Error al leer el archivo {archivo}: {e}")
    return aulas


def leer_materias(archivo):
    materias = []
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar encabezado
            for row in reader:
                if len(row) >= 12:  # Ajustado para asegurar que todas las columnas requeridas estén presentes
                    # Convertir lista de diccionarios a un string con nombres de profesores
                    profesores = row[11]
                    try:
                        profesores_lista = ast.literal_eval(profesores)
                        if isinstance(profesores_lista, list):
                            profesores = ', '.join(
                                f"{prof['nombre']} {prof['apellido']}" for prof in profesores_lista)
                    except (ValueError, SyntaxError):
                        pass
                    materias.append({
                        'codigo_guarani': row[0],
                        'nombre': row[1],
                        'carrera': row[2],
                        'anio': row[3],
                        'cuatrimestre': row[4],
                        'profesores': profesores,
                        'alumnos_esperados': int(row[7]) if row[7].isdigit() else 0,
                        'horas_frente_curso': int(row[10]) if row[10].isdigit() else 0,
                        'comisiones': row[8]
                    })
                else:
                    print(f"Error: Fila con menos de 12 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error as e:
        print(f"Error: Error al leer el archivo {archivo}: {e}")
    return materias


def leer_profesores(archivo):
    profesores = []
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar encabezado
            for row in reader:
                if len(row) >= 8:  # Ajustado para asegurar que todas las columnas requeridas estén presentes
                    profes_dict = {
                        'nombre': row[2],
                        'apellido': row[1],
                        'condicion': row[3],
                        'materias': row[7],
                        'horarios_disponibles': row[6],
                    }
                    profesores.append(profes_dict)
                else:
                    print(f"Error: Fila con menos de 8 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error as e:
        print(f"Error: Error al leer el archivo {archivo}: {e}")
    return profesores


def organizar_horarios_profesores(profesores):
    horarios_disponibles = defaultdict(lambda: defaultdict(list))

    for profesor in profesores:
        profesor_horarios = defaultdict(list)
        str_copia_horarios_disponibles = profesor['horarios_disponibles']

        for bloque_dia_horas in str_copia_horarios_disponibles.split(';'):
            dia_horas = bloque_dia_horas.strip().split(',')  # Separar por comas
            dia = dia_horas[0].strip()  # Obtener el día

            for horas_rango in dia_horas[1:]:
                horas = horas_rango.strip().split('-')
                if len(horas) == 2:
                    hora_inicio = int(horas[0].strip())
                    hora_fin = int(horas[1].strip())
                    profesor_horarios[dia].append(f"{hora_inicio}-{hora_fin}")

        nombre_completo = f"{profesor['nombre']} {profesor['apellido']}"
        horarios_disponibles[nombre_completo] = profesor_horarios

    return horarios_disponibles


def organizar_horarios_aulas(aulas):
    horarios_disponibles_aulas = defaultdict(lambda: defaultdict(list))

    for aula in aulas:
        disponibilidad_aula = aula['disponibilidad']

        for dia, disponibilidad_horaria in disponibilidad_aula.items():
            for hora, disponible in enumerate(disponibilidad_horaria, start=8):
                if disponible:
                    horarios_disponibles_aulas[aula['nombre']][dia].append(
                        f"{hora}-{hora + 1}")

    return horarios_disponibles_aulas


def asignar_materias_a_aulas(materias, horarios_profesores, horarios_aulas):
    asignaciones = []

    for materia in materias:
        nombre_profesor = materia['profesores']
        horarios_profesor = horarios_profesores.get(nombre_profesor, {})

        if not horarios_profesor:
            print(f"No se encontraron horarios disponibles para el profesor {
                  nombre_profesor}")
            continue

        asignado = False
        for dia, horas_profesor in horarios_profesor.items():
            if asignado:
                break
            for aula_nombre, horas_aula in horarios_aulas.items():
                horas_disponibles_aula = horas_aula.get(dia, [])

                for hora in horas_disponibles_aula:
                    if hora in horas_profesor:
                        asignaciones.append({
                            'materia': materia['nombre'],
                            'aula': aula_nombre,
                            'dia': dia,
                            'hora': hora,
                            'profesor': nombre_profesor
                        })
                        horarios_aulas[aula_nombre][dia].remove(hora)
                        asignado = True
                        break

    return asignaciones


def encontrar_horario_profesor(nombre_o_apellido, horarios_profesores):
    profesores_encontrados = []
    for nombre_completo, horario in horarios_profesores.items():
        if nombre_o_apellido.lower() in nombre_completo.lower():
            profesores_encontrados.append((nombre_completo, horario))
    return profesores_encontrados


def encontrar_horarios_coincidentes(teacher_name, horarios_profesores, horarios_aulas):
    profesores_encontrados = []
    for nombre_completo, horario in horarios_profesores.items():
        if teacher_name.lower() in nombre_completo.lower():
            profesores_encontrados.append((nombre_completo, horario))

    if not profesores_encontrados:
        print(f"No se encontró el horario del profesor {teacher_name}.")
        return []

    coincidencias = []
    for nombre_completo, horario_profesor in profesores_encontrados:
        for dia, horas_profesor in horario_profesor.items():
            for aula_nombre, horario_aula in horarios_aulas.items():
                horas_aula = horario_aula.get(dia, [])
                horas_coincidentes = set(
                    horas_profesor).intersection(horas_aula)
                if horas_coincidentes:
                    coincidencias.append({
                        'profesor': nombre_completo,
                        'aula': aula_nombre,
                        'dia': dia,
                        'horas': list(horas_coincidentes)
                    })

    return coincidencias


def buscar_aulas_disponibles(horarios_aulas, hora_inicio, hora_fin):
    aulas_disponibles = []

    for aula, horarios_dia in horarios_aulas.items():
        for dia, horas in horarios_dia.items():
            for hora_aula in horas:
                inicio_aula, fin_aula = map(int, hora_aula.split('-'))
                # Verificar si el rango de la aula cubre el rango solicitado por el profesor
                if (hora_inicio >= inicio_aula and hora_inicio < fin_aula) or \
                   (hora_fin > inicio_aula and hora_fin <= fin_aula) or \
                   (hora_inicio <= inicio_aula and hora_fin >= fin_aula):
                    aulas_disponibles.append({
                        'aula': aula,
                        'dia': dia,
                        'hora': hora_aula
                    })

    return aulas_disponibles


def buscar_aulas_disponibles2(horarios_aulas, horarios_profesor):
    aulas_disponibles = []

    for aula, horarios_dia_aula in horarios_aulas.items():
        for dia_aula, horas_aula in horarios_dia_aula.items():
            for hora_aula_str in horas_aula:
                inicio_aula, fin_aula = map(int, hora_aula_str.split('-'))
                # print(dia_aula, horas_aula, horarios_dia_aula.items)
                for dia_profesor, horarios_profesor_dia in horarios_profesor.items():
                    print(dia_profesor, horarios_profesor_dia,
                          horarios_profesor.items)
                    if dia_aula == dia_profesor:
                        for hora_profesor_str in horarios_profesor_dia:
                            inicio_prof, fin_prof = map(
                                int, hora_profesor_str.split('-'))

                            # Verificar disponibilidad de horas (convertidas a enteros)
                            if (inicio_prof <= inicio_aula < fin_prof or
                                inicio_prof < fin_aula <= fin_prof or
                                inicio_aula <= inicio_prof < fin_aula or
                                    inicio_aula < fin_prof <= fin_aula):

                                aulas_disponibles.append({
                                    'aula': aula,
                                    'dia': dia_aula,
                                    'hora_aula': hora_aula_str,
                                    'hora_profesor': hora_profesor_str
                                })

    return aulas_disponibles


# Leer los archivos
aulas = leer_aulas('Aulas.csv')
materias = leer_materias('Materias.csv')
profesores = leer_profesores('Profesores.csv')

# Procesar horarios disponibles por día para cada profesor
horarios_profesores = organizar_horarios_profesores(profesores)

# Imprimir o devolver los horarios organizados almacenados en horarios_disponibles_aulas
horarios_aulas = organizar_horarios_aulas(aulas)

# # # Asignar materias a aulas
# asignaciones = asignar_materias_a_aulas(
#     materias, horarios_profesores, horarios_aulas)

# Imprime todo lo obtenido en el codigo

# Aulas
# for aula in horarios_aulas:
#     print(f"\nAula: {aula}")
#     for dia, horas in horarios_aulas[aula].items():
#         print(f"  {dia}: {', '.join(horas)}")

# Profesores
# for profesor in horarios_profesores:
#     print(f"\nProfesor: {profesor}")
#     for dia, horas in horarios_profesores[profesor].items():
#         print(f"  {dia}: {', '.join(horas)}")

# Materias
# for materia in materias:
#     print(f"\nMateria: {materia['nombre']}, Profesor: {materia['profesores']}")

# Asignaciones
# print("Asignaciones realizadas:")
# for asignacion in asignaciones:
#     print(f"Materia: {asignacion['materia']}, Aula: {asignacion['aula']}, Día: {
#           asignacion['dia']}, Hora: {asignacion['hora']}, Profesor: {asignacion['profesor']}")


# Introduce el nombre o apellido del profesor que deseas buscar
# teacher_name = "Caterina"  # Reemplaza con el nombre o apellido del profesor

# # Busca el horario del profesor
# profesores_encontrados = encontrar_horario_profesor(
#     teacher_name, horarios_profesores)

# # Imprime los resultados encontrados
# if profesores_encontrados:
#     for nombre_completo, horario in profesores_encontrados:
#         print(f"Horario del profesor {nombre_completo}:")
#         for dia, horas in horario.items():
#             print(f"  {dia}: {', '.join(horas)}")
# else:
#     print(f"No se encontró el horario del profesor {teacher_name}.")


# Obtener los horarios del profesor deseado (ejemplo)
# Reemplazar con el nombre completo del profesor
# profesor_deseado = "Lamperti Caterina"
# horarios_profesor = horarios_profesores.get(profesor_deseado, {})

# # Buscar aulas disponibles basándose en los horarios del profesor
# aulas_disponibles2 = buscar_aulas_disponibles2(
#     horarios_aulas, horarios_profesor)

# # Imprimir los resultados encontrados
# if aulas_disponibles2:
#     print(f"Aulas disponibles para el profesor {profesor_deseado}:")
#     for aula_disponible in aulas_disponibles2:
#         print(f"  Aula: {aula_disponible['aula']}, Día: {aula_disponible['dia']}, "
#               f"Hora Aula: {aula_disponible['hora_aula']}, Hora Profesor: {aula_disponible['hora_profesor']}")
# else:
#     print(f"No se encontraron aulas disponibles para el profesor {
#           profesor_deseado}.")
