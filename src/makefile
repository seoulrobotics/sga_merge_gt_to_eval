run:
	python3 add_time_offset.py sg.csv -h 9 -m 54 -s 32 --sub
	python3 split_lanes.py output_files/sg_offset.tsv
	python3 merge_tsv.py output_files/sg_lane1.tsv gt_data/gt_lane1.tsv ra_data/radar_lane1.tsv
	python3 merge_tsv.py output_files/sg_lane2.tsv gt_data/gt_lane2.tsv ra_data/radar_lane2.tsv
