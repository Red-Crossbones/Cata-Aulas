import csv
import ast
import sys
from collections import defaultdict
import shutil

# Configurar la salida estándar a ISO-8859-1 (o cambiar a 'utf-8' si se prefiere)
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
                            row[3]) if row[3] else {}
                        # Arreglar claves con caracteres incorrectos
                        disponibilidad = {
                            k.replace('�', 'ó'): v for k, v in disponibilidad.items()}
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
                if len(row) >= 12:
                    profesores = row[11]
                    try:
                        profesores_lista = ast.literal_eval(profesores)
                        if isinstance(profesores_lista, list):
                            profesores = ', '.join(f"{prof['nombre']} {
                                                   prof['apellido']}" for prof in profesores_lista)
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
                if len(row) >= 8:
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
            dia_horas = bloque_dia_horas.strip().split(',')
            dia = dia_horas[0].strip()
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
                    horarios_disponibles_aulas[aula['nombre']][dia].append(f"{
                                                                           hora}")
    return horarios_disponibles_aulas


def separar_horas(horas_disponibles):
    rangos_separados = []
    for hora_rango in horas_disponibles:
        hora_inicio, hora_fin = hora_rango.split('-')
        rangos_separados.append((int(hora_inicio), int(hora_fin)))
    return rangos_separados


def separar_profesores(profesores):
    return [prof.strip() for prof in profesores.split(',')]


def verificar_disponibilidad(profesor_nombre, horarios_profesores, horarios_aulas):
    aula_con_disponibilidad = []
    if profesor_nombre not in horarios_profesores:
        return aula_con_disponibilidad
    for dia, horas_disponibles in horarios_profesores[profesor_nombre].items():
        horas_separadas = separar_horas(horas_disponibles)
        for hora_inicio, hora_fin in horas_separadas:
            for aula, aulas_disponibles in horarios_aulas.items():
                for dia, horas in aulas_disponibles.items():
                    horas_aula = [int(horas)
                                  for horas in aulas_disponibles[dia]]
                    if hora_inicio in horas_aula and hora_fin in horas_aula:
                        aula_con_disponibilidad.append({
                            "Aula:": aula, "Dia:": dia, "Hora Inicio:": hora_inicio, "Hora Fin:": hora_fin
                        })
    return aula_con_disponibilidad


def asignar_materias_a_aulas(materias, horarios_profesores, horarios_aulas, edificio_predefinido):
    sugerencias = []
    for materia in materias:
        profesores_separados = separar_profesores(materia['profesores'])
        for profesor_nombre in profesores_separados:
            aulas_con_disponibilidad = verificar_disponibilidad(
                profesor_nombre, horarios_profesores, horarios_aulas)
            if aulas_con_disponibilidad:
                for aula in aulas_con_disponibilidad:
                    aula_nombre = aula['Aula:']
                    aula_edificio = next(
                        (a['edificio'] for a in aulas if a['nombre'] == aula_nombre), None)
                    if aula_edificio == edificio_predefinido:
                        sugerencias.append({
                            'Materia': materia['nombre'],
                            'Profesor': profesor_nombre,
                            'Aula': aula['Aula:'],
                            'Dia': aula['Dia:'],
                            'Hora inicio': aula['Hora Inicio:'],
                            'Hora fin': aula['Hora Fin:'],
                            'Edificio': aula_edificio
                        })
            else:
                print(f"{materia['nombre']} | No hay aulas disponibles")
    return sugerencias


def escribir_sugerencias(sugerencias, archivo):
    with open(archivo, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Materia', 'Profesor', 'Aula', 'Dia',
                        'Hora inicio', 'Hora fin', 'Edificio'])
        for sugerencia in sugerencias:
            writer.writerow([
                sugerencia['Materia'],
                sugerencia['Profesor'],
                sugerencia['Aula'],
                sugerencia['Dia'],
                sugerencia['Hora inicio'],
                sugerencia['Hora fin'],
                sugerencia['Edificio']
            ])


def copiar_archivo_aulas(archivo_origen, archivo_destino):
    try:
        shutil.copy(archivo_origen, archivo_destino)
        print(f"Archivo copiado exitosamente a {archivo_destino}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo_origen} no encontrado")
    except IOError as e:
        print(f"Error: No se pudo copiar el archivo {
              archivo_origen} a {archivo_destino}: {e}")


def reordenar_materias_por_alumnos(materias):
    return sorted(materias, key=lambda x: x['alumnos_esperados'], reverse=True)


def crear_sugerencia_asignacion(archivo_aulas, archivo_destino_aulas, archivo_materias, archivo_destino_materias):
    copiar_archivo_aulas(archivo_aulas, archivo_destino_aulas)
    materias = leer_materias(archivo_materias)
    materias_reordenadas = reordenar_materias_por_alumnos(materias)
    with open(archivo_destino_materias, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Codigo Guarani', 'Nombre', 'Carrera', 'Año', 'Cuatrimestre',
                        'Profesores', 'Alumnos Esperados', 'Horas Frente Curso', 'Comisiones'])
        for materia in materias_reordenadas:
            writer.writerow([
                materia['codigo_guarani'],
                materia['nombre'],
                materia['carrera'],
                materia['anio'],
                materia['cuatrimestre'],
                materia['profesores'],
                materia['alumnos_esperados'],
                materia['horas_frente_curso'],
                materia['comisiones']
            ])
    print(f"Materias reordenadas y guardadas en {archivo_destino_materias}")


# Leer los archivos
aulas = leer_aulas('Aulas.csv')
materias = leer_materias('Materias.csv')
profesores = leer_profesores('Profesores.csv')

# Procesar horarios disponibles por día para cada profesor
horarios_disponibles_profesores = organizar_horarios_profesores(profesores)
horarios_disponibles_aulas = organizar_horarios_aulas(aulas)

# Asignar materias a aulas
sugerencias = asignar_materias_a_aulas(
    materias, horarios_disponibles_profesores, horarios_disponibles_aulas, 'Anasagasti II')

# Escribir las sugerencias en un archivo
escribir_sugerencias(sugerencias, 'Sugerencias.csv')
print("Asignación completada. Las sugerencias se han guardado en 'Sugerencias.csv'.")

# Crear archivos de sugerencia
crear_sugerencia_asignacion(
    'Aulas.csv', 'sugerencia_asignacion.csv', 'Materias.csv', 'Materias_reordenadas.csv')
