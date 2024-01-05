import argparse
import re

from csv_to_tsv import csv_to_tsv

def closeFiles(files):
    for f in files:
        f.close()

def hasLine(lines, count):
    return count < len(lines)

parser = argparse.ArgumentParser(description='Script for merging .tsv files.')

parser.add_argument('file1', type=str, nargs=1)
parser.add_argument('other', type=str, nargs='+')
    
args = parser.parse_args()

# Convert input files from .csv -> .tsv if applicable
files = args.file1 + args.other
for i, f in enumerate(files):
    if '.csv' in f:
        csv_to_tsv(f)
    files[i] = open(f'{f.replace(".csv", ".tsv")}', "r")

# Keep track of files to close
# files = [files[0], files[1], files[2]]

# Extract header row information
headers = [f.readline().upper().strip() for f in files]
cols = [h.split('\t') for h in headers]
time_idxs = [c.index('TIME') for c in cols]
lane_idxs = [c.index('LANE') for c in cols]

# at_h = files[0].readline().upper().strip()
# at_cols = at_h.split('\t')
# AT_TIME_IDX = at_cols.index('TIME')
# AT_LANE_IDX = at_cols.index('LANE')

# gt_h = files[1].readline().upper().strip()
# gt_cols = gt_h.split('\t')
# GT_TIME_IDX = gt_cols.index('TIME')
# GT_LANE_IDX = gt_cols.index('LANE')

# ra_h = files[2].readline().upper().strip()
# ra_cols = ra_h.split('\t')
# RA_TIME_IDX = ra_cols.index('TIME')
# RA_LANE_IDX = ra_cols.index('LANE')

# Extract data rows
# f_data = [f.readlines() for f in files] TODO
at = files[0].readlines()
gt = files[1].readlines()
ra = files[2].readlines()

# EOF counters
eof_c = [0] * len(files)

# Output file
filename_without_extension = args.file1[0].split('.')[0]
out_f = open(f"{filename_without_extension}_merged.tsv", "a")
out_h = '\t\t'.join(headers)
out_f.write(f"{out_h}\n")
files.append(out_f)

at_hasLine = hasLine(at, eof_c[0])
gt_hasLine = hasLine(gt, eof_c[1])
ra_hasLine = hasLine(ra, eof_c[2])

while (at_hasLine or gt_hasLine or ra_hasLine):
    res = ''
    x_time = y_time = z_time = float('inf')

    # Extract timestamp and lane number of current row
    if at_hasLine:
        AT_TIME_IDX = time_idxs[0]
        AT_LANE_IDX = lane_idxs[0]
        x_cols = re.split(r'\t+', at[eof_c[0]])
        x_time = x_cols[AT_TIME_IDX]            # HH:MM:SS
        x_time = int(x_time.replace(':', ''))   # HHMMSS
        x_lane = int(x_cols[AT_LANE_IDX])

    if gt_hasLine:
        GT_TIME_IDX = time_idxs[1]
        GT_LANE_IDX = lane_idxs[1]
        y_cols = re.split(r'\t+', gt[eof_c[1]])
        y_time = y_cols[GT_TIME_IDX]            # HH:MM:SS
        y_time = int(y_time.replace(':', ''))   # HHMMSS
        y_lane = int(y_cols[GT_LANE_IDX])

    if ra_hasLine:
        RA_TIME_IDX = time_idxs[2]
        RA_LANE_IDX = lane_idxs[2]
        z_cols = re.split(r'\t+', ra[eof_c[2]])
        z_time = z_cols[RA_TIME_IDX]            # yyyy-mm-ddTHH:MM:SS.f+11:00
        z_time = re.split('T|\.', z_time)[1]    # HH:MM:SS
        z_time = int(z_time.replace(':', ''))   # HHMMSS
        z_lane = int(z_cols[RA_LANE_IDX])

    # Calculate minimum timestamp, lane number
    minTime, minLane = min(
        (x_time, x_lane),
        (y_time, y_lane),
        (z_time, z_lane)
    )
    
    # Write row to output file
    if (at_hasLine and
        x_time - minTime <= 1 and
        x_lane == minLane):
        res += at[eof_c[0]].strip() + '\t\t'
        eof_c[0] += 1
    else:
        res += (len(cols[0]) + 1) * '\t'
    
    if (gt_hasLine and
        y_time - minTime <= 1 and
        y_lane == minLane):
        res += gt[eof_c[1]].strip() + '\t\t'
        eof_c[1] += 1
    else:
        res += (len(cols[1]) + 1) * '\t'
    
    if (ra_hasLine and
        z_time - minTime <= 1 and
        z_lane == minLane):
        res += ra[eof_c[2]].strip()
        eof_c[2] += 1

    at_hasLine = hasLine(at, eof_c[0])
    gt_hasLine = hasLine(gt, eof_c[1])
    ra_hasLine = hasLine(ra, eof_c[2])

    out_f.write(res + '\n')

closeFiles(files)
