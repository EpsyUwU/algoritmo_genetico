import itertools
import random
import math
import matplotlib.pyplot as plt
import imageio
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from termcolor import colored
#Carlos Esteban Rivera Perez

class Poblacion:
    def __init__(self, tamaño_poblacion, tamaño_maximo_poblacion, radio_mutacion, radio_mutacion_individuo, numero_generaciones, limite_inferior, limite_superior, referencia_resolucion, funcion, tipo_optimizacion):
        self.tamaño_poblacion = tamaño_poblacion
        self.tamaño_maximo_poblacion = tamaño_maximo_poblacion
        self.radio_mutacion = radio_mutacion
        self.radio_mutacion_individuo = radio_mutacion_individuo
        self.numero_generaciones = numero_generaciones
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior
        self.referencia_resolucion = referencia_resolucion
        self.rango = self.limite_superior - self.limite_inferior
        self.bits = self.numero_bits()
        self.delta_x = self.deltaX()
        self.funcion = funcion
        self.tipo_optimizacion = tipo_optimizacion
        self.posibilidad_numeros = 2**self.bits - 1
        self.resolucion_sistema = self.rango / self.posibilidad_numeros
        self.resolucion_sistema = round(self.resolucion_sistema, int(math.log10(1 / self.referencia_resolucion)) + 1)

    def numero_bits(self):
        numero_puntos = (self.rango / self.referencia_resolucion) + 1
        n_bits = math.ceil(math.log2(numero_puntos))
        return n_bits

    def deltaX(self):
        deltaX = self.rango / ((2**self.bits - 1))
        deltaX = round(deltaX, int(math.log10(1/deltaX)) + 1)
        return deltaX

    def f(self, x):
        return self.funcion(x)

    def generarPoblacion(self, poblacion):
        return [self.generarIndividuo() for i in range(poblacion)]

    def generarIndividuo(self):
        return [int(digit) for digit in bin(random.randint(0, 2**self.bits - 1))[2:].zfill(self.bits)]

    def reproducir(self, poblacion, n):
        nuevaPoblacion = []
        for individuo in poblacion:
            m = random.randint(0, n)  # Genera un número aleatorio m entre [0, n]
            for _ in range(m):  # Realiza m cruces
                otroIndividuo = individuo
                while otroIndividuo == individuo:  # Asegura que el individuo no se cruce consigo mismo
                    otroIndividuo = random.choice(poblacion)
                hijo1, hijo2 = self.cruza(individuo, otroIndividuo)
                nuevaPoblacion.append(hijo1)
                nuevaPoblacion.append(hijo2)
        return nuevaPoblacion

    def cruza(self, individuo1, individuo2):
        puntoCorte = random.randint(0, self.bits - 1)  # Selecciona un punto de cruce aleatorio
        # Crea el primer y segundo hijo
        hijo1 = list(itertools.chain(individuo1[:puntoCorte], individuo2[puntoCorte:]))
        hijo2 = list(itertools.chain(individuo2[:puntoCorte], individuo1[puntoCorte:]))
        return hijo1, hijo2

    def mutar(self, poblacion):
        if random.random() < self.radio_mutacion:  # Decide si debe ocurrir alguna mutación en la población
            for individuo in poblacion:
                if random.random() < self.radio_mutacion_individuo:  # Decide si el individuo debe mutar
                    bit = random.randint(0, self.bits - 1)  # Decide qué bit debe mutar
                    individuo[bit] = 1 - individuo[bit]  # Realiza la mutación del gen mediante la negación del bit
        return poblacion

    def obtenerAptitud(self, individuo):
        numero = int(''.join(str(bit) for bit in individuo), 2)
        x = self.limite_inferior + numero * self.delta_x
        return self.f(x)

    def podar(self, poblacion):
        # Elimina los individuos duplicados y los convierte de nuevo a listas
        poblacion = [list(x) for x in set(tuple(x) for x in poblacion)]

        # Calcula la aptitud de cada individuo y los ordena en orden descendente de aptitud
        poblacion = sorted(poblacion, key=self.obtenerAptitud, reverse=self.tipo_optimizacion)

        # Devuelve los individuos más aptos hasta el tamaño máximo de la población
        return poblacion[:self.tamaño_maximo_poblacion]

    def crearVideo(self, poblacion):
        fig, ax = plt.subplots()

        def animate(i):
            ax.clear()
            x_values = [self.limite_inferior + j * self.resolucion_sistema for j in range(self.posibilidad_numeros + 1)]
            y_values = [self.f(x) for x in x_values]
            ax.plot(x_values, y_values, label='f(x)')

            # Obtener aptitudes y posiciones x para todos los individuos
            aptitudes = [self.f(self.limite_inferior + int(''.join(map(str, individuo)), 2) * self.resolucion_sistema) for individuo in poblacion[i]]
            xs = [self.limite_inferior + int(''.join(map(str, individuo)), 2) * self.resolucion_sistema for individuo in poblacion[i]]

            # Encontrar mejor y peor individuo según su aptitud
            if self.tipo_optimizacion == 1:
                mejor_aptitud = max(aptitudes)
                peor_aptitud = min(aptitudes)
            elif self.tipo_optimizacion == 0:
                mejor_aptitud = min(aptitudes)
                peor_aptitud = max(aptitudes)

            # Graficar todos los individuos
            ax.scatter(xs, aptitudes, color='orange', alpha=0.6)  # Dibujar todos los individuos en gris

            # Resaltar el mejor y el peor individuo
            mejor_idx = aptitudes.index(mejor_aptitud)
            peor_idx = aptitudes.index(peor_aptitud)
            ax.scatter(xs[mejor_idx], aptitudes[mejor_idx], color='green', label='Mejor', edgecolors='black', s=100)
            ax.scatter(xs[peor_idx], aptitudes[peor_idx], color='red', label='Peor', edgecolors='black', s=100)

            media_aptitud = sum(aptitudes) / len(aptitudes)
            ax.axhline(y=media_aptitud, color='pink', linestyle='--', label='Media')

            plt.title(f'Generacion {i}')
            plt.xlabel('Rango')
            plt.ylabel('Aptitud')
            ax.legend()

        ani = animation.FuncAnimation(fig, animate, frames=self.numero_generaciones, interval=200)
        ani.save('output.mp4', writer='ffmpeg')
        plt.close(fig)


    def ordenar(self, poblacion):
        aptitudes = [self.obtenerAptitud(individuo) for individuo in poblacion]
        pares = list(zip(aptitudes, poblacion))
        pares_ordenados = sorted(pares, reverse=self.tipo_optimizacion)

        atributosOrdenados, poblacionOrdenada = zip(*pares_ordenados)

        return poblacionOrdenada, atributosOrdenados

