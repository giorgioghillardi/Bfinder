import FWCore.ParameterSet.Config as cms

### Run on MC?
runOnMC = False

process = cms.Process("demo")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("/store/data/Run2016B/Charmonium/AOD/23Sep2016-v1/50000/02F5116E-2986-E611-BFEA-02163E011437.root")
)
#/store/mc/RunIISummer16DR80Premix/BcToJPsiBcPt8Y2p5_MuNoCut_13TeV-bcvegpy2-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/90000/028E2B40-F115-E711-9788-FA163E1A91FB.root")
##/store/data/Run2016B/Charmonium/AOD/23Sep2016-v1/50000/02F5116E-2986-E611-BFEA-02163E011437.root file for data 2015

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = cms.vstring('HLT_DoubleMu4_3_Jpsi_Displaced_v*')

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
if runOnMC:
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v6') #auto:run2_mc is the default one
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data')
# use 'auto:run2_data' for 2016H
# "80X_dataRun2_2016SeptRepro_v5
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
                0,#RECONSTRUCTION: J/psi + K
                1,#RECONSTRUCTION: J/psi + Pi
                0,#RECONSTRUCTION: J/psi + Ks 
                0,#RECONSTRUCTION: J/psi + K* (K+, Pi-)
                0,#RECONSTRUCTION: J/psi + K* (K-, Pi+)
                0,#RECONSTRUCTION: J/psi + phi
                0,#RECONSTRUCTION: J/psi + pi pi <= psi', X(3872), Bs->J/psi f0
                0,#RECONSTRUCTION: J/psi + lambda (p+, pi-) 
                0,), #RECONSTRUCTION: J/psi + lambda (p-, pi+) 
               
    MuonTriggerMatchingPath = cms.vstring("HLT_Dimuon*", "HLT_DoubleMu*"),
        HLTLabel        = cms.InputTag('TriggerResults::HLT'),
    GenLabel        = cms.InputTag('genParticles'),
        MuonLabel       = cms.InputTag('selectedPatMuons'),         #selectedPatMuons
        TrackLabel      = cms.InputTag('selectedPatTrackCands'),    #selectedPat
    PUInfoLabel     = cms.InputTag("addPileupInfo"),
    BSLabel     = cms.InputTag("offlineBeamSpot"),
    PVLabel     = cms.InputTag("offlinePrimaryVerticesWithBS"),
    tkPtCut = cms.double(0.4),
    jpsiPtCut = cms.double(0.0),
    bPtCut = cms.double(0.0),
    RunOnMC = cms.bool(False),
    doTkPreCut = cms.bool(True),
    doMuPreCut = cms.bool(True)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('bfinder.root')
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
    HLTProcessName       = cms.string("HLT")
    )

process.filter = cms.Sequence(process.primaryVertexFilter+process.noscraping)

process.p = cms.Path(process.filter*process.analysis*process.hltanalysis)
