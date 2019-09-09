## Recommender Systems Tarea 1

### Integrantes

| Nombre        | Github     |
|---------------|------------|
| Franco Méndez | [fnmendez](https://github.com/fnmendez)   |
| Martín Álamos | [wayoalamos](https://github.com/wayoalamos) |


### Explicacion de los archivos

La carpeta files tiene los archivos del enunciado: test.csv y training.csv

La carpeta data tiene los archivos:
  training_set.csv: que tiene algunas filas del archivo training.csv
  testing_set.csv: que tiene algunas filas del archivo training.csv

para el correcto uso del testing_set, en este solo hay filas que no estan en el training_set, y al mismo tiempo que el usuario de esa fila tenga informacion en el training

Luego estan los archivos new_testing_set y new_training_set que son los mismos archivos anteriores pero limpios (sin decimal y sin la primera fila). Esto para un mejor manejo de los datos

metrics.py: archivo con las métricas a medir.
pregunta1.py: código para la pregunta 1
pregunta2.py: código para la pregunta 2
pregunta3.py: codigo para la pregunta 3

prepare_dataset.py: el código que se ejecutó para separar el archivo training.csv en uno set de training y otro de test
