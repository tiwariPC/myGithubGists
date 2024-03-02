import ROOT as ROOT
import os
import sys
import glob
sys.path.append('../../ExoPieProducer/ExoPieAnalyzer/')
from Year import era
from SampleName import samp_name

def jetSF(reader, flav, pt, eta):
    maxPt = 999.99
    lowPt = 20.1
    scale = 1.0
    if pt > maxPt:
        pt = maxPt
        scale = 2
    if pt < lowPt:
        pt = lowPt
        scale = 2
    sf_c = reader.eval_auto_bounds('central', flav, eta, pt)
    sf_low = reader.eval_auto_bounds('down', flav, eta, pt)
    sf_up = reader.eval_auto_bounds('up', flav, eta, pt)
    btagsf = [sf_c, sf_low*scale, sf_up*scale]
    return btagsf


def jetflav(flav):
    if flav == 5:
        flavor = 0
    elif flav == 4:
        flavor = 1
    else:
        flavor = 2
    return flavor


def getBeff_MWP(pt, eta, flav):
    maxPt = 999.99
    if pt > maxPt:
        pt = maxPt
    if flav == 5:
        xbin = b_med_eff.GetXaxis().FindBin(eta)
        ybin = b_med_eff.GetYaxis().FindBin(pt)
        btag_eff = b_med_eff.GetBinContent(xbin, ybin)
        return btag_eff
    elif flav == 4:
        xbin = c_med_eff.GetXaxis().FindBin(eta)
        ybin = c_med_eff.GetYaxis().FindBin(pt)
        ctag_eff = c_med_eff.GetBinContent(xbin, ybin)
        return ctag_eff
    elif flav != 4 and flav != 5:
        xbin = udsg_med_eff.GetXaxis().FindBin(eta)
        ybin = udsg_med_eff.GetYaxis().FindBin(pt)
        lighttag_eff = udsg_med_eff.GetBinContent(xbin, ybin)
        return lighttag_eff


def getBeff_LWP(pt, eta, flav):
    maxPt = 999.99
    if pt > maxPt:
        pt = maxPt
    if flav == 5:
        xbin = b_loose_eff.GetXaxis().FindBin(eta)
        ybin = b_loose_eff.GetYaxis().FindBin(pt)
        btag_eff = b_loose_eff.GetBinContent(xbin, ybin)
        return btag_eff
    elif flav == 4:
        xbin = c_loose_eff.GetXaxis().FindBin(eta)
        ybin = c_loose_eff.GetYaxis().FindBin(pt)
        ctag_eff = c_loose_eff.GetBinContent(xbin, ybin)
        return ctag_eff
    elif flav != 4 and flav != 5:
        xbin = udsg_loose_eff.GetXaxis().FindBin(eta)
        ybin = udsg_loose_eff.GetYaxis().FindBin(pt)
        lighttag_eff = udsg_loose_eff.GetBinContent(xbin, ybin)
        return lighttag_eff


def getJetWeight(pt, eta, flavor, csv, WP, era):
    if WP == 'MWP':
        deepcsvWP = deepCSVMWP
        tag_eff = getBeff_MWP(pt, eta, flavor)
        SF_jet = jetSF(reader1, jetflav(flavor), pt, abs(eta))
    else:
        deepcsvWP = deepCSVLWP
        tag_eff = getBeff_LWP(pt, eta, flavor)
        SF_jet = jetSF(reader0, jetflav(flavor), pt, abs(eta))

    if era == '2016':
        maxEta = 2.4
    else:
        maxEta = 2.5
    if abs(eta) > maxEta:
        jetweight = 1.0
        jetweight_up = 1.0
        jetweight_down = 1.0
    elif csv > deepcsvWP:
        jetweight = SF_jet[0]
        jetweight_up = SF_jet[2]
        jetweight_down = SF_jet[1]
    else:
        jetweight = (1 - (SF_jet[0] * tag_eff)) / (1 - tag_eff)
        jetweight_up = (1 - (SF_jet[2] * tag_eff)) / (1 - tag_eff)
        jetweight_down = (1 - (SF_jet[1] * tag_eff)) / (1 - tag_eff)
    return jetweight, jetweight_up, jetweight_down

ROOT.gROOT.ProcessLine('.L '+os.path.dirname(__file__) +'/btagSF_Files/BTagCalibrationStandalone.cpp+')
if era == '2016':
    calib1 = ROOT.BTagCalibrationStandalone('deepcsv', os.path.dirname(
        __file__)+'/btagSF_Files/DeepCSV_2016LegacySF_V1.csv')
    tag_eff_file = ROOT.TFile(glob.glob(os.path.dirname(
        __file__)+'/btagSF_Files/analysis_histo_eff_v16_07-04/*'+samp_name+'*.root')[0])
    deepCSVLWP = 0.2217
    deepCSVMWP = 0.6321
    deepCSVTWP = 0.8953
elif era == '2017':
    calib1 = ROOT.BTagCalibrationStandalone('deepcsv', os.path.dirname(
        __file__)+'/btagSF_Files/DeepCSV_94XSF_V5_B_F.csv')
    tag_eff_file = ROOT.TFile(os.path.dirname(
        __file__)+'/btagSF_Files/bTagEffs_2017.root')
    deepCSVLWP = 0.1522
    deepCSVMWP = 0.4941
    deepCSVTWP = 0.8001
elif era == '2018':
    calib1 = ROOT.BTagCalibrationStandalone('deepcsv', os.path.dirname(
        __file__)+'/btagSF_Files/DeepCSV_102XSF_V2.csv')
    tag_eff_file = ROOT.TFile(os.path.dirname(
        __file__)+'/btagSF_Files/bTagEffs_2018.root')
    deepCSVLWP = 0.1241
    deepCSVMWP = 0.4184
    deepCSVTWP = 0.7527

#============== for MWP ============================
b_med_eff = tag_eff_file.Get('efficiency_btag_mwp')
c_med_eff = tag_eff_file.Get('efficiency_ctag_mwp')
udsg_med_eff = tag_eff_file.Get('efficiency_lighttag_mwp')

#============= for LWP ============================

b_loose_eff = tag_eff_file.Get('efficiency_btag_lwp')
c_loose_eff = tag_eff_file.Get('efficiency_ctag_lwp')
udsg_loose_eff = tag_eff_file.Get('efficiency_lighttag_lwp')


othersys = ROOT.std.vector('string')()
othersys.push_back('down')
othersys.push_back('up')
reader0 = ROOT.BTagCalibrationStandaloneReader( 0, "central", othersys)
reader0.load(calib1, 0,  "comb" )
reader0.load(calib1, 1,  "comb" )
reader0.load(calib1, 2,  "incl" )

reader1 = ROOT.BTagCalibrationStandaloneReader(1, "central", othersys)
reader1.load(calib1, 0,  "comb")
reader1.load(calib1, 1,  "comb")
reader1.load(calib1, 2,  "incl")

def btag_weight(nJets, ptList, etalist, flavlist, depCSVlist, WP, index=False):
    btagweight = 1.0
    btagweight_up = 1.0
    btagweight_down = 1.0
    if index:
        runOn = nJets
    if not index:
        runOn = range(nJets)
    # jet weight calculation
    for i in runOn:
        jetweight, jetweight_up, jetweight_down = getJetWeight(
            ptList[i], etalist[i], flavlist[i], depCSVlist[i], WP, era)
        btagweight *= jetweight
        btagweight_up *= jetweight_up
        btagweight_down *= jetweight_down
    return btagweight, btagweight_up, btagweight_down