def main(tamaño_poblacion,tamaño_maximo_poblacion,radio_mutacion_individuo, radio_mutacion, numero_generaciones, limite_inferior, limite_superior, delta_asterisco, funcion, tipo_optimizacion, valor_n):
    poblacion = Poblacion(tamaño_poblacion,tamaño_maximo_poblacion, radio_mutacion, radio_mutacion_individuo, numero_generaciones, limite_inferior, limite_superior, delta_asterisco, funcion, tipo_optimizacion)
    poblacionI = poblacion.generarPoblacion(poblacion.tamaño_poblacion)

    mejores = []
    media = []
    peores = []
    poblaciones = []
    mejor_individuo = []

    n = valor_n
    datos_tabla = pd.DataFrame(columns=['Cadena de bits', 'Índice', 'X', 'Aptitud'])

    for i in range(poblacion.numero_generaciones):
        hijos = poblacion.reproducir(poblacionI, n)
        hijosMutados = poblacion.mutar(hijos)
        poblacionI = tuple(list(poblacionI) + hijosMutados)
        atributosPoblacion = [poblacion.obtenerAptitud(individuo) for individuo in poblacionI]

        if tipo_optimizacion == 1:
            mejores.append(max(atributosPoblacion))
            peores.append(min(atributosPoblacion))
        elif tipo_optimizacion == 0:
            mejores.append(min(atributosPoblacion))
            peores.append(max(atributosPoblacion))
        media.append(sum(atributosPoblacion) / len(atributosPoblacion))

        poblaciones.append(poblacionI)

        poblacionI = poblacion.podar(poblacionI)

        fig, axs = plt.subplots(1, figsize=(5, 5))
        axs.plot(mejores, label='Mejores')
        axs.plot(peores, label='Peores')
        axs.plot(media, label='Media')
        axs.legend()

        axs.set_title('Evolución de la aptitud de la población')
        axs.set_xlabel('Generación')
        axs.set_ylabel('Aptitud')
        plt.savefig('ultima_grafica.png')
        print('Mejor individuo:', max(mejores))
        print('Peor individuo:', min(peores))

        plt.close(fig)

        mejor_individuo.append(poblacionI[0])

    poblacionOrdenada, atributosOrdenados = poblacion.ordenar(mejor_individuo)
    numero = int(''.join(str(bit) for bit in poblacionOrdenada[0]), 2)
    x = limite_inferior + numero * poblacion.delta_x

    datos_tabla = datos_tabla._append({
        'Cadena de bits': ''.join(map(str, poblacionOrdenada[0])),
        'Índice': numero,
        'X': x,
        'Aptitud': atributosOrdenados[0]
    }, ignore_index=True)

    datos_tabla.to_csv('mejor_individuo.csv', index=False)
    poblacion.crearVideo(poblaciones)

if __name__ == "__main__":
    def main():
        pass
