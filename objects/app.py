import numpy as np
from copy import deepcopy
from modules.notification import notification

class App(object):

    def __init__(self):
        self.activeProject = None
        self.activeSubject = None
        self.activeTest = None
        self.activeMode = None
        self.projects = []
        self.settings = None

        self.sidePanel = None
        self.sidepanel_projectList = None
        self.sidepanel_subjectList = None
        self.sidepanel_testList = None

        self.detailsPanel = None
        self.projectDetailModule = None
        self.testDetailModule = None
        self.envDetailModule = None
        self.plottingPanel = None
        self.menu = None

        self.root = None
        self.strVars = None
        self.intVars = None

    def setActiveTest(self, test):
        self.activeTest = test

    def getActiveTest(self):
        return self.activeTest

    def setActiveSubject(self, subject):
        self.activeSubject = subject

    def getActiveSubject(self):
        return self.activeSubject

    def setActiveProject(self, project):
        self.activeProject = project

    def getActiveProject(self):
        return self.activeProject
    
    def addProject(self, project):
        self.projects.append(project)

    def getActiveMode(self):
        return self.activeMode

    def setActiveMode(self, mode):
        self.activeMode = mode

    def getPlottingPanel(self):
        return self.plottingPanel

    def getProjects(self):
        return self.projects

    def getMaxMinAvg(self, plotProject=False, subjects=None):
        if plotProject == True:
            activeProject = app.getActiveProject()
            subjects = activeProject.getSubjects()

        self.vo2List = []
        self.hrList = []
        self.svList = []
        self.qList = []
        self.hbList = []
        self.sao2List = []
        self.do2List = []
        self.qao2List = []
        self.cao2List = []
        self.svo2List = []
        self.cvo2List = []
        self.cavo2List = []
        self.pvo2List = []
        
        for s in subjects:
            tests = s.getTests()

            for t in tests:
                # details = t.getMaxLoad()
                wOrig = t.getWorkLoads()[-1] # Last workload object
                w = deepcopy(wOrig)
                details = w.getDetails().getWorkLoadDetails()

                validValues = app.getPlottingPanel().calc(w, details)
                if validValues == False:
                    notification.create('error', f"Couldn't calculate project metrics. Check values of subject: {s.id} test: {t.id}", '5000')
                details = w.getDetails().getWorkLoadDetails()

                self.vo2List.append(float(details['VO2']))
                self.hrList.append(float(details['HR']))
                self.svList.append(float(details['Sv']))
                self.qList.append(float(details['Q']))
                self.hbList.append(float(details['Hb']))
                self.sao2List.append(float(details['SaO2']))

                self.cao2List.append(float(details['CaO2']))
                self.svo2List.append(float(details['SvO2']))
                self.cvo2List.append(float(details['CvO2']))
                self.cavo2List.append(float(details['CavO2']))
                self.pvo2List.append(float(details['PvO2']))
                self.do2List.append(float(details['DO2']))
                self.qao2List.append(float(details['QaO2']))
    
        # self.avgVO2 = np.median(self.vo2List)
        self.VO2q75, self.VO2q50, self.VO2q25 = np.percentile(self.vo2List, [75, 50, 25])
        # self.avgHR = np.median(self.hrList)
        self.HRq75, self.HRq50, self.HRq25 = np.percentile(self.hrList, [75, 50, 25])
        # self.avgSv= np.median(self.svList)
        self.SVq75, self.SVq50, self.SVq25 = np.percentile(self.svList, [75, 50, 25])
        # self.avgQ = np.median(self.qList)
        self.Qq75, self.Qq50, self.Qq25 = np.percentile(self.qList, [75, 50, 25])
        # self.avgHb = np.median(self.hbList)
        self.HBq75, self.HBq50, self.HBq25 = np.percentile(self.hbList, [75, 50, 25])
        # self.avgSaO2 = np.median(self.sao2List)
        self.SAO2q75, self.SAO2q50, self.SAO2q25 = np.percentile(self.sao2List, [75, 50, 25])
        # self.avgDO2 = np.median(self.do2List)
        self.DO2q75, self.DO2q50, self.DO2q25 = np.percentile(self.do2List, [75, 50, 25])
        # self.avgQaO2 = np.median(self.qao2List)
        self.QAO2q75, self.QAO2q50, self.QAO2q25 = np.percentile(self.qao2List, [75, 50, 25])
        # self.avgCaO2 = np.median(self.cao2List)
        self.CAO2q75, self.CAO2q50, self.CAO2q25 = np.percentile(self.cao2List, [75, 50, 25])
        # self.avgSvO2 = np.median(self.svo2List)
        self.SVO2q75, self.SVO2q50, self.SVO2q25 = np.percentile(self.svo2List, [75, 50, 25])
        # self.avgCvO2 = np.median(self.cvo2List)
        self.CVO2q75, self.CVO2q50, self.CVO2q25 = np.percentile(self.cvo2List, [75, 50, 25])
        # self.avgCavO2 = np.median(self.cavo2List)
        self.CAVO2q75, self.CAVO2q50, self.CAVO2q25 = np.percentile(self.cavo2List, [75, 50, 25])
        # self.avgPvO2 = np.median(self.pvo2List)
        self.PVO2q75, self.PVO2q50, self.PVO2q25 = np.percentile(self.pvo2List, [75, 50, 25])

        self.HRstd = np.std(self.hrList)
        self.SVstd = np.std(self.svList)
        self.Qstd = np.std(self.qList)
        self.HBstd = np.std(self.hbList)
        self.SAO2std = np.std(self.sao2List)

        if plotProject == True:
            activeProject.VO2max = max(self.vo2List)
            activeProject.VO2min = min(self.vo2List)
            activeProject.VO2mean = self.VO2q50

            activeProject.DO2max = max(self.do2List)
            activeProject.DO2min = min(self.do2List)
            activeProject.DO2mean = self.DO2q50

            activeProject.QaO2max = max(self.qao2List)
            activeProject.QaO2min = min(self.qao2List)
            activeProject.QaO2mean = self.QAO2q50
        self.VO2std = np.std(self.vo2List)
        # print(f'SD VO2: {self.VO2std}')
        self.DO2std = np.std(self.do2List)
        # print(f'SD DO2: {np.std(self.do2List)}')
        self.QAO2std = np.std(self.qao2List)
        # print(f'SD QaO2: {np.std(self.qao2List)}')
        self.CAO2std = np.std(self.cao2List)
        # print(f'SD CaO2: {np.std(self.cao2List)}')
        self.SVO2std = np.std(self.svo2List)
        # print(f'SD SvO2: {np.std(self.svo2List)}')
        self.CVO2std = np.std(self.cvo2List)
        # print(f'SD CvO2: {np.std(self.cvo2List)}')
        self.CAVO2std = np.std(self.cavo2List)
        # print(f'SD CavO2: {np.std(self.cavo2List)}')
        self.PVO2std = np.std(self.pvo2List)
        # print(f'SD PvO2: {np.std(self.pvo2List)}')

        # self.QAO2q75, self.QAO2q50, self.QAO2q25 = np.percentile(self.qao2List, [75, 50, 25])
        # self.QAO2iqr = self.QAO2q75 - self.QAO2q25

        # print(f'q75: {self.QAO2q75}, q50: {self.QAO2q50} q25: {self.QAO2q25}, iqr {self.QAO2iqr}')

        if plotProject == True:
            self.projectDetailModule.refreshDetails()

    def plotMean(self, test=None, plotProject=False, subjects=None, iqr=False):
        self.meanTestObject = test

        if plotProject == True:
            if iqr == False:
                self.meanTestObject.setId('Project mean/SD')
            else:
                self.meanTestObject.setId('Project mean/IQR')
        else:
            if len(subjects) > 1:
                self.meanTestObject.setId('Subjects mean')
            else:
                self.meanTestObject.setId(f'{subjects[0].id} mean')

        self.minLoad = self.meanTestObject.getWorkLoads()[0]
        if iqr == False:
            self.minLoad.setName('-1 SD')
            self.avgLoad = self.meanTestObject.createLoad()
            self.avgLoad.setName('Mean')
            self.maxLoad = self.meanTestObject.createLoad()
            self.maxLoad.setName('+1 SD')
        else:
            self.minLoad.setName('Q1')
            self.avgLoad = self.meanTestObject.createLoad()
            self.avgLoad.setName('Mean')
            self.maxLoad = self.meanTestObject.createLoad()
            self.maxLoad.setName('Q3')

        # project = app.getActiveProject()
        # projectTest = project.getMetricsTestObject()
        # app.setActiveTest(projectTest)
        app.setActiveTest(self.meanTestObject)

        self.getMaxMinAvg(plotProject, subjects)

        # Min load
        minLoad = self.meanTestObject.getWorkLoads()[0]
        self.setValues(minLoad, 'min', iqr)
        self.updateMC(minLoad)
        self.calcCoords(minLoad)

        # Avg load
        avgLoad = self.meanTestObject.getWorkLoads()[1]
        self.setValues(avgLoad, 'avg', iqr)
        self.updateMC(avgLoad)
        self.calcCoords(avgLoad)

        # Max load
        maxLoad = self.meanTestObject.getWorkLoads()[2]
        self.setValues(maxLoad, 'max', iqr)
        self.updateMC(maxLoad)
        self.calcCoords(maxLoad)

        app.getPlottingPanel().plotProject()

    def updateMC(self, load):
        load.getDetails().setMC('VO2_MC', 1)
        load.getDetails().setMC('HR_MC', 1)
        load.getDetails().setMC('Sv_MC', 1)
        load.getDetails().setMC('Q_MC', 1)
        load.getDetails().setMC('Hb_MC', 1)
        load.getDetails().setMC('SaO2_MC', 1)
        load.getDetails().setMC('CaO2_MC', 1)
        load.getDetails().setMC('SvO2_MC', 1)
        load.getDetails().setMC('CvO2_MC', 1)
        load.getDetails().setMC('CavO2_MC', 1)
        load.getDetails().setMC('PvO2_MC', 1)
        load.getDetails().setMC('QaO2_MC', 1)

    def setValues(self, load, mode, iqr):

        if mode == 'min':
            if iqr == False:
                load.getDetails().setValue('VO2', self.VO2q50-self.VO2std)
                load.getDetails().setValue('HR', self.HRq50-self.HRstd)
                load.getDetails().setValue('Sv', self.SVq50-self.SVstd)
                load.getDetails().setValue('Q', self.Qq50-self.Qstd)
                load.getDetails().setValue('Hb', self.HBq50-self.HBstd)
                load.getDetails().setValue('SaO2', self.SAO2q50-self.SAO2std)
                load.getDetails().setValue('CaO2', self.CAO2q50-self.CAO2std)
                load.getDetails().setValue('SvO2', self.SVO2q50-self.SVO2std)
                load.getDetails().setValue('CvO2', self.CVO2q50-self.CVO2std)
                load.getDetails().setValue('CavO2', self.CAVO2q50-self.CAVO2std)
                load.getDetails().setValue('PvO2', self.PVO2q50-self.PVO2std)
                load.getDetails().setValue('QaO2', self.QAO2q50-self.QAO2std)
                load.getDetails().setValue('DO2', self.DO2q50-self.DO2std)
            else:
                load.getDetails().setValue('VO2', self.VO2q25)
                load.getDetails().setValue('HR', self.HRq25)
                load.getDetails().setValue('Sv', self.SVq25)
                load.getDetails().setValue('Q', self.Qq25)
                load.getDetails().setValue('Hb', self.HBq25)
                load.getDetails().setValue('SaO2', self.SAO2q25)
                load.getDetails().setValue('CaO2', self.CAO2q25)
                load.getDetails().setValue('SvO2', self.SVO2q25)
                load.getDetails().setValue('CvO2', self.CVO2q25)
                load.getDetails().setValue('CavO2', self.CAVO2q25)
                load.getDetails().setValue('PvO2', self.PVO2q25)
                load.getDetails().setValue('QaO2', self.QAO2q25)
                load.getDetails().setValue('DO2', self.DO2q25)
        elif mode == 'avg':
            load.getDetails().setValue('VO2', self.VO2q50)
            load.getDetails().setValue('HR', self.HRq50)
            load.getDetails().setValue('Sv', self.SVq50)
            load.getDetails().setValue('Q', self.Qq50)
            load.getDetails().setValue('Hb', self.HBq50)
            load.getDetails().setValue('SaO2', self.SAO2q50)
            load.getDetails().setValue('CaO2', self.CAO2q50)
            load.getDetails().setValue('SvO2', self.SVO2q50)
            load.getDetails().setValue('CvO2', self.CVO2q50)
            load.getDetails().setValue('CavO2', self.CAVO2q50)
            load.getDetails().setValue('PvO2', self.PVO2q50)
            load.getDetails().setValue('QaO2', self.QAO2q50)
            load.getDetails().setValue('DO2', self.DO2q50)
        elif mode == 'max':
            if iqr == False:
                load.getDetails().setValue('VO2', self.VO2q50 + self.VO2std)
                load.getDetails().setValue('HR', self.HRq50 + self.HRstd)
                load.getDetails().setValue('Sv', self.SVq50 + self.SVstd)
                load.getDetails().setValue('Q', self.Qq50 + self.Qstd)
                load.getDetails().setValue('Hb', self.HBq50 + self.HBstd)
                load.getDetails().setValue('SaO2', self.SAO2q50 + self.SAO2std)
                load.getDetails().setValue('CaO2', self.CAO2q50 + self.CAO2std)
                load.getDetails().setValue('SvO2', self.SVO2q50 + self.SVO2std)
                load.getDetails().setValue('CvO2', self.CVO2q50 + self.CVO2std)
                load.getDetails().setValue('CavO2', self.CAVO2q50 + self.CAVO2std)
                load.getDetails().setValue('PvO2', self.PVO2q50 + self.PVO2std)
                load.getDetails().setValue('QaO2', self.QAO2q50 + self.QAO2std)
                load.getDetails().setValue('DO2', self.DO2q50 + self.DO2std)
            else:
                load.getDetails().setValue('VO2', self.VO2q75)
                load.getDetails().setValue('HR', self.HRq75)
                load.getDetails().setValue('Sv', self.SVq75)
                load.getDetails().setValue('Q', self.Qq75)
                load.getDetails().setValue('Hb', self.HBq75)
                load.getDetails().setValue('SaO2', self.SAO2q75)
                load.getDetails().setValue('CaO2', self.CAO2q75)
                load.getDetails().setValue('SvO2', self.SVO2q75)
                load.getDetails().setValue('CvO2', self.CVO2q75)
                load.getDetails().setValue('CavO2', self.CAVO2q75)
                load.getDetails().setValue('PvO2', self.PVO2q75)
                load.getDetails().setValue('QaO2', self.QAO2q75)
                load.getDetails().setValue('DO2', self.DO2q75)

    def calcCoords(self, load):
        temp = load.getDetails().getWorkLoadDetails()
        PvO2 = np.arange(0,100,1)
        y = 2* temp['DO2'] * PvO2

        with np.errstate(divide='ignore'):
            SvO2 = np.float_power( ( 23400 * np.float_power( (PvO2)**3 + 150*PvO2, -1 ) ) + 1, -1 )
        SvO2[np.isnan(SvO2)] = 0
        y2 = temp['Q'] * ( 1.34 * temp['Hb'] * ( temp['SaO2']/ 100 - SvO2 ) )

        load.getDetails().y = y
        load.getDetails().y2 = y2
        load.getDetails().xi = -1
        load.getDetails().yi = -1

app = App()