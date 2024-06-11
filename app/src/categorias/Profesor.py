class Profesor:
    def __init__(self, dni, apellido, nombre, condicion, categoria, dedicacion, materias):
        self.dni = dni
        self.apellido = apellido
        self.nombre = nombre
        self.condicion = condicion
        self.categoria = categoria
        self.dedicacion = dedicacion
        self.materias = materias

    def __str__(self):
        materias_str = ", ".join([materia['nombre']
                                 for materia in self.materias])
        return f"Profesor: {self.apellido} {self.nombre} (DNI: {self.dni}), Materias: {materias_str}"

    def to_dict(self):
        return {
            "dni": self.dni,
            "apellido": self.apellido,
            "nombre": self.nombre,
            "condicion": self.condicion,
            "categoria": self.categoria,
            "dedicacion": self.dedicacion,
            "materias": self.materias
        }
