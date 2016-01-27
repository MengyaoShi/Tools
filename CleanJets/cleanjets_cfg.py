import FWCore.ParameterSet.Config as cms

process = cms.Process("CLEANJETS")

#######################################
# Loading all processes and functions
#######################################
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.GlobalTag.globaltag = cms.string('74X_dataRun2_Prompt_v3')

#######################################
# Declaring Input and configurations
#######################################
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource",
         fileNames = cms.untracked.vstring('root://eoscms//eos/cms/store/user/mshi/gg2H2aa2mumutautau_STEP_2_9GeV/gg2H2aa2mumutautau_STEP_2_9GeV_NUM.root')
)

#########################################################
# this will produce a ref to the original muon collection
#########################################################
process.muonsRef = cms.EDFilter('MuonRefSelector',
                   src = cms.InputTag('muons'),
                   cut = cms.string('pt > 0.0'),
                   filter = cms.bool(True)
)

#############################
# Clean Jets Definition
##############################
process.CleanJets = cms.EDProducer(
    'CleanJets',
    jetSrc = cms.InputTag("ak4PFJets"),
    muonSrc = cms.InputTag("muonsRef"),
    PFCandSrc = cms.InputTag("pfIsolatedMuonsEI"),
    outFileName = cms.string('file:/afs/cern.ch/user/k/ktos/NMSSM_Analysis/CMSSW_7_4_12_patch4/src/Tools/CleanJets/BSUB/DIRNAME/CleanJets_Plots.root')
)

#######################################
# HPS Tau Reconstruction alterations 
#######################################
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
process.ak4PFJetTracksAssociatorAtVertex.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.recoTauAK4PFJets08Region.src = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')

process.ak4PFJetsLegacyHPSPiZeros.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.ak4PFJetsRecoTauChargedHadrons.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')
process.combinatoricRecoTaus.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'CLEANJETS')

#######################################
# Configuring Output
#######################################
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:DIRNAME_NUM.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
)

process.p = cms.Path(process.muonsRef*
		     process.CleanJets*
	             process.PFTau)
process.e = cms.EndPath(process.out)
