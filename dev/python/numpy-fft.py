import numpy as np
np.fft.fft(np.exp(2j * np.pi * np.arange(8) / 8))
# array([ -3.44505240e-16 +1.14383329e-17j,
# 8.00000000e+00 -5.71092652e-15j,
# 2.33482938e-16 +1.22460635e-16j,
# 1.64863782e-15 +1.77635684e-15j,
# 9.95839695e-17 +2.33482938e-16j,
# 0.00000000e+00 +1.66837030e-15j,
# 1.14383329e-17 +1.22460635e-16j,
# -1.64863782e-15 +1.77635684e-15j])

import matplotlib.pyplot as plt
t = np.arange(256)
sp = np.fft.fft(np.sin(t))
freq = np.fft.fftfreq(t.shape[-1])
plt.plot(freq, sp.real, freq, sp.imag)
# [<matplotlib.lines.Line2D object at 0x...>, <matplotlib.lines.Line2D object at 0x...>]
plt.show()
