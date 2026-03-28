# Manual de uso de Amazon EMR con datos de egresados de FP en Canarias

## 1. Introducción y objetivo de la práctica

En esta práctica se utilizará Amazon EMR como herramienta de análisis de datos dentro de AWS.  
El objetivo es trabajar con un conjunto de datos real del Gobierno de Canarias relacionado con los egresados de Formación Profesional, almacenarlo en Amazon S3 y procesarlo posteriormente con EMR.

Además, se documentará el proceso completo mediante capturas de pantalla, mostrando la carga del dataset, la configuración de la herramienta y la ejecución del análisis.

## 2. Descripción del dataset

El conjunto de datos utilizado en esta práctica procede del portal estadístico del Gobierno de Canarias (ISTAC) y contiene información sobre los egresados y egresadas de Formación Profesional residentes en Canarias.

El dataset fue descargado en formato comprimido e incluye dos archivos en formato TSV:

- `observations.tsv`, que contiene las observaciones y los valores principales del conjunto de datos.
- `attributes.tsv`, que contiene metadatos y descripciones complementarias para interpretar correctamente la información.

Para el desarrollo de la práctica se utilizó principalmente el archivo `observations.tsv`, ya que es el que contiene los datos empleados posteriormente en el procesamiento con Amazon EMR.

Entre las variables más relevantes del dataset se encuentran:

- `TIME_PERIOD`, que representa el periodo o año de referencia.
- `SEXO`, que indica la categoría de sexo.
- `TITULACION`, que recoge la titulación o familia profesional.
- `MODALIDAD_FORMACION`, relacionada con la modalidad de formación.
- `LUGAR_RESIDENCIA`, que indica el ámbito territorial considerado.
- `TIEMPO_EGRESO`, que representa el tiempo transcurrido desde el egreso.
- `RELACION_ACTIVIDAD`, que describe la situación del egresado respecto a la actividad.
- `MEDIDAS`, que diferencia entre tipos de medida como el número de egresados o el porcentaje de egresados.
- `OBS_VALUE`, que contiene el valor numérico asociado a cada observación.


## 3. Subida del dataset a Amazon S3

Una vez revisados los archivos descargados, el siguiente paso consistió en subir el dataset a Amazon S3 para poder utilizarlo posteriormente con Amazon EMR.

Amazon S3 se utilizó como sistema de almacenamiento del proyecto, ya que permite guardar los archivos de entrada y facilita su acceso desde otros servicios de AWS.

En este caso, se trabajó principalmente con el archivo `observations.tsv`, que contiene las observaciones y valores numéricos del conjunto de datos. El archivo `attributes.tsv` se conservó como apoyo para interpretar la información y los metadatos del dataset.

El proceso realizado fue el siguiente:

1. Acceder al servicio Amazon S3 desde la consola de AWS.
2. Crear un bucket para almacenar los archivos de la práctica.
3. Subir al bucket el archivo `observations.tsv`.
4. Organizar el archivo dentro de una ruta o carpeta para mantener una mejor estructura del proyecto.

Ejemplo de organización dentro del bucket:

- `s3://edu-javi-bucket/dataset/observations.tsv`

Esta subida a S3 es un paso fundamental, ya que Amazon EMR utilizará posteriormente estos archivos como fuente de datos para su procesamiento.

<img width="1918" height="389" alt="image" src="https://github.com/user-attachments/assets/07fdfc3b-9c6b-4b01-a761-7079aeee7c61" />

## 4. Preparación del entorno en Amazon EMR

Después de almacenar el dataset en Amazon S3, se procedió a preparar el entorno de trabajo en Amazon EMR. Para esta práctica se utilizó EMR como herramienta de procesamiento de datos, aprovechando su integración con Amazon S3 y su capacidad para ejecutar trabajos de análisis sobre grandes volúmenes de información.

El objetivo de esta fase fue crear un clúster de EMR con la configuración necesaria para ejecutar el procesamiento del archivo `observations.tsv`.

Durante este paso se realizó lo siguiente:

