import matplotlib.pyplot as plt
import numpy as np

N = 128
x=np.arange(-5,5,10./(2*N))
y = np.exp(-x*x)
#y_fft = np.fft.fftshift(np.abs(np.fft.fft(y)))/ np.sqrt(2 * N)
y_fft = np.abs(np.fft.fft(y))/ np.sqrt(2 * N)
plt.plot(x,y, label='time domain')
plt.plot(x,y_fft, label='freq domain')
plt.show()
