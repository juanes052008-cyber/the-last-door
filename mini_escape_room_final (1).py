import random

VIDAS_INICIALES = 3
PISTAS_INICIALES = 2

LISTA_ADIVINANZAS = [
    ("python", "Lenguaje de programación con el que hicimos este juego.",
     ["Empieza con la letra P.", "Su logo tiene dos serpientes entrelazadas."]),
    ("teclado", "Dispositivo que usas para escribir en la computadora.",
     ["Tiene la tecla ENTER.", "Empieza con la letra T."]),
    ("algoritmo", "Secuencia de pasos para resolver un problema.",
     ["Empieza con la letra A.", "Una receta de cocina es un ejemplo de esto."]),
    ("funcion", "Bloque de código reutilizable con un propósito específico.",
     ["En Python se define con 'def'.", "Empieza con la letra F."]),
    ("variable", "Espacio en memoria que guarda un valor que puede cambiar.",
     ["Empieza con la letra V.", "Su valor puede reasignarse durante la ejecución."]),
]

LISTA_SECUENCIAS = [
    ([2, 4, 6, 8, None], 10,
     ["Cada número aumenta de 2 en 2.", "Son los números pares en orden."]),
    ([1, 2, 4, 8, None], 16,
     ["Cada número es el doble del anterior.", "Es la sucesión de potencias de 2."]),
    ([1, 1, 2, 3, 5, None], 8,
     ["Es la secuencia de Fibonacci: suma los dos anteriores.", "El siguiente número es 5 + 3."]),
    ([3, 6, 9, 12, None], 15,
     ["Es la tabla del 3.", "Cada número aumenta de 3 en 3."]),
    ([20, 17, 14, 11, None], 8,
     ["Cada número disminuye de 3 en 3.", "El siguiente número es 11 - 3."]),
]


LISTA_DECISIONES = [
    (
        "La salida del escape room está bloqueada por dos puertas. Una tiene un letrero "
        "que dice 'la verdad te libera' y la otra 'la mentira te libera'. Solo puedes abrir una.",
        ["Elegir la puerta de 'la verdad te libera'",
         "Elegir la puerta de 'la mentira te libera'",
         "Intentar forzar ambas puertas al mismo tiempo"],
        0,
        ["Piensa en cuál de las dos frases sería consistente si fuera cierta.",
         "Si la puerta de 'la mentira' dijera la verdad, se contradice a sí misma."],
    ),
    (
        "Encuentras una palanca y un botón. Un cartel indica que solo una de las dos "
        "acciones abre la salida, y la otra hace sonar una alarma.",
        ["Presionar el botón",
         "Mover la palanca",
         "Presionar el botón y mover la palanca al mismo tiempo"],
        1,
        ["Las palancas suelen usarse para mecanismos de apertura en este tipo de retos.",
         "Los botones suelen usarse para alarmas o trampas en este tipo de retos."],
    ),
]
PISTAS_TRIQUI = [
    "Ocupar el centro del tablero suele ser una buena primera jugada.",
    "Si la máquina tiene dos fichas en línea, bloquea la tercera casilla antes de atacar.",
]


def leer_opcion_entero(mensaje, minimo, maximo):
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print(f"Entrada inválida. Ingresa un número entero entre {minimo} y {maximo}.")
            continue
        if valor < minimo or valor > maximo:
            print(f"Fuera de rango. Ingresa un número entre {minimo} y {maximo}.")
            continue
        return valor


