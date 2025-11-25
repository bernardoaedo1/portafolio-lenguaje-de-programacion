import tkinter as tk
from tkinter import messagebox
import webbrowser

class Calculadora:
    """
    Clase principal para la calculadora básica con interfaz gráfica.
    
    Maneja la creación de widgets y la lógica de operaciones aritméticas
    utilizando una matriz de botones.
    """
    def __init__(self, ventana):
        """
        Inicializa la ventana de la calculadora y sus componentes.
        
        Args:
            ventana (tk.Tk): La ventana raíz de la aplicación.
        """
        # Configuración de la ventana
        self.ventana = ventana
        self.ventana.title('Calculadora')
        # variable para almacenar la operación
        self.operacion = ""
        # pantalla o display
        self.pantalla = tk.Entry(ventana, width=15, font=('Arial', 20), justify='right')
        self.pantalla.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        
        # Definir los botones de la calculadora por matriz
        botones = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # posición de los botones en la cuadrícula
        fila = 1
        columna = 0
        for boton in botones:
            # botón
            comando = lambda x=boton: self.click_boton(x)
            tk.Button(ventana, text=boton, width=5, height=2,
                     command=comando).grid(row=fila, column=columna) # botones de tkinter
            
            # actualizacion de la posición del boton
            columna += 1
            if columna > 3:
                columna = 0
                fila += 1
        
        # [AUDITORÍA] NOTA DE DISEÑO:
        # El botón 'C' se agrega fuera del bucle, dependiendo del estado final 
        # de las variables 'fila' y 'columna'. Si se agregan más botones a la lista,
        # este botón podría quedar desalineado.
        
        # Botón para limpiar la pantalla
        tk.Button(ventana, text='C', width=5, height=2,
                 command=self.limpiar).grid(row=fila, column=columna)
    
    def click_boton(self, valor): # funcion para el clickeo de botones
        """
        Maneja el evento de clic en los botones de la calculadora.
        
        Args:
            valor (str): El carácter asociado al botón presionado.
        """
        if valor == '=':
            # cálculo
            try:
                # [AUDITORÍA] ERROR DE SEGURIDAD CRÍTICO:
                # El uso de 'eval()' permite la ejecución de código arbitrario (inyección).
                # Se mantiene para fines demostrativos, pero no debe usarse en producción.
                resultado = str(eval(self.operacion))
                
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(0, resultado)
                self.operacion = resultado
            except ZeroDivisionError:
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(0, "Error") # mensaje de error
                messagebox.showerror("Error", "eso no se hace no no")                
                webbrowser.open("https://www.youtube.com/watch?v=XnAQtDEaI2I")
                self.operacion = ""
        else:
            # operadores
            self.operacion += valor
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, self.operacion)
    
    def limpiar(self):
        """Resetea la operación actual y limpia la pantalla."""
        # funcion limpiar
        self.operacion = ""
        self.pantalla.delete(0, tk.END)

# Crear y ejecutar la calculadora
if __name__ == "__main__":
    ventana = tk.Tk()
    calculadora = Calculadora(ventana)
    ventana.mainloop()