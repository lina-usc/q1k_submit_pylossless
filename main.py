import pylossless as ll
import mne
import mne_bids
import sys
from os.path import exists
import re

project_path = sys.argv[1] # '/project/def-emayada/q1k/pilot/q1k-external-pilot/'
subject_id = sys.argv[2] # '012'
session_id = sys.argv[3] # '01'
task_id = sys.argv[4] # 'ssaep'
run_id = sys.argv[5] # 1
out_path = sys.argv[6] # '/project/def-emayada/q1k/pilot/q1k-external-pilot/derivatives/pylossless/


bids_path = mne_bids.BIDSPath(
    subject=subject_id, session=session_id, task=task_id, run=run_id, datatype="eeg", root=project_path
)

print('running on: ', subject_id)
#if not exists(subject_file):
#	raise ValueError('File not found.')
#print('Starting MNE on subject: ', subject_id)

raw = mne_bids.read_raw_bids(bids_path=bids_path)
raw.load_data()

# Select EEG-only channels
#eeg_only_raw = raw.copy().pick_types(eeg=True)


#raw = mne.io.read_raw_edf(bids_path)

# Get chan type mapping
#types = {"eyegaze": ["xpos_left", "ypos_left", "xpos_right", "ypos_right"],
#         "pupil": ["pupil_left", "pupil_right"],
#         "misc": ["x_head", "y_head", "distance"]}
#chan_type_map = {ch_name: "eeg" for ch_name in raw.ch_names if ch_name[0] == "E"}
#chan_type_map["VREF"] = "eeg"
#for type_, ch_names in types.items():
#    for ch_name in ch_names:
#        if ch_name in raw.ch_names:
#            chan_type_map[ch_name] = type_
#chan_type_map.update({ch_name: "stim" for ch_name in raw.ch_names if ch_name not in chan_type_map})

#raw.set_channel_types(chan_type_map)

# Allow breaks to be detected from events
# annos = mne.annotations_from_events(events=mne.find_events(raw, initial_event=True), sfreq=raw.info['sfreq'], orig_time=raw.info['meas_date'],shortest_event=1)
# raw.set_annotations(annos)

# Mark out EOG channels
eog_chans = ['E125', 'E126', 'E127', 'E128']
raw.info['bads'].extend(eog_chans)
#raw.set_montage('biosemi64', on_missing='ignore')
#mapper = {item:'eog' for item in eog_chans}
#raw.set_channel_types(mapper)



# Execute only on EEG and EOG channels
config = ll.config.Config()
config.load_default()
pipeline = ll.LosslessPipeline(config=config)
#pipeline = ll.LosslessPipeline('q1k_pyll_config.yaml')
pipeline.run_with_raw(raw)

# Stdout
# print(pipeline.flagged_chs)
# print(pipeline.flagged_epochs)

# Save
bids_path = mne_bids.BIDSPath(subject=subject_id, session=session_id, task=task_id, run=run_id, suffix='eeg', extension='.edf', datatype='eeg', root=out_path)
pipeline.save(pipeline.get_derivative_path(bids_path),overwrite=True)

