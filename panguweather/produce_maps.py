import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import numpy as np

# SETTINGS
grib_file = "panguweather.grib"
output_dir = "maps"
fields = ['z','q','t','u','v']


os.makedirs(output_dir, exist_ok=True)

# Load dataset
ds = xr.load_dataset(grib_file, engine="cfgrib")

# # Compute global vmin/vmax for each field
# field_ranges = {}
# for field in fields:
#     if field in ds:
#         field_data = ds[field]  # (step, level, lat, lon)
#         vmin = float(field_data.min())
#         vmax = float(field_data.max())
#         field_ranges[field] = (vmin, vmax)
#         print(f"{field}: vmin={vmin}, vmax={vmax}")
#     else:
#         print(f"Skipping missing field: {field}")

field_ranges = {}
field_ranges['u']=(-24,30)
field_ranges['v']=(-23,26)
field_ranges['z']=(0,2000)
field_ranges['t']=(235,317)
field_ranges['q']=(0.0001,0.0222)
ds['t']=ds['t'].clip(min=field_ranges['t'][0],max=field_ranges['t'][1])
ds['u']=ds['u'].clip(min=field_ranges['u'][0],max=field_ranges['u'][1])
ds['v']=ds['v'].clip(min=field_ranges['v'][0],max=field_ranges['v'][1])
ds['z']=ds['z'].clip(min=field_ranges['z'][0],max=field_ranges['z'][1])
ds['q']=ds['q'].clip(min=field_ranges['q'][0],max=field_ranges['q'][1])

dpi=100

# Plot each frame with consistent colorbar
for field in fields:
    if field not in ds:
        continue

    vmin, vmax = field_ranges[field]
    data_field = ds[field]

    for step_index in range(data_field.sizes['step']):
        # Optionally: loop over levels if needed, here just one level (index 0)
        # data = data_field.isel(step=step_index, isobaricInhPa=0)
        data=ds[field].isel(step=step_index, isobaricInhPa=0).clip(min=field_ranges[field][0],max=field_ranges[field][1])
        
        fig = plt.figure(figsize=(8, 4), dpi=dpi)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()

        im = ax.pcolormesh(
            ds.longitude,
            ds.latitude,
            data,
            cmap="viridis",    # or choose another like 'plasma', 'coolwarm', etc.
            vmin=vmin,
            vmax=vmax,
            transform=ccrs.PlateCarree()
        )

        ax.set_global()
        ax.axis('off')

        filename = os.path.join(output_dir, f"{field}_{step_index:02d}.png")
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close(fig)
        del data