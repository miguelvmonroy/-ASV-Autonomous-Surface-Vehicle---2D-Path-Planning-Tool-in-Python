import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from interpolador import eliminar_outliers, validar_puntos, mi_interpolacion
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
import numpy as np
import os
import matplotlib.pyplot as plt
import tkinter.font as tkFont

# Instrumentos personalizados
from voltimetro import Voltmeter
from amperimetro import Ammeter
from tacometro import Speedometer


class InterpolacionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Interpolador Cúbico")

        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.crear_pestana_dashboard()
        self.crear_pestana_interpolacion()

    def crear_pestana_dashboard(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Pestañ 1")

    def crear_pestana_interpolacion(self):
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Dashboard")

        self.tab2.rowconfigure(0, weight=1)
        self.tab2.columnconfigure(0, weight=3)
        self.tab2.columnconfigure(1, weight=1)

        self.figura = Figure(figsize=(14, 6), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self._configurar_grafico()
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.tab2)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky='nsew')
        self.canvas.mpl_connect("button_press_event", self.agregar_punto)

        self.panel_derecho = tk.Frame(self.tab2, bd=2, relief="flat")
        self.panel_derecho.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.panel_derecho.rowconfigure([0, 1, 2, 3], weight=1)
        self.panel_derecho.columnconfigure(0, weight=1)

        self.fuentes = []
        self.botones = []

        self.seccion1 = self.crear_seccion(self.panel_derecho, 0, "Propiedades de Interpolación")
        self.seccion2 = self.crear_seccion(self.panel_derecho, 1, "Revoluciones por Minuto (RPM)")
        self.seccion3 = self.crear_seccion(self.panel_derecho, 2, "Voltaje")
        self.seccion4 = self.crear_seccion(self.panel_derecho, 3, "Corriente")

        # Tacómetro (RPM)
        contenedor_rpm = tk.Frame(self.seccion2, bg='black')
        contenedor_rpm.place(relx=0.5, rely=0.5, anchor='center', relwidth=1.0, relheight=1.0)
        self.tacometro = Speedometer(contenedor_rpm)
        self.tacometro.pack(expand=True, fill='both')

        # Voltímetro
        contenedor_voltimetro = tk.Frame(self.seccion3, bg='black')
        contenedor_voltimetro.place(relx=0.5, rely=0.5, anchor='center', relwidth=1.0, relheight=1.0)
        self.voltimetro = Voltmeter(contenedor_voltimetro)
        self.voltimetro.pack(expand=True, fill='both')

        # Amperímetro
        contenedor_amperimetro = tk.Frame(self.seccion4, bg='black')
        contenedor_amperimetro.place(relx=0.5, rely=0.5, anchor='center', relwidth=1.0, relheight=1.0)
        self.amperimetro = Ammeter(contenedor_amperimetro)
        self.amperimetro.pack(expand=True, fill='both')

        btn1 = tk.Button(self.seccion1, text="Finalizar Interpolación", command=self.ejecutar_interpolacion)
        btn2 = tk.Button(self.seccion1, text="Resetear", command=self.resetear)
        btn1.pack(pady=5, fill='x')
        btn2.pack(pady=5, fill='x')
        self.botones.extend([btn1, btn2])

        self.master.bind("<Configure>", self.ajustar_fuentes)
        self.puntos = []

    def crear_seccion(self, parent, row, titulo_inicial):
        frame = tk.Frame(parent, bd=2, relief="groove")
        frame.grid(row=row, column=0, sticky="nsew", padx=2, pady=2)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)

        fuente = tkFont.Font(family="Segoe UI", size=10, weight="bold")
        self.fuentes.append(fuente)

        entry = tk.Entry(frame, font=fuente)
        entry.insert(0, titulo_inicial)
        entry.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        content = tk.Frame(frame)
        content.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        return content

    def ajustar_fuentes(self, event):
        ancho = self.master.winfo_width()
        alto = self.master.winfo_height()
        base_size = max(8, int(min(ancho, alto) / 100))

        for fuente in self.fuentes:
            fuente.configure(size=base_size)

        for btn in self.botones:
            btn.configure(font=("Segoe UI", base_size))

    def _configurar_grafico(self):
        self.ax.clear()
        self.ax.set_title("Haz clic para capturar puntos")
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.grid(True)
        self.ax.set_aspect('auto')

    def agregar_punto(self, event):
        if event.inaxes != self.ax:
            return
        self.puntos.append((event.xdata, event.ydata))
        self.ax.plot(event.xdata, event.ydata, 'ro')
        self.canvas.draw()

    def resetear(self):
        self.puntos = []
        self._configurar_grafico()
        self.canvas.draw()

    def ejecutar_interpolacion(self):
        if len(self.puntos) < 4:
            messagebox.showwarning("Insuficientes puntos", "Se necesitan al menos 4 puntos únicos.")
            return

        X, Y = map(np.array, zip(*self.puntos))
        X, Y = eliminar_outliers(X, Y)

        try:
            validar_puntos(X, Y)
        except Exception as e:
            messagebox.showerror("Error de validación", str(e))
            return

        with ProcessPoolExecutor() as executor:
            fx = executor.submit(mi_interpolacion, X)
            fy = executor.submit(mi_interpolacion, Y)
            int_x, dx, ddx = fx.result()
            int_y, dy, ddy = fy.result()

        try:
            K = np.abs((dx * ddy - dy * ddx) / (dx**2 + dy**2)**1.5)
            K = np.log(K + 1e-9)
            K -= K.min()
            Kmax = K.max() if K.max() > 0 else 1.0
        except Exception as e:
            messagebox.showerror("Error en curvatura", str(e))
            return

        centroide_x, centroide_y = np.mean(X), np.mean(Y)
        radios = np.hypot(X - centroide_x, Y - centroide_y)
        radio_max = np.max(radios) * 1.1

        self._configurar_grafico()
        cmap = plt.get_cmap('turbo')
        for i in range(len(K) - 1):
            self.ax.plot([int_x[i], int_x[i+1]], [int_y[i], int_y[i+1]],
                         color=cmap(K[i] / Kmax), linewidth=4, solid_capstyle='round')

        self.ax.scatter(X, Y, s=80, facecolors='white', edgecolors='red', linewidths=1.5)
        buffer = Circle((centroide_x, centroide_y), radio_max,
                        color='blue', linewidth=1.5, linestyle='--', fill=False, alpha=0.6)
        self.ax.add_patch(buffer)

        self.ax.set_title("Interpolación cúbica con curvatura + buffer")
        self.ax.set_aspect('auto')
        self.ax.grid(True)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = InterpolacionApp(root)
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    root.mainloop()
