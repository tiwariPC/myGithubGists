import FWCore.ParameterSet.Config as cms
from RecoBTag.Combined.pfDeepCSVJetTags_cfi import *

caloDeepCSVJetTags = pfDeepCSVJetTags.clone()

caloDeepCSVJetTags.src = cms.InputTag('caloDeepCSVTagInfos')

from Configuration.Eras.Modifier_phase1Pixel_cff import phase1Pixel
phase1Pixel.toModify(caloDeepCSVJetTags, NNConfig = cms.FileInPath('RecoBTag/Combined/data/DeepCSV_PhaseI.json'))
phase1Pixel.toModify(caloDeepCSVJetTags, checkSVForDefaults = cms.bool(True))
phase1Pixel.toModify(caloDeepCSVJetTags, meanPadding = cms.bool(True))
phase1Pixel.toModify(caloDeepCSVJetTags, toAdd = cms.PSet())

from Configuration.Eras.Modifier_phase2_common_cff import phase2_common
phase2_common.toModify(caloDeepCSVJetTags, NNConfig = cms.FileInPath('RecoBTag/Combined/data/DeepCSV_PhaseI.json'))
phase2_common.toModify(caloDeepCSVJetTags, checkSVForDefaults = cms.bool(True))
phase2_common.toModify(caloDeepCSVJetTags, meanPadding = cms.bool(True))
phase2_common.toModify(caloDeepCSVJetTags, toAdd = cms.PSet())
