# MVCD
A comprehensive video coding dataset, namely MVCD, contains nearly 4 million records of encoding and decoding processes. It enables the usage of machine learning models on video streaming applications such as bitrate ladder prediction, resource allocation, rate-quality control, and energy-efficient streaming.

Content:
- [Input Videos](#input-videos)
- [Dataset Characteristics](#dataset-characteristics)
- [Usage](#usage)
- [Build your own video compression dataset](#build-your-own-video-compression-dataset)
- [Citation](#citation)


## Input Videos
To create MVCD, 1000 video sequences are collected from Inter4K, which have a resolution of 4K and a frame rate of 60 fps. The input videos can be downloaded from: [https://tinyurl.com/inter4KUHD](https://tinyurl.com/inter4KUHD)

## Dataset Characteristics
The provided dataset includes information on energy consumption, time complexity, video quality, and bitrate for various video codecs used on different devices.
- Energy Consumption: measured using [CodeCarbon](https://codecarbon.io/) and [Powermetrics](https://firefox-source-docs.mozilla.org/performance/powermetrics.html) tools and covers CPU, RAM, total energy consumption in kWh, and CO2 emissions in Kg.
- Time Complexity: measured using the time command in the Linux operating system and includes user-time and run-time values.
- Video Quality: reported video quality includes four different metrics, namely PSNR, VMAF, SSIM, and MS-SSIM.
- Bitrate: reported in Kbps.

## Usage
The dataset is provided in four category files:
- Video Complexity: contains the value of [SITI](https://github.com/VQEG/siti-tools), [Eh](https://github.com/cd-athena/VCA), and [SCTC](https://github.com/cd-athena/EVCA) video complexity metrics for each video sequence.
- Video Encoding: contains information about encoding energy consumption, time complexity, video quality, and bitrate for all encoding processes.
- Video Decoding: contains decoding energy consumption, and time complexity for H.264/AVC, H.265/HEVC, AV1, H.266/VVC video codecs and encoding parameters across three different devices. Each decoding process is repeated five times for consistent results, so the aggregated values can be used here.
- Video Decoding and Upscaling to Original Resolutions: contains the same information as the decoding file provided, but here the impact of upscaling on the mentioned parameters is also considered.


To read CSV files and generate an output file, namely ```dataset_output.csv```, with all the necessary information, use the following command.
```
python3 generate_output.py -a aggregation_method -o dataset_output.csv
```
The aggregation method is utilized to combine decoding information that has been repeated five times.

Available aggregation methods:
- **mean** (Default)
- **median**
- **min**
- **max**
- **first**
- **last**


## Build your own video compression dataset
To create the video compression dataset, make sure to install the necessary requirements.
- [FFmpeg](https://ffmpeg.org/) (make sure that livsvtav1 is supported.)
- [VVenC](https://github.com/fraunhoferhhi/vvenc) and [VVdeC](https://github.com/fraunhoferhhi/vvdec)
- [EVCA](https://github.com/cd-athena/EVCA)
- [VMAF](https://github.com/Netflix/vmaf)
- Python and package requirements

Run the following command to get the required Python packages
```
pip3 install -r requirements.txt
```

To calculate video complexities:
```
```

To run encoding tasks:
```
```

To run decoding tasks:
```
```

To run decoding and upscaling tasks:
```
```



## Citation

If this work is helpful for your research, please consider citing MVCD.

```
@inproceedings{amirpour_mvcd_2024,
	title = {{MVCD}: {Multi-Dimensional} {Video} {Compression} {Dataset}},
	volume = {2024},
	shorttitle = {{MVCD}},
	language = {English},
	author = {Amirpour, H. and Ghasempour, M. and Tashtarian, F. and Afzal, S. and Hamodouche, W. and Timmerer, C.},
	year = {2024},
	keywords = {Video encoding, decoding, energy, complexity, quality},
}
```