def leer_numero_entero(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            return int(entrada)
        except ValueError:
            print("Entrada inválida. Debes ingresar un número entero.")


def preguntar_si_no(mensaje):
    while True:
        entrada = input(mensaje + " (s/n): ").strip().casefold()
        if entrada in ("s", "si", "sí"):
            return True
        if entrada in ("n", "no"):
            return False
        print("Respuesta no válida. Escribe 's' para sí o 'n' para no.")


def ofrecer_pista(estado, lista_pistas, contador_pistas_reto):
    if estado["pistas"] <= 0:
        print("No te quedan pistas disponibles.")
        return
    indice = contador_pistas_reto[0]
    if indice >= len(lista_pistas):
        print("Ya usaste todas las pistas disponibles para este reto.")
        return
    if preguntar_si_no(f"Tienes {estado['pistas']} pista(s) disponible(s). ¿Deseas usar una?"):
        print(f"PISTA: {lista_pistas[indice]}")
        contador_pistas_reto[0] += 1
        estado["pistas"] -= 1


def registrar_error(estado, mensaje_error):
    estado["vidas"] -= 1
    vidas_restantes = estado['vidas']
    print(f"{mensaje_error} Pierdes una vida. Vidas restantes: {vidas_restantes}")
    return estado["vidas"] <= 0

def reto_adivinanza(estado):
    palabra, definicion, pistas = random.choice(LISTA_ADIVINANZAS)
    contador_pistas = [0]
    print("\n--- RETO 1: Adivinanza ---")
    print(f"Definición: {definicion}")
    print(f"(Pista de formato: la palabra tiene {len(palabra)} letras).")

    while True:
        respuesta = input("¿Cuál es la palabra secreta?: ").strip().casefold()
        if respuesta == palabra.casefold():
            print("¡Correcto! Superaste el reto de adivinanza.")
            return True
        juego_terminado = registrar_error(estado, "Respuesta incorrecta.")
        if juego_terminado:
            return False
        ofrecer_pista(estado, pistas, contador_pistas)


def reto_secuencia(estado):
    secuencia, respuesta_correcta, pistas = random.choice(LISTA_SECUENCIAS)
    contador_pistas = [0]
    texto_secuencia = ", ".join(str(n) if n is not None else "?" for n in secuencia)
    print("\n--- RETO 2: Secuencia numérica ---")
    print(f"Completa la secuencia: {texto_secuencia}")

    while True:
        numero_ingresado = leer_numero_entero("¿Qué número sigue?: ")
        if numero_ingresado == respuesta_correcta:
            print("¡Correcto! Superaste el reto de la secuencia.")
            return True
        juego_terminado = registrar_error(estado, "Número incorrecto.")
        if juego_terminado:
            return False
        ofrecer_pista(estado, pistas, contador_pistas)


def crear_tablero_triqui():
    return [[" " for _ in range(3)] for _ in range(3)]


def imprimir_tablero_triqui(tablero):
    print()
    for i, fila in enumerate(tablero):
        print(" " + " | ".join(fila))
        if i < 2:
            print("---+---+---")
    print()


def posiciones_disponibles(tablero):
    return [(f, c) for f in range(3) for c in range(3) if tablero[f][c] == " "]


def verificar_ganador_triqui(tablero, ficha):
    lineas = []
    lineas.extend(tablero)  # filas
    lineas.extend([[tablero[f][c] for f in range(3)] for c in range(3)])  # columnas
    lineas.append([tablero[i][i] for i in range(3)])  # diagonal principal
    lineas.append([tablero[i][2 - i] for i in range(3)])  # diagonal secundaria
    return any(all(celda == ficha for celda in linea) for linea in lineas)


def turno_maquina_triqui(tablero):
    fila, columna = random.choice(posiciones_disponibles(tablero))
    tablero[fila][columna] = "O"


def turno_jugador_triqui(tablero):
    while True:
        fila = leer_opcion_entero("Elige la fila (0, 1 o 2): ", 0, 2)
        columna = leer_opcion_entero("Elige la columna (0, 1 o 2): ", 0, 2)
        if tablero[fila][columna] != " ":
            print("Esa casilla ya está ocupada. Elige otra.")
            continue
        tablero[fila][columna] = "X"
        return


def jugar_partida_triqui():
    tablero = crear_tablero_triqui()
    turno_del_jugador = random.choice([True, False])

    print("\nTú juegas con la ficha 'X' y la máquina juega con la ficha 'O'.")
    if turno_del_jugador:
        print("Comienza el JUGADOR (X).")
    else:
        print("Comienza la MÁQUINA (O).")

    while True:
        imprimir_tablero_triqui(tablero)
        if turno_del_jugador:
            turno_jugador_triqui(tablero)
            if verificar_ganador_triqui(tablero, "X"):
                imprimir_tablero_triqui(tablero)
                return "jugador"
        else:
            turno_maquina_triqui(tablero)
            if verificar_ganador_triqui(tablero, "O"):
                imprimir_tablero_triqui(tablero)
                return "maquina"

        if not posiciones_disponibles(tablero):
            imprimir_tablero_triqui(tablero)
            return "empate"
        turno_del_jugador = not turno_del_jugador


def reto_triqui(estado):
    print("\n--- RETO 3: Triqui contra la máquina ---")
    contador_pistas = [0]
    while True:
        resultado = jugar_partida_triqui()
        if resultado == "jugador":
            print("¡Ganaste el triqui! Superaste el reto.")
            return True
        mensaje = "Perdiste la partida de triqui." if resultado == "maquina" else "La partida terminó en empate."
        juego_terminado = registrar_error(estado, mensaje)
        if juego_terminado:
            return False
        print("Se reinicia el triqui, ¡inténtalo de nuevo!")
        ofrecer_pista(estado, PISTAS_TRIQUI, contador_pistas)

def reto_decision_final(estado):
    situacion, opciones, indice_correcto, pistas = random.choice(LISTA_DECISIONES)
    contador_pistas = [0]
    print("\n--- RETO 4: Decisión estratégica final ---")
    print(situacion)

    while True:
        for i, texto_opcion in enumerate(opciones):
            print(f"  {i + 1}. {texto_opcion}")
        eleccion = leer_opcion_entero("¿Qué decisión tomas? Ingresa el número: ", 1, len(opciones)) - 1
        if eleccion == indice_correcto:
            print("¡Tomaste la decisión correcta! Encuentras la salida del escape room.")
            return True
        juego_terminado = registrar_error(estado, "Esa decisión no era la correcta.")
        if juego_terminado:
            return False
        ofrecer_pista(estado, pistas, contador_pistas)

def jugar_partida():
    estado = {"vidas": VIDAS_INICIALES, "pistas": PISTAS_INICIALES}
    retos = [reto_adivinanza, reto_secuencia, reto_triqui, reto_decision_final]

    for indice, reto in enumerate(retos):
        superado = reto(estado)
        if not superado:
            return "perdio"
        if indice < len(retos) - 1:
            if not preguntar_si_no("\n¿Deseas continuar con el siguiente reto?"):
                return "abandono"
    return "gano"


def mostrar_instrucciones():
    print("""
=================== INSTRUCCIONES ===================
Bienvenido a The last door, un Mini Escape Room por consola.
programado por :
Juan Jacobo Rodriguez
Samuel Valencia
Juan Esteban Saldarriaga
Samuel Dominguez

- Inicias con 3 vidas y 2 pistas para toda la partida.
- Debes superar 4 retos en orden:
    1. Adivinanza de una palabra (basada en strings).
    2. Completar una secuencia numérica.
    3. Ganar una partida de Triqui contra la máquina
       (tú juegas con 'X', la máquina con 'O'; quién empieza
       se decide al azar y se te informa al inicio de cada partida).
    4. Tomar la decisión estratégica correcta.
- Cada error te resta una vida. Si tus vidas llegan a 0,
  pierdes el juego inmediatamente.
- Puedes usar hasta 2 pistas en total, en el reto que
  prefieras. Cada reto ofrece 2 pistas distintas.
- Las respuestas de texto no distinguen entre mayúsculas
  y minúsculas.
- Ganas si superas los 4 retos conservando al menos 1 vida.
=======================================================
""")


def mostrar_menu_principal():
    print("""
============ THE LAST DOOR - MINI ESCAPE ROOM ============
programado por :
Juan Jacobo Rodriguez
Samuel Valencia
Juan Esteban Saldarriaga
Samuel Dominguez

1. Iniciar nueva partida
2. Ver instrucciones
3. Salir
=========================================================
""")


def main():
    print("¡Bienvenido a The last door!")
    while True:
        mostrar_menu_principal()
        opcion = leer_opcion_entero("Elige una opción: ", 1, 3)

        if opcion == 1:
            jugar_otra = True
            while jugar_otra:
                resultado_partida = jugar_partida()
                if resultado_partida == "gano":
                    print("\n*** ¡FELICITACIONES! Escapaste de la sala. ***")
                elif resultado_partida == "perdio":
                    print("\n*** GAME OVER. Te quedaste sin vidas. ***")
                else:
                    print("\nDecides no continuar. Abandonas el escape room.")
                jugar_otra = preguntar_si_no(
                    "\n¿Deseas continuar jugando (s) o volver al menú principal (n)?"
                )
            print("\nVolviendo al menú principal...")
        elif opcion == 2:
            mostrar_instrucciones()
        elif opcion == 3:
            print("Gracias por jugar The last door. ¡Hasta pronto!")
            break


if __name__ == "__main__":
    main()
