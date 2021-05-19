import numpy as np
from ECE16Lib.HRMonitor import HRMonitor
from scipy import stats
import matplotlib.pyplot as plt


listsamples = ["./a15616273/a15616273_01_13.csv","./a15616273/a15616273_02_14.csv","./a15616273/a15616273_03_12.csv","./a15616273/a15616273_04_13.csv","./a15616273/a15616273_05_13.csv","./a15616273/a15616273_06_13.csv","./a15616273/a15616273_07_12.csv","./a15616273/a15616273_08_13.csv","./a15616273/a15616273_09_12.csv","./a15616273/a15616273_10_13.csv"]



def eval_hr_monitor(file):
  estimates = np.zeros(len(file)) # array of zeros with length 10
  ground_truth = np.zeros(len(file))

  hr_monitor = HRMonitor(500, 50)
  for i in range(len(file)): # length of file is 10
    data = np.genfromtxt(file[i], delimiter=",") # gets data from first sample and so on
    t = data[:, 0]
    t = (t - t[0]) / 1e3
    ppg = data[:, 1]

    hr_monitor.add(t, ppg)  # runs data through hrmonitor class
    hr, ___, ___ = hr_monitor.process() # get heart rate
    estimates[i] = hr # saves the estimated heart rate
    # This portion returns the ground_truth from the file name
    string = file[i].split("_") # creates list with 3 elements
    string = string[2].split(".")  # gets "12.csv" and creates list with ["12","csv"]
    gnd_hr = int(string[0]) # gets the number of heart beats

    ground_truth[i] = gnd_hr * 6

  return ground_truth, estimates

ground_truth,estimates = eval_hr_monitor(listsamples)

[R,p] = stats.pearsonr(ground_truth, estimates) # correlation coefficient
print(ground_truth)
print(estimates)
plt.figure(1)
plt.clf()

# Correlation Plot
plt.subplot(211)
plt.plot(estimates, estimates)
plt.scatter(ground_truth, estimates)

plt.ylabel("Estimated HR (BPM)")
plt.xlabel("Reference HR (BPM)")
plt.title("Correlation Plot: Coefficient (R) = {:.2f}".format(R))

# Bland-Altman Plot
avg = np.mean(np.vstack((ground_truth,estimates)), axis = 0)
dif = ground_truth - estimates # take the difference between ground_truth and estimates
std = np.std(dif) # get the standard deviation of the difference (using np.std)
bias = np.mean(dif) # get the mean value of the difference
upper_std = bias + 1.96*std # the bias plus 1.96 times the std
lower_std = bias - 1.96*std # the bias minus 1.96 times the std


plt.subplot(212)
plt.scatter(avg, dif)

plt.plot(avg, len(avg)*[bias])
plt.plot(avg, len(avg)*[upper_std])
plt.plot(avg, len(avg)*[lower_std])

plt.legend(["Mean Value: {:.2f}".format(bias),
  "Upper bound (+1.96*STD): {:.2f}".format(upper_std),
  "Lower bound (-1.96*STD): {:.2f}".format(lower_std)
])

plt.ylabel("Difference between estimates and ground_truth (BPM)")
plt.xlabel("Average of estimates and ground_truth (BPM)")
plt.title("Bland-Altman Plot")
plt.show()