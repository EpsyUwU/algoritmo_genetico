import tkinter as tk
from tkinter import messagebox
from main import main
from PIL import Image, ImageTk, ImageSequence
from sympy import symbols, lambdify, sympify
from pandastable import Table, TableModel
import pandas as pd
import cv2
import threading
#Carlos Esteban Rivera Perez

def update_table():
    new_data = pd.read_csv('datos_tabla.csv')

    global data, table
    data = new_data
    table.updateModel(TableModel(data))
    table.redraw()
def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def mostrar_grafica():
    # Leer la imagen
    limpiar_frame(gif_frame)
    im = Image.open('ultima_grafica.png')

    # Crear un PhotoImage a partir de la imagen
    photo = ImageTk.PhotoImage(im)

    label = tk.Label(gif_frame, image=photo)
    label.image = photo  # Guardar una referencia a la imagen para evitar que sea eliminada por el recolector de basura
    label.pack()
def play_video():
    # Leer el video
    cap = cv2.VideoCapture('output.mp4')

    def video_stream():
        ret, frame = cap.read()
        if ret:  # Solo procesar el frame si es válido
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image).resize((480, 360))  # Cambia el tamaño según tus necesidades
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        root.after(40, video_stream)

    limpiar_frame(gif_frame)
    label = tk.Label(gif_frame)
    label.pack()
    video_stream()  # Iniciar el streaming de video

    # Iniciar el streaming de video en un hilo separado para evitar que la interfaz gráfica se congele
    threading.Thread(target=video_stream, daemon=True).start()

def ejecutar():
    try:
        tamaño_poblacion = int(entry_tamaño_poblacion.get())
    except ValueError:
        print("Valor inválido para 'tamaño_poblacion':", entry_tamaño_poblacion.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        radio_mutacion = float(entry_radio_mutacion.get())
    except ValueError:
        print("Valor inválido para 'radio_mutacion':", entry_radio_mutacion.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        radio_mutacion_individuo = float(entry_radio_mutacion_individuo.get())
    except ValueError:
        print("Valor inválido para 'radio_mutacion_individuo':", entry_radio_mutacion_individuo.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        numero_generaciones = int(entry_numero_generaciones.get())
    except ValueError:
        print("Valor inválido para 'numero_generaciones':", entry_numero_generaciones.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        tamaño_maximo_poblacion = int(entry_tamaño_maximo_poblacion.get())
    except ValueError:
        print("Valor inválido para 'tamaño_maximo_poblacion':", entry_tamaño_maximo_poblacion.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        limite_inferior = float(entry_limite_inferior.get())
    except ValueError:
        print("Valor inválido para 'limite_inferior':", entry_limite_inferior.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        limite_superior = float(entry_limite_superior.get())
    except ValueError:
        print("Valor inválido para 'limite_superior':", entry_limite_superior.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        referencia_resolucion = float(entry_referencia_resolucion.get())
    except ValueError:
        print("Valor inválido para 'delta_asterisco':", entry_referencia_resolucion.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        valor_n = int(entry_valor_n.get())
    except ValueError:
        print("Valor inválido para 'valor_n':", entry_valor_n.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        funcion_str = entry_funcion.get()
    except ValueError:
        print("Valor inválido para 'funcion':", entry_funcion.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    try:
        tipo_optimizacion = optimizacion.get()
    except ValueError:
        print("Valor inválido para 'tipo_optimizacion':", optimizacion.get())
        messagebox.showerror("Error", "Por favor, ingrese valores válidos")
        return

    x = symbols('x')
    funcion_sympy = sympify(funcion_str)
    funcion = lambdify(x, funcion_sympy, "math")

    main(tamaño_poblacion,tamaño_maximo_poblacion, radio_mutacion, radio_mutacion_individuo, numero_generaciones, limite_inferior, limite_superior, referencia_resolucion, funcion, tipo_optimizacion, valor_n)
    mostrar_grafica()
    update_table()

root = tk.Tk()

# Crear un marco principal
main_frame = tk.Frame(root)
main_frame.pack()

# Crear un marco para los botones
button_frame = tk.Frame(main_frame)
button_frame.pack(side=tk.LEFT)

# Crear un marco para el GIF
gif_frame = tk.Frame(main_frame)
gif_frame.pack(side=tk.RIGHT)

label_tamaño_poblacion = tk.Label(button_frame, text="Tamaño de la población")
label_tamaño_poblacion.pack()
entry_tamaño_poblacion = tk.Entry(button_frame)
entry_tamaño_poblacion.pack()

label_tamaño_maximo_poblacion = tk.Label(button_frame, text="Tamaño máximo de la población")
label_tamaño_maximo_poblacion.pack()
entry_tamaño_maximo_poblacion = tk.Entry(button_frame)
entry_tamaño_maximo_poblacion.pack()

label_radio_mutacion = tk.Label(button_frame, text="Radio de mutación")
label_radio_mutacion.pack()
entry_radio_mutacion = tk.Entry(button_frame)
entry_radio_mutacion.pack()

label_radio_mutacion_individuo = tk.Label(button_frame, text="Radio de mutación del individuo")
label_radio_mutacion_individuo.pack()
entry_radio_mutacion_individuo = tk.Entry(button_frame)
entry_radio_mutacion_individuo.pack()

label_numero_generaciones = tk.Label(button_frame, text="Número de generaciones")
label_numero_generaciones.pack()
entry_numero_generaciones = tk.Entry(button_frame)
entry_numero_generaciones.pack()

label_limite_inferior = tk.Label(button_frame, text="Límite inferior")
label_limite_inferior.pack()
entry_limite_inferior = tk.Entry(button_frame)
entry_limite_inferior.pack()

label_limite_superior = tk.Label(button_frame, text="Límite superior")
label_limite_superior.pack()
entry_limite_superior = tk.Entry(button_frame)
entry_limite_superior.pack()

label_referencia_resolucion = tk.Label(button_frame, text="Resolucion de referencia")
label_referencia_resolucion.pack()
entry_referencia_resolucion = tk.Entry(button_frame)
entry_referencia_resolucion.pack()

label_valor_n = tk.Label(button_frame, text="Numero de parejas del individuo")
label_valor_n.pack()
entry_valor_n = tk.Entry(button_frame)
entry_valor_n.pack()

label_funcion = tk.Label(button_frame, text="Ingrese una funcion")
label_funcion.pack()
entry_funcion = tk.Entry(button_frame)
entry_funcion.pack()

label_optimizacion = tk.Label(button_frame, text="Optimización")
label_optimizacion.pack()
optimizacion = tk.IntVar(value=1)  # 1 para maximizar, 0 para minimizar
radio_max = tk.Radiobutton(button_frame, text="Maximizar", variable=optimizacion, value=1)
radio_max.pack()
radio_min = tk.Radiobutton(button_frame, text="Minimizar", variable=optimizacion, value=0)
radio_min.pack()

button = tk.Button(button_frame, text="Ejecutar", command=ejecutar)
button.pack()

button_gif = tk.Button(button_frame, text="Mostrar video", command=play_video)
button_gif.pack()

button_grafica = tk.Button(button_frame, text="Mostrar gráfica", command=mostrar_grafica)
button_grafica.pack()

table_frame = tk.Frame(main_frame)
table_frame.pack(side=tk.RIGHT)

data = pd.DataFrame(columns=["Cadena de bits", "Índice", "X", "Aptitud"])

table = Table(table_frame, dataframe=data, showtoolbar=True, showstatusbar=True)
table.show()

root.mainloop()