## Scripts for quickly merging and modifying .csv/.tsv files.

### How to use:
1. Make sure the input file is named `sg.csv`.
2. Make sure you have two folders `gt_data` and `ra_data` containing lane-separated gt and ra files.
3. Make sure that each file has non-empty column headers. Having empty column headers could result in formatting issues or other errors. Most likely, you will only need to modify or remove the last column of `sg.csv`, e.g. "DATE,TIME,LANE,SPEED,LENGTH,NUMBER_PLATE,DISTANCE_FROM_CURB,-" will suffice.

If you wish to customize any of the above, please modify the makefile and the relevant scripts.

To run, simply modify the time offset inside the makefile and execute with `make run`. The relevant output files can be found inside the newly created `output_files` folder. The order of execution is as follows:
1. A copy of the input file is created with modified timestamps.
2. The modified copy is split into two files, separated by lane number.
3. The resulting files are both used to merge with their corresponding gt and ra files. The merged output files are by default named `sg_lane1_merged.tsv` and `sg_lane2_merged.tsv`.

### Manually adding a time offset to a file:
`python3 add_time_offset.py <filename>` can be used to arbitrarily add a datetime offset to a column containing datetime timestamps.
- Input: any .csv or .tsv file with a column named 'time' (case insensitive) containing DateTime formatted timestamps.
- Output: a .tsv file with modified timestamps.
- Flags:
    - `-h <int>` to set the number of hours to modify.
    - `-m <int>` to set the number of minutes to modify.
    - `-s <int>` to set the number of seconds to modify.
    - `--sub` to subtract instead of add.

### Utility methods:
- `csv_to_tsv.py` can be used to quickly convert .csv files to .tsv format.
- `split_lanes.py` is used to split the data of a single file over two separate files, by lane number.
