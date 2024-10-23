import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
import random

#Función para aplicar filtros y calcular el PSNR
def evaluate(params):
    #Desempaquetar parámetros
    kernel_size, nlm_h = map(int, params)

    #Asegurarse de que kernel_size es impar y mayor que 1
    if kernel_size % 2 == 0:
        kernel_size += 1
    if kernel_size < 3:
        kernel_size = 3

    #Abrir la imagen original
    img = cv2.imread("ovni.jpeg")

    #1. Aplicar filtro de Mediana
    img_median = cv2.medianBlur(img, kernel_size)

    #2. Aplicar Non-Local Means (NLM) para reducción de ruido
    img_nlm = cv2.fastNlMeansDenoisingColored(img_median, None, nlm_h, nlm_h, 7, 21)

    #3. Aplicar un filtro de nitidez sutil (opcional, tal vez podamos omitirlo, si pueden probar ajustarlo esataría genial a ver si reduce el brillo)
    kernel = np.array([[0, -1/7, 0],
                       [-1/7, 2, -1/7],  #Nitidez más sutil
                       [0, -1/7, 0]])
    img_final = cv2.filter2D(img_nlm, -1, kernel)

    #Calcular PSNR (valores negativos porque la búsqueda Tabú busca minimizar)
    return -psnr(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))

#Parámetros iniciales para Tabú
lb = [3, 10]  #Límites inferiores para kernel_size y nlm_h
ub = [15, 50]  #Límites superiores
tabu_list = []
tabu_list_size = 10
max_iter = 50
neighborhood_size = 5

#Generar una solución inicial aleatoria
def random_solution():
    return [random.randint(lb[i], ub[i]) for i in range(2)]  # Ahora solo 2 parámetros (kernel y h)

#Generar vecindarios (vecinos) para explorar
def get_neighbors(solution):
    neighbors = []
    for _ in range(neighborhood_size):
        neighbor = solution[:]
        for i in range(2):  # Dos parámetros a modificar
            neighbor[i] = min(max(neighbor[i] + random.randint(-2, 2), lb[i]), ub[i])
        neighbors.append(neighbor)
    return neighbors

#Función de Búsqueda Tabú
def tabu_search():
    best_solution = random_solution()
    best_score = evaluate(best_solution)
    
    current_solution = best_solution[:]
    current_score = best_score

    for _ in range(max_iter):
        neighbors = get_neighbors(current_solution)
        best_candidate = None
        best_candidate_score = float('inf')

        for candidate in neighbors:
            if candidate not in tabu_list:
                candidate_score = evaluate(candidate)
                if candidate_score < best_candidate_score:
                    best_candidate = candidate
                    best_candidate_score = candidate_score

        if best_candidate is not None:
            current_solution = best_candidate[:]
            current_score = best_candidate_score

            if best_candidate_score < best_score:
                best_solution = best_candidate[:]
                best_score = best_candidate_score

            tabu_list.append(current_solution)
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)

    return best_solution, best_score

#Ejecutar la Búsqueda Tabú
best_params, best_score = tabu_search()

#Aplicar el filtro con los mejores parámetros
print("Mejores parámetros encontrados:", best_params)

#Abrir la imagen original nuevamente
img = cv2.imread("ovni.jpeg")

#Aplicar los filtros finales
kernel_size, nlm_h = map(int, best_params)

#Asegurarse de que kernel_size es impar y mayor que 1
if kernel_size % 2 == 0:
    kernel_size += 1
if kernel_size < 3:
    kernel_size = 3

#Filtro de Mediana
img_median = cv2.medianBlur(img, kernel_size)

#Non-Local Means (NLM)
img_nlm = cv2.fastNlMeansDenoisingColored(img_median, None, nlm_h, nlm_h, 7, 21)

#Filtro de nitidez
kernel = np.array([[0, -1/7, 0],
                   [-1/7, 2, -1/7],  # Mantener nitidez sutil
                   [0, -1/7, 0]])
img_final = cv2.filter2D(img_nlm, -1, kernel)

#Guardar la imagen mejorada
cv2.imwrite('imagen_mejorada_tabu_final_ovni.jpeg', img_final)

print("Imagen mejorada guardada exitosamente.")
