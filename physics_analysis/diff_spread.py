import edepparser
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
from tools import bin20, calculate_centroid, calculate_rms


parser = edepparser.EdepSimParser(sys.argv[1])

# n = neutron; nn = non-neutron
n_w_rms_pts = []
n_uw_rms_pts = []
nn_w_rms_pts = []
nn_uw_rms_pts = []
E_in_pts = []
m_n = 940.6 #MeV


for ev in parser:
    # getting information ---------------------------------------------------------------
    # get incoming energy
    for primary in ev.event.Primaries:
        for particle in primary.Particles:
            kinetic_E = particle.GetMomentum().E() - m_n
            E_in_pts.append(kinetic_E)

    
    # determine neutron vs. noneutron trajectories
    PDGs = []
    trajectories = ev.trajectories
    for traj in trajectories:
        PDGs.append(traj.GetPDGCode())

    n_indices = [i for i, pdg in enumerate(PDGs) if pdg == 2112]
    nn_indices = [i for i, pdg in enumerate(PDGs) if pdg != 2112]
    
    neutrons = [trajectories[i] for i in n_indices]
    nonneutrons = [trajectories[i] for i in nn_indices]
    
    n_track_ids = []
    for neutron in neutrons:
        n_track_ids.append(neutron.GetTrackId())
    nn_track_ids = []
    for nonneutron in nonneutrons:
        nn_track_ids.append(nonneutron.GetTrackId())

    # find associated segments
    segments = ev.segments
    seg_track_ids = [] # track ids of all segments
    for seg in segments:
        seg_track_ids.append(seg.Contrib[0])

    n_seg_indices = [i for i, track_id in enumerate(seg_track_ids) if track_id in n_track_ids]
    nn_seg_indices = [i for i, track_id in enumerate(seg_track_ids) if track_id in nn_track_ids]

    neutron_segs = [segments[i] for i in n_seg_indices]
    nonneutron_segs = [segments[i] for i in nn_seg_indices]


    # calculations -------------------------------------------------------------------------
    # neutrons --------------------------
    n_uw_centroid, n_w_centroid = calculate_centroid(neutron_segs)
    n_uw_rms = calculate_rms(neutron_segs, n_uw_centroid, 'uw')
    n_w_rms = calculate_rms(neutron_segs, n_w_centroid, 'w')
    
    n_w_rms_pts.append(n_w_rms)
    n_uw_rms_pts.append(n_uw_rms)

    # nonneutrons --------------------------
    nn_uw_centroid, nn_w_centroid = calculate_centroid(nonneutron_segs)
    nn_uw_rms = calculate_rms(nonneutron_segs, nn_uw_centroid, 'uw')
    nn_w_rms = calculate_rms(nonneutron_segs, nn_w_centroid, 'w')

    nn_w_rms_pts.append(nn_w_rms)
    nn_uw_rms_pts.append(nn_uw_rms)


# binning --------------------------------------------------------------------------------
n_uw_avg_x, n_uw_avgs, n_uw_errors, n_uw_relative_rms = bin20(E_in_pts, n_uw_rms_pts)
n_w_avg_x, n_w_avgs, n_w_errors, n_w_relative_rms = bin20(E_in_pts, n_w_rms_pts)
nn_uw_avg_x, nn_uw_avgs, nn_uw_errors, nn_uw_relative_rms = bin20(E_in_pts, nn_uw_rms_pts)
nn_w_avg_x, nn_w_avgs, nn_w_errors, nn_w_relative_rms = bin20(E_in_pts, nn_w_rms_pts)

    
# plots -----------------------------------------------------------------------------------    
plt.style.use('dark_background')
fig, ax = plt.subplots(2, 2, figsize = (12, 8))

# neutron unweighted RMS vs. KE
ax[0, 0].plot(E_in_pts, n_uw_rms_pts, '.')
ax[0, 0].set_title('Neutron Unweighted RMS vs. Incoming Neutron Energy')
ax[0, 0].set_xlabel('Kinetic Energy (MeV)')
ax[0, 0].set_ylabel('RMS (mm)')
    
ax[0, 1].plot(E_in_pts, n_w_rms_pts, '.')
ax[0, 1].set_title('Neutron Weighted RMS vs. Incoming Neutron Energy')
ax[0, 1].set_xlabel('Kinetic Energy (MeV)')
ax[0, 1].set_ylabel('RMS (mm)')

ax[1, 0].plot(E_in_pts, nn_uw_rms_pts, '.')
ax[1, 0].set_title('Non-neutron Unweighted RMS vs. Incoming Neutron Energy')
ax[1, 0].set_xlabel('Kinetic Energy (MeV)')
ax[1, 0].set_ylabel('RMS (mm)')
    
ax[1, 1].plot(E_in_pts, nn_w_rms_pts, '.')
ax[1, 1].set_title('Non-neutron Weighted RMS vs. Incoming Neutron Energy')
ax[1, 1].set_xlabel('Kinetic Energy (MeV)')
ax[1, 1].set_ylabel('RMS (mm)')

"""
ax[0, 0].errorbar(n_uw_avg_x, n_uw_avgs, n_uw_errors, fmt = '.', capsize = 4, ecolor = 'white')
ax[0, 0].set_title('Neutron Unweighted RMS vs. Incoming Neutron Energy')
ax[0, 0].set_xlabel('Kinetic Energy (MeV)')
ax[0, 0].set_ylabel('RMS (mm)')

ax[0, 1].errorbar(n_w_avg_x, n_w_avgs, n_w_errors, fmt = '.', capsize = 4, ecolor = 'white')
ax[0, 1].set_title('Neutron Weighted RMS vs. Incoming Neutron Energy')
ax[0, 1].set_xlabel('Kinetic Energy (MeV)')
ax[0, 1].set_ylabel('RMS (mm)')

ax[1, 0].errorbar(nn_uw_avg_x, nn_uw_avgs, nn_uw_errors, fmt = '.', capsize = 4, ecolor = 'white')
ax[1, 0].set_title('Non-neutron Unweighted RMS vs. Incoming Neutron Energy')
ax[1, 0].set_xlabel('Kinetic Energy (MeV)')
ax[1, 0].set_ylabel('RMS (mm)')

ax[1, 1].errorbar(nn_w_avg_x, nn_w_avgs, nn_w_errors, fmt = '.', capsize = 4, ecolor = 'white')
ax[1, 1].set_title('Non-neutron Weighted RMS vs. Incoming Neutron Energy')
ax[1, 1].set_xlabel('Kinetic Energy (MeV)')
ax[1, 1].set_ylabel('RMS (mm)')
"""

plt.tight_layout()
#plt.show()
plt.savefig('diff_spread.png')

