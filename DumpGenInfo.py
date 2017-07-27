import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
ivars = VarParsing.VarParsing('analysis')

#ivars.inputFiles=('file:/afs/cern.ch/user/k/kfjack/scratch0/temp/CMSSW_7_4_6_patch5/src/BPH-RunIIWinter15GS-00023.root')
ivars.inputFiles=('/store/mc/Summer12_DR53X/BuToJPsiK_K2MuPtEtaEtaFilter_8TeV-pythia6-evtgen/AODSIM/PU_S10_START53_V7A-v2/0000/001253E4-95DD-E111-865A-E41F131817F8.root')

ivars.outputFile='DumpGenInfo_all.root'
# get and parse the command line arguments
ivars.parseArguments()

process = cms.Process("demo")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

### output module
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('test.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *',
    )
)

### Set maxEvents
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))

process.GlobalTag.globaltag = cms.string( 'START53_V7F::All' )

### PoolSource will be ignored when running crab
process.source = cms.Source("PoolSource",
    skipEvents=cms.untracked.uint32(0),
	fileNames = cms.untracked.vstring(ivars.inputFiles)
)

process.demo = cms.EDAnalyzer('DumpGenInfo',
    GenLabel        = cms.InputTag('genParticles')
)

### Set output
process.TFileService = cms.Service("TFileService",
	fileName = cms.string(ivars.outputFile)
)

process.p = cms.Path(	
    process.demo
)
process.schedule = cms.Schedule(
	process.p
)
