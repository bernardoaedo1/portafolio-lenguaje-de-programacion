# Portafolio: Programación Aplicada a Ingeniería Mecánica
**Autor:** Bernardo Aedo  
**Carrera:** Ingeniería de Ejecución en Mecánica  
**Institución:** Instituto Profesional Virginio Gómez  
**Año:** 2025

## Descripción del Repositorio
Repositorio oficial de la asignatura **Lenguaje de Programación**. Este portafolio contiene software en **Python** para material didáctico, de reflexión y estudio en ingeniería.

> **Nota:** Los códigos presentados corresponden a las versiones originales evaluadas. Se incluye una sección de documentación de errores conocidos con fines de estudio y mejora continua.

---

## Proyectos

### 1. Calculadora de Ingeniería (GUI)
* **Ubicación:** `/calculadora/Baedo_t1.py`
* **Librerías:** `tkinter`
* **Descripción:** Interfaz gráfica que simula una unidad aritmético-lógica. Incluye manejo de excepciones y validación de errores matemáticos.

### 2. Planificador de Turnos Rotativos
* **Ubicación:** `/calendario_turnos/Baedo_t2.py`
* **Librerías:** `tkinter`, `datetime`
* **Descripción:** Algoritmo de gestión temporal que proyecta ciclos laborales (4x4, 7x7) utilizando aritmética modular sobre fechas.

### 3. Análisis Demográfico: China (POO)
* **Ubicación:** `/analisis_poblacion/Baedo_t3.ipynb`
* **Librerías:** `Matplotlib`
* **Descripción:** Implementación de Programación Orientada a Objetos para encapsular y visualizar datos demográficos complejos mediante gráficos de barras.

### 4. Algoritmo Genético (Optimización)
* **Ubicación:** `/algoritmo_genetico/Baedo_t4.ipynb`
* **Librerías:** `scikit-learn`, `numpy`
* **Descripción:** * Implementación manual de un motor evolutivo (selección, cruce, mutación) para optimizar un modelo de Inteligencia Artificial (Random Forest).
  * Incluye explicación teórica y comparativa técnica con la librería profesional `GASearchCV`.

---

## 🛠 Auditoría Técnica: Errores Detectados y Análisis
*Esta sección documenta errores técnicos y lógicos presentes en la versión original entregada, identificados posteriormente para estudio.*

### En el Gráfico de Población (`Baedo_t3.ipynb`):
* **Error de Ámbito (Scope):** En los métodos de la clase `China`, se hace referencia directa a la variable externa `regiones` en lugar de llamar al método interno mediante `self`.
    * *Consecuencia:* La clase pierde encapsulamiento y fallaría si se importa en otro script.
    * *Solución:* Usar `self.poblacion_regional()` internamente.

### En el Calendario de Turnos (`Baedo_t2.py`):
* **Superposición de Grid (UI):** En la configuración de turnos, las etiquetas de "Hora inicio" y "Hora término" fueron asignadas a la misma fila (`row=2`), provocando una superposición visual.
    * *Lección:* Revisar siempre los índices secuenciales al usar gestores de geometría como `.grid()`.

### En la Calculadora (`Baedo_t1.py`):
* **Seguridad en Evaluación:** Se utiliza la función `eval()` para procesar operaciones matemáticas.
    * *Nota:* Aunque funcional para prototipos académicos, en software de producción se considera una vulnerabilidad de seguridad (inyección de código).
