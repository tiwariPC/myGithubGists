import numpy as np
import pandas as pd
import ROOT as ROOT


ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(1)
ROOT.gStyle.SetFrameLineWidth(3)
ROOT.gStyle.SetLineWidth(3)


def myCanvas1D():
    c = ROOT.TCanvas("myCanvasName", "The Canvas Title", 650, 600)
    c.SetBottomMargin(0.050)
    c.SetRightMargin(0.050)
    c.SetLeftMargin(0.050)
    c.SetTopMargin(0.050)
    return c

def set_overflow(hist):
    bin_num = hist.GetXaxis().GetNbins()
    #print (bin_num)
    hist.SetBinContent(bin_num, hist.GetBinContent(
        bin_num+1)+hist.GetBinContent(bin_num))  # Add overflow bin content to last bin
    hist.SetBinContent(bin_num+1, 0.)
    return hist

def SetLegend(coordinate_=[.50,.65,.90,.90],ncol=2):
    c_=coordinate_
    legend=ROOT.TLegend(c_[0], c_[1],c_[2],c_[3])
    legend.SetBorderSize(0)
    legend.SetNColumns(ncol)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(2)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    return legend

def SetCMSAxis(h, xoffset=1., yoffset=1.):
    h.GetXaxis().SetTitleSize(0.047)
    h.GetYaxis().SetTitleSize(0.047)

    print(type(h))
    if type(h) is ((not ROOT.TGraphAsymmErrors) or (not ROOT.TGraph)):
        h.GetZaxis().SetTitleSize(0.047)

    h.GetXaxis().SetLabelSize(0.047)
    h.GetYaxis().SetLabelSize(0.047)
    if type(h) is ((not ROOT.TGraphAsymmErrors) or (not ROOT.TGraph)):
        h.GetZaxis().SetLabelSize(0.047)

    h.GetXaxis().SetTitleOffset(xoffset)
    h.GetYaxis().SetTitleOffset(yoffset)
    return h

def DrawVerticalLine(x,c):
   line1 = ROOT.TLine()
   xndc = 0.8*((x-c.GetUxmin())/(c.GetUxmax()-c.GetUxmin()))+0.1
   line1.SetLineStyle(2)
   line1.SetLineColor(4)
   line1.SetLineWidth(3)
   line1.Draw("same")
   line1.DrawLineNDC(xndc,0.1,xndc,0.9)
   return line1


def plotHist(datafile,data2file,histName,treename):
    fdata= ROOT.TFile(datafile)
    fmc= ROOT.TFile(data2file)
    treedata = fdata.Get(treename)
    treemc = fmc.Get(treename)
    print (treedata.GetEntries())
    # tree.keys()
    legend = SetLegend([.15,.45,.45,.60],ncol=1)
    hist = {}
    hist["hist_data"] = ROOT.TH1F('hist_data','hist_data',30, 30, 300)
    hist["hist_mc"] = ROOT.TH1F('hist_mc','hist_mc',30, 30, 300)
    treedata.Draw(str(histName)+'>>hist_data')
    treemc.Draw(str(histName)+'>>hist_mc')
    hist["hist_data"] = set_overflow(hist["hist_data"])
    hist["hist_mc"] = set_overflow(hist["hist_mc"])
    c1 = myCanvas1D()
    c1_1 = ROOT.TPad("c1_1", "newpad", 0, 0.05, 1, 1)
    c1_1.SetTicky(1)
    c1_1.SetBottomMargin(0.10)
    c1_1.SetTopMargin(0.08)
    c1_1.SetLeftMargin(0.12)
    c1_1.SetRightMargin(0.06)
    c1_1.Draw()
    c1_1.cd()
    hist["hist_data"].SetTitle(str(treename)+"_"+str(histName))
    hist["hist_data"].GetXaxis().SetTitle('Leading Electron p_{T}')
    hist["hist_data"].GetYaxis().SetTitle('Events')
    hist["hist_data"].SetLineColor(1)
    hist["hist_data"].SetMinimum(float(hist["hist_data"].GetMinimum())/5)
    hist["hist_data"].SetMaximum(float(hist["hist_data"].GetMaximum()*4))
    hist["hist_data"] = SetCMSAxis(hist["hist_data"])
    hist["hist_data"].Draw('E HIST')
    legend.AddEntry(hist["hist_data"],"No Electron Trigger","PEL")
    hist["hist_mc"].SetLineColor(2)
    hist["hist_mc"].Draw('same E HIST')
    legend.AddEntry(hist["hist_mc"],'Electron Trigger',"PEL")
    legend.Draw('same')
    c1_1.Update()
    line1 = DrawVerticalLine(115,c1_1)
    c1_1.SetLogy(1)
    c1_1.SetGrid()
    c1.cd()
    c1_2 = ROOT.TPad("c1_2", "newpad", 0, 0.00, 1, 0.3)
    c1_2.SetLeftMargin(0.12)
    c1_2.SetRightMargin(0.06)
    c1_2.SetTopMargin(0.01)
    c1_2.SetBottomMargin(0.42)
    c1_2.Draw()
    c1_2.cd()
    hist["hist_mc_ratio"] = hist["hist_mc"].Clone("hist_mc_ratio")
    hist["hist_mc_ratio"].Divide(hist["hist_data"])
    hist["hist_mc_ratio"].GetYaxis().SetTitleSize(0.12)
    hist["hist_mc_ratio"].GetYaxis().SetTitleOffset(0.42)
    hist["hist_mc_ratio"].GetYaxis().SetTitleFont(42)
    hist["hist_mc_ratio"].GetYaxis().SetLabelSize(0.12)
    hist["hist_mc_ratio"].GetYaxis().CenterTitle()
    hist["hist_mc_ratio"].GetXaxis().SetTitle('Leading Electron p_{T}')
    hist["hist_mc_ratio"].GetXaxis().SetLabelSize(0.14)
    hist["hist_mc_ratio"].GetXaxis().SetTitleSize(0.16)
    hist["hist_mc_ratio"].GetXaxis().SetTitleOffset(1)
    hist["hist_mc_ratio"].GetXaxis().SetTitleFont(42)
    hist["hist_mc_ratio"].GetXaxis().SetTickLength(0.07)
    hist["hist_mc_ratio"].GetXaxis().SetLabelFont(42)
    hist["hist_mc_ratio"].GetYaxis().SetLabelFont(42)
    hist["hist_mc_ratio"].GetYaxis().SetNdivisions(505)
    hist["hist_mc_ratio"].SetTitle(' ')
    hist["hist_mc_ratio"].GetYaxis().SetRangeUser(0.5, 1.5)
    hist["hist_mc_ratio"].Draw('HIST')
    c1_2.SetGrid()
    c1.cd()
    c1.SetLogy(1)
    c1.Update()
    c1.SaveAs(str(treename)+"_"+str(histName)+".pdf")
    c1.SaveAs(str(treename)+"_"+str(histName)+".png")
    c1.Close()

files = {}
#trigger_SF
files["data"]= '/home/ptiwari/t3store3/CMSSW_10_3_0/src/v07-04-01/ExoPieProducer/ExoPieAnalyzer/CondorJobs_Analyser/analysis_histo_BR_Outputs_noEleTrig/combinedroot_SE.root'
files["data2"] = '/home/ptiwari/t3store3/CMSSW_10_3_0/src/v07-04-01/ExoPieProducer/ExoPieAnalyzer/CondorJobs_Analyser/analysis_histo_BR_Outputs_EleTrig/combinedroot_SE.root'

for tree in ['bbDM_WenuCR_1b','bbDM_WenuCR_2b','bbDM_TopenuCR_1b','bbDM_TopenuCR_2b']:
    plotHist(files["data"],files["data2"],'leadingLepPt', tree)