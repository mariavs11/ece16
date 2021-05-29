# The GMM Import
from sklearn.mixture import GaussianMixture as GMM
import numpy as np
from tutorial_ml_data_prep import get_data
from tutorial_ml_data_prep import get_subjects
from tutorial_ml_data_prep import process
from tutorial_ml_data_prep import get_hr
from tutorial_ml_data_prep import estimate_fs
import matplotlib.pyplot as plt
# Import for Gaussian PDF
from scipy.stats import norm

# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks


# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)

#gmm = GMM(n_components=2)       # 2-mixture GMM
#gmm = gmm.fit(train_data)       # train the GMM
#labels = gmm.predict(test_data) # predict the labels

# Test GMM Modeling
if __name__ == "__main__":
  fs = 50
  directory = "./data"
  subject = "a03884563"

  # Load all the data for the subject
  train_data = np.array([])
  bad_data = np.array([])
  for trial in range(1,11):
    t, ppg, hr, fs_est,bad_data, dontUse = get_data(directory, subject, trial, fs,bad_data)
    if (dontUse ==False):
      ppg_filtered = process(ppg) # filters the signal
      train_data = np.append(train_data, ppg_filtered) # adds ppg_filtered to previously empty array "train_data"

  # Train the GMM with the training data
  gmm = GMM(n_components=2).fit(train_data.reshape(-1,1))

  # Compare the histogram with the GMM to make sure it is a good fit
  plt.hist(train_data, 100, density=True)
  plot_gaussian(gmm.weights_[0], gmm.means_[0], gmm.covariances_[0])  # plots gaussian for y=0 (lower signal)
  plot_gaussian(gmm.weights_[1], gmm.means_[1], gmm.covariances_[1]) # plots gaussian for y=1 (upper signal)
  plt.show()

  # Test the GMM on the same training data... BAD!!!
  for trial in range(1,11):
    t, ppg, hr, fs_est,bad_data, dontUse = get_data(directory, subject, trial, fs, bad_data)

    ppg_filtered = process(ppg)

    labels = gmm.predict(ppg_filtered.reshape(-1,1))
    hr_est, peaks = estimate_hr(labels, len(ppg), fs)
    print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (subject, trial, hr, hr_est))

    plt.plot(ppg_filtered)
    plt.plot(peaks)
    plt.show()
    plt.plot(ppg_filtered)
    plt.plot(labels)
    plt.show()
