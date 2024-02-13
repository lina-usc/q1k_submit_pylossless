## Load required modules
module load python/3.10

## navigate to the pylossless derivative directory
cd /project/def-emayada/q1k/pilot/q1k-external-pilot/derivatives/pylossless/code

## Download the repo
git clone https://github.com/lina-usc/q1k_submit_pylossless.com

## Navigate into the repo dirctory and install the tools
cd q1k_submit_pylossless

virtualenv --no-download env
source eeg-env/bin/activate

pip install --no-index mne
pip install --no-index pandas
pip install --no-index xarray
pip install --no-index pyyaml
pip install --no-index sklearn
pip install --no-index EDFlib
pip install --no-index openneuro-py
pip install --no-index mne_bids

# Clone down mne-iclabel and switch to the right version and install it locally
git clone https://github.com/mne-tools/mne-icalabel.git
cd mne-icalabel
git checkout maint/0.4
pip install .
cd ..

# Clone down pipeline and install without reading dependencies
git clone git@github.com:lina-usc/pylossless.git
cd pylossless
pip install --no-deps .
cd ..

