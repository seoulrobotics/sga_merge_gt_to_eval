Three scripts used to merge and modify .tsv files.

`merge_tsv.py` reads from three input .tsv files containing at, gt and radar data. It reformats the data and outputs a single file containing complete data of the input files, organized row-by-row, leaving entries that do not exist blank.

`csv_to_tsv.py` can be used to quickly convert .csv files to .tsv format.

`add_time_offset.py` can be used to arbitrarily add a datetime offset to a column containing datetime timestamps.
