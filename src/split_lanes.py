import argparse

parser = argparse.ArgumentParser(description='Splits .tsv files by lane number.')

parser.add_argument('filename')
parser.add_argument('-l', '--lanes', type=int, nargs=1, default=[2])
    
args = parser.parse_args()

# filename_without_extension = args.filename.split('.')[0]
f_in = open(f'{args.filename}', "r")

files_out = [open(f'output_files/sg_lane{lane + 1}.tsv', "w+") for lane in range(args.lanes[0])]

headers = f_in.readline().upper().strip()
LANE_IDX = headers.split('\t').index('LANE')

for f in files_out:
    f.seek(0)
    f.write(headers + '\n')

lines = f_in.readlines()
for line in lines:
    lane = int(line.split('\t')[LANE_IDX])
    
    files_out[lane - 1].write(line)
        
for f in files_out:
    f.truncate()
    f.close()

f_in.close()
