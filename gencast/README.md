# Gencast forecast

## Install dependencies
```bash
uv pip install ai-models
uv pip install ai-models-gencast
uv pip install jax[cuda12]
uv pip install git+https://github.com/deepmind/graphcast.git
```

## Download the model
```bash
ai-models --download-assets gencast
```
here we use gencast-1.0 which fits in 16Gb of VRAM
```bash
ai-models --download-assets gencast-1.0
```

<!-- 
```bash
ai-models --lead-time 12 --input opendata --file data/20250427000000-0h-oper-fc.grib2 gencast-1.0
``` -->

## Run the model
```bash
ai-models --lead-time 360 --input cds --date 20250422 --time 0000 --path ../outputs/gencast-1.0_20250422_0000_360.grib gencast-1.0
```

## Produce forecast maps
```bash
uv pip install xarray matplotlib cartopy
```

```bash
python produce_maps.py
```