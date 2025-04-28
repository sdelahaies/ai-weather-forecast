import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import json

# SETTINGS
grib_file = "outputs/gencast-1.0_20250422_0000_360.grib"

jsonfile="gencast-1.0_viz_1.json"
prefix = "fields/gencast-1.0_viz_1" 
output_dir = f"../viz-weather-forecast/public/{prefix}"
fields = ['u','v','t','q']
maxSteps=29
steps=[i for i in range(maxSteps+1)]
# levels=[i for i in range(0,13,3)]
levels=[3]

jsondata = {
            'prefix':prefix,
            'fields':fields,
            'maxSteps':maxSteps,
            'levels':levels,
            }

with open(f"outputs/{jsonfile}",'w') as f:
    json.dump(jsondata,f)

# step_index = 0
# level_index = 0

os.makedirs(output_dir, exist_ok=True)

ds = xr.load_dataset(grib_file, engine="cfgrib", backend_kwargs={
    "filter_by_keys": {"typeOfLevel": "isobaricInhPa"}
})

print(ds)

dpi=100

# adjust these values to clip the data 
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

for level in levels:
    for step in steps:
        for field in fields:
            if field not in ds:
                print(f"Skipping missing field: {field}")
                continue

            data = ds[field].isel(step=step, isobaricInhPa=level)
            data=ds[field].isel(step=step, isobaricInhPa=level).clip(min=field_ranges[field][0],max=field_ranges[field][1])
            # data
            fig = plt.figure(figsize=(12, 6), dpi=dpi)
            ax = plt.axes(projection=ccrs.PlateCarree())
            
            data.plot.imshow(ax=ax, transform=ccrs.PlateCarree(), cmap='viridis', add_colorbar=False,add_labels=False)
            
            ax.coastlines(resolution='110m',color='white', linewidth=.5)
            ax.set_global()
            ax.axis('off')

            # Save the figure as transparent PNG
            out_path = os.path.join(output_dir, f"{field}_{step:02d}_{level:02d}.jpg")
            plt.savefig(out_path, bbox_inches='tight', pad_inches=0, transparent=True,dpi=dpi)
            plt.close()
            print(f"Saved {out_path}")
