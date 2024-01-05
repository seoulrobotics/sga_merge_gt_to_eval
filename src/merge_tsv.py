import argparse
import re

from csv_to_tsv import csv_to_tsv

def closeFiles(files):
    for f in files:
        f.close()

def hasLine(lines, count):
    return count < len(lines)

parser = argparse.ArgumentParser(description='Script for merging .tsv files.')

parser.add_argument('filename1')
parser.add_argument('filename2')
parser.add_argument('filename3')
    
args = parser.parse_args()

# Convert input files from .csv -> .tsv if applicable
files = [args.filename1, args.filename2, args.filename3]
for i, f in enumerate(files):
    if '.csv' in f:
        csv_to_tsv(f)
        files[i] = files[i].replace(".csv", ".tsv")

at_f = open(f'{files[0]}', "r")
gt_f = open(f'{files[1]}', "r")
ra_f = open(f'{files[2]}', "r")

# Keep track of files to close
files = [at_f, gt_f, ra_f]

# Extract header row information
at_h = at_f.readline().upper().strip()
at_cols = at_h.split('\t')
AT_TIME_IDX = at_cols.index('TIME')
AT_LANE_IDX = at_cols.index('LANE')
gt_h = gt_f.readline().upper().strip()
gt_cols = gt_h.split('\t')
GT_TIME_IDX = gt_cols.index('TIME')
GT_LANE_IDX = gt_cols.index('LANE')
ra_h = ra_f.readline().upper().strip()
ra_cols = ra_h.split('\t')
RA_TIME_IDX = ra_cols.index('TIME')
RA_LANE_IDX = ra_cols.index('LANE')

# Extract data rows
at = at_f.readlines()
gt = gt_f.readlines()
ra = ra_f.readlines()

# EOF counters
c_at, c_gt, c_ra = 0, 0, 0

# Output file
filename_without_extension = args.filename1.split('.')[0]
out_f = open(f"{filename_without_extension}_merged.tsv", "a")
# out_f.write(f"{at_h}\t\t{gt_h}\t\t{ra_h}\n")
out_f.write(f"{at_h}\t\t{ra_h}\n")
files.append(out_f)

at_hasLine = hasLine(at, c_at)
# gt_hasLine = hasLine(gt, c_gt)
gt_hasLine = False
ra_hasLine = hasLine(ra, c_ra)

while (at_hasLine or gt_hasLine or ra_hasLine):
    res = ''
    x_time = y_time = z_time = float('inf')

    # Extract timestamp and lane number of current row
    if at_hasLine:
        x_cols = re.split(r'\t+', at[c_at])
        x_time = x_cols[AT_TIME_IDX]            # HH:MM:SS
        x_time = int(x_time.replace(':', ''))   # HHMMSS
        x_lane = int(x_cols[AT_LANE_IDX])

    if gt_hasLine:
        y_cols = re.split(r'\t+', gt[c_gt])
        y_time = y_cols[GT_TIME_IDX]            # HH:MM:SS
        y_time = int(y_time.replace(':', ''))   # HHMMSS
        y_lane = int(y_cols[GT_LANE_IDX])

    if ra_hasLine:
        z_cols = re.split(r'\t+', ra[c_ra])
        z_time = z_cols[RA_TIME_IDX]            # yyyy-mm-ddTHH:MM:SS.f+11:00
        z_time = re.split('T|\.', z_time)[1]    # HH:MM:SS
        z_time = int(z_time.replace(':', ''))   # HHMMSS
        z_lane = int(z_cols[RA_LANE_IDX])

    # Calculate minimum timestamp, lane number
    minTime, minLane = min(
        (x_time, x_lane),
        # (y_time, y_lane),
        (z_time, z_lane)
    )
    
    # Write row to output file
    if (at_hasLine and
        x_time - minTime <= 1 and
        x_lane == minLane):
        res += at[c_at].strip() + '\t\t'
        c_at += 1
    else:
        res += (len(at_cols) + 1) * '\t'
    
    # if (gt_hasLine and
    #     y_time - minTime <= 1 and
    #     y_lane == minLane):
    #     res += gt[c_gt].strip() + '\t\t'
    #     c_gt += 1
    # else:
    #     res += (len(gt_cols) + 1) * '\t'
    
    if (ra_hasLine and
        z_time - minTime <= 1 and
        z_lane == minLane):
        res += ra[c_ra].strip()
        c_ra += 1

    at_hasLine = hasLine(at, c_at)
    # gt_hasLine = hasLine(gt, c_gt)
    gt_hasLine = False
    ra_hasLine = hasLine(ra, c_ra)

    out_f.write(res + '\n')

closeFiles(files)
