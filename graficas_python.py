# Se importan todas las librerías necesarias
import sys
import serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pyqtgraph as pg
import csv

class SerialPlot(QWidget):
    def __init__(self, parent=None):
        super(SerialPlot, self).__init__(parent)
        self.setWindowTitle("Cohete Alfa")
        self.setGeometry(0, 0, 800, 600)

        # Configuración de la ventana principal
        layout = QVBoxLayout(self)

        # Configuración del gráfico de la aceleración
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', 'Giroscopio', units='grados/s')
        self.graphWidget.setLabel('bottom', 't')
        layout.addWidget(self.graphWidget)

        # Configuración del gráfico del giroscopio
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget2.setBackground('w')
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setLabel('left', 'Acelerometro', units='km/s^2')
        self.graphWidget2.setLabel('bottom', 't')
        layout.addWidget(self.graphWidget2)

        # Configuración del gráfico de la Altura
        self.graphWidget3 = pg.PlotWidget()
        self.graphWidget3.setBackground('w')
        self.graphWidget3.showGrid(x=True, y=True)
        self.graphWidget3.setLabel('left', 'Altitud', units='metros')
        self.graphWidget3.setLabel('bottom', 't')
        layout.addWidget(self.graphWidget3)

        self.setLayout(layout)
        self.showMaximized()

        # Configuración del puerto serial
        self.ser = serial.Serial('COM3', 9600)
        self.ser.flush()

        # Variables para almacenar los datos
        num_points = 100  # Número de puntos a mostrar en la gráfica
        self.x_data = np.zeros(num_points)  ## Tiempo
        self.y_data_1 = np.zeros(num_points)  # AX
        self.y_data_2 = np.zeros(num_points)  # AY
        self.y_data_3 = np.zeros(num_points)  # AZ
        self.y_data_4 = np.zeros(num_points)  # GX
        self.y_data_5 = np.zeros(num_points)  # GY
        self.y_data_6 = np.zeros(num_points)  # GZ
        self.y_data_7 = np.zeros(num_points)  # Altura

        # Crear las líneas para cada valor a graficar
        self.curve1 = self.graphWidget.plot(self.x_data, self.y_data_1, pen='r', name='AX')
        self.curve2 = self.graphWidget.plot(self.x_data, self.y_data_2, pen='g', name='AY')
        self.curve3 = self.graphWidget.plot(self.x_data, self.y_data_3, pen='b', name='AZ')
        self.curve4 = self.graphWidget2.plot(self.x_data, self.y_data_4, pen='r', name='GX')
        self.curve5 = self.graphWidget2.plot(self.x_data, self.y_data_5, pen='g', name='GY')
        self.curve6 = self.graphWidget2.plot(self.x_data, self.y_data_6, pen='b', name='GZ')
        self.curve7 = self.graphWidget3.plot(self.x_data, self.y_data_7, pen='orange', name='Altura')

        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)

    def update_data(self):
        # Leer los datos del puerto serie
        line = self.ser.readline().decode().strip()
        values = line.split(',')

        # Añadir los nuevos valores a los datos de la aceleración
        self.y_data_1[:-1] = self.y_data_1[1:]
        self.y_data_1[-1] = float(values[0])
        self.y_data_2[:-1] = self.y_data_2[1:]
        self.y_data_2[-1] = float(values[1])
        self.y_data_3[:-1] = self.y_data_3[1:]
        self.y_data_3[-1] = float(values[2])
        # Añadir los nuevos valores a los datos del giroscopio
        self.y_data_4[:-1] = self.y_data_4[1:]
        self.y_data_4[-1] = float(values[3])
        self.y_data_5[:-1] = self.y_data_5[1:]
        self.y_data_5[-1] = float(values[4])
        self.y_data_6[:-1] = self.y_data_6[1:]
        self.y_data_6[-1] = float(values[5])
        # Añadir los nuevos valores a los datos de la altura
        self.y_data_7[:-1] = self.y_data_7[1:]
        self.y_data_7[-1] = float(values[6])
        # Crear valores para el tiempo
        self.x_data[:-1] = self.x_data[1:]
        self.x_data[-1] = self.x_data[-2] + 1

        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Aceleración)
        self.curve1.setData(self.x_data, self.y_data_1)
        self.curve2.setData(self.x_data, self.y_data_2)
        self.curve3.setData(self.x_data, self.y_data_3)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Giroscopio)
        self.curve4.setData(self.x_data, self.y_data_4)
        self.curve5.setData(self.x_data, self.y_data_5)
        self.curve6.setData(self.x_data, self.y_data_6)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Altura)
        self.curve7.setData(self.x_data, self.y_data_7)

        # Guardar los datos en un archivo CSV
        self.save_data_csv()

    def save_data_csv(self):
        # Crear una lista con los datos actuales
        datos = list(zip(self.x_data, self.y_data_1, self.y_data_2, self.y_data_3,
                         self.y_data_4, self.y_data_5, self.y_data_6, self.y_data_7))

        # Abrir un archivo CSV en modo escritura
        with open('save_data.csv', 'w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)            # Escribir los encabezados en el archivo CSV
            writer.writerow(['Tiempo', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'ALTURA'])
            
            # Escribir los datos en el archivo CSV
            writer.writerows(datos)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialPlot()
    ex.show()
    sys.exit(app.exec_())