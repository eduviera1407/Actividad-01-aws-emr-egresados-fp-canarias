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