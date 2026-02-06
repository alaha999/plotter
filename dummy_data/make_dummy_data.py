import ROOT
import random

ROOT.gROOT.SetBatch(True)


def make_dummy_hist(hname,mean,sd,nEvents,opt=1):
    h = ROOT.TH1D(hname, hname, 200,0,200)
    for _ in range(nEvents):
        if opt==1:h.Fill(random.gauss(mean, sd))
        if opt==2:h.Fill(random.uniform(mean,sd))
    return h

def savefile(h,histoname,filename):
    myfile = ROOT.TFile(filename,"RECREATE")
    h.SetName(histoname)
    h.Write()
    myfile.Close()


# dummy background
h_bkg1 = make_dummy_hist("Bkg1",100,20,1000,opt=1)
h_bkg2 = make_dummy_hist("Bkg2",0,200,800,opt=2)
h_bkg3 = make_dummy_hist("Bkg3",80,50,700,opt=1)

# dummy signal
h_signal= make_dummy_hist("Signal",140,10,40)

# dummy data = sum of backgrounds + Gaussian fluctuation
h_data=h_bkg1.Clone("Data")
for i in range(1, h_bkg1.GetNbinsX() + 1):
    y = h_bkg1.GetBinContent(i) + h_bkg2.GetBinContent(i) + h_bkg3.GetBinContent(i)
    fluct = random.gauss(0, ROOT.TMath.Sqrt(y)) if y > 0 else 0
    h_data.SetBinContent(i, y + fluct)
    h_data.SetBinError(i, ROOT.TMath.Sqrt(abs(y + fluct)))

# save the files
savefile(h_bkg1,  "dummyvar_base", "bkg1.root")
savefile(h_bkg2,  "dummyvar_base", "bkg2.root")
savefile(h_bkg3,  "dummyvar_base", "bkg3.root")
savefile(h_signal,"dummyvar_base", "signal.root")
savefile(h_data,  "dummyvar_base", "data.root")    
