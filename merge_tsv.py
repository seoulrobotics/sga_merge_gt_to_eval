import argparse
import re
from datetime import datetime

def hasLine(lines, count):
    return count < len(lines)

parser = argparse.ArgumentParser(description='Script for merging .tsv files.')

parser.add_argument('filename1', required=True)
parser.add_argument('filename2', required=True)
parser.add_argument('filename3', required=True)

args = parser.parse_args()

at_f = open(f'{args.filename1}', "r")
gt_f = open(f'{args.filename2}', "r")
ra_f = open(f'{args.filename3}', "r")

# Skip header rows
gt_f.readline()
ra_f.readline()

at = at_f.readlines()
gt = gt_f.readlines()
ra = ra_f.readlines()

c_at, c_gt, c_ra = 0, 0, 0

out_f = open("merged.tsv", "a")
out_f.write("date\ttime\tlane\tspeed\tlength\t\tdate\ttime\t\tlane\tspeed\tclass\t\ttime\tlane\tspeed\n")

at_hasLine = hasLine(at, c_at)
gt_hasLine = hasLine(gt, c_gt)
ra_hasLine = hasLine(ra, c_ra)

# i = 0
while (at_hasLine or gt_hasLine or ra_hasLine):
    res = ''
    x_time = y_time = z_time = float('inf')

    if at_hasLine:
        x_cols = re.split(r'\t+', at[c_at])
        x_time = int(re.split('\.', x_cols[1])[0])
        x_lane = int(x_cols[2])
    
    if gt_hasLine:
        y_cols = re.split(r'\t+', gt[c_gt])
        y_time = int(y_cols[1].replace(':', ''))
        y_lane = int(y_cols[3])

    if ra_hasLine:
        z_cols = re.split(r'\t+', ra[c_ra])
        z_time = re.split('T|\+', z_cols[0])[1].replace(':', '')
        z_time = int(re.split('\.', z_time)[0])
        z_lane = int(z_cols[1])

    minTime, minLane = min(
        (x_time, x_lane),
        (y_time, y_lane),
        (z_time, z_lane)
    )
    
    if (at_hasLine and
        x_time - minTime <= 1 and
        x_lane == minLane):
        res += at[c_at].replace('\n', '')
        c_at += 1
    else:
        res += '\t' * 6
    
    if (gt_hasLine and
        y_time - minTime <= 1 and
        y_lane == minLane):
        res += gt[c_gt].replace('\n', '\t\t')
        c_gt += 1
    else:
        res += '\t' * 7
    
    if (ra_hasLine and
        z_time - minTime <= 1 and
        z_lane == minLane):
        res += ra[c_ra]
        c_ra += 1
    else:
        res += '\n'

    at_hasLine = hasLine(at, c_at)
    gt_hasLine = hasLine(gt, c_gt)
    ra_hasLine = hasLine(ra, c_ra)

    # i += 1
    out_f.write(res)

out_f.close()
at_f.close()
gt_f.close()
ra_f.close()
