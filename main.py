import itertools
import random
import math
import matplotlib.pyplot as plt
import imageio
import pandas as pd
from PIL import Image
import numpy as np


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
def main(tamaño_poblacion,tamaño_maximo_poblacion,radio_mutacion_individuo, radio_mutacion, numero_generaciones, limite_inferior, limite_superior, delta_asterisco, funcion, tipo_optimizacion, valor_n):
    poblacion = Poblacion(tamaño_poblacion,tamaño_maximo_poblacion, radio_mutacion, radio_mutacion_individuo, numero_generaciones, limite_inferior, limite_superior, delta_asterisco, funcion, tipo_optimizacion)
    poblacionI = poblacion.generarPoblacion(poblacion.tamaño_poblacion)

    mejores = []
    media = []
    peores = []
    imagenes = []

    n = valor_n
    datos_tabla = pd.DataFrame(columns=['Cadena de bits', 'Índice', 'X', 'Aptitud'])

    for i in range(poblacion.numero_generaciones):
        hijos = poblacion.reproducir(poblacionI, n)
        hijosMutados = poblacion.mutar(hijos)
        poblacionI = tuple(list(poblacionI) + hijosMutados)
        aptitudes = [poblacion.obtenerAptitud(individuo) for individuo in poblacionI]
        indice_mejor = aptitudes.index(max(aptitudes))
        mejor_individuo = poblacionI[indice_mejor]
        datos_tabla = datos_tabla._append({'Cadena de bits': ''.join(str(bit) for bit in mejor_individuo), 'Índice': i, 'X': poblacion.limite_inferior + int(''.join(str(bit) for bit in mejor_individuo), 2) * poblacion.delta_x, 'Aptitud': poblacion.obtenerAptitud(mejor_individuo)}, ignore_index=True)
        atributosPoblacion = [poblacion.obtenerAptitud(individuo) for individuo in poblacionI]

        if tipo_optimizacion == 1:
            mejores.append(max(atributosPoblacion))
            peores.append(min(atributosPoblacion))
        elif tipo_optimizacion == 0:
            mejores.append(min(atributosPoblacion))
            peores.append(max(atributosPoblacion))

        media.append(sum(atributosPoblacion) / len(atributosPoblacion))

        poblacionI = poblacion.podar(poblacionI)

        # Crear y guardar la gráfica
        x = range(i + 1)
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

        nombre_archivo = f"grafica{i}.png"
        fig.savefig(nombre_archivo)
        imagenes.append(imageio.imread(nombre_archivo))

        plt.close(fig)

    datos_tabla.to_csv('datos_tabla.csv', index=False)

    imagenes_resized = [Image.fromarray(img).resize((img.shape[1] // 2, img.shape[0] // 2), Image.LANCZOS) for img in imagenes]

    # Volver a cambiar el tamaño de las imágenes al tamaño original
    imagenes_resized = [img.resize((img.size[0] * 2, img.size[1] * 2), Image.LANCZOS) for img in imagenes_resized]

    # Convertir las imágenes a arrays de numpy
    imagenes_resized = [np.array(img) for img in imagenes_resized]

    with imageio.get_writer('output.mp4', fps=0.5) as writer:
        for img in imagenes_resized:
            writer.append_data(img)

if __name__ == "__main__":
    def main():
        pass
