import csv
import ast
import sys

# Configurar la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='ISO-8859-1')

# Función para leer el archivo de aulas


def leer_aulas(archivo):
    aulas = []
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 4:
                    aulas.append({
                        'nombre': row[0],
                        'capacidad': int(row[1]) if row[1].isdigit() else 0,
                        'edificio': row[2],
                        'disponibilidad': ast.literal_eval(row[3]) if row[3] else []
                    })
                else:
                    print(f"Error: Fila con menos de 4 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error:
        print(f"Error: Error al leer el archivo {archivo}")
    except IndexError:
        print(f"Error: Indice fuera de rango en {archivo}")
    except ValueError:
        print(
            f"Error: No se puede convertir la capacidad a un entero en {archivo}")
    return aulas


# Función para leer el archivo de materias
def leer_materias(archivo):
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            materias = []
            for row in reader:
                if len(row) >= 8:
                    materias.append({
                        'codigo_guarani': row[0],
                        'nombre': row[1],
                        'carrera': row[2],
                        'anio': row[3],
                        'cuatrimestre': row[4],
                        'profesores': None,
                        'alumnos_esperados': row[7],
                    })
                else:
                    print(f"Error: Fila con menos de 8 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error:
        print(f"Error: Error al leer el archivo {archivo}")
    except IndexError:
        print(f"Error: Indice fuera de rango en {archivo}")
    return materias


# Leer los archivos
aulas = leer_aulas('Aulas.csv')
materias = leer_materias('Materias.csv')

# Imprimir los datos
print("Aulas:")
for aula in aulas:
    print(aula['nombre'])
print("\nMaterias:")
for materia in materias:
    print(materia['nombre'])
