import re
from datetime import datetime

def hasLine(lines, count):
    return count < len(lines)

at_f = open("result_with_offset_lane2.tsv", "r")
gt_f = open("gt_lane2.tsv", "r")
radar_f = open("radar_lane2.tsv", "r")

at = at_f.readlines()
gt = gt_f.readlines()
ra = radar_f.readlines()

c_at, c_gt, c_ra = 0, 0, 0

out_f = open("lane2_2712.tsv", "a")
out_f.write("date\ttime\tlane\tspeed\tlength\t\tdate\ttime\t\tlane\tspeed\tclass\t\ttime\tlane\tspeed\n")

# i = 0
while (hasLine(at, c_at) or hasLine(gt, c_gt) or hasLine(ra, c_ra)):
    x = y = z = float('inf')

    if hasLine(at, c_at):
        x = re.split(r'\t+', at[c_at])[1]
        x = int(re.split('\.', x)[0])
    
    if hasLine(gt, c_gt):
        y = re.split(r'\t+', gt[c_gt])[1]
        y = int(y.replace(':', ''))

    if hasLine(ra, c_ra):
        z = re.split(r'\t+', ra[c_ra])[0]
        z = re.split('T|\+', z)[1].replace(':', '')
        z = int(re.split('\.', z)[0])

    res = ''
    minTime = min(x, y, z)
    
    if hasLine(at, c_at) and x - minTime <= 1:
        res += at[c_at].replace('\n', '\t\t')
        c_at += 1
    else:
        res += '\t' * 6
    
    if hasLine(gt, c_gt) and y - minTime <= 1:
        res += gt[c_gt].replace('\n', '\t\t')
        c_gt += 1
    else:
        res += '\t' * 7
    
    if hasLine(ra, c_ra) and z - minTime <= 1:
        res += ra[c_ra]
        c_ra += 1
    else:
        res += '\n'

    out_f.write(res)

out_f.close()
at_f.close()
gt_f.close()
radar_f.close()

### Split files ###
# at_1 = open("at_1.tsv", "a")
# at_2 = open("at_2.tsv", "a")
# for line in at:
#     if re.split(r'\t+', line)[2] == '1':
#         at_1.write(line)
#     else:
#         at_2.write(line)
# at_1.close()
# at_2.close()

# gt_1 = open("gt_1.tsv", "a")
# gt_2 = open("gt_2.tsv", "a")
# for line in gt:
#     if re.split(r'\t+', line)[3] == '1':
#         gt_1.write(line)
#     else:
#         gt_2.write(line)
# gt_1.close()
# gt_2.close()

# radar_1 = open("radar_1.tsv", "a")
# radar_2 = open("radar_2.tsv", "a")
# for line in radar:
#     if re.split(r'\t+', line)[1] == '1':
#         radar_1.write(line)
#     else:
#         radar_2.write(line)
# radar_1.close()
# radar_2.close()
