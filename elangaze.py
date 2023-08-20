"""ELANgaze - Extraction of PupilLabs gaze data into ELAN (eaf) annotation files. 

See README.md for usage.

Copyright (C) 2023  Erik Billing, erik.billing@his.se

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""


import os, json
from pympi import Eaf
import pandas as pd
import argparse

class PupilRecording:
    def __init__(self, path, fixations, startTime, endTime, participant, label):
        self.path = path
        self.startTime = startTime
        self.endTime = endTime
        self.participant = participant
        self.label = label
        self.fixations = self.selectFixations(fixations,startTime,endTime)

    def getEaf(self,template='templates/template.etf'):
        eaf = Eaf(template)
        eaf.add_linked_file(self.path,mimetype='video/mp4')
        for i, row in self.fixations.iterrows():
            eaf.add_annotation('Fixations', round((row['start timestamp [ns]']-self.startTime)/1000000), round((row['end timestamp [ns]']-self.startTime)/1000000), str(row['fixation id']))
        return eaf
    
    def getEafPath(self):
        parts = os.path.split(self.path)
        return '%s/P%s_%s_%s.eaf'%(parts[0],self.participant,self.label,parts[1].replace('.mp4',''))

    def selectFixations(self,fixations,startTime,endTime):
        fixations = pd.read_csv(fixations)
        return fixations[(fixations['start timestamp [ns]'] > startTime) & (fixations['end timestamp [ns]'] < endTime)]

    def selectGazeData(self,gazeData,startTime,endTime):
        gazeData = pd.read_csv(gazeData)
        ts = gazeData['timestamp [ns]']
        return gazeData[(ts > startTime) & (ts < endTime)]

    @classmethod
    def loadRecordings(cls,enritchmentFolder,rawDataFolder):
        assert os.path.isdir(enritchmentFolder)
        assert os.path.isdir(rawDataFolder)

        sections = pd.read_csv(os.path.join(enritchmentFolder,'sections.csv'))

        for i, row in sections.iterrows():
            # print(row)
            # print('----')
            
            recording = cls.findSection(enritchmentFolder,row['section id'])
            rawRecording = cls.findRecording(rawDataFolder,row['recording id'])
            if recording and rawRecording:
                yield cls(recording,os.path.join(rawRecording,'fixations.csv'),row['section start time [ns]'],row['section end time [ns]'],row['wearer name'],row['start event name'].replace('-Start',''))
            else:
                print('Unable to locate raw data for section', row['section id'])
            
    @classmethod
    def findRecording(cls,path,recordingId):
        for root, dirs, files in os.walk(path):
            if os.path.exists(os.path.join(root,'info.json')):
                info = json.load(open(os.path.join(root,'info.json')))
                if info["recording_id"] == recordingId:
                    return root

    @classmethod
    def findSection(cls,path,sectionId):
        """Returns the folder path to the recording with specified section id"""
        sectionParts = sectionId.split('-')
        for root, dirs, files in os.walk(path):
            for f in files:
                fParts = f.split('_')
                if f.endswith('.mp4') and fParts[0] == sectionParts[0]:
                    return os.path.join(root,f)


def main():
    parser = argparse.ArgumentParser(
                    prog='ELANgaze',
                    description='Extraction of PupilLabs gaze data into ELAN (eaf) annotation files',
                    epilog='See README.md for usage.')
    parser.add_argument('overlay', nargs='+',help='gaze overlay data folder to be processed')
    parser.add_argument('--raw',default='data/raw-data-export',help='raw gaze data folder')
    parser.add_argument('--template',default='templates/template.etf',help='ELAN template file to be used')

    args = parser.parse_args()    
    for overlay in args.overlay:
        for r in PupilRecording.loadRecordings(overlay,args.raw):
            print('Analyzing',r.path,'...')
            eaf = r.getEaf(args.template)
            eaf.to_file(r.getEafPath())
            print('ELAN annotations saved to',r.getEafPath())

if __name__ == '__main__':
    main()