import sys
import matplotlib.pyplot as plt
import h5py
import numpy as np
from GAMPixTools import electron_track_tools

file = sys.argv[1]
f = h5py.File(file)
depth = 0
m_n = 940.6

E_in_pts = []
drifted_pts = []
drifted_corrected_pts = []
detected_corrected_pts = []


for traj in f['trajectories']:
    if traj['traj_id'] == 0:
        ev_n = traj['event_id']
        KE = traj['E_start'] - m_n
        E_in_pts.append(KE)

        print('----------------------------------------')
        print(f'Event {ev_n}')

        track = electron_track_tools.Track(file, ev_n,
                                           input_format='dumpTree',
                                           origin_shift=[0, 0, -5])

        track.reset_params(charge_readout='GAMPixD')
        track.readout_charge(depth)

        true = track.raw_track['num_e'].sum()
        
        drifted_arr = track.pixel_samples['samples_raw']
        drifted = drifted_arr.sum()


        # correction
        drift_length = track.params.charge_drift['drift_length']
        drifted_corrected = 0
        for i, cluster in enumerate(drifted_arr):
            drift_distance = abs(track.pixel_samples['r_raw'][2, :][i])
            corrected_cluster = cluster * np.exp(drift_distance / drift_length)        
            drifted_corrected += corrected_cluster

        drifted_corrected_pts.append(drifted_corrected)


        correction = drifted_corrected - drifted
        detected = track.pixel_samples['samples_triggered'].sum()
        detected_corrected = detected + correction
        detected_corrected_pts.append(detected_corrected)
        
        print(f'# of ionized e-: {true}')
        print(f'# of drifted e- after correction: {drifted_corrected}')
        print(f'# of drifted e-: {drifted}')
        print(f'# of detected e-: {detected}')
        print(f'# of detected e-: after correction: {detected_corrected}')


"""
print()
print('Summary:')
print()
print(f'evs w good correction: {good_evs}')
print(f'length: {len(good_evs)}')
print()
print(f'evs w bad correction: {fail_evs}')
print(f'length: {len(fail_evs)}')
"""

plt.style.use('dark_background')

#plt.plot(E_in_pts, drifted_corrected_pts, '.')
#plt.title('Electrons corrected for attenuation, after drift')
#plt.xlabel('Kinetic Energy (MeV)')
#plt.ylabel('Number of electrons')
#plt.savefig('att_corrected_after_drift.png')

plt.plot(E_in_pts, detected_corrected_pts, '.')
plt.title('Electrons corrected for attenuation, after detection')
plt.xlabel('Kinetic Energy (MeV)')
plt.ylabel('Number of electrons')
plt.savefig('att_corrected_after_det.png')
