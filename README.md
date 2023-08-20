# ElanGaze
A Python library for automatic generation of [ELAN](https://archive.mpi.nl/tla/elan) (eaf) video annotation files from eye-tracking data collected with the [Pupil Labs](https://pupil-labs.com/) eye tracking glasses. The library generates annotations for fixations and sacades for further processing in ELAN. 

## Requirements

Install ELANgaze dependencies:

    pip install -r requirements.txt

## Data preparation

Sign in to your [Pupil Cloud](https://cloud.pupil-labs.com) account and create a project for the recordings you want to analyze.

### Data selection

If you have made your recordings by manually starting and stopping, you typically want to select parts of the recorded video for further analysis. This can be done directly in PupilCloud by placing *events* at the suitable start and stop times. Name the events something like *X-start* and *X-stop* where X is a label for the corresponding section. By placing several *X-start* and *X-stop* pairs in a single video, you may indicate several shorter sections that you want to analyze separately, in individual ELAN files. 

### Gaze overlay

Now create a gaze overlay by selecting the *Analysis* tab in the left menu of PupilCloud, click *New visualization* and select *Video Renderer*. Select the options you prefer, expand the *Advanced* section, and select the suitable start and stop events you created during *Data selection*. Now click *Run* and let the recordings process. 

If you used events with several different labels, you'll need to create one visualization for each label. PupilCloud will however analyze all videos in the project with the specified label, so no need to repeat this for each recording. 

### Download the data

Once the visualization processing is finished, download the gaze overlay data and extract into a folder of your choice. This will be your *gaze overlay* folder. Note that you may pass several gaze overlay folders to ELANgaze for joint processing. 

Unfortunately, the gaze overlay export does not comprise the actual gaze data, so we will also need the raw gaze data from PupilCloud. Select the *Downloads* tab in the left menu and download the *Raw data export*.

### Prepare a template

Now prepare a ELAN template (etf) file with the tiers and options you need. Note that this file must comprise a tier named *Fixations*, this is where the exported fixation data will be placed. 

## Usage

    python elangaze.py path/to/gaze-overlay-folder --raw=path/to/raw-gaze-data --template=path/to/my/template 

This will generate one ELAN (eaf) file for each recording in the specified gaze overlay folder. Each fixation is indicated as an annotation on the *Fixations* tier, with its corresponding index. Happy analysis!  

For more details and options are available in the help section: 

    python elangaze.py --help

## License

**Copyright (C) 2023  Erik Billing, erik.billing@his.se**

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.