def bin20(xpts, ypts):
    import numpy as np
    import math
    import sys

    
    bins = np.linspace(0, 1000, 21)
    bin_indices = np.digitize(xpts, bins) - 1
    binned_data = {i: [] for i in range(len(bins) - 1)}
    for i, bin_index in enumerate(bin_indices):
        binned_data[bin_index].append(ypts[i])

    # calculate averages in each bin
    avgs = []
    for i in binned_data:
        y_list = binned_data[i]
        avg_num = 0
        avg_n = len(y_list)

        if avg_n == 0:
            sys.exit('no points in bin, run with more events')

        for y in y_list:
            avg_num += y

        avg = avg_num / avg_n
        avgs.append(avg)


    # calculate midpoints of bins
    avgs_x = []
    for i in range(len(bins) - 1):
        x = (bins[i] + bins[i + 1]) / 2
        avgs_x.append(x)


    # calculate RMS
    errors = []
    for i in binned_data:
        y_list = binned_data[i]
        error_num = 0
        error_n = len(y_list)

        for y in y_list:
            error_num += abs(y - avgs[i]) ** 2

        error = math.sqrt(error_num / error_n)
        errors.append(error)


    # calculate relative RMS
    relative_rms = []
    for i in range(len(bins) - 1):
        relative_rms.append(errors[i] / avgs[i])


    return avgs_x, avgs, errors, relative_rms


def calculate_centroid(segments):
    import numpy as np
    
    uw_num = 0
    uw_denom = 0
    w_num = 0
    w_denom = 0
    for seg in segments:
        seg_E = seg.GetEnergyDeposit()
        seg_x = seg.GetStart().X()
        seg_y = seg.GetStart().Y()
        seg_z = seg.GetStart().Z()
        position = np.array([seg_x, seg_y, seg_z])

        uw_num += position
        uw_denom += 1
        w_num += position * seg_E
        w_denom += seg_E
        
    uw_centroid = uw_num / uw_denom
    w_centroid = w_num / w_denom
    
    return uw_centroid, w_centroid

def calculate_rms(segments, avg, weight):
    import numpy as np
    import math

    num = 0
    denom = 0
    for seg in segments:
        seg_E = seg.GetEnergyDeposit()
        seg_x = seg.GetStart().X()
        seg_y = seg.GetStart().Y()
        seg_z = seg.GetStart().Z()
        position = np.array([seg_x, seg_y, seg_z])
        diff = position - avg

        
        if weight == 'uw':
            num += np.dot(diff, diff)
            denom += 1
            

        elif weight == 'w':
            num += np.dot(diff, diff) * seg_E
            denom += seg_E
        
    rms = math.sqrt(num / denom)
    return rms
    
