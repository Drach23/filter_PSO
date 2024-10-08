# filter_PSO
Este proyecto optimiza el proceso de mejora de imágenes aplicando filtros bilaterales y de nitidez, utilizando el algoritmo PSO (Particle Swarm Optimization) para encontrar los mejores parámetros que maximizan la calidad de la imagen basada en el PSNR (relación señal-ruido pico). 

# Optimización de Filtros de Imagen con PSO

Este proyecto utiliza el algoritmo de optimización de enjambre de partículas (PSO) para ajustar los parámetros de filtros bilaterales y de nitidez, mejorando la calidad de las imágenes. El objetivo es maximizar la relación señal-ruido pico (PSNR), lo que garantiza una mejor calidad visual.

## Descripción

El programa optimiza los parámetros del filtro bilateral aplicando el PSO para lograr una mejora óptima en la imagen. El flujo principal del código incluye:

1. **Aplicación de filtros bilaterales y de nitidez** a una imagen.
2. **Cálculo del PSNR** entre la imagen original y la mejorada.
3. **Optimización de parámetros** usando PSO para maximizar la calidad visual.
4. **Guardado de la imagen mejorada** con los parámetros óptimos.

## Requisitos

Para ejecutar este proyecto, necesitas tener instaladas las siguientes bibliotecas:

- `opencv-python`
- `numpy`
- `scikit-image`
- `pyswarm`

Instálalas utilizando `pip`:

```bash
pip install opencv-python numpy scikit-image pyswarm

