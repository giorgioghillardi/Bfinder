import FWCore.ParameterSet.Config as cms

### Run on MC?
runOnMC = True

process = cms.Process("demo")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

## Source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring("/store/mc/RunIISummer16DR80Premix/BuToJpsiK_BMuonFilter_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/100000/00B52C05-EBDB-E611-AE40-0025905B860E.root")
                            #fileNames = cms.untracked.vstring("root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/BuToJpsiKV2_BFilter_TuneCUEP8M1_13TeV-pythia8-evtgen/AODSIM/Asympt25ns_MCRUN2_74_V9_ext1-v1/100000/00066715-4AD7-E611-981B-0025905A60EE.root")
                            )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

#process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
#process.hltHighLevel.HLTPaths = cms.vstring('HLT_DoubleMu4_3_Jpsi_Displaced_v*')

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

from Configuration.AlCa.GlobalTag import GlobalTag

if runOnMC:
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_v14')
    #process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V9')
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data') # was 80X_dataRun2_2016SeptRepro_v6

process.load("Configuration.StandardSequences.MagneticField_cff")

## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)

## load tau sequences up to selectedPatMuons
process.load("PhysicsTools.PatAlgos.producersLayer1.muonProducer_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi")

from PhysicsTools.PatAlgos.tools.coreTools import *
if not runOnMC:
    runOnData(process, ['Muons'])

from PhysicsTools.PatAlgos.tools.trackTools import *
if runOnMC:
    makeTrackCandidates(process,              # patAODTrackCands
        label='TrackCands',                   # output collection will be 'allLayer0TrackCands', 'allLayer1TrackCands', 'selectedLayer1TrackCands'
        tracks=cms.InputTag('generalTracks'), # input track collection
        preselection='pt > 0.3',              # preselection cut on candidates. Only methods of 'reco::Candidate' are available
        selection='pt > 0.3',                 # Selection on PAT Layer 1 objects ('selectedLayer1TrackCands')
        isolation={},                         # Isolations to use ('source':deltaR; set to {} for None)
        isoDeposits=[],
        mcAs='muon'                           # Replicate MC match as the one used for Muons
    );                                        # you can specify more than one collection for this
  ### MC+mcAs+Match/pat_label options
    process.patTrackCandsMCMatch.resolveByMatchQuality = cms.bool(True)
    process.patTrackCandsMCMatch.resolveAmbiguities = cms.bool(True)
    process.patTrackCandsMCMatch.checkCharge = cms.bool(True)
    process.patTrackCandsMCMatch.maxDPtRel = cms.double(0.5)
    process.patTrackCandsMCMatch.maxDeltaR = cms.double(0.7)
    process.patTrackCandsMCMatch.mcPdgId = cms.vint32(111, 211, 311, 321)   
    process.patTrackCandsMCMatch.mcStatus = cms.vint32(1)

else :
    makeTrackCandidates(process,              # patAODTrackCands
        label='TrackCands',                   # output collection will be 'allLayer0TrackCands', 'allLayer1TrackCands', 'selectedLayer1TrackCands'
        tracks=cms.InputTag('generalTracks'), # input track collection
        preselection='pt > 0.3',              # preselection cut on candidates. Only methods of 'reco::Candidate' are available
        selection='pt > 0.3',                 # Selection on PAT Layer 1 objects ('selectedLayer1TrackCands')
        isolation={},                         # Isolations to use ('source':deltaR; set to {} for None)
        isoDeposits=[],
        mcAs=None                             # Replicate MC match as the one used for Muons
    );                                        # you can specify more than one collection for this

### ExcitedBc analyizer
process.analysis = cms.EDAnalyzer('Bfinder',
        Bchannel                = cms.vint32(
                1,#RECONSTRUCTION: J/psi + K
                1,#RECONSTRUCTION: J/psi + Pi
                1,#RECONSTRUCTION: J/psi + Ks 
                1,#RECONSTRUCTION: J/psi + K* (K+, Pi-)
                1,#RECONSTRUCTION: J/psi + K* (K-, Pi+)
                1,#RECONSTRUCTION: J/psi + phi
                1,#RECONSTRUCTION: J/psi + pi pi <= psi', X(3872), Bs->J/psi f0
                1,#RECONSTRUCTION: J/psi + lambda (p+, pi-) 
                1,),#RECONSTRUCTION: J/psi + lambda (p-, pi+) 
    MuonTriggerMatchingPath = cms.vstring("HLT_Dimuon*", "HLT_DoubleMu*"),
        HLTLabel        = cms.InputTag('TriggerResults::HLT'),
    GenLabel        = cms.InputTag('genParticles'),
        MuonLabel       = cms.InputTag('selectedPatMuons'),         #selectedPatMuons
        TrackLabel      = cms.InputTag('selectedPatTrackCands'),    #selectedPat
    PUInfoLabel     = cms.InputTag("addPileupInfo"),
    BSLabel     = cms.InputTag("offlineBeamSpot"),
    PVLabel     = cms.InputTag("offlinePrimaryVerticesWithBS"),
    GenEvtInfoLabel = cms.InputTag("generator"),
    tkPtCut = cms.double(0.4),
    jpsiPtCut = cms.double(0.0),
    bPtCut = cms.double(0.0),
    RunOnMC = cms.bool(runOnMC),
    doTkPreCut = cms.bool(True),
    doMuPreCut = cms.bool(True)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('bfinder_mc.root')
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('test.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *',)
)

process.muonTriggerMatchHLTMuons = cms.EDProducer(
  # matching in DeltaR, sorting by best DeltaR
  "PATTriggerMatcherDRLessByR"
  # matcher input collections
, src     = cms.InputTag( 'selectedPatMuons' )
, matched = cms.InputTag( 'patTrigger' )
  # selections of trigger objects
, matchedCuts = cms.string( 'type( "TriggerMuon" ) && path( "HLT_*" )' )
  # selection of matches
, maxDPtRel   = cms.double( 0.5 ) # no effect here
, maxDeltaR   = cms.double( 0.1 )
  # definition of matcher output
, resolveAmbiguities    = cms.bool( True )
, resolveByMatchQuality = cms.bool( True )
)

from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process ) # This is optional and can be omitted.
switchOnTriggerMatching( process, triggerMatchers = [ 'muonTriggerMatchHLTMuons' ] )

### Set basic filter
process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
vertexCollection = cms.InputTag('offlinePrimaryVertices'),
        minimumNDOF = cms.uint32(2),
        maxAbsZ = cms.double(24),
        maxd0 = cms.double(2)
)

process.noscraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
        debugOn = cms.untracked.bool(False),
        numtrack = cms.untracked.uint32(10),
        thresh = cms.untracked.double(0.25)
)

from HLTrigger.HLTanalyzers.HLTBitAnalyser_cfi import *
hltbitanalysis.UseTFileService = cms.untracked.bool(True)
process.hltanalysis = hltbitanalysis.clone(
    dummyBranches = cms.untracked.vstring(
    ),

    l1GtReadoutRecord            = cms.InputTag("gtDigis"),
    l1GctHFBitCounts     = cms.InputTag("gctDigis"),
    l1GctHFRingSums      = cms.InputTag("gctDigis"),
    l1extramu            = cms.string('l1extraParticles'),
    l1extramc            = cms.string('l1extraParticles'),
    hltresults           = cms.InputTag("TriggerResults","","HLT"),
    HLTProcessName       = cms.string("HLT"),
    genParticles         = cms.InputTag("genParticles")
    )

process.filter = cms.Sequence(process.primaryVertexFilter+process.noscraping)

process.p = cms.Path(process.filter*process.analysis*process.hltanalysis)

