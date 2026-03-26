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