# Gencast forecast

## Install dependencies
```bash
uv venv
source .venv/bin/activate
```

```bash
uv pip install ai-models
ONNXRUNTIME=onnxruntime-gpu uv pip install ai-models-panguweather
uv pip install jax[cuda12]
uv pip install git+https://github.com/deepmind/graphcast.git
```


```bash
wget https://data.ecmwf.int/ecpds/home/opendata/20250427/00z/aifs-single/0p25/oper/20250427000000-0h-oper-fc.grib2
```

```bash
# ai-models --lead-time 24 --input opendata --file data/20250427000000-0h-oper-fc.grib2 --path panguweather_20250427_0000_24.grib panguweather
ai-models --lead-time 24 --input cds --date 20250422 --time 0000 --path outputs/pangu_20250422_0000_24.grib panguweather
```

```bash
uv pip install matplotlib cartopy
```