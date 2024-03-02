import os
import sys
from ROOT import TFile, TH1, TH1F, TH1D
from copy import copy
from TFPlotter import plotTF

fout = TFile("bin/TF.root","RECREATE")

f = TFile("AllMETHistos/AllMETHistos_v17_12-00-02.root", "READ")

## macro is setup for the inverted transfer factors.

def GetTF(sr_bkg, cr_bkg, postfix=""):
    print ("histogram used for TF are:", sr_bkg+postfix, cr_bkg+postfix)

    if postfix=="Prefire" or postfix=="JEC" or postfix=="allbin":h_sr_bkg = f.Get(sr_bkg+postfix)
    else:h_sr_bkg = f.Get(sr_bkg)
    h_cr_bkg = f.Get(cr_bkg+postfix)

    tf_sr_cr = h_sr_bkg.Clone()
    tf_sr_cr.Divide(h_cr_bkg)

    print (tf_sr_cr.GetBinContent(1),tf_sr_cr.GetBinContent(2),tf_sr_cr.GetBinContent(3),tf_sr_cr.GetBinContent(4) )

    histname = ("tf_"+sr_bkg+"_to_"+cr_bkg+postfix).replace("bbDM2017_","").replace("bbDM2016_","").replace("bbDM2018_","")
    tf_sr_cr.SetName(histname)
    tf_sr_cr.SetTitle(histname)

    return tf_sr_cr





def GetFracUncertainty(tfs):
    tf= tfs[0].Clone()
    tf_up = tfs[1].Clone()
    tf_down = tfs[2].Clone()
    unc_up = tfs[1].Clone()    ## up - central

    unc_up.Add(tf,-1)
    unc_up.Divide(tf)

    name_up = "Unc_"+tf_up.GetName()
    unc_up.SetName(name_up)

    unc_down = tfs[2].Clone()  ## central - down
    unc_down.Add(tf,-1)
    unc_down.Divide(tf)
    name_down = "Unc_"+tf_down.GetName()
    unc_down.SetName(name_down)

    return [unc_up,unc_down]


''' mode can be all, up, down, central
syst: name of the systematics as in the AllMETHisto.root
sr_bkg: bkg histo in SR
cr_bkg: bkg histo in CR
'''
def GetAllTF(sr_bkg, cr_bkg,  syst="Prefire", mode="all",):
    postfix=[]
    if mode=="all": postfix = ["Up","Down"]
    if mode=="up": postfix = ["Up"]
    if mode=="down": postfix = ["Down"]

    postfix= ["_"+syst+i for i in postfix]
    central_ = GetTF(sr_bkg,cr_bkg)
    up_      = GetTF(sr_bkg,cr_bkg,postfix[0])
    down_    = GetTF(sr_bkg,cr_bkg,postfix[1])

    #return [central_,up_,down_]
    return ([central_,up_,down_] + GetFracUncertainty([central_,up_,down_]) )




def GetStatsUncTF(sr_bkg, cr_bkg, nbin=4):
    print ("reading histo: ",sr_bkg+"_binUp", cr_bkg+"_bin1Up")
    sr_bin1up = f.Get(sr_bkg+"_bin1Up")
    cr_bin1up = f.Get(cr_bkg+"_bin1Up")

    tf_sr_cr_bin1up  = sr_bin1up.Clone()
    tf_sr_cr_bin1up.Divide(cr_bin1up)


    sr_bin1down = f.Get(sr_bkg+"_bin1Down")
    cr_bin1down = f.Get(cr_bkg+"_bin1Down")

    tf_sr_cr_bin1down  = sr_bin1down.Clone()
    tf_sr_cr_bin1down.Divide(cr_bin1down)

    print (tf_sr_cr_bin1up.GetBinContent(1),tf_sr_cr_bin1up.GetBinContent(2),tf_sr_cr_bin1up.GetBinContent(3),tf_sr_cr_bin1up.GetBinContent(4) )
    ## call this function
    #systbin=GetStatsUncTF(analysisType+"_"+icat+"_SR_zjets"   ,  analysisType+"_"+icat+"_ZEE_dyjets")        ; alltfhists.append(systbin)

    return [tf_sr_cr_bin1up, tf_sr_cr_bin1down]


