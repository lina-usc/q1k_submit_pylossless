import pylossless as ll
import mne
import mne_bids
import sys
from os.path import exists
import re

project_path = sys.argv[1] # '/scratch/jdesjard/q1k/pilot/q1k-external-pilot/'
subject_id = sys.argv[2] # '012'
session_id = sys.argv[3] # '01'
task_id = sys.argv[4] # 'ssaep'
out_path = sys.argv[5] # '/scratch/jdesjard/q1k/pilot/q1k-external-pilot/derivatives/pylossless/


bids_path = mne_bids.BIDSPath(
    subject=subject_id, session=session_id, task=task_id, run="1", datatype="eeg", root=project_path
)

print('running on: ', subject_id)
#if not exists(subject_file):
#	raise ValueError('File not found.')
#print('Starting MNE on subject: ', subject_id)

raw = mne_bids.read_raw_bids(bids_path=bids_path)
raw.load_data()

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
pipeline = ll.LosslessPipeline('q1k_pyll_config.yaml')
pipeline.run_with_raw(raw)

# Stdout
# print(pipeline.flagged_chs)
# print(pipeline.flagged_epochs)

# Save
bids_path = mne_bids.BIDSPath(subject=subject_id, session=session_id, task=task_id, suffix='eeg', extension='.edf', datatype='eeg', root=out_path)
pipeline.save(pipeline.get_derivative_path(bids_path),overwrite=True)
