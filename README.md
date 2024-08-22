# neutron-analysis
A group of programs to analyze characteristics of a neutron in a LArTPC. While the programs were written with neutrons in mind, they could in principle be used for other particles, with a few tweaks. 

$\sqrt{3x-1}+(1+x)^2$

Neutrons in a volume of LAr were simulated using edeps-sim. The output of this was fed into GAMPixTools, which simulates the detector. 

# edep-sim analysis
Analysis at this stage is purely of the physics of a neutron in a sea of LAr. All programs take .root files as input, and are run as python <program-name.py> <input-file.root>

## energy 
Plots energy in downstream particles vs. kinetic energy of the primary neutron. Downstream energy is determined as the sum of dEs in all edep-sim segments associated with that event. 

## spread
Plots spatial RMS vs. kinetic energy of primary neutron.  Unweighted RMS calculated as
$$ \sqrt \frac {\displaystyle\sum_{i}(\vec r_i - \vec{\bar{\mu}})^2} {N} $$
Where $ \vec r_i $ is the position of the ith segment, $ \vec{\bar{\mu}} $ is the position of the centroid of the segments, and N is the number of segments. Weighted RMS calculated as
$$ \sqrt \frac {\displaystyle\sum_{i}(\vec r_i - \vec{\bar{\mu}})^2 E_I} {\displaystyle\sum_{i}E_i} $$
where $ E_i $ is dE of the ith segment. The centroid is also weighted, here. 
Spatial RMS quantifies how spread out the particles are; higher RMS indicates greater spread, and vice versa. 

### diff spread
Plots the same thing as spread, except creates plots for just neutrons and plots for all other particles. I.e., differentiates between neutrons and non-neutrons. 

# gampix analysis
Looks at detector effects, uses only ionized electron information. All programs take .h5 files as input, and are run as python <program-name.py> <input-file.h5>

## zcut.py
