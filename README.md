# neutron-analysis
A group of programs to analyze characteristics of a neutron in a LArTPC. While the programs were written with neutrons in mind, they could in principle be used for other particles, with a few tweaks. 

Neutrons in a volume of LAr were simulated using edep-sim. The output of this was fed into GAMPixTools, which simulates the detector. 


## edep-sim analysis
Analysis at this stage is purely of the physics of a neutron in a sea of LAr. All programs take .root files as input, and are run as python <program-name.py> <input-file.root>

### energy 
Plots energy in downstream particles vs. kinetic energy of the primary neutron. Downstream energy is determined as the sum of dEs in all edep-sim segments associated with that event. 

### spread
Plots spatial RMS vs. kinetic energy of primary neutron.  Unweighted RMS calculated as
```math
\sqrt \frac {\displaystyle\sum_{i}(\vec r_i - \vec{\overline{\mu}})^2} {N}
```
Where $\vec{r_i}$ is the position of the ith segment, $\vec{\overline{\mu}}$ is the position of the centroid of the segments, and N is the number of segments. Weighted RMS calculated as
```math
\sqrt \frac {\displaystyle\sum_{i}(\vec{r_i} - \vec{\overline{\mu}})^2 E_i} {\displaystyle\sum_{i}E_i}
```
where $E_i$ is dE of the ith segment. The centroid is also weighted, here. 
Spatial RMS quantifies how spread out the particles are; higher RMS indicates greater spread, and vice versa. 

### diff spread
Plots the same thing as spread, except creates plots for just neutrons and plots for all other particles. I.e., differentiates between neutrons and non-neutrons. 


## gampix analysis
Looks at detector effects, uses only ionized electron information. All programs take .h5 files as input, and are run as python <program-name.py> <input-file.h5>

### true ionization
Plots number of electrons ionized (after recombination) vs. kinetic energy of primary neutron. Actually, this does not include any detector effects, but uses electron information, so has to be done after the detector simulation. Uses electrons ionized in all downstream segments, regardless of whether or not they are within the detctor volume. 

### zcut
GAMPixTools places the anode at z=0 and defines the detector space to z < 0. Currently, it assumes all segments are in z < 0 and does not handle other cases well. zcut.py generates an output file with all z > 0 segments removed from input file. Recommended to use a copy of your original file as in put to preserve the original information. 

### detector 
Presumes a segments in z > 0 have been removed using zcut.py. Plots how the number of ionized electrons within detector volume (-z only), the number of electrons after drift to anode (-z only, attenuation, diffusion), and the number of electrons after detection (-z only, attenuation, diffusion, threshold, noise) depend on the kinetic energy of the primary neutron. Also plots how efficiency depends on the kinetic energy of the neutron, where efficiency is defined as:
```math
\frac {\# of detected electrons} {\# of ionized electrons}
```

### attenuation correction
Attenuation follows the established equation,
```math
n_d = n_0 e^{\frac {z} {\tau v_drift}}
```
where $n_d$ is the number of electrons after drift, $n_0$ is the number of ionized electrons, $z$ is the cluster's distance from the anode, $tau$ is the drift lifetime, and $v_drift$ is the drift velocity of the electrons, determined by the electric field. For each cluster, the program solves for $n_0$ and uses that as the cluster after corrected for attenuation. When GAMPixTools applies attenuation, binomial selection is performed, so there is some uncertainty. 

### depth
Plots how efficiency depends on the centroid's distance from the anode. 

