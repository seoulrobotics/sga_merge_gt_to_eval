## Scripts for quickly merging and modifying .csv/.tsv files.

`python3 merge_tsv.py <filename1> <filename2> <filename3>` reads from three input .tsv files containing at, gt and radar data. It reformats the data and outputs a single file containing complete data of the input files, organized row-by-row, leaving entries that do not exist blank. It assumes that an input file has a header for each of its columns. To avoid problems during parsing, please ensure columns without a header are removed or given some arbitrary header, e.g. '-' or 'nothing'. Do not put numbers in the header row, as the script might be assume it is data to be parsed.
- Input: any three at.tsv, gt.tsv and radar.tsv files to merge, in that specific order.
- Output: a merged.tsv file, or merged_lane1.tsv and merged_lane2.tsv files if the `--split` flag is set.

`python3 add_time_offset.py <filename>` can be used to arbitrarily add a datetime offset to a column containing datetime timestamps.
- Input: any .csv or .tsv file with a column named 'time' (case insensitive) containing DateTime formatted timestamps.
- Output: a .tsv file with modified timestamps.
- Flags:
    - `-h <int>` to set the number of hours to modify.
    - `-m <int>` to set the number of minutes to modify.
    - `-s <int>` to set the number of seconds to modify.
    - `--sub` to subtract instead of add.

The `utils` folder contains optional utility functions.
- `csv_to_tsv.py` can be used to quickly convert .csv files to .tsv format. It is automatically called when a .csv file is given as parameter argument to the `merge_tsv.py` and `add_time_offset.py` scripts.
