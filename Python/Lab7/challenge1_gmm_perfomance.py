# Import for searching a directory
import glob

# The usual suspects
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt
from scipy import stats

# The GMM Import
from sklearn.mixture import GaussianMixture as GMM

# Import for Gaussian PDF
from scipy.stats import norm

# Retrieve a list of the names of the subjects
def get_subjects(directory):
  filepaths = glob.glob(directory + "/*")
  return [filepath.split("/")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
  search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
  filepath = glob.glob(search_key)[0]
  bad_data = [ './data/a15810765/a15810765_10_14.csv','./data/a15732175/a15732175_08_10.csv','./data/a15495275/a15495275_08_14.csv','./data/a15664286/a15664286_02_15.csv','./data/a15994771/a15994771_03_9.csv','./data/a15810765/a15810765_07_12.csv', './data/a15810765/a15810765_08_15.csv','./data/a15810765/a15810765_06_13.csv','.data/a15664286/a15664286_02_15']
  dontUse = False
  if filepath in bad_data:
    dontUse = True

  t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
  t = (t-t[0])/1e3
  hr = get_hr(filepath, len(ppg), fs)

  fs_est = estimate_fs(t)

  if(fs_est < fs-1 or fs_est > fs):
    dontUse = True


  return t, ppg, hr, fs_est, dontUse

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
  count = int(filepath.split("_")[-1].split(".")[0])
  seconds = num_samples / fs
  return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
  return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  return filt.normalize(x)

# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)

# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks

# Run the GMM with Leave-One-Subject-Out-Validation
if __name__ == "__main__":
  fs = 50
  directory = "./data"
  subjects = get_subjects(directory)

  ground_truth = []
  estimates = []
  #print("using get_subjects"+ str(subjects))
  # Leave-One-Subject-Out-Validation
  # 1) Exclude subject
  # 2) Load all other data, process, concatenate
  # 3) Train the GMM
  # 4) Compute the histogram and compare with GMM
  # 5) Test the GMM on excluded subject
  for exclude in subjects:
    print("Training - excluding subject: %s" % exclude)
    train_data = np.array([])
    for subject in subjects:

      for trial in range(1,11):
        t, ppg, hr, fs_est,dontUse = get_data(directory, subject, trial, fs)

        if subject != exclude or dontUse == False:
          train_data = np.append(train_data, process(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)

    # Compare the histogram with the GMM to make sure it is a good fit
    """plt.hist(train_data, 100, density=True)
    plot_gaussian(gmm.weights_[0], gmm.means_[0], gmm.covariances_[0])
    plot_gaussian(gmm.weights_[1], gmm.means_[1], gmm.covariances_[1])
    plt.show()
    """

    # Test the GMM on excluded subject
    #print("Testing on  %s" % exclude)
    for trial in range(1,11):
      t, ppg, hr, fs_est, dontUse = get_data(directory, exclude, trial, fs)

      if not dontUse:

        test_data = process(ppg)

        labels = gmm.predict(test_data.reshape(-1,1))

        hr_est, peaks = estimate_hr(labels, len(ppg), fs)
        #print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude, trial, hr, hr_est))
        #print(subject)
        ground_truth.append(hr)
        estimates.append(hr_est)
        #plt.plot(test_data)
        #plt.plot(peaks)
        #plt.plot(labels)
        #plt.show()
  ground_truth = np.array(ground_truth)
  #print("this is ground " + str(ground_truth))
  estimates = np.array(estimates)
  #print("this is estimate " + str(estimates))
  # Compute the RMSE of all trials
  RMSE = np.sqrt(np.mean(np.power(ground_truth - estimates, 2)))


  # Correlation
  [R, p] = stats.pearsonr(ground_truth, estimates)  # correlation coefficient

  # Plotting all ground-truth and estimates heartrates in a Correlation plot
  plt.subplot(211)
  plt.scatter(ground_truth, estimates, c='r')
  plt.plot(ground_truth, ground_truth)

  plt.ylabel("Estimated HR (BPM)")
  plt.xlabel("Reference HR (BPM)")
  plt.title("Correlation Plot: Coefficient (R) = {:.2f}".format(R))

  # Bland-Altman Plot
  avg = np.mean(np.vstack((ground_truth, estimates)), axis=0)
  dif = ground_truth - estimates
  std = np.std(dif)  # get the standard deviation of the difference (using np.std)
  bias = np.mean(dif)  # get the mean value of the difference
  print(bias)
  print("this the standard deviation "+str(std))
  upper_std = bias + 1.96 * std  # the bias plus 1.96 times the std
  lower_std = bias - 1.96 * std  # the bias minus 1.96 times the std

  plt.subplot(212)
  plt.scatter(avg, dif)

  # The lines that show the bias, upper and lower standard deviation
  plt.plot(avg, len(avg) * [bias])
  plt.plot(avg, len(avg) * [upper_std])
  plt.plot(avg, len(avg) * [lower_std])

  plt.legend(["Mean Value: {:.2f}".format(bias),
              "Upper bound (+1.96*STD): {:.2f}".format(upper_std),
              "Lower bound (-1.96*STD): {:.2f}".format(lower_std)
              ], loc='lower center')

  plt.ylabel("Difference between estimates and ground_truth (BPM)")
  plt.xlabel("Average of estimates and ground_truth (BPM)")
  plt.title("Bland-Altman Plot")

  print(f"The RMSE of all trials was {RMSE}")

  plt.show()