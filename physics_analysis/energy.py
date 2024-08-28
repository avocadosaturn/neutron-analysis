import os
import math
import sys
import edepparser
import matplotlib.pyplot as plt
import numpy as np
from tools import bin20


parser = edepparser.EdepSimParser(sys.argv[1])


# print number of events
ev_n = 0
for ev in parser:
    ev_n += 1
print(f"Number of events: {ev_n}")


E_in_pts = []
E_out_pts = []
m_n = 940.6


for ev in parser:
    print("---------------------------------------------------")
    # Get primary particle(s)
    for traj in ev.trajectories:
        if traj.GetTrackId() == 0:
            print(f"Primary: {traj.GetName()}")
            
    # Get incoming energy
    for primary in ev.event.Primaries:
        for particle in primary.Particles:
            kinetic_E = particle.GetMomentum().E() - m_n
            E_in_pts.append(kinetic_E)      # total energy, mass and KE 
            print(f"Incoming Energy: {kinetic_E}")
            
    # Get deposited energy
    E_out = 0
    for seg in ev.segments:
        E_out += seg.GetEnergyDeposit()
    E_out_pts.append(E_out)
    print(f"Energy deposited: {E_out}")


# plot
plt.style.use('dark_background')
plt.plot(E_in_pts, E_out_pts, '.')
plt.title('Energy Deposited vs. Neutron Energy', fontsize = 14)
plt.xlabel("Kinetic Energy (MeV)", fontsize = 12)
plt.ylabel("Energy Deposited (MeV)", fontsize = 12)
#plt.show()
plt.savefig('energy.png')


"""
# plots with binning, statistical analysis
avgs_x, avgs, errors, relative_rms = bin20(E_in_pts, E_out_pts)

plt.style.use('dark_background')

fig1, ax1 = plt.subplots()
ax1.errorbar(avgs_x, avgs, errors, fmt = '.', capsize = 4, ecolor='white')
ax1.set_title('Energy Deposited vs. Neutron Energy')
ax1.set_xlabel('Kinetic Energy (MeV)')
ax1.set_ylabel('Energy Deposited (MeV)')

fig2, ax2 = plt.subplots()
ax2.plot(avgs_x, relative_rms, '.')
ax2.set_title('Relative RMS for Energy Deposited vs. Neutron Energy')
ax2.set_xlabel('Kinetic Energy (MeV)')
ax2.set_ylabel('Relative RMS for Energy Deposited')

#plt.show()
fig1.savefig('energy_analysis_w_rms.png')
fig2.savefig('energy_analysis_relative_rms.png')
"""
