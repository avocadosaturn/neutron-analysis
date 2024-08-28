import sys
import edepparser
import h5py
import numpy as np
import matplotlib.pyplot as plt
from GAMPixTools import electron_track_tools
from tools import calculate_centroid

# input file must have +z removed already
file = sys.argv[1]
f = h5py.File(file)


z_pts = []
true_pts = []
detected_pts = []
efficiency_pts = []


for traj in f['trajectories']:
    if traj['primary'] == True:
        ev_n = traj['event_id']

        print('----------------------------------')
        print(f'Event {ev_n}')

        
        ev_mask = f['segments']['event_id'] == ev_n
        segs = f['segments'][ev_mask]

        # centroid
        num = 0
        denom = 0
        for seg in segs:
            seg_z = seg['z']

            num += seg_z
            denom += 1
        avg_z = abs(num / denom) / 100
        print(avg_z)
        z_pts.append(avg_z)


        track = electron_track_tools.Track(file, ev_n,
                                       input_format='dumpTree',
                                       origin_shift=[0, 0, -5])
        track.reset_params(charge_readout='GAMPixD')
        track.readout_charge()

    
        true = track.raw_track['num_e'].sum()
        true_pts.append(true)

        detected = track.pixel_samples['samples_triggered'].sum()
        detected_pts.append(detected)

        eff = detected / true
        efficiency_pts.append(eff)
        if eff > 1:
            print(f'EFF > 1 {eff}')


plt.style.use('dark_background')
plt.plot(z_pts, efficiency_pts, '.')
plt.title('Detection Efficiency vs. Distance')
plt.xlabel('Distance from anode (m)')
plt.ylabel('Efficiency (detected/true)')
plt.savefig('depth.png')


