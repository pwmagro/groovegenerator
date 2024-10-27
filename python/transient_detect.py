from matplotlib import pyplot as pp
from scipy.io import wavfile
import scipy.signal as sps
import numpy as np
import os
import shutil

# generate an envelope from audio signal using given attack/release coeffs
def envfollow(audio: list[float], attack: float, release: float) -> np.ndarray:
    rectaudio = [abs(x) for x in audio]
    follower = 0
    env = []
    for x in rectaudio:
        if x > follower:
            follower = (x - follower) * attack + follower
        else:
            follower = (x - follower) * release + follower

        env.append(follower)
    print(len(env))
    return np.array(env)


# generate a difference of envelopes using given attack/release coeffs
def envdiff(audio: list[float], attack1: float, release1: float, attack2: float, release2: float):
    a = envfollow(audio, attack1, release1)
    b = envfollow(audio, attack2, release2)
    diff = a - b
    return diff.clip(0,1)


def bandpass(audio, low_freq, hi_freq):
    coeffs = sps.butter(2, [low_freq, hi_freq], 'bandpass', fs=fs)
    return sps.lfilter(coeffs[0], coeffs[1], audio)


def get_sample_windows(detect, sensitivity, cooldown):
    windows = np.zeros(len(detect))
    i = 0
    while i < len(detect):
        if detect[i] > sensitivity:
            print(f"low: {i}")

            # skip ahead 0.15s after finding a transient, to avoid duplicates
            for j in range(i, i+cooldown):
                windows[j] = 1
            windows[i+cooldown] = 0
            i += cooldown
        else:
            windows[i] = 0
            i += 1
    return windows



########
# main #
########

# get audio
fs, w = wavfile.read("foley (consolidated).wav")

# sum to mono then normalize
wmono = w.mean(axis=1)
wmono = wmono.squeeze()
wmono /= max(wmono)
print(max(wmono))

# filter the audio
wlo = bandpass(wmono, 50, 200)
wmd = bandpass(wmono, 500, 6000)
whi = bandpass(wmono, 10000, 20000)

# transient analysis
envhi = envdiff(whi, 0.1, 0.0005, 0.001, 0.0001)
envmd = envdiff(wmd, 0.1, 0.0005, 0.001, 0.0001)
envlo = envdiff(wlo, 0.1, 0.0005, 0.001, 0.0001)

# differentiate each transient array
dhi = []
dmd = []
dlo = []
for i in range(1, len(envhi)):
    cmphi = envhi[i-1]
    cmpmd = envmd[i-1]
    cmplo = envlo[i-1]
    dhi.append(envhi[i] - cmphi)
    dmd.append(envmd[i] - cmpmd)
    dlo.append(envlo[i] - cmplo)

# normalize
dhi = np.array(dhi)
dmd = np.array(dmd)
dlo = np.array(dlo)
dhi /= max(dhi)
dmd /= max(dmd)
dlo /= max(dlo)

# get 0.15-second windows for low, mid, high hits

cooldown = int(0.15 * fs)
sensitivity = 0.5

detecthi = get_sample_windows(dhi, sensitivity, cooldown)
detectmd = get_sample_windows(dmd, sensitivity, cooldown)
detectlo = get_sample_windows(dlo, sensitivity, cooldown)

transhi = []
transmd = []
translo = []
transall = []

# cooldown = int(0.02 * fs)
hilag = int(0.001 * fs)
mdlag = int(0.005 * fs)
lolag = int(0.04 * fs)

# get transient times and sort into kick/snare/hat
i = 1
while i < len(detecthi):
    lookahead = min(i + cooldown, len(detecthi)-1)
    # beginning of high transient
    if detecthi[i-1] == 0 and detecthi[i] == 1:
        actual = max(i-hilag, 0)
        if detectlo[lookahead]:
            translo.append(actual)
            transall.append(actual)
        elif detectmd[lookahead]:
            transmd.append(actual)
            transall.append(actual)
        else:
            transhi.append(actual)
            transall.append(actual)
        i += cooldown
        continue
    # beginning of mid transient
    elif detectmd[i-1] == 0 and detectmd[i] == 1:
        actual = max(i-mdlag, 0)
        if detectlo[lookahead]:
            translo.append(actual)
            transall.append(actual)
        else:
            transmd.append(actual)
            transall.append(actual)
        i += cooldown
        continue
    elif detectlo[i-1] == 0 and detectlo[i] == 1:
        actual = max(i-lolag, 0)
        translo.append(actual)
        transall.append(actual)
        i += cooldown
        continue
    i += 1


# get actual samples
if os.path.exists("./out/"):
    shutil.rmtree("./out")
os.makedirs('./out/kicks')
os.makedirs('./out/snares')
os.makedirs('./out/hats')
for i,s in enumerate(transall):
    if i != len(transall)-1:
        end = transall[i+1]
    else:
        end = len(wmono)-1
    sample = w[s:end]
    if s in translo:
        wavfile.write(f"./out/kicks/{i}.wav", fs, sample)
    elif s in transmd:
        wavfile.write(f"./out/snares/{i}.wav", fs, sample)
    elif s in transhi:
        wavfile.write(f"./out/hats/{i}.wav", fs, sample)
    else:
        raise ValueError

# plot results
pp.plot(wmono, 'lightgray', linewidth=1)
pp.plot(envhi, 'r', linewidth=1)
pp.plot(envmd, 'g', linewidth=1)
pp.plot(envlo, 'b', linewidth=1)
pp.plot(dhi, 'r', linewidth=1)
pp.plot(dmd, 'g', linewidth=1)
pp.plot(dlo, 'b', linewidth=1)
pp.plot((detecthi * 0.2) - 0.4, 'r', linewidth=1)
pp.plot((detectmd * 0.2) - 0.7, 'g', linewidth=1)
pp.plot((detectlo * 0.2) - 1,   'b', linewidth=1)
pp.vlines(transhi,1.7,2,'r',linewidth=1)
pp.vlines(transmd,1.4,1.7,'g',linewidth=1)
pp.vlines(translo,1.1,1.4,'b',linewidth=1)
# pp.plot(envdiff > 0.3)
pp.show()