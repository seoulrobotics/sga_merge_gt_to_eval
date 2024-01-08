## Scripts for quickly merging and modifying .csv/.tsv files.

### Example use case (see makefile):
1. Make sure the input file is named `sg.csv` and placed inside the `src` folder.
2. Make sure you have two folders `gt_data` and `ra_data` containing lane-separated gt and ra files.
3. Make sure that each file has non-empty column headers. Having empty column headers could result in formatting issues or other errors. Most likely, you will only need to modify or remove the last column of `sg.csv`, e.g. "DATE,TIME,LANE,SPEED,LENGTH,NUMBER_PLATE,DISTANCE_FROM_CURB,-" will suffice.
4. To run, simply modify the time offset inside the makefile and execute with `make run`. `merge_tsv.py` requires at least 2 files as arguments. If there are more than 2 lanes, please modify the -l flag of the `split_lanes.py` script. The relevant output files can be found inside the newly created `output_files` folder. The order of execution is as follows:
    - A copy of the input file is created with modified timestamps.
    - The modified copy is split into two files, separated by lane number.
    - The resulting files are both used to merge with their corresponding gt and ra files. The merged output files are by default named `sg_lane1_merged.tsv` and `sg_lane2_merged.tsv`.

If you wish to alter the filenames or paths, specify a different time offset or split more than two lanes, please modify the makefile accordingly.

### Manually adding a time offset to a file:
`python3 add_time_offset.py <filename>` can be used to arbitrarily add a datetime offset to a column, with header 'TIME', containing timestamps of the format `HHMMSS` or `HHMMSS.f`.
- Input: any .csv or .tsv file with a column named 'time' (case insensitive) containing timestamps of the format `HHMMSS` or `HHMMSS.f` (i.e. excluding ':' or any other special characters).
- Output: a .tsv file with modified timestamps.
- Flags:
    - `-h <int>` set the number of hours to modify.
    - `-m <int>` set the number of minutes to modify.
    - `-s <int>` set the number of seconds to modify.
    - `--sub` subtract instead of add.

### Utility methods:
`csv_to_tsv.py` can be used to quickly convert .csv files to .tsv format.

`split_lanes.py` is used to split the data of a single file over two separate files, by lane number.
- Flags:
    - `-f <int>` set the number of lanes.

