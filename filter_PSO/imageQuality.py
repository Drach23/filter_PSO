import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from pyswarm import pso

# Función para aplicar filtros y calcular el PSNR
def evaluate(params):
    # Desempaquetar parámetros
    diameter, sigma_color, sigma_space = map(int, params)

    # Abrir la imagen original
    img = cv2.imread(r'C:\Users\Richard\Desktop\girl2.jpg')

    # Aplicar filtro bilateral
    img_bilateral = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)

    # Aplicar un filtro de nitidez más sutil
    kernel = np.array([[0, -1/7, 0],
                       [-1/7, 1, -1/7],  # Cambié de 5 a 2 para una nitidez más sutil
                       [0, -1/7, 0]])
    img_final = cv2.filter2D(img_bilateral, -1, kernel)

    # Calcular PSNR
    return -psnr(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))

# Definir límites para los parámetros de PSO
lb = [3, 10, 10]  # Límites inferiores para diameter, sigma_color, sigma_space
ub = [15, 100, 100]  # Límites superiores

# Ejecutar PSO
best_params, best_score = pso(evaluate, lb, ub, swarmsize=30, maxiter=30)

# Aplicar el filtro con los mejores parámetros
print("Mejores parámetros encontrados:", best_params)

# Abrir la imagen original nuevamente
img = cv2.imread(r'C:\Users\Richard\Desktop\girl2.jpg')

# Aplicar el filtro final
img_bilateral = cv2.bilateralFilter(img, int(best_params[0]), int(best_params[1]), int(best_params[2]))
kernel = np.array([[0, -1/7, 0],
                   [-1/7, 2, -1/7],  # Mantener la nitidez sutil
                   [0, -1/7, 0]])
img_final = cv2.filter2D(img_bilateral, -1, kernel)

# Guardar la imagen mejorada
cv2.imwrite('imagen_mejorada.jpg', img_final)

print("Imagen mejorada guardada exitosamente.")