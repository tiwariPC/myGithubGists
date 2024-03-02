import os
import ROOT
import math

def myCanvas1D():
    c = ROOT.TCanvas("myCanvasName", "The Canvas Title", 1980, 720)
    c.SetBottomMargin(0.12)
    c.SetRightMargin(0.10)
    c.SetLeftMargin(0.1)
    c.SetTopMargin(0.09)
    return c

inputFile = ROOT.TFile('fitDiagnostics.root','r')
covar = inputFile.Get('shapes_prefit/overall_total_covar')
corr_hist = covar.Clone('Correlation')
for i,j in zip(range(1,covar.GetNbinsX()+1), range(1,covar.GetNbinsY()+1)):
    corr_hist.SetBinContent(i, j, covar.GetBinContent(i,j)/math.sqrt(covar.GetBinContent(i,i)*covar.GetBinContent(j,j)))

ROOT.gStyle.SetOptStat(0)
c1 = myCanvas1D()
corr_hist.SetTitle('Correlation Signal+Background')
corr_hist.Draw('TEXTCOLZ')
c1.SaveAs('overall_total_corr.pdf')
 