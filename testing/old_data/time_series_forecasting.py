import pandas
import matplotlib.pyplot as plt
dataset = pandas.read_csv('BeachHouse.csv', usecols=[0, 7], engine='python', skipfooter=3)
plt.plot(dataset)
plt.show()
