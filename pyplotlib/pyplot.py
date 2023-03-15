###################################
#                                 #
#      pyROOT Plotter             #
#      Arnab Laha                 #
###################################
import ROOT
from ROOT import *
import os,sys
from plothelper import *
import copy
from array import array


class Plot(object):
    
    channel       = None
    year          = 2018
    data_lumi     = 59700 #pb
    analysisPhase = 'wip'
    
    #plot
    canvas      = None
    pad         = None
    ratiopad    = True
    ratioPad    = None
    legend_     = None
    obsexpleg   = None
    histogram   = None
    allbkghisto = None
    stack       = None
    uncgraph    = None
    xlabel_     = "plotname"
    ylabel_     = "Count"
    xlim_       = [0,1000]
    ylim_       = [0.01,1e8]

    
    def __setattr__(self,key,value):
        if not hasattr(self,key):
            raise TypeError("%r is not a valid pset parameter" % key)
        object.__setattr__(self,key,value)
    
    def __init__(self,channel='XYZ analysis',year=2018,analysisPhase='wip',xlabel_='',ylabel_='',xlim_=[0,1000],ylim_=[0.01,1e8]):
        """
        -initialize a plot object
        -arguments it can take:
        -channel: Analysis Name and Channel Name
        -year   : Analysis Year or Era( 2018/2017/2016preVFP/2016postVFP)
        -analysisPhase: Phase of the analysis (Work In Progress, Publication, Internal, PrivateWork)
        -xlabel_: x-axis label name
        -ylabel_: y-axis label name
        -xlim_  : x-axis range
        -ylim_  : y-axis range
        """
        self.channel = channel
        self.year    = year
        self.analysisPhase = analysisPhase
        if(self.year==2018):self.data_lumi=59800
        if(self.year==2017):self.data_lumi=41600
        self.xlabel_=xlabel_
        self.ylabel_=ylabel_
        self.xlim_  =xlim_
        self.ylim_  =ylim_
        
    def show(self):
        """
        Show Plot object information
        """
        print(f"Analysis Channel   = {self.channel}")
        print(f"Analysis year(era) = {self.year}")
        print(f"Analysis lumi      = {self.data_lumi}")
        
    def figure(self,plotname="canvas",ratiopad=True):
        """
        Create a canvas with pad and ratiopad(optional)
        - plotname: canvas name (usually name it as plotted variable)
        - ratiopad: True/False  (ratiopanel will be plotted)
        """
        self.ratiopad=ratiopad
        plotsetting.PlotRatioPad=ratiopad
        ##################################
        
        cName=plotname
        canvas=TCanvas(cName,cName,700,600)
        pad=plotsetting.CreatePad("pad",0,1.0)
        #pad.SetLogy(0)                                                           
        pad.SetFillStyle(4000)
        pad.SetTickx(1)
        #pad.Draw()
        #RatioPad
        if(self.ratiopad):
            ratioPad = plotsetting.CreateRatioPad('ratioPad',0,0.25)
            ratioPad.SetGrid(1)
            #ratioPad.Draw()

        #
        self.canvas= canvas
        self.pad   = pad
        if(self.ratiopad):self.ratioPad=ratioPad
            

        #histoInit
        self.histogram=[]
        
    def legend(self,loc='inside',legpos=[0.99,0.40,0.80,0.86],fontsize=0.03,style='lf'):
        """
        TLegend object
        -loc: legend location(default: inside)
        -legpos: customized legend position(only works when loc=None)
        -fontsize: size of the legend entry(default: 0.03)
        -style: legend style(default: line fill or lf)

        stored legend and obs/exp ratio legend(if plotdata=True) in self object
        """
        ##legend position coordinate
        if(loc=='outside'):x1,x2,y1,y2=0.99,0.60,0.80,0.86
        if(loc=='inside'):x1,x2,y1,y2=0.50,0.60,0.80,0.86
        if(loc==None):x1,x2,y1,y2=legpos[0],legpos[2],legpos[1],legpos[3]
        
        #TLegendClass
        leg_ = ROOT.TLegend(x1, x2, y1,y2) 
        plotsetting.SetLegendStyle(leg_)
        leg_.SetTextSize(fontsize)

        ##Obs/Exp Legend
        ratioleg = ROOT.TLegend(0.99, 0.90, 0.81,0.87)
        plotsetting.SetLegendStyle(ratioleg)
        ratioleg.SetTextSize(fontsize)
        #ratioleg.SetHeader("obs/exp="+(str(obs/exp)[:5]))

        #FILL
        self.histogram = sorted(self.histogram,key = lambda x: x[2],reverse=True)
        expBkg=0;obs=0
        for index,item in enumerate(self.histogram):
            histo = item[-1]
            histo_label = item[0]
            tag= item[1]

            #add in legend
            if(tag=='data'):
                obs=histo.Integral()
                leg_.AddEntry(histo,f"{histo_label} [{int(histo.Integral())}]",'ep')
        
            elif(tag=='MC'):    
                leg_.AddEntry(histo,f"{histo_label} [{histo.Integral():.2f}]",style)
                expBkg=expBkg+histo.Integral()
        #obs/exp        
        if(expBkg!=0 and obs!=0):ratioleg.SetHeader("obs/exp="+(str(obs/expBkg)[:5]))        
        
        #Add Uncertainty in legend
        self.get_allbkghisto()
        leg_.AddEntry(self.allbkghisto,"Stat. Uncertainty",'f')
        
        self.legend_=leg_
        self.obsexpleg =ratioleg
        #self.legend.Draw('SAME')
        
    def xlabel(self,xlab_='plotname'):
        """
        set xlabel of the plot
        - xlab_: xlabel
        """
        self.xlabel_=xlab_

    def ylabel(self,ylab_='Count'):
        """
        set ylabel of the plot
        - ylab_: ylabel
        """
        self.ylabel_=ylab_

    def xlim(self,xlim_=[0,1000]):
        """
        set x range of the plot
        - xlim_: x-range
        """
        self.xlim_=xlim_

    def ylim(self,ylim_=[0.01,1e8]):
        """
        set y range of the plot
        - ylim_: y-range
        """

        self.ylim_=ylim_

        
    def CMSLabel(self):
        """
        CMS Label optimized for with/without ratiopanel
        """
        ##Text Cosmetics
        CMSLabelName1='CMS'
        CMSLabelName2=''
        CMSLabelName3=''
        
        if(self.analysisPhase=='Internal'):
            CMSLabelName2='Internal'
        elif(self.analysisPhase=='WIP'):
            CMSLabelName2='Work in progress'
        elif(self.analysisPhase=='PUB'): 
            CMSLabelName2='Preliminary'
        else:CMSLabelName2= self.analysisPhase    

        ##Label at right
        year_str= f'({self.year}) '
        lumi_str= "{:.1f} fb^{{-1}}".format(self.data_lumi/1000)#infb
        CMSLabelName3= year_str+lumi_str

        text = ROOT.TLatex()
        text.SetNDC(True)

        #RatioPad
        if(self.ratiopad):
            #CMSLabelName1&3(same font and size)
            text.SetTextFont(42)
            text.SetTextSize(0.043)
            text.DrawLatex(0.15, 0.92, CMSLabelName1)
            text.DrawLatex(self.pad.GetUxmax()-0.365, 0.92,CMSLabelName3)
            #CMSLabelName2
            text.SetTextFont(72)
            text.SetTextSize(0.03)
            text.DrawLatex(0.21, 0.92, CMSLabelName2)

        else:
            #CMSLabelName1&3(same font and size)
            text.SetTextFont(42)
            text.SetTextSize(0.04)
            text.DrawLatex(0.15, 0.92, CMSLabelName1)
            text.DrawLatex(self.pad.GetUxmax()-0.40, 0.92,CMSLabelName3)
            #CMSLabelName2
            text.SetTextFont(72)
            text.SetTextSize(0.025)
            text.DrawLatex(0.22, 0.92, CMSLabelName2)

        return text
    
        
    def hist(self,mchist,color,rebin=1,label='',tag='MC',fill=False,lw=2,leg='lf',scale=1.0,density=False):
        histo=mchist.Clone()
        plotsetting.SetHistoStyle(histo)
        histo.SetLineWidth(lw)
        histo.SetLineColor(eval(color))
        if(fill):histo.SetFillColor(eval(color))

        #Rebin
        if type(rebin) is int:histo.Rebin(rebin)
        else:
            xbins=array('d',rebin)
            histo=histo.Rebin(len(xbins)-1,"h1",xbins)
        #------
        plotsetting.SetOverflowBin(histo)
        if(tag=='data'):plotsetting.SetHistoStyle(histo,xlabel="")
        #------
        if(density==True):histo.Scale(1.0/histo.Integral())
        else:histo.Scale(scale)

        #--------------
        #totalhist error
        totbins=histo.Clone().GetNbinsX()
        hist_evtErr=(histo.Clone().Rebin(totbins).GetBinError(1))
        
        #--------------
        #histo.Draw('HIST')
        self.histogram.append([label,tag,histo.Integral(),hist_evtErr*scale,histo])
        #print(self.histogram)
        

    def make_overlay(self,style):
        self.histogram = sorted(self.histogram,key = lambda x: x[2],reverse=True)
        for index,item in enumerate(self.histogram):
            h = item[-1]
            h.GetXaxis().SetTitle(self.xlabel_)
            h.GetXaxis().SetRangeUser(self.xlim_[0],self.xlim_[1])
            h.GetYaxis().SetRangeUser(self.ylim_[0],self.ylim_[1])
            if(index==0):h.DrawCopy(style)
            else:h.DrawCopy(f'{style} SAME')

    def make_stack(self):
        #sort the histogram list based on event
        self.histogram = sorted(self.histogram,key = lambda x: x[2],reverse=False)
        ###
        self.stack=THStack()
        for index,item in enumerate(self.histogram):
            h = item[-1].Clone()
            tag=item[1]
            if(tag=='MC'): #only add bkg in stack
                h.SetLineWidth(0)
                self.stack.Add(h)

        self.stack.SetMaximum(self.ylim_[1])
        self.stack.SetMinimum(self.ylim_[0])       
        self.stack.Draw("HIST")

    def get_dataHisto(self):
        for index,item in enumerate(self.histogram):
            tag=item[1]
            if(tag=='data'):
                dataHisto=item[-1]

        dataHisto.GetXaxis().SetRangeUser(self.xlim_[0],self.xlim_[1])
        dataHisto.GetYaxis().SetRangeUser(self.ylim_[0],self.ylim_[1])
        return dataHisto        

    def get_allbkghisto(self):
        self.histogram = sorted(self.histogram,key = lambda x: x[2],reverse=False)
        for index,item in enumerate(self.histogram):
            h = item[-1].Clone()
            tag=item[1]
            if(tag=='MC'):
                if(index==0):h_Allbkg=h.Clone();
                else:h_Allbkg.Add(h)

        #all bkg Style for uncertainty        
        h_Allbkg.SetFillColor(kBlack)
        h_Allbkg.SetLineColor(kBlack)
        h_Allbkg.SetFillStyle(3004)
        h_Allbkg.SetMarkerStyle(0)
        h_Allbkg.GetXaxis().SetRangeUser(self.xlim_[0],self.xlim_[1])
        self.allbkghisto=h_Allbkg
        
    
    def make_ratioHisto(self,plotdata):
        for index,item in enumerate(self.histogram):
            h = item[-1].Clone()
            tag=item[1]
            if(tag=='data'):ratioHisto=h
            elif(index==0):h_allbkg=h.Clone();ratioHisto=h.Clone()
            else:h_allbkg.Add(h)
            
        ratioHisto.Divide(h_allbkg)
        if(plotdata==False):ratioHisto.Divide(ratioHisto);SetZeroErrorHisto(ratioHisto)
        
        #ratioPad.Draw()    
        plotsetting.SetRatioHistoStyle(ratioHisto,xlabel=self.xlabel_)

        return ratioHisto

    def make_uncertaintyGraph(self):
        ##StatUncInRatioPanel
        nbins,x,y,ex,ey=getTGraphStatUnc(self.allbkghisto)
        gr = TGraphErrors( nbins, x, y, ex, ey )
        plotsetting.SetRatioHistoStyle(gr,xlabel=self.xlabel_)
        gr.SetMarkerStyle(0)
        gr.SetFillColor(kGray+1)
        gr.SetLineColor(kGray+1)
        gr.SetFillStyle(3001)
        
        return gr

    def savefig(self,name):
        self.canvas.SaveAs(f'{name}')
        
    def Draw(self,mode='stack',style="HIST",plotdata=False):
        canvas= self.canvas
        pad   = self.pad
        if(self.ratiopad):ratioPad= self.ratioPad
                    
        #---------------------------
        pad.Draw()
        if(self.ratiopad):ratioPad.Draw()
        #----------------------------
        pad.cd()
        #overlay
        if(mode == 'overlay'):
            self.make_overlay(style)
            cmslabel=self.CMSLabel()
            cmslabel.Draw()

        #stack
        if(mode=='stack'):
            self.make_stack()
            cmslabel=self.CMSLabel()
            cmslabel.Draw()
            
            if(plotdata):
                data_h=self.get_dataHisto()
                data_h.Draw('ep same')

            ###stackhistostyle
            plotsetting.SetStackHistoStyle(self.stack,xlabel=self.xlabel_)
            self.stack.GetYaxis().SetTitle(self.ylabel_)
            self.stack.GetXaxis().SetRangeUser(self.xlim_[0],self.xlim_[1])    
            
        #legend
        self.legend_.Draw('SAME')    
        if(plotdata):self.obsexpleg.Draw('SAME')
        
        
        #ratioPanel
        if(self.ratiopad):
            ratioPad.cd()
            gr=self.make_uncertaintyGraph()
            ratio_h=self.make_ratioHisto(plotdata)
            plotsetting.SetRatioHistoStyle(ratio_h,xlabel=self.xlabel_)
            ratio_h.GetXaxis().SetRangeUser(self.xlim_[0],self.xlim_[1])
            gr.GetYaxis().SetRangeUser(0.5,1.5)
            gr.GetXaxis().SetLimits(self.xlim_[0],self.xlim_[1])
            gr.GetXaxis().SetTickSize(0.1)
            ratio_h.DrawCopy('ep')
            gr.Draw(' AP E2 SAME')
            ratio_h.DrawCopy('ep SAME')

            self.uncgraph=gr    

        #legend
        #self.legend_.Draw('SAME')    
        #if(plotdata):self.obsexpleg.Draw('SAME')

            
        canvas.Draw()
        
        
    #def __del__(self):
    #    pass



def pyplot():
    plot = Plot()
    plot.show()

    return plot
    
