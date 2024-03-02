import ROOT
f = ROOT.TFile.Open("MET_2018.root")
eve_list = []
for event in f.bbDM_WmunuCR_1b:
    element  = str(event.run)+','+str(event.lumi)+','+str(event.event)
    eve_list.append(element)
print('length of event', len(eve_list), len(set(eve_list)))