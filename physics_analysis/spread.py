import sys
import edepparser
import numpy as np
import matplotlib.pyplot as plt
import math
import os
from tools import calculate_centroid, bin20, calculate_rms


parser = edepparser.EdepSimParser(sys.argv[1])

ev_n = 0
m_n = 940.6 # mass of neutron in MeV

w_rms_pts = []
uw_rms_pts = []
E_in_pts = []


for ev in parser:
    # get initial position
    for traj in ev.trajectories:
        if traj.GetTrackId() == 0:
            start_x = traj.GetInitialMomentum().X()
            start_y = traj.GetInitialMomentum().Y()
            start_z = traj.GetInitialMomentum().Z()
            initial_position = np.array([start_x, start_y, start_z])


    # get incoming energy
    for primary in ev.event.Primaries:
        for particle in primary.Particles:
            kinetic_E = particle.GetMomentum().E() - m_n
            E_in_pts.append(kinetic_E)
            
    uw_centroid, w_centroid = calculate_centroid(ev.segments)
    
    uw_rms = calculate_rms(ev.segments, uw_centroid, 'uw')
    uw_rms_pts.append(uw_rms)
    w_rms = calculate_rms(ev.segments, w_centroid, 'w')
    w_rms_pts.append(w_rms)


    """
    # output values
    print("-----------------------------------------------------")
    print(f"Event {ev_n}")
    ev_n += 1
    print()

    print(f"Centroid: <{centroid[0]}, {centroid[1]}, {centroid[2]}>")
    print(f"Average distance: {avg_distance} mm")
    print(f"RMS: {rms} mm")
    """

    
# binning
w_rms_avgx, w_rms_avgs, w_rms_errors, w_relative_rms = bin20(E_in_pts, w_rms_pts)
uw_rms_avgx, uw_rms_avgs, uw_rms_errors, uw_relative_rmsx = bin20(E_in_pts, uw_rms_pts)


# plots
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 5))

ax1.plot(E_in_pts, uw_rms_pts, '.')
ax1.set_title('Unweighted Spatial RMS vs. Neutron Energy')
ax1.set_xlabel('Kinetic Energy (MeV)')
ax1.set_ylabel('Spatial RMS (mm)')

ax2.plot(E_in_pts, w_rms_pts, '.')
ax2.set_title('Weighted Spatial RMS vs. Neutron Energy')
ax2.set_xlabel('Kinetic Energy (MeV)')
ax2.set_ylabel('Spatial RMS (mm)')

#ax1.errorbar(uw_rms_avgx, uw_rms_avgs, uw_rms_errors, fmt = '.', capsize = 4, ecolor = 'white')
#ax1.set_title('Unweighted RMS vs. Neutron Energy')
#ax1.set_xlabel('Kinetic Energy (MeV)')
#ax1.set_ylabel('RMS (mm)')

#ax2.errorbar(w_rms_avgx, w_rms_avgs, w_rms_errors, fmt = '.', capsize = 4, ecolor = 'white')
#ax2.set_title('Weighted RMS vs. Neutron Energy')
#ax2.set_xlabel('Kinetic Energy (MeV)')
#ax2.set_ylabel('RMS (mm)')

plt.tight_layout()
#plt.show()
plt.savefig('spread.png')