# systematic_source = ["allbin"]
# systematic_source = ['allbin','CMS2017_MuID', 'JECRelativeSample_2017', 'JECFlavorQCD', 'En', 'CMS2017_mu_scale', 'CMS2017_pdf', 'JECAbsolute', 'JECRelativeBal', 'CMS2017_trig_met', 'JECHF_2017', 'CMS2017_eff_b', 'CMS2017_fake_b', 'CMS2017_EleRECO', 'JECEC2_2017', 'CMS2017_MuTRK', 'JECHF', 'CMS2017_EleID', 'JECBBEC1_2017', 'JECAbsolute_2017', 'EWK', 'CMS2017_trig_ele', 'JECEC2', 'CMS2017_prefire', 'CMS2017_MuISO', 'JECBBEC1', 'CMS2017_PU']
systematic_source = ['allbin', 'CMS2017_trig_ele', 'CMS2017_EleID', 'CMS2017_EleRECO','CMS2017_trig_met', 'CMS2017_MuID', 'CMS2017_MuISO', 'CMS2017_MuTRK']
analysis="bbDM"
year="2017"
analysisType=analysis+year

alltfhists=[]
for icat in ["1b", "2b"]:
    for isyst in systematic_source:
        # gen_ = any([i for i in ['allbin', 'JECRelativeSample_2017', 'JECFlavorQCD', 'En', 'CMS2017_mu_scale', 'CMS2017_pdf', 'JECAbsolute', 'JECRelativeBal', 'JECHF_2017', 'CMS2017_eff_b', 'CMS2017_fake_b', 'JECEC2_2017', 'JECHF', 'JECBBEC1_2017', 'JECAbsolute_2017', 'EWK', 'JECEC2', 'CMS2017_prefire', 'JECBBEC1', 'CMS2017_PU'] if isyst==i])
        gen_ = any([i for i in ['allbin'] if isyst==i])
        for_ele = any([i for i in ['CMS2017_trig_ele', 'CMS2017_EleID', 'CMS2017_EleRECO'] if isyst==i])
        for_mu = any([i for i in ['CMS2017_trig_met', 'CMS2017_MuID', 'CMS2017_MuISO', 'CMS2017_MuTRK'] if isyst==i])
        # if (isyst == "CMS2017_MuID" or isyst == "CMS2017_MuTRK" or isyst == "allbin" or isyst == "CMS2017_trig_met" or isyst == 'CMS2017_MuISO'):
        if for_mu or gen_:
            tf_wmunu_wjets = GetAllTF(analysisType+"_"+icat+"_SR_wjets",  analysisType+"_"+icat+"_WMU_wjets", isyst);      alltfhists.append(tf_wmunu_wjets)
            tf_topmu_wjets = GetAllTF(analysisType+"_"+icat+"_SR_tt",  analysisType+"_"+icat+"_TOPMU_wjets", isyst);      alltfhists.append(tf_topmu_wjets)
            tf_topmu_top   = GetAllTF(analysisType+"_"+icat+"_SR_tt"   ,  analysisType+"_"+icat+"_TOPMU_tt" , isyst);      alltfhists.append(tf_topmu_top)
            tf_zmumu_zj    = GetAllTF(analysisType+"_"+icat+"_SR_zjets"   ,  analysisType+"_"+icat+"_ZMUMU_dyjets" , isyst);      alltfhists.append(tf_zmumu_zj)
        # if (isyst == "CMS2017_trig_ele" or isyst == "CMS2017_EleID" or isyst == "CMS2017_EleRECO" or isyst == "allbin"):
        if for_ele or gen_:
            tf_wenu_wjets  = GetAllTF(analysisType+"_"+icat+"_SR_wjets",  analysisType+"_"+icat+"_WE_wjets" , isyst);      alltfhists.append(tf_wenu_wjets)
            tf_topen_wjets = GetAllTF(analysisType+"_"+icat+"_SR_tt",  analysisType+"_"+icat+"_TOPE_wjets", isyst);      alltfhists.append(tf_topen_wjets)
            tf_topen_top   = GetAllTF(analysisType+"_"+icat+"_SR_tt"   ,  analysisType+"_"+icat+"_TOPE_tt"  , isyst);      alltfhists.append(tf_topen_top)
            tf_zee_zj      = GetAllTF(analysisType+"_"+icat+"_SR_zjets"   ,  analysisType+"_"+icat+"_ZEE_dyjets"  , isyst);      alltfhists.append(tf_zee_zj)


fout.cd()
for isyst in alltfhists:
    for ihist in isyst:
        ihist.Write()


## close the file outside of loop
fout.Close()

'''
CALLING TF PLotter Macro
'''
infile='bin/TF.root'
SR_BKG = ['SR_zjets','SR_zjets','SR_wjets','SR_wjets','SR_tt','SR_tt','SR_tt','SR_tt']
CR_BKG = ['ZEE_dyjets','ZMUMU_dyjets','WE_wjets','WMU_wjets','TOPE_wjets','TOPMU_wjets','TOPE_tt','TOPMU_tt']  #PLEASE MAKE SURE YOU GIVE PROCESS NAME IN AN ORDER AS SR
# postfix= ['allbinUp','CMS2017_eff_bUp','JECAbsolute_2017Up','JECRelativeBalUp','CMS2017_PUUp','JECHF_2017Up', 'CMS2017_mu_scaleUp', 'JECBBEC1Up', 'JECAbsoluteUp', 'JECHFUp', 'JECEC2_2017Up', 'EnUp', 'JECBBEC1_2017Up', 'JECRelativeSample_2017Up', 'JECFlavorQCDUp', 'CMS2017_fake_bUp', 'JECEC2Up', 'EWKUp', 'CMS2017_pdfUp', 'CMS2017_prefireUp']
postfix= ['allbinUp','CMS2017_trig_eleUp', 'CMS2017_EleIDUp', 'CMS2017_EleRECOUp','CMS2017_trig_metUp', 'CMS2017_MuIDUp', 'CMS2017_MuISOUp', 'CMS2017_MuTRKUp']
# postfix=['allbinUp','CMS2017_eff_bUp', 'CMS2017_EleIDUp', 'JECAbsolute_2017Up', 'JECRelativeBalUp', 'CMS2017_trig_metUp', 'CMS2017_trig_eleUp', 'CMS2017_PUUp', 'JECHF_2017Up', 'CMS2017_mu_scaleUp', 'JECBBEC1Up', 'JECAbsoluteUp', 'JECHFUp', 'CMS2017_MuISOUp', 'JECEC2_2017Up', 'EnUp', 'JECBBEC1_2017Up', 'CMS2017_MuTRKUp', 'JECRelativeSample_2017Up', 'JECFlavorQCDUp', 'CMS2017_fake_bUp', 'JECEC2Up', 'EWKUp', 'CMS2017_EleRECOUp', 'CMS2017_pdfUp', 'CMS2017_prefireUp', 'CMS2017_MuIDUp'] #PROVIDE SYS HISTS WITH UP OR DOWN

cats   = ['1b','2b']
# yaxis  = ['transfer factor (z#nu#nu SR/zee )','transfer factor (z#nu#nu SR/z#mu#mu )',\
#         'transfer factor (Wl#nu SR/we#nu )','transfer factor (wl#nu SR/w#mu#nu )',\
#         'transfer factor (t#bar{t}_{SR}/t#bar{t}_{TopeCR})','transfer factor (t#bar{t}_{SR}/t#bar{t}_{Top#mu CR} )']
yaxis  = ['transfer factor (Z(#rightarrow#nu#nu)_{SR}/Z_{ee})','transfer factor (Z(#rightarrow#nu#nu)_{SR}/Z_{#mu#mu})','transfer factor (W_{SR}/W_{e#nu})','transfer factor (W_{SR}/W_{#mu#nu})','transfer factor (t#bar{t}_{SR}/t#bar{t}_{We#nuCR})','transfer factor (t#bar{t}_{SR}/t#bar{t}_{W#muCR})','transfer factor (t#bar{t}_{SR}/t#bar{t}_{TopeCR})','transfer factor (t#bar{t}_{SR}/t#bar{t}_{Top#muCR})']
plotTF(infile,SR_BKG,CR_BKG,postfix,cats,yaxis)

