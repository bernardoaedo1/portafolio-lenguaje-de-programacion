import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, timedelta

class planificador:
    """
    Clase para gestionar y visualizar turnos laborales rotativos (4x4, 7x7, etc.).
    Permite calcular proyecciones de trabajo/descanso en un calendario.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("planificador")
        self.fecha_actual = datetime.now()
        self.modalidad = tk.StringVar(value="4x4")
        self.dias_modificados = {}
        self.dia_inicio_turno = None
        self.crear_frame_superior()
        self.crear_calendario()
        self.crear_configuracion_turnos()
        self.crear_leyenda()
        
    def crear_frame_superior(self):
        """Crea la cabecera con navegación de meses."""
        frame_superior = ttk.Frame(self.root, padding="10")
        frame_superior.grid(row=0, column=0, sticky="ew")
        ttk.Button(frame_superior, text="<", command=self.mes_anterior).grid(row=0, column=0)
        self.lbl_fecha = ttk.Label(frame_superior, text=f"{calendar.month_name[self.fecha_actual.month]} {self.fecha_actual.year}")
        self.lbl_fecha.grid(row=0, column=1, padx=10)
        ttk.Button(frame_superior, text=">", command=self.mes_siguiente).grid(row=0, column=2)
        
    def crear_calendario(self):
        """Inicializa la estructura de la grilla del calendario."""
        self.frame_calendario = ttk.Frame(self.root, padding="10")
        self.frame_calendario.grid(row=1, column=0, sticky="nsew")
        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for i, dia in enumerate(dias):
            ttk.Label(self.frame_calendario, text=dia).grid(row=0, column=i)
        self.actualizar_calendario()
        
    def crear_configuracion_turnos(self):
        """Crea los inputs para seleccionar modalidad y horarios."""
        frame_configuracion = ttk.Frame(self.root, padding="10")
        frame_configuracion.grid(row=2, column=0, sticky="ew")
        # sleccion de modalidad
        ttk.Label(frame_configuracion, text="Modalidad: ").grid(row=0, column=0)
        modalidades = ["4x4", "7x7", "14x14"]  # Modalidades actualizadas
        combo_modalidad = ttk.Combobox(frame_configuracion, values=modalidades, textvariable=self.modalidad, state="readonly")
        combo_modalidad.grid(row=0, column=1)
        combo_modalidad.bind("<<ComboboxSelected>>", self.actualizar_calendario)
        
        # horarios
        
        # [AUDITORÍA] ERROR DE INTERFAZ (UI):
        # Conflicto de índices en .grid().
        # 'Hora inicio' está en row=2.
        # 'Hora término' TAMBIÉN se asigna a row=2 más abajo.
        # Esto causa que los widgets se superpongan visualmente.
        
        ttk.Label(frame_configuracion, text="Hora inicio: ").grid(row=2, column=0)
        self.entrada_inicio = ttk.Entry(frame_configuracion, width=10)
        self.entrada_inicio.grid(row=1, column=1)
        self.entrada_inicio.insert(0, "08:00")
        
        ttk.Label(frame_configuracion, text="Hora término: ").grid(row=2, column=0) # ERROR: row=2 colisiona con el anterior
        self.entrada_termino = ttk.Entry(frame_configuracion, width=10)
        self.entrada_termino.grid(row=2, column=1)
        self.entrada_termino.insert(0, "18:00")
        
    def toggle_dia_trabajo(self, btn, dia):
        """
        Calcula y proyecta los días de trabajo/descanso basándose en el día seleccionado.
        Usa aritmética modular para determinar el estado del ciclo.
        """
        # Resetear todos los días modificados
        self.dias_modificados.clear()
        
        # Guardar el día de inicio y crear la fecha inicial
        self.dia_inicio_turno = dia
        fecha_inicio = self.fecha_actual.replace(day=dia)
        
        # Obtener el número de días según la modalidad
        dias_trabajo = int(self.modalidad.get().split("x")[0])
        dias_descanso = int(self.modalidad.get().split("x")[1])
        dias_ciclo = dias_trabajo + dias_descanso
        
        # Calcular días de trabajo y descanso
        for mes_offset in range(-6, 7):  # Procesar 6 meses antes y 6 meses después
            fecha_mes = self.fecha_actual.replace(day=1)
            fecha_mes = fecha_mes.replace(day=1)
            if mes_offset != 0:
                # Ajustar el mes
                año = self.fecha_actual.year + ((self.fecha_actual.month + mes_offset - 1) // 12)
                mes = ((self.fecha_actual.month + mes_offset - 1) % 12) + 1
                fecha_mes = fecha_mes.replace(year=año, month=mes)
            
            _, dias_en_mes = calendar.monthrange(fecha_mes.year, fecha_mes.month)
            
            for d in range(1, dias_en_mes + 1):
                fecha = fecha_mes.replace(day=d)
                diferencia_dias = (fecha - self.fecha_actual.replace(day=self.dia_inicio_turno)).days
                
                # Calculamos la posición en el ciclo desde el día inicial
                posicion_en_ciclo = diferencia_dias % dias_ciclo
                if posicion_en_ciclo < 0:
                    posicion_en_ciclo += dias_ciclo
                es_trabajo = posicion_en_ciclo < dias_trabajo
                
                clave = f"{fecha.year}-{fecha.month}-{fecha.day}"
                self.dias_modificados[clave] = "#90ee90" if es_trabajo else "#FFB6C1"
        
        # Actualizar el calendario
        self.actualizar_calendario()
            
    def color_original(self, dia):
        """Retorna el color base del día según la modalidad."""
        dias_trabajo = int(self.modalidad.get().split("x")[0])
        dias_total = dias_trabajo * 2
        es_trabajo = (dia % dias_total) <= dias_trabajo
        return "#90ee90" if es_trabajo else "#FFB6C1"
        
    def crear_leyenda(self):
        """Muestra la leyenda de colores para Trabajo vs Descanso."""
        frame_leyenda = ttk.Frame(self.root, padding="5")
        frame_leyenda.grid(row=3, column=0, sticky="ew", pady=5)
        
        # Crear etiqueta para días de trabajo (verde)
        frame_trabajo = ttk.Frame(frame_leyenda)
        frame_trabajo.pack(side="left", padx=10)
        ttk.Label(frame_trabajo, text="■", foreground="#90ee90", font=("Arial", 12, "bold")).pack(side="left")
        ttk.Label(frame_trabajo, text=" Días de trabajo", font=("Arial", 10)).pack(side="left")
        
        # Crear etiqueta para días de descanso (rojo)
        frame_descanso = ttk.Frame(frame_leyenda)
        frame_descanso.pack(side="left", padx=10)
        ttk.Label(frame_descanso, text="■", foreground="#FFB6C1", font=("Arial", 12, "bold")).pack(side="left")
        ttk.Label(frame_descanso, text=" Días de descanso", font=("Arial", 10)).pack(side="left")
    
    def mes_anterior(self):
        """Retrocede la visualización al mes previo."""
        self.fecha_actual = self.fecha_actual.replace(day=1) - timedelta(days=1)
        self.actualizar_vista()
        
    def mes_siguiente(self):
        """Avanza la visualización al mes siguiente."""
        self.fecha_actual = self.fecha_actual.replace(day=28) + timedelta(days=5)
        self.actualizar_vista()
    
    def actualizar_vista(self):
        """Refresca la etiqueta del mes y la grilla."""
        self.lbl_fecha.config(text=f"{calendar.month_name[self.fecha_actual.month]} {self.fecha_actual.year}")
        self.actualizar_calendario()
        
    def actualizar_calendario(self, event=None):
        """
        Redibuja los botones del calendario aplicando los colores
        almacenados en self.dias_modificados.
        """
        for widget in self.frame_calendario.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        cal = calendar.monthcalendar(self.fecha_actual.year, self.fecha_actual.month)
        
        dias_trabajo = int(self.modalidad.get().split("x")[0])
        dias_total = dias_trabajo * 2
        
        for i, semana in enumerate(cal):
            for j, dia in enumerate(semana):
                if dia != 0:
                    dia_del_mes = dia
                    clave = f"{self.fecha_actual.year}-{self.fecha_actual.month}-{dia}"
                    
                    if clave in self.dias_modificados:
                        color = self.dias_modificados[clave]
                    else:
                        color = "#FFB6C1" 
                    
                    btn = ttk.Label(self.frame_calendario, text=str(dia), padding=5, background=color)
                    btn.grid(row=i+1, column=j)
                    btn.bind("<Button-1>", lambda e, btn=btn, dia=dia: self.toggle_dia_trabajo(btn, dia))
        
def main():
    root = tk.Tk()
    app = planificador(root)
    root.mainloop()
if __name__ == "__main__":
    main()