1. Acceder al servicio Amazon EMR desde la consola de AWS.
2. Seleccionar la opción de crear un nuevo clúster.
3. Elegir la versión de EMR v7.12.0.
4. Seleccionar paquete de aplicaciones Spark Interactive.
5. Configurar las instancias del clúster de tipo m4.large.
6. Revisar la configuración general y lanzar el clúster.

Una vez creado el clúster, este quedó preparado para ejecutar los scripts de procesamiento sobre los datos almacenados en S3.

<img width="1920" height="559" alt="image" src="https://github.com/user-attachments/assets/6fa85f73-93fe-4bdc-b428-dd4da41e95a5" />

## 5. Ejecución del proceso con Amazon EMR

Una vez que el clúster de EMR está activo y nuestro dataset de egresados está correctamente almacenado en S3, el siguiente proceso consiste en ejecutar el análisis de datos. En EMR, el procesamiento se define mediante la creación de "Pasos", que son unidades de trabajo que el clúster ejecuta de manera secuencial.

En esta fase, utilizaremos scripts de PySpark para procesar y transformar el archivo `observations.tsv`. A continuación, se detalla el proceso exacto para añadir y configurar un paso en el clúster:

### 5.1. Añadir un nuevo paso

1. En la consola de AWS seleccionar el clúster de EMR.
2. Nos dirigimos a la pestaña de Pasos o Steps.
3. Hacemos clic en el botón Add step.

<img width="1920" height="293" alt="image" src="https://github.com/user-attachments/assets/7a94379f-67f5-4baa-9370-15c3aa115641" />

### 5.2. Configuración del paso
Al  añadir el paso, aparece un formulario que debemos rellenar con los parámetros específicos de nuestro script de analasis. Lo configuraremos de la siguiente manera:

- Tipo: Seleccionamos Aplicación de Spark.
- Nombre: Introducimos un nombre descriptivo.
- Modo implementación: Seleccionamos Modo de clúster.
- Ubicación de la aplicación: Indicamos la ruta exacta del S3 donde hemos subido previamente el script de PySpark.
- Argumentos (opcional): Introducimos separadas por un espacio la ruta del dataset de entrada y la ruta donde queremos que se guarden los resultados.
- Acción si ocurre un error en el paso: Seleccionamos Continue para que el clúster no se destruya si hay un error en el código.

<img width="1919" height="631" alt="image" src="https://github.com/user-attachments/assets/d785332a-e305-4f65-9c8f-3da0b4489d99" />

### 5.3. Ejecución
Una vez confirmada la creación haciendo clic en Add, el paso comenzará su ciclo de vida:

1. El paso aparecerá en la lista con el estado Pending y pasará a Running.
2. Cuando el estado cambie a completed, el análisis habrá terminado con éxito.

<img width="1918" height="596" alt="image" src="https://github.com/user-attachments/assets/1c8803d9-b5db-42a9-9fbe-40eead5ebc44" />

3. Para verificar que los datos se han procesado correctamente, nos dirigimos a nuestro bucket de S3 `s3://edu-javi-bucket/resultados/` donde encontraremos los archivos generados por PySpark listos para su descarga y evaluación.

<img width="1919" height="453" alt="image" src="https://github.com/user-attachments/assets/a3bd9030-98d3-49ef-86d9-d4a404024428" />

## 6. Análisis e interpretación de los datos

### 6.1 Distribución de egresados por titulación

El primer análisis se centró en la distribución total de egresados por titulación. Para ello, se agruparon los registros según la variable `TITULACION` y se calculó la suma de `OBS_VALUE` en aquellos casos donde la medida era `Egresados`.


``` python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, regexp_replace, desc

spark = SparkSession.builder.appName("AnalisisEgresados").getOrCreate()

input_path = "s3://edu-javi-bucket/dataset/observations.tsv"
output_path = "s3://edu-javi-bucket/resultados/egresados_por_titulacion/"

# Leer el archivo TSV
df = spark.read.option("header", "true").option("sep", "\t").csv(input_path)

print("Columnas del dataset:")
print(df.columns)

# Filtrar solo los registros donde la medida sea Egresados
df_filtrado = df.filter(col("MEDIDAS") == "Egresados")

# Convertir OBS_VALUE a número
df_filtrado = df_filtrado.withColumn(
    "OBS_VALUE",
    regexp_replace(col("OBS_VALUE"), ",", ".").cast("double")
)

# Eliminar filas con valores nulos
df_filtrado = df_filtrado.filter(col("OBS_VALUE").isNotNull())

# Agrupar por titulación, sumar y ordenar de mayor a menor
resultado = df_filtrado.groupBy("TITULACION").agg(
    sum("OBS_VALUE").alias("Total_Egresados")
).orderBy(desc("Total_Egresados"))

# Guardar el resultado en S3
resultado.write.mode("overwrite").option("header", "true").csv(output_path)

# Mostrar el resultado
resultado.show()

spark.stop()
```
Los resultados muestran que algunas categorías presentan un volumen especialmente alto, como `CFGS (LOE)`, `CFGM (LOE)`, `Administración y Gestión`, `Servicios Socioculturales y a la Comunidad` y `Sanidad`. Esto indica que una parte importante de los egresados del conjunto de datos se concentra en ramas formativas relacionadas con administración, servicios sociales y sanitarios.

No obstante, este resultado debe interpretarse con cautela, ya que la variable `TITULACION` incluye distintos niveles de agregación. En algunas filas aparecen familias profesionales amplias, en otras ciclos concretos y en otras niveles formativos generales. Además, también se detectaron algunas diferencias de escritura entre categorías similares, lo que sugiere que sería recomendable realizar una normalización adicional de los nombres antes de un análisis definitivo.

| TITULACION                                                               | Total_Egresados |
|:-------------------------------------------------------------------------|---------------:|
| CFGS (LOE)                                                               |       2165616.0 |
| CFGM (LOE)                                                               |       1270624.0 |
| Administración y Gestión                                                 |        657208.0 |
| Servicios Socioculturales y a la Comunidad                               |        587224.0 |
| Sanidad                                                                  |        394216.0 |
| Administración y finanzas                                                |        355752.0 |
| Hostelería y Turismo                                                     |        352968.0 |
| CFGB (LOE)                                                               |        297096.0 |
| Comercio y Marketing                                                     |        293392.0 |
| .... | ....|
| Gestión del agua                                                         |           144.0 |
| Inteligencia artificial y Big Data                                       |           112.0 |
| Instalación y mantenimiento de sistemas conectados a internet (IoT)      |            16.0 |



### 6.2 Distribución de egresados según el sexo

En el segundo análisis se estudió la distribución de los egresados según la variable `SEXO`. Para ello, se agruparon los datos y se calculó el total de egresados en cada categoría.


``` python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, regexp_replace, desc

spark = SparkSession.builder.appName("EgresadosPorSexo").getOrCreate()

input_path = "s3://edu-javi-bucket/dataset/observations.tsv"
output_path = "s3://edu-javi-bucket/resultados/egresados_por_sexo/"

# Leer el archivo TSV
df = spark.read.option("header", "true").option("sep", "\t").csv(input_path)

print("Columnas del dataset:")
print(df.columns)

# Filtrar solo los registros donde la medida sea Egresados
df_filtrado = df.filter(col("MEDIDAS") == "Egresados")

# Convertir OBS_VALUE a número
df_filtrado = df_filtrado.withColumn(
    "OBS_VALUE",
    regexp_replace(col("OBS_VALUE"), ",", ".").cast("double")
)

# Eliminar filas con valores nulos
df_filtrado = df_filtrado.filter(col("OBS_VALUE").isNotNull())

# Agrupar por sexo, sumar y ordenar de mayor a menor
resultado = df_filtrado.groupBy("SEXO").agg(
    sum("OBS_VALUE").alias("Total_Egresados")
).orderBy(desc("Total_Egresados"))

# Guardar resultado en S3
resultado.write.mode("overwrite").option("header", "true").csv(output_path)

# Mostrar resultado en pantalla
resultado.show()

spark.stop()
```
Los resultados muestran una distribución bastante equilibrada entre hombres y mujeres, aunque se observa una ligera mayoría masculina. Mientras que el total de mujeres egresadas se sitúa en torno a 2,77 millones, el total de hombres supera ligeramente esa cifra, alcanzando aproximadamente 2,84 millones.

Esta diferencia no es muy grande en términos relativos, por lo que puede afirmarse que la distribución por sexo es bastante equilibrada dentro del conjunto de datos analizado. Aun así, el ligero predominio de hombres puede resultar relevante en función del tipo de titulaciones que tengan más peso en el dataset.

| SEXO    |   Total_Egresados |
|:--------|------------------:|
| Total   |         5609964.0 |
| Hombres |         2842788.0 |
| Mujeres |         2767176.0 |


### 6.3 Distribución de los egresados según la relación con la actividad un año después del egreso

El tercer análisis se centró en la variable `RELACION_ACTIVIDAD`, aplicando previamente el filtro `TIEMPO_EGRESO = "4 trimestres después del egreso"`. De esta forma, el estudio no mezcla situaciones correspondientes a distintos momentos temporales y se centra en un punto concreto: la situación de los egresados un año después de finalizar sus estudios.



``` python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, regexp_replace, desc

spark = SparkSession.builder.appName("RelacionActividadUnAnoDespues").getOrCreate()

input_path = "s3://edu-javi-bucket/dataset/observations.tsv"
output_path = "s3://edu-javi-bucket/resultados/relacion_actividad_1_anio_despues/"

# Leer el archivo TSV
df = spark.read.option("header", "true").option("sep", "\t").csv(input_path)

print("Columnas del dataset:")
print(df.columns)

# Filtrar solo registros del indicador Egresados
df_filtrado = df.filter(col("MEDIDAS") == "Egresados")

# Filtrar solo 1 año después del egreso
df_filtrado = df_filtrado.filter(col("TIEMPO_EGRESO") == "4 trimestres después del egreso")

# Quitar la categoría Total de relación con la actividad
df_filtrado = df_filtrado.filter(col("RELACION_ACTIVIDAD") != "Total")

# Convertir OBS_VALUE a número
df_filtrado = df_filtrado.withColumn(
    "OBS_VALUE",
    regexp_replace(col("OBS_VALUE"), ",", ".").cast("double")
)

# Eliminar filas con valores nulos
df_filtrado = df_filtrado.filter(col("OBS_VALUE").isNotNull())

# Agrupar por relación con la actividad, sumar y ordenar de mayor a menor
resultado = df_filtrado.groupBy("RELACION_ACTIVIDAD").agg(
    sum("OBS_VALUE").alias("Total_Egresados")
).orderBy(desc("Total_Egresados"))

# Guardar resultado en S3
resultado.write.mode("overwrite").option("header", "true").csv(output_path)

# Mostrar resultado
resultado.show()

spark.stop()
```
Este enfoque permite obtener una lectura más útil del dataset, ya que muestra cómo se distribuyen los egresados entre distintas situaciones, como personas asalariadas registradas, desempleadas registradas, estudiantes, personas que trabajan por cuenta propia y otras categorías.

La utilidad principal de este análisis es que introduce una perspectiva más cercana a la inserción o continuidad de la trayectoria de los egresados. Frente a otros análisis más descriptivos, este permite observar mejor cuál es la posición de los egresados en relación con la actividad después de un periodo razonable desde su egreso.

| RELACION_ACTIVIDAD                        |   Total_Egresados |
|:------------------------------------------|------------------:|
| Personas asalariadas registradas          |          297900.0 |
| Otro                                      |          141360.0 |
| Personas desempleadas registradas         |          123660.0 |
| Estudiantes                               |           98268.0 |
| Personas que trabajan por cuenta propia   |           11568.0 |

## 7. Conclusiones

En general, esta práctica me sirvió no solo para entender mejor el funcionamiento básico de Amazon EMR, sino también para ver de forma práctica cómo se pueden transformar y analizar datos reales dentro de un flujo de trabajo basado en AWS.

Entre los resultados más importantes, destacaría la identificación de las titulaciones con mayor número de egresados, una distribución bastante equilibrada según el sexo y la posibilidad de analizar su relación con la actividad en un momento posterior al egreso.
