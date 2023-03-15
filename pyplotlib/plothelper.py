import os,sys
import ROOT
from ROOT import *
import plot_settings as plotsetting
from array import array
#####################################

def getTGraphStatUnc(histo):
    y     =array('f',[])
    ey    =array('f',[])
    x     =array('f',[])
    ex    =array('f',[])
    nbins =histo.GetNbinsX()
    for i in range(histo.GetNbinsX()):
        bin_=i+1
        binlow = histo.GetBinLowEdge(bin_)
        binhi  = binlow+histo.GetBinWidth(bin_)
        nevt   = histo.GetBinContent(bin_)
        nevtErr= histo.GetBinError(bin_)
            
        x.append((binlow+binhi)/2)
        ex.append((binhi-binlow)/2)
        y.append(1)
        if(nevt!=0):
            ey.append(nevtErr/nevt)
        else:
            ey.append(0)
        
    return nbins,x,y,ex,ey    


def SquareRootHisto(histo):
    for i in range(histo.GetNcells()):
        bin=i
        #print(histo.GetBinContent(bin))
        histo.SetBinContent(bin,sqrt(histo.GetBinContent(bin)))
        #print(histo.GetBinContent(bin))
    return histo

def ClearHisto(histo):
    for i in range(histo.GetNcells()):
        bin=i
        #print(histo.GetBinContent(bin))
        histo.SetBinContent(bin,0)
        #print(histo.GetBinContent(bin))
        histo.SetBinError(bin,0)
    return histo

def SetZeroErrorHisto(histo):
    for i in range(histo.GetNcells()):
        bin=i
        #print(histo.GetBinContent(bin))
        histo.SetBinContent(bin,0)
        #print(histo.GetBinContent(bin))
        histo.SetBinError(bin,0)
    return histo

    
def __init__():
    pass




