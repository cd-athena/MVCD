import time
from subprocess import PIPE, Popen
import pandas as pd
from codecarbon import OfflineEmissionsTracker
import sys

tracker = OfflineEmissionsTracker(country_iso_code="AUT")

INPUT_PATH = sys.argv[1]
BIN_PATH = './dataset'

ww = [3840, 1920, 1280, 960]
hh = [2160, 1080, 720, 540]
qps = [[22, 27, 32, 37], [22, 27, 32, 35, 37, 46, 55], [22, 27, 32, 37], [22, 27, 32, 37]]
codecs = ['vvenc', 'libsvtav1', 'libx264', 'libx265']
presets = ['faster', 13, 'ultrafast', 'ultrafast']
ext = ['h266', 'mp4', 'mp4', 'mp4']
frame_rate = [60, 30]
n_frames = [64, 32]

df = pd.DataFrame()

cnt = 0
for c_idx, c in enumerate(codecs):
    for f_idx, f in enumerate(frame_rate):
        for v in range(1, 1001):
            video = f'{v:04d}'
            for w_idx, w in enumerate(ww):
                for q in qps[c_idx]:
                    for e in range(5):
                        df.loc[cnt, 'video'] = video
                        df.loc[cnt, 'resolution'] = '{}p'.format(hh[w_idx])
                        df.loc[cnt, 'framerate'] = f
                        df.loc[cnt, 'qp'] = q
                        df.loc[cnt, 'codec'] = c
                        df.loc[cnt, 'preset'] = presets[c_idx]
                        f_name = "{}_{}_{}_{}_{}_{}".format(video, df.loc[cnt, 'resolution'], f, q, c,
                                                                presets[c_idx])

                        t1 = time.time()
                        tracker.start_task('video{}'.format(cnt))
                        cmd = ("time ffmpeg -i {}/{}.mp4 -frames {} -g {} -vf scale={}x{} -preset {} "
                               "-c:v {} -qp {} -y {}/{}/{}.{}").format(INPUT_PATH, video, n_frames, 32, w, hh[w_idx],
                                                                     presets[c_idx], c, q, BIN_PATH, c, f_name, ext[c_idx])
                        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                        stdout, stderr = p.communicate()
                        utime = str(stderr, encoding='utf-8').split('\n')[-3].split('u')[0]
                        cc = tracker.stop_task('video{}'.format(cnt))
                        t2 = time.time()
                        df.loc[cnt, 'emissions'] = format(cc.__getattribute__("emissions"), "f")
                        df.loc[cnt, 'cpu_energy'] = format(cc.__getattribute__("cpu_energy"), "f")
                        df.loc[cnt, 'ram_energy'] = format(cc.__getattribute__("ram_energy"), "f")
                        df.loc[cnt, 'total_energy'] = format(cc.__getattribute__("energy_consumed"), "f")
                        df.loc[cnt, 'runtime'] = format(t2 - t1, "f")
                        df.loc[cnt, 'usertime'] = float(utime)
                        cnt += 1
            df.to_csv('encoding.csv', index=False)
tracker.stop()
