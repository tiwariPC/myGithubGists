#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, glob, math, operator
import ROOT as ROOT
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend,gROOT,TGraph
from ROOT import kBlack, kBlue, kRed
from array import array
import matplotlib.pyplot as plt, numpy as np
from matplotlib import text
from matplotlib.colors import LogNorm
import datetime
import pandas as pd 

def SetCanvas():
    c = TCanvas("myCanvasName","The Canvas Title",650,600)
    c.SetBottomMargin(0.100)
    c.SetRightMargin(0.020)
    c.SetLeftMargin(0.150)
    c.SetTopMargin(0.080)
    return c

def SetCMSAxis(h, xoffset=1., yoffset=1.):
    h.GetXaxis().SetTitleSize(0.047)
    h.GetYaxis().SetTitleSize(0.047)

    print (type(h))
    if type(h) is ( (not ROOT.TGraphAsymmErrors) or (not ROOT.TGraph)):
        h.GetZaxis().SetTitleSize(0.047)

    h.GetXaxis().SetLabelSize(0.047)
    h.GetYaxis().SetLabelSize(0.047)
    if type(h) is ( (not ROOT.TGraphAsymmErrors) or (not ROOT.TGraph)):
        h.GetZaxis().SetLabelSize(0.047)

    h.GetXaxis().SetTitleOffset(xoffset)
    h.GetYaxis().SetTitleOffset(yoffset)
    return h

def SetLegend(coordinate_=[.50,.65,.90,.90],ncol=2):
    c_=coordinate_
    legend=ROOT.TLegend(c_[0], c_[1],c_[2],c_[3])
    legend.SetBorderSize(0)
    legend.SetNColumns(ncol)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    return legend


def drawenergy1D(is2017, text_="Work in progress 2018", data=True):
    #pt = ROOT.TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt = ROOT.TPaveText(0.0997181,0.95,0.9580537,0.96,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(52)

    cmstextSize = 0.07
    preliminarytextfize = cmstextSize * 0.7
    lumitextsize = cmstextSize *0.7
    pt.SetTextSize(cmstextSize)
    text = pt.AddText(0.03,0.57,"#font[60]{CMS}")

    #pt1 = ROOT.TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt1 = ROOT.TPaveText(0.0877181,0.95,0.9580537,0.96,"brNDC")
    pt1.SetBorderSize(0)
    pt1.SetTextAlign(12)
    pt1.SetFillStyle(0)
    pt1.SetTextFont(52)

    pt1.SetTextSize(preliminarytextfize)
    #text1 = pt1.AddText(0.215,0.4,text_)
    text1 = pt1.AddText(0.15,0.4,text_)

    #pt2 = ROOT.TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt2 = ROOT.TPaveText(0.0997181,0.95,0.9580537,0.96,"brNDC")
    pt2.SetBorderSize(0)
    pt2.SetTextAlign(12)
    pt2.SetFillStyle(0)
    pt2.SetTextFont(52)
    pt2.SetTextFont(42)
    pt2.SetTextSize(lumitextsize)

    pavetext = ''
    if is2017 and data: pavetext = str(luminosity_)+' fb^{-1}'+" (13 TeV)"
    if (not is2017) and data: pavetext = str(luminosity_)+' fb^{-1}'+"(13 TeV)"

    if is2017 and not data: pavetext = "13 TeV"
    if (not is2017) and not data: pavetext = "13 TeV"

    if data: text3 = pt2.AddText(0.68,0.5,pavetext)
    if not data: text3 = pt2.AddText(0.85,0.5,pavetext)

    return [pt,pt1,pt2]

def getLatex():
    latex =  TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    latex.SetTextAlign(11);
    latex.SetTextColor(1);
    return latex


def getGraph(n,x,y,lc,mc,ms):
    gr =TGraph(n,x,y)
    gr.SetFillColor(4)
    #gr.SetFillStyle(3004)
    gr.SetLineColor(4)
    gr.SetLineWidth(2)
    gr.SetMarkerStyle(ms)
    gr.SetMarkerSize(1.5)
    gr.SetLineColor(lc)
    gr.SetLineWidth(1)
    gr.SetMarkerColor(mc)
    gr.GetYaxis().SetTitle("Signal Efficiency")
    gr.GetXaxis().SetTitle("M_{a} (GeV)")
    return gr
    



datestr = str(datetime.date.today().strftime("%d%m%Y"))
luminosity_ = '{0:.2f}'.format(35.82)




gStyle.SetErrorX(0.5)
gStyle.SetFrameLineWidth(3)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetFillColor(2)
gStyle.SetLineWidth(1)
gStyle.SetHistFillStyle(2)
gROOT.SetBatch(True)
sig_plots = {}

xsec_scan = pd.read_csv('/Users/ptiwari/Downloads/Document/tanbeta_vs_ma_scan_mA_1200_fixed.csv',sep=",",) 
xsec_scan = xsec_scan[1:]
tanb = [1,10,20,25,30,35,40,45,50]

for beta in tanb:
    loc_dict = {}
    for i in range(len(xsec_scan.query('tanbeta == '+str(beta))['ma'])):
        loc_dict.update({xsec_scan.query('tanbeta == '+str(beta))['ma'].iloc[i]:xsec_scan.query('tanbeta == '+str(beta))['xsec'].iloc[i]})
    sig_plots.update({'tan#beta_=_'+str(beta):loc_dict})
    
print(sig_plots)


c1 = SetCanvas()
c1.SetTickx()
c1.SetTicky()
c1.SetGridx()
c1.SetGridy()
c1.SetLogy(1)
c1.cd()
#legend = SetLegend([.65,.45,.85,.80],ncol=1)
legend = SetLegend([.60,.28,.95,.45],ncol=2)
fst_ele = 1
all_graph = ROOT.TMultiGraph()
for key in sig_plots: 
    sig_eff_sorted = sorted(sig_plots[key].items(), key=operator.itemgetter(0))
    x12, y12 = zip(*sig_eff_sorted)
    x12 = array('d',x12)
    y12 = array('d',y12)
    gr12 = getGraph(len(x12),x12,y12,fst_ele,fst_ele,20+fst_ele)
    gr12 = SetCMSAxis(gr12,1,1.6)
    all_graph.Add(gr12)
    legend.AddEntry(gr12,str(key).replace('_',' '),"PEL")
    fst_ele+=1
all_graph.Draw("ALP")
legend.Draw('p same')
all_graph.SetTitle(";M_{a}GeV;Signal cross-section(pb)");
all_graph= SetCMSAxis(all_graph,1,1.6)
pt = drawenergy1D(True,text_="    Internal",data=False)
for ipt in pt: ipt.Draw()
latex=getLatex()
latex.DrawLatex(0.55, 0.84,'#splitline{2HDM+a model}{mA = 1200 GeV, sin#theta = 0.7}')

c1.Update()
c1.Draw()

c1.SaveAs('xSection_tanbScan_'+datestr+'.pdf')
c1.SaveAs('xSection_tanbScan_'+datestr+'.png')
