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
parser.add_argument('--split', action='store_true')
    
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

files = [at_f, gt_f, ra_f]

# Extract header rows
at_h = at_f.readline().upper().strip()
at_cols = at_h.count('\t')
gt_h = gt_f.readline().upper().strip()
gt_cols = gt_h.count('\t')
ra_h = ra_f.readline().upper().strip()
# ra_cols = ra_h.count('\t')

# Extract data rows
at = at_f.readlines()
gt = gt_f.readlines()
ra = ra_f.readlines()

# EOF counters
c_at, c_gt, c_ra = 0, 0, 0

# Output file
out_filename = "sensys_gatso"
if args.split:
    out_f1 = open(f"{out_filename}_merged_lane1.tsv", "a")
    out_f1.write(f"{at_h}\t\t{gt_h}\t\t{ra_h}\n")
    out_f2 = open(f"{out_filename}_merged_lane2.tsv", "a")
    out_f2.write(f"{at_h}\t\t{gt_h}\t\t{ra_h}\n")
    files.append(out_f1)
    files.append(out_f2)
else:
    out_f = open(f"{out_filename}_merged.tsv", "a")
    out_f.write(f"{at_h}\t\t{gt_h}\t\t{ra_h}\n")
    files.append(out_f)

at_hasLine = hasLine(at, c_at)
gt_hasLine = hasLine(gt, c_gt)
ra_hasLine = hasLine(ra, c_ra)

while (at_hasLine or gt_hasLine or ra_hasLine):
    res = ''
    x_time = y_time = z_time = float('inf')

    if at_hasLine:
        x_cols = re.split(r'\t+', at[c_at])
        x_time = int(re.split('\.', x_cols[1])[0])
        x_lane = int(x_cols[2])

    if gt_hasLine:
        y_cols = re.split(r'\t+', gt[c_gt])
        y_time = int(re.sub("[^0-9]", "", y_cols[1].replace(':', '')))
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
        res += at[c_at].strip() + '\t\t'
        c_at += 1
    else:
        res += (at_cols + 2) * '\t'
    
    if (gt_hasLine and
        y_time - minTime <= 1 and
        y_lane == minLane):
        res += gt[c_gt].strip() + '\t\t'
        c_gt += 1
    else:
        res += (gt_cols + 2) * '\t'
    
    if (ra_hasLine and
        z_time - minTime <= 1 and
        z_lane == minLane):
        res += ra[c_ra].strip() + '\n'
        c_ra += 1
    else:
        res += '\n'

    at_hasLine = hasLine(at, c_at)
    gt_hasLine = hasLine(gt, c_gt)
    ra_hasLine = hasLine(ra, c_ra)

    if args.split:
        if minLane == 1:
            out_f1.write(res)
        elif minLane == 2:
            out_f2.write(res)
    else:
        out_f.write(res)

closeFiles(files)
