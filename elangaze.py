
import os, json
from pympi import Eaf
import pandas as pd

class PupilRecording:
    def __init__(self, path, fixations, startTime, endTime):
        self.path = path
        self.startTime = startTime
        self.endTime = endTime
        self.fixations = self.selectFixations(fixations,startTime,endTime)

    def getEaf(self,template='template2.etf'):
        eaf = Eaf(template)
        eaf.add_linked_file(self.path,mimetype='video/mp4')
        for i, row in self.fixations.iterrows():
            eaf.add_annotation('Fixations', round((row['start timestamp [ns]']-self.startTime)/1000000), round((row['end timestamp [ns]']-self.startTime)/1000000), str(row['fixation id']))
        return eaf

    def selectFixations(self,fixations,startTime,endTime):
        fixations = pd.read_csv(fixations)
        return fixations[(fixations['start timestamp [ns]'] > startTime) & (fixations['end timestamp [ns]'] < endTime)]

    def selectGazeData(self,gazeData,startTime,endTime):
        gazeData = pd.read_csv(gazeData)
        ts = gazeData['timestamp [ns]']
        return gazeData[(ts > startTime) & (ts < endTime)]

    @classmethod
    def loadRecordings(cls,enritchmentFolder,rawDataFolder):
        sections = pd.read_csv(os.path.join(enritchmentFolder,'sections.csv'))

        for i, row in sections.iterrows():
            print(row)
            print('----')
            
            recording = cls.findSection(enritchmentFolder,row['section id'])
            rawRecording = cls.findRecording(rawDataFolder,row['recording id'])
            if recording and rawRecording:
                yield cls(recording,os.path.join(rawRecording,'fixations.csv'),row['section start time [ns]'],row['section end time [ns]'])
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



if __name__ == '__main__':
    for r in PupilRecording.loadRecordings('exampleData/VCC_Bumper_GAZE-OVERLAY_F3','exampleData/raw-data-export'):
        print(r.path)
        eaf = r.getEaf()
        eaf.to_file(r.path.replace('.mp4','.eaf'))

