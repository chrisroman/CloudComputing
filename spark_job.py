

'''
Spark Mongo connector example - current data on Mongo will result in a terrible prediction 
'''

'''
from pyspark.sql import SparkSession

my_spark = SparkSession.builder.appName("please_work").config("spark.mongodb.input.uri", 
                    "mongodb://0.0.0.0/location_history.parking_info").config("spark.mongodb.output.uri", 
                    "mongodb://0.0.0.0/location_history.parking_info").getOrCreate()

print(my_spark)

df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

'''


#from IPython.display import display
import pyspark
import random

from pyspark import SparkContext

from pyspark.sql import SQLContext

sc = SparkContext("local", "Simple App")

sqlContext = SQLContext(sc)

pklotsdf = sqlContext.read.format('csv').options(header='true',).load('testing/data/Lot1North.csv')



from pyspark.sql.functions import unix_timestamp
from pyspark.sql.functions import monotonically_increasing_id
import pyspark.sql.functions as func
from pyspark.sql.window import Window

#Refer to pattern for timestamps: https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html

pattern = 'MM/dd/yyyy hh:mm:ss aa'

df_beast = pklotsdf.withColumn("DateTimeStamp", unix_timestamp(pklotsdf["Date/Time"], pattern).cast(
        "timestamp"))

#df.show(n=100)
new_df = df_beast.orderBy("DateTimeStamp")

my_window = Window.orderBy("DateTimeStamp")

#df2 = new_df.withColumn("id", monotonically_increasing_id())
df2 = new_df.withColumn("id", func.row_number().over(my_window))


import pyspark.sql.functions as func
from pyspark.sql import Window

#Assuming we don't have data from immediately prior, I'm only going to be able to use prior weeks 
# in order to make predictions
num_intervals_in_one_day= int(24 * 60 / 5)
num_intervals_in_one_day_offset_hour = int(24 * 60 / 5) - 12
num_intervals_15_min = int(15/5)
num_intervals_30_min = int(30/5)
num_intervals_45_min = int(45/5)
num_intervals_60_min = int(60/5)
num_intervals_120_min = int(120/5)
num_intervals_180_min = int(180/5)
num_intervals_240_min = int(240/5)

intervals = [num_intervals_in_one_day, num_intervals_in_one_day_offset_hour, num_intervals_15_min, num_intervals_30_min,
            num_intervals_60_min, num_intervals_60_min, num_intervals_120_min, 
            num_intervals_180_min, num_intervals_240_min]


my_window = Window.partitionBy().orderBy("id")

df3 = df2.select('Available', 'DateTimeStamp', "id")
#df3.show(n=1000)

for interval in intervals:
    col_name = str(interval*5) + 'min interval'
    col_time_stamp_name = str(interval*5) + 'min interval timestamp'
    df4 = df3.withColumn(col_name, func.lag(df3["Available"], 
            count = interval, default=None).over(my_window)).withColumn(col_time_stamp_name,
            func.lag(df2["DateTimeStamp"], count = interval, default=None).over(my_window))
    df3 = df4 
    

#df4.show(n=1000)

df5 = df4.where(df4['id'] >= 300)


import pyspark.mllib
import pyspark.mllib.regression
from pyspark.mllib.regression import LabeledPoint
from pyspark.sql.functions import *
print (new_df.schema)

temp_features = df5.rdd.map(lambda line:LabeledPoint(float(line[0]),
                    [float(line[3]),float(line[5]),float(line[7]), float(line[9]), float(line[11]), 
                     float(line[13])])).cache()


from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel

#print(temp_features.take(300))

model = LinearRegressionWithSGD.train(temp_features, iterations=100000, step=0.0000038)

valuesAndPreds = temp_features.map(lambda p: (p.label, model.predict(p.features)))

MSE = valuesAndPreds \
    .map(lambda vp: (vp[0] - vp[1])**2) \
    .reduce(lambda x, y: x + y) / valuesAndPreds.count()
print("Mean Squared Error = " + str(MSE))
#https://www.arundhaj.com/blog/calculate-difference-with-previous-row-in-pyspark.html

print(model.weights)
#Have to calculate offset in row values



