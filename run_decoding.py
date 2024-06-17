import time
import numpy as np
from subprocess import PIPE, Popen

import pandas as pd
from codecarbon import OfflineEmissionsTracker

class VideoCaptureYUV:
    def __init__(self, filename, size):
        self.height, self.width = size
        self.frame_len = self.width * self.height * 3 // 2
        self.f = open(filename, 'rb')
        self.shape = (int(self.height * 3 // 2), self.width)

    def read(self):
        try:
            raw = self.f.read(self.frame_len)
            yuv = np.frombuffer(raw, dtype=np.uint8)
            yuv = yuv.reshape(self.shape)
        except Exception as e:
            print(str(e))
            return False, None
        return True, yuv


def temporal_upscaling(input_yuv, output_yuv):
    cap = VideoCaptureYUV(input_yuv, (2160, 3840))
    with open(output_yuv, 'wb') as yuv_file:
        while 1:
            ret, frame = cap.read()
            if not ret:
                break
            yuv_file.write(frame.tobytes())
            yuv_file.write(frame.tobytes())


tracker = OfflineEmissionsTracker(country_iso_code="AUT")

ww = [3840, 1920, 1280, 960]
hh = [2160, 1080, 720, 540]
qps = [[22, 27, 32, 37], [22, 27, 32, 35, 37, 46, 55], [22, 27, 32, 37], [22, 27, 32, 37]]
codecs = ['vvenc', 'libsvtav1', 'libx264', 'libx265']
presets = ['faster', 13, 'ultrafast', 'ultrafast']
ext = ['h266', 'mp4', 'mp4', 'mp4']
frame_rate = [60, 30]
n_frames = [64, 32]
upscale = ['ups', 'dws']


df = pd.DataFrame(columns=['video', 'resolution', 'framerate', 'qp', 'codec', 'preset',
                           'cc_duration', 'cc_emissions', 'cc_cpu_energy', 'cc_ram_energy', 'cc_energy_consumed',
                           'time'])


c = 0
df = pd.DataFrame(columns=['video', 'resolution', 'framerate', 'qp', 'codec', 'preset',
                           'cc_duration', 'cc_emissions', 'cc_cpu_energy', 'cc_ram_energy',
                           'cc_energy_consumed',
                           'time', 'epoch', 'upscale', 'time30to60'])
for u in upscale:
    for j in range(4):                                              # Codec
        for n in range(2):                                          # Framerate
            for v in range(1, 1001):                                # Video
                video = f'{v:04d}'
                for i in range(4):                                  # Resolution
                    for q in qps[j]:                                # QP
                        for e in range(5):                          # Iteration
                            df.loc[c, 'video'] = video
                            df.loc[c, 'resolution'] = '{}p'.format(hh[i])
                            df.loc[c, 'framerate'] = frame_rate[n]
                            df.loc[c, 'qp'] = q
                            df.loc[c, 'codec'] = codecs[j]
                            df.loc[c, 'preset'] = presets[j]
                            df.loc[c, 'epoch'] = e
                            df.loc[c, 'upscale'] = u

                            f_name = "{}_{}_{}_{}_{}_{}".format(video, df.loc[c, 'resolution'], frame_rate[n], q,
                                                                df.loc[c, 'codec'], df.loc[c, 'preset'])

                            tracker.start_task('video{}'.format(c))
                            t1 = time.time()

                            if u == 'dws':
                                cmd = ("time ffmpeg -i ./dataset/{}/{}.{} -y temp.yuv").format(codecs[j], f_name, ext[j])
                                p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                                stdout, stderr = p.communicate()
                                stderr = str(stderr, encoding='utf-8')
                                utime = stderr.split('\n')[-3].split()[-1]
                                t3 = time.time()
                            else:
                                cmd = ("time ffmpeg -i ./dataset/{}/{}.{} -vf scale=3840x2160 -y temp.yuv").format(codecs[j], f_name, ext[j])
                                p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                                print(cmd)
                                stdout, stderr = p.communicate()
                                stderr = str(stderr, encoding='utf-8')
                                utime = stderr.split('\n')[-3].split()[-1]
                                t3 = time.time()

                                if frame_rate[n] == 30:
                                    temporal_upscaling("temp.yuv", "temp_up.yuv")

                            t2 = time.time()
                            cc = tracker.stop_task('video{}'.format(c))

                            df.loc[c, 'cc_duration'] = format(cc.__getattribute__("duration"), ".12f")
                            df.loc[c, 'cc_emissions'] = format(cc.__getattribute__("emissions"), ".12f")
                            df.loc[c, 'cc_cpu_energy'] = format(cc.__getattribute__("cpu_energy"), ".12f")
                            df.loc[c, 'cc_ram_energy'] = format(cc.__getattribute__("ram_energy"), ".12f")
                            df.loc[c, 'cc_energy_consumed'] = format(cc.__getattribute__("energy_consumed"), ".12f")
                            df.loc[c, 'time'] = format(t3 - t1, ".12f")
                            df.loc[c, 'time30to60'] = format(t2 - t3, ".12f")
                            df.loc[c, 'utime'] = int(utime.split('m')[0]) * 60 + float(utime.split('m')[-1][:-1])
                            c = c + 1
                df.to_csv('decoding.csv', index=False)
tracker.stop()
