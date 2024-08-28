import sys
import matplotlib.pyplot as plt
import h5py
from GAMPixTools import electron_track_tools


file = sys.argv[1]
f = h5py.File(file)
depth = 0
m_n = 940.6

E_in_pts = []
true_pts = []

for traj in f['trajectories']:
    # if this is the priamry
    if traj['traj_id'] == 0:
        ev_n = traj['event_id'] # note: events will be in order
        KE = traj['E_start'] - m_n 
        E_in_pts.append(KE)

        print('----------------------------------------------------')
        print(f'Event {ev_n}')
        
        track = electron_track_tools.Track(file, ev_n,
                                           input_format = 'dumpTree',
                                           origin_shift = [0, 0, -5])

        track.reset_params(charge_readout = 'GAMPixD')
        track.readout_charge(depth)
    
        # ionization yield (includes  recombination), no z cut
        true = track.raw_track['num_e'].sum()
        true_pts.append(true)

            
plt.style.use('dark_background')


# ionization yield before zcut vs. KE
plt.plot(E_in_pts, true_pts, '.')
plt.title('Total Ionization Yield vs. Neutron Energy')
plt.xlabel('Kinetic Energy (MeV)')
plt.ylabel('Ionized Electrons (number of electrons)')

plt.tight_layout()
#plt.show()
plt.savefig('ionized_nocut.png')
