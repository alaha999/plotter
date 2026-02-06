import ROOT
from array import array

def SetOverflowBin(histo):
    nbins = histo.GetNbinsX()
    histo.SetBinContent(nbins, histo.GetBinContent(nbins) + histo.GetBinContent(nbins+1)); ## Overflow
    histo.SetBinContent(1, histo.GetBinContent(1)+ histo.GetBinContent(0));                ## Underflow

def SetOverflowBin_Xrange(histo):
    nbins = histo.GetNbinsX()
    last_visible_bin = int(histo.GetXaxis().GetLast())
    histo.SetBinContent(last_visible_bin, histo.Integral(last_visible_bin+1,histo.GetNbinsX()+1)); ## Overflow
    #histo.SetBinContent(1, histo.GetBinContent(1)+ histo.GetBinContent(0));                ## Underflow
    
    

def PadStyling(pad,rpad,pubstyle=False):
    L,R = 0.12,0.30
    if pubstyle:L,R=0.12,0.05
    T_up,B_up=0.09,0.01
    T_dn,B_dn=0.04,0.35
    pad.SetLeftMargin(L)
    pad.SetRightMargin(R)
    pad.SetTopMargin(T_up)
    pad.SetBottomMargin(B_up)
    pad.SetTickx(1)
    pad.SetTicky(1)

    rpad.SetLeftMargin(L)
    rpad.SetRightMargin(R)
    rpad.SetTopMargin(T_dn)
    rpad.SetBottomMargin(B_dn)
    rpad.SetTickx(1)
    rpad.SetTicky(1)
    #rpad.SetGrid(1)


def StackStyle(h_stack,ylabel='Events'):
    h_stack.GetYaxis().SetTitle(ylabel)
    h_stack.GetYaxis().CenterTitle()
    
    #beautification
    h_stack.GetXaxis().SetTitleFont(43)
    h_stack.GetXaxis().SetTitleSize(20)
    h_stack.GetXaxis().SetTitleOffset(0.8)
    h_stack.GetXaxis().SetLabelFont(43)
    h_stack.GetXaxis().SetLabelSize(0)
    h_stack.GetXaxis().SetNdivisions(513)
    h_stack.GetXaxis().SetTickSize(0.05)
    h_stack.GetYaxis().SetTitleFont(43)
    h_stack.GetYaxis().SetTitleSize(18)
    h_stack.GetYaxis().SetTitleOffset(1.7)
    h_stack.GetYaxis().SetLabelFont(43)
    h_stack.GetYaxis().SetLabelSize(15)
    h_stack.GetYaxis().SetNdivisions(510)
    h_stack.GetYaxis().SetTickSize(0.02)
    h_stack.SetTitle('')

def RatioHistoStyle(h_ratio,xlabel='X',ylabel='obs/exp'):
    h_ratio.GetXaxis().SetTitle(xlabel)
    h_ratio.GetYaxis().SetTitle(ylabel)
    h_ratio.GetXaxis().CenterTitle()
    h_ratio.GetYaxis().CenterTitle()
    #beautification
    h_ratio.GetXaxis().SetTitleFont(43)
    h_ratio.GetXaxis().SetTitleSize(20)
    h_ratio.GetXaxis().SetTitleOffset(1.2)
    h_ratio.GetXaxis().SetLabelFont(43)
    h_ratio.GetXaxis().SetLabelSize(14)
    h_ratio.GetXaxis().SetNdivisions(513)
    h_ratio.GetYaxis().SetTitleFont(43)
    h_ratio.GetYaxis().SetTitleSize(18)
    h_ratio.GetYaxis().SetTitleOffset(1.6)
    h_ratio.GetYaxis().SetLabelFont(43)
    h_ratio.GetYaxis().SetLabelSize(14)
    h_ratio.GetYaxis().SetNdivisions(503)
    #h_ratio.GetYaxis().SetRangeUser(0,2)    
    h_ratio.SetTitle('')

def LegendStyle(legend):
    legend.SetTextFont(41)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)
    

def setCMSExperimentLabelStyle():
    cmsTextFont,cmsTextSize= 61, 0.07
    extraTextFont=52
    additionalTextFont = 42
    additionalTextSize=0.044
    
    CMSLabel  = ROOT.TLatex();
    CMSLabel.SetNDC(True);
    CMSLabel.SetTextSize(cmsTextSize);
    CMSLabel.SetTextFont(cmsTextFont)
    
    extraLabel= ROOT.TLatex();
    extraLabel.SetNDC(True);
    extraLabel.SetTextFont(extraTextFont)
    extraLabel.SetTextSize(additionalTextSize)

    lumiLabel = ROOT.TLatex();
    lumiLabel.SetNDC(True);
    lumiLabel.SetTextAlign(31);
    lumiLabel.SetTextFont(additionalTextFont);
    lumiLabel.SetTextSize(additionalTextSize);
    
    return CMSLabel,extraLabel,lumiLabel

def setATLASExperimentLabelStyle():
    atlasTextFont,atlasTextSize= 72, 0.055
    extraTextFont,extraTextSize= 42, 0.053
    additionalTextFont= 42
    additionalTextSize=0.044
    
    ATLASLabel  = ROOT.TLatex();
    ATLASLabel.SetNDC(True);
    ATLASLabel.SetTextSize(atlasTextSize);
    ATLASLabel.SetTextFont(atlasTextFont)
    
    extraLabel= ROOT.TLatex();
    extraLabel.SetNDC(True);
    extraLabel.SetTextFont(extraTextFont)
    extraLabel.SetTextSize(extraTextSize)

    lumiLabel = ROOT.TLatex();
    lumiLabel.SetNDC(True);
    #lumiLabel.SetTextAlign(31);
    lumiLabel.SetTextFont(additionalTextFont);
    lumiLabel.SetTextSize(additionalTextSize);
    
    return ATLASLabel,extraLabel,lumiLabel


def mc_uncertainty_band_ratio(h_mc):
    n_bins = h_mc.GetNbinsX()
    unc_band = ROOT.TGraphAsymmErrors()
    unc_band.SetName("unc_band_ratio")
    unc_band.SetTitle("Ratio panel Uncertainty Band")

    for i in range(1, n_bins + 1):
        mc_val = h_mc.GetBinContent(i)
        mc_err = h_mc.GetBinError(i)

        x = h_mc.GetBinCenter(i)
        width = h_mc.GetBinWidth(i) / 2.0
        
        if mc_val > 0:
            rel_err = mc_err / mc_val
        else:
            rel_err = 0.0

        unc_band.SetPoint(i - 1, x, 1.0)  # y = 1 line
        unc_band.SetPointError(i - 1, width, width, rel_err, rel_err)

    return unc_band

def truncate_histogram(h_orig, xmin, xmax, new_name="h_subrange"):
    # Get bin range corresponding to xmin and xmax
    bin_low = h_orig.FindBin(xmin)
    bin_high = h_orig.FindBin(xmax)-1

    # Get the bin edges
    xlow = h_orig.GetXaxis().GetBinLowEdge(bin_low)
    xhigh = h_orig.GetXaxis().GetBinUpEdge(bin_high)
    nbins = bin_high - bin_low + 1

    # Create new histogram
    h_new = ROOT.TH1D(new_name, h_orig.GetTitle(), nbins, xlow, xhigh)
    #h_new = h_orig.Clone()
    h_new.SetName(new_name)
    h_new.SetDirectory(0)  # optional: detach from current file

    # Copy style
    h_new.SetLineColor(h_orig.GetLineColor())
    h_new.SetFillColor(h_orig.GetFillColor())
    h_new.SetMarkerColor(h_orig.GetMarkerColor())
    h_new.SetMarkerStyle(h_orig.GetMarkerStyle())
    h_new.SetLineStyle(h_orig.GetLineStyle())
    h_new.SetLineWidth(h_orig.GetLineWidth())
    h_new.SetFillStyle(h_orig.GetFillStyle())
    h_new.SetTitle(h_orig.GetTitle())
    h_new.GetXaxis().SetTitle(h_orig.GetXaxis().GetTitle())
    h_new.GetYaxis().SetTitle(h_orig.GetYaxis().GetTitle())
    
    # Copy bin contents and errors
    for i in range(nbins):
        source_bin = bin_low + i
        target_bin = i + 1

        content = h_orig.GetBinContent(source_bin)
        error = h_orig.GetBinError(source_bin)

        h_new.SetBinContent(target_bin, content)
        h_new.SetBinError(target_bin, error)

    return h_new




class Plotter():
    
    def __setattr__(self,key,value):
        if not hasattr(self,key):
            raise TypeError("%r is not a valid pset parameter" % key)
        object.__setattr__(self,key,value)

    def __init__(self):
        pass

    ##params
    lumi=0
    year=0
    experiment='CMS'
    extraText='Internal'
    energy='13 TeV'
    
    canvas=None
    mainPad=None
    ratioPad=None

    histogram=[]
    h_stack =None
    h_totbkg=None
    h_data  =None
    h_err   =None
    h_ratio =None
    yerr_ratio=None

    mainleg  = None
    ratioleg= None
    
    
    xlabel ='X'
    ylabel ='Events'
    xrange =None
    yrange =(0.01,1E8)
    ylabel_ratio='obs/exp'
    yrange_ratio=(0,2)

    extraTextCaption=[]
    

    pubStyle=False

    debug=True
    print_info=False
    
    def setPubStyle(self,pubStyle):
        self.pubStyle=pubStyle
    
    def setLumi(self,lumi):
        self.lumi = lumi
        
    def setYear(self,year):
        self.year = year

    def setExperiment(self,experiment):
        self.experiment = experiment

    def setExtraText(self,extraText):
        self.extraText = extraText
        
    def setEnergy(self,energy):
        self.energy = energy
    
    def set_xaxis(self,xlabel='X-axis',xrange=()):
        self.xlabel=xlabel
        if xrange:self.xrange=xrange
        

    def set_yaxis(self,ylabel='Y-axis',yrange=(0.01,1E8)):
        self.ylabel=ylabel
        self.yrange=yrange

    def set_yaxis_ratio(self,ylabel='obs/exp',yrange=(0,2)):
        self.ylabel_ratio=ylabel
        self.yrange_ratio=yrange

    def createPlaceHolderHisto(self,myhisto):
        h_placeholder = myhisto.Clone("h_placeholder")
        for i in range(1,h_placeholder.GetNbinsX()+1):
            h_placeholder.SetBinContent(i,1)
            h_placeholder.SetBinError(i,0)
        return h_placeholder
        
    def show(self):
        print('plot settings')
        print('Experiment: ',self.experiment)
        print('ExtraText : ',self.extraText)
        print('Energy    : ',self.energy)
        print('Year      : ',self.year)
        print('Luminosity: ',self.lumi)
        print('PubStyle  : ',self.pubStyle)

    def printInfo(self,stack_histo,signal_histo,data_histo):
        from tabulate import tabulate
        info=[]
        if stack_histo:nbins=stack_histo[0].GetNbinsX()
        elif signal_histo:nbins=signal_histo[0].GetNbinsX()
        else:nbins=data_histo[0].GetNbinsX()
        headers=[]
        headers.extend(["BinNo","range"])
        for ibin in range(1,nbins+1):
            decorated_info=[]
            decorated_info.append(f"Bin{ibin}")            
            for h in stack_histo:
                if ibin==1:headers.append(h.GetName())
                decorated_info.extend([f"{(h.GetBinLowEdge(ibin)):.1f},{(h.GetBinLowEdge(ibin)+h.GetBinWidth(ibin)):.1f}"])
                decorated_info.append(f"{h.GetBinContent(ibin):.1f}\u00B1{h.GetBinError(ibin):.1f}")
            for h in signal_histo:
                if ibin==1:headers.append(h.GetName())
                decorated_info.append(f"{h.GetBinContent(ibin):.1f}\u00B1{h.GetBinError(ibin):.1f}")
            for h in data_histo:
                if ibin==1:headers.append(h.GetName())
                decorated_info.append(f"{h.GetBinContent(ibin):.1f}\u00B1{h.GetBinError(ibin):.1f}")

            if(ibin==1):headers.append("obs/exp")
            if(self.h_totbkg.GetBinContent(ibin)!=0):
                obs_exp=self.h_data.GetBinContent(ibin)/self.h_totbkg.GetBinContent(ibin)
            else:obs_exp = -1
            decorated_info.extend([f"{obs_exp:.2f}"])
            info.append(decorated_info)

        #print(info)
        #print(headers)
        print(tabulate(info, headers=headers, tablefmt="github"))
        print()
        print(f"totbkg = {self.h_totbkg.Integral():.2f}")
        print(f"  data = {self.h_data.Integral():.2f}")
        print(f"obs/exp= {(self.h_data.Integral()/self.h_totbkg.Integral()):.3f}")
        print()

        
    def legend(self,pos=[0.70,0.01,0.92,0.86],fontsize=0.03,col=1):
        x1,y1,x2,y2=pos[0],pos[1],pos[2],pos[3]
        #if self.pubStyle:
            #x1,y1=0.50,0.40
            #x2,y2=x1+0.15*col,0.86
            
        #legend
        self.mainleg = ROOT.TLegend(x1,y1,x2,y2)
        LegendStyle(self.mainleg)
        self.mainleg.SetTextSize(fontsize)
        self.mainleg.SetTextFont(42)
        self.mainleg.SetNColumns(col)
        self.mainleg.SetColumnSeparation(0.1)
        
        #EXP/OBS ratio legend
        self.ratioleg = ROOT.TLegend(x1,y2+0.01,x2,y2+0.03)
        LegendStyle(self.ratioleg)
        self.ratioleg.SetTextSize(fontsize)


    def set_extraTextCaption(self,textCaption):
        return self.extraTextCaption.append(textCaption)
        
    
    def figure(self,canvName='can',w=800,h=600):
        if self.pubStyle:w,h=600,600
        self.canvas = ROOT.TCanvas(canvName,"canvas",w,h)
        ROOT.gStyle.SetOptStat(0)
        ratioPadSize = 0.30
        self.mainPad  = ROOT.TPad("mpad","mainpad",0,ratioPadSize,1,1)
        self.ratioPad = ROOT.TPad("rpad","ratiopad",0,0,1.0,ratioPadSize)
        PadStyling(self.mainPad,self.ratioPad,self.pubStyle)

        self.histogram=[]
        self.h_stack =None
        self.h_totbkg=None
        self.h_data  =None
        self.h_err   =None
        self.h_ratio =None
        self.yerr_ratio=None
        self.mainleg=None
        self.ratioleg=None
        self.extraTextCaption=[]

        
    def hist(self,histo,color='ROOT.kBlue',label='name',stack=False,fill=False,lwidth=2,ls=0.7,lstyle='ROOT.kSolid',legendStyle='lf',scale=1.0,density=False,isData=False):
        h=histo.Clone(f"{histo.GetName()}")
        SetOverflowBin(h)
        #styling
        h.SetLineWidth(lwidth)
        if stack:h.SetLineWidth(0)
        h.SetLineColor(eval(color))
        h.SetLineStyle(eval(lstyle))
        if fill:h.SetFillColor(eval(color))
        
        ##label
        if self.xrange==None:self.xrange=(h.GetBinLowEdge(1),h.GetBinLowEdge(1)+h.GetNbinsX()*h.GetBinWidth(1))
        if self.debug:
            print(f"xmin={h.GetBinLowEdge(1)}/nbins={h.GetNbinsX()}/binwidth={h.GetBinWidth(1)}/xmax = {h.GetBinLowEdge(1)+h.GetNbinsX()*h.GetBinWidth(1)}")
        ##data
        if isData:
            h.SetMarkerSize(ls)
            h.SetMarkerStyle(8)

        ##density
        if density:h.Scale(1.0/h.Integral())
        else:h.Scale(scale)
            
        self.histogram.append([label,stack,isData,h])
        
    def Draw(self,logY=True,logX=False,truncate_xrange=False,rebin=1,unc_fstyle=1003,unc_fcolor=ROOT.kGray,extraTextOffset=0.08,sigLegStyle="lf",sortLegend=True):
        
        if self.debug:
            print("debugging at the start of Draw")
            print("xlabel: ",self.xlabel)
            print("ylabel: ",self.ylabel)
            print("xrange: ",self.xrange)
            print("yrange: ",self.yrange)
            print("ylabel_ratio: ",self.ylabel_ratio)
            print("yrange_ratio: ",self.yrange_ratio)
            
        
        ##log-scale
        if logY: self.mainPad.SetLogy(1)
        if logX: self.mainPad.SetLogx(1)
        if logX: self.ratioPad.SetLogx(1)
        
        ##truncate-hist if subrange of X-axis is chosen
        if truncate_xrange:
            truncated_histogram=[]
            for item in self.histogram:
                hist = item[-1]
                hist_xmin = hist.GetBinLowEdge(1)
                hist_xmax = hist.GetNbinsX()*hist.GetBinWidth(1)
                user_xmin = self.xrange[0]
                user_xmax = self.xrange[1]
                if user_xmin < hist_xmin:user_xmin = hist_xmin
                if user_xmax > hist_xmax:user_xmax = hist_xmax                
                hist_new=truncate_histogram(hist,user_xmin,user_xmax,hist.GetName()+"_trimmed")
                truncated_histogram.append([item[0],item[1],item[2],hist_new])

            self.histogram = truncated_histogram

        
        ##Rebin Histograms
        for item in self.histogram:
            h = item[-1]
            #Rebin                                                                                                                                                
            if type(rebin) is int:
                h.Rebin(rebin)
            else:
                xbins=array('d',rebin)
                h=h.Rebin(len(xbins)-1,"h1",xbins)
            item[-1] = h
            
        
        ##divide histograms into stack, data, signal
        stack_histograms =[]
        data_histograms  =[]
        signal_histograms=[]
        for item in self.histogram:
            label   = item[0]
            isStack = item[1]
            isData  = item[2]
            hist    = item[-1]
            if isStack:
                stack_histograms.append(hist)
            else:
                if isData:
                    data_histograms.append(hist)
                else:
                    signal_histograms.append(hist)

        ###stack
        if stack_histograms:self.h_stack=ROOT.THStack("stack","")
        stack_histograms=sorted(stack_histograms,key=lambda x:x.Integral(),reverse=False)
        for i,hist in enumerate(stack_histograms):
            self.h_stack.Add(hist)

        ##tot_bkg
        if self.h_stack:
            self.h_totbkg=self.h_stack.GetStack().Last().Clone("total background")
            
        ##MC uncertainty band
        if self.h_totbkg !=None:
            self.h_err=self.h_totbkg.Clone("MC Uncertainty band")            
            self.h_err.SetFillColorAlpha(unc_fcolor+1,0.6)
            self.h_err.SetFillStyle(unc_fstyle)#1003
            self.h_err.SetMarkerStyle(0)
            self.h_err.SetLineWidth(0)

            
        ###data
        for i,hist in enumerate(data_histograms):
            if(i==0):self.h_data = hist.Clone("h_data")
            else:self.h_data.Add(hist)


        ##Debugging    
        if self.debug:
            print("h_data:",self.h_data)
            print("h_stack:",self.h_stack)
            print("h_totbkg:",self.h_totbkg)
            print("h_MCuncband",self.h_err)
            
        
        ###Legend
        if self.mainleg==None:self.legend()
        stack_legend=[]
        signal_legend=[]
        for item in self.histogram:
            label   = item[0]
            isStack = item[1]
            isData  = item[2]
            hist    = item[-1]

            if isStack:stack_legend.append([label,hist])
            else:
                if not isData:
                    signal_legend.append([label,hist])

        if(sortLegend):stack_legend=sorted(stack_legend,key=lambda x:x[-1].Integral(),reverse=True)
        if(sortLegend):signal_legend=sorted(signal_legend,key=lambda x:x[-1].Integral(),reverse=True)
        if(self.pubStyle):
            if self.h_data!=None:
                self.mainleg.AddEntry(self.h_data,f"{label}",'ep')
            for item in stack_legend:
                label,histo=item[0],item[-1]                
                self.mainleg.AddEntry(histo,f"{label}",'f')
            for item in signal_legend:
                label,histo=item[0],item[-1]
                self.mainleg.AddEntry(histo,label,sigLegStyle)

            if self.h_err:self.mainleg.AddEntry(self.h_err,"Uncertainty","f")
            
        else:
            if(self.h_data!=None and self.h_totbkg.Integral() and self.h_data.Integral()):
                self.ratioleg.SetHeader(f"obs/exp={(self.h_data.Integral()/self.h_totbkg.Integral()):.2f}, Exp={self.h_totbkg.Integral():.3e}")
            if self.h_data!=None:
                self.mainleg.AddEntry(self.h_data,f"{label} [{self.h_data.Integral():.3e}]",'ep')
            for item in stack_legend:
                label,histo=item[0],item[-1]
                self.mainleg.AddEntry(histo,f"{label} [{histo.Integral():.3e}]",'f')
            for item in signal_legend:
                label,histo=item[0],item[-1]
                print(f"{label}")
                self.mainleg.AddEntry(histo,f"{label} [{histo.Integral():.3e}]",sigLegStyle)

            if self.h_err:self.mainleg.AddEntry(self.h_err,"Uncertainty","f")
            

            
        ##Drawing
        self.mainPad.Draw()                
        self.ratioPad.Draw()
        
        self.mainPad.cd()
        if(self.h_stack!=None):
            self.h_stack.Draw("HIST")
            StackStyle(self.h_stack,self.ylabel)
            self.h_stack.SetMinimum(self.yrange[0])
            self.h_stack.SetMaximum(self.yrange[1])
            self.h_stack.GetXaxis().SetRangeUser(self.xrange[0],self.xrange[1])
            self.h_err.Draw("e2same0")
            

        for index,h_signal in enumerate(signal_histograms):
            StackStyle(h_signal,self.ylabel)
            h_signal.GetXaxis().SetRangeUser(self.xrange[0],self.xrange[1])
            h_signal.GetYaxis().SetRangeUser(self.yrange[0],self.yrange[1])
            SetOverflowBin_Xrange(h_signal)
            if(index==0 and self.h_stack==None):
                h_signal.Draw("HIST")
            else:
                h_signal.Draw("HIST SAME")

        if(self.h_data!=None):
            self.h_data.SetBinErrorOption(ROOT.TH1.EBinErrorOpt.kPoisson)
            self.h_data.GetXaxis().SetRangeUser(self.xrange[0],self.xrange[1])
            self.h_data.GetYaxis().SetRangeUser(self.yrange[0],self.yrange[1])
            SetOverflowBin_Xrange(self.h_data)
            self.h_data.Draw("E1X0 SAME")

        ##debug
        if self.print_info:self.printInfo(stack_histograms,signal_histograms,data_histograms)
        
        ##Draw Legend
        self.mainleg.Draw()
        if not self.pubStyle: self.ratioleg.Draw()

        ##DrawExperimentLabel
        if self.experiment == "CMS":
            expLabel,extraLabel,lumiLabel=setCMSExperimentLabelStyle()
            exp_label_y=0.925
            left_margin =round(self.mainPad.GetLeftMargin(),2)
            right_margin=round(self.mainPad.GetRightMargin(),2)
        elif self.experiment == "ATLAS":
            expLabel,extraLabel,lumiLabel=setATLASExperimentLabelStyle()
            exp_label_y= 0.825
            left_margin =round(self.mainPad.GetLeftMargin(),2)+0.03
            right_margin=round(self.mainPad.GetRightMargin(),2)
        if self.pubStyle:extraTextOffset +=0.02
        expLabel.DrawLatex(left_margin,exp_label_y,self.experiment) #CMS/ATLAS
        extraLabel.DrawLatex(left_margin+extraTextOffset,exp_label_y,self.extraText) #Preliminary/Internal/Simulation
        if self.experiment == "CMS":
            lumiLabel.SetTextAlign(31);
            lumiLabel.DrawLatex(1-right_margin,exp_label_y,self.lumi+" fb^{#minus1} ("+self.energy+")") #138 ifb (13 TeV)
        elif self.experiment == "ATLAS":
            lumiLabel.DrawLatex(left_margin,exp_label_y-0.05,"#sqrt{s} = "+ self.energy+", "+self.lumi+" fb^{#minus1}")

        ##ExtraTextCaption
        for i,textCaption in enumerate(self.extraTextCaption):
            text = ROOT.TLatex()
            text.SetNDC(True)
            text.SetTextSize(0.042 if self.experiment == "ATLAS" else 0.044)
            text.SetTextFont(42)
            offset = (i+2)*0.05
            text.DrawLatex(left_margin,exp_label_y-offset,textCaption)
        
        ##Redraw axis
        ROOT.gPad.RedrawAxis()
        self.mainPad.SetTickx(1)
        self.mainPad.SetTicky(1)
        self.mainPad.Update()

        ##safety if h_totbkg and h_data is None
        ##Set some default for them to avoid runtime error
        if self.h_totbkg==None:self.h_totbkg=self.createPlaceHolderHisto(self.histogram[0][-1].Clone())
        #if self.h_data == None:self.h_data=self.h_totbkg.Clone("h_data_placeholder")
        
            
        ##RatioPad
        self.ratioPad.cd()
        if self.h_data!=None:
            self.h_ratio=self.h_data.Clone("h_ratio")
            
        if self.h_totbkg!=None and self.h_ratio!=None:
            self.h_ratio.Divide(self.h_totbkg)

        if self.h_ratio!=None:
            RatioHistoStyle(self.h_ratio,self.xlabel,self.ylabel_ratio)
            self.h_ratio.GetXaxis().SetRangeUser(self.xrange[0],self.xrange[1])
            self.h_ratio.GetYaxis().SetRangeUser(self.yrange_ratio[0],self.yrange_ratio[1])
            self.h_ratio.GetXaxis().SetTickSize(0.08)
            ##handle cases for bin content=0
            for i in range(1,self.h_ratio.GetNbinsX()+1):
                if(self.h_ratio.GetBinContent(i)):
                    self.h_ratio.SetBinError(i, self.h_ratio.GetBinError(i))
                else:
                    self.h_ratio.SetBinError(i,0.000001)
                    self.h_ratio.SetBinContent(i,-10)

        else:
            self.h_ratio = self.h_totbkg.Clone("h_ratio")
            RatioHistoStyle(self.h_ratio,self.xlabel,self.ylabel_ratio)
            self.h_ratio.SetMarkerSize(0)
            self.h_ratio.SetFillColor(0)
            self.h_ratio.SetLineColor(ROOT.kGray+1)
            self.h_ratio.SetLineStyle(ROOT.kDotted)
            self.h_ratio.GetXaxis().SetRangeUser(self.xrange[0],self.xrange[1])
            self.h_ratio.GetYaxis().SetRangeUser(self.yrange_ratio[0],self.yrange_ratio[1])
            self.h_ratio.GetXaxis().SetTickSize(0.08)
            for i in range(1,self.h_ratio.GetNbinsX()+1):
                self.h_ratio.SetBinContent(i,1)
                self.h_ratio.SetBinError(i,0)
            
                    
        ###Uncertainty band in ratio pad
        #self.yerr_ratio= ROOT.TGraphAsymmErrors()
        #self.yerr_ratio.Divide(self.h_data, self.h_totbkg, 'pois') ##pois
        #for i in range(1,self.yerr_ratio.GetN()+1):
        #    self.yerr_ratio.SetPointY(i,1)                
        self.yerr_ratio=mc_uncertainty_band_ratio(self.h_totbkg)
        
        RatioHistoStyle(self.yerr_ratio,self.xlabel,self.ylabel_ratio)
        self.yerr_ratio.SetLineWidth(100)
        self.yerr_ratio.SetMarkerSize(0)
        self.yerr_ratio.SetFillStyle(unc_fstyle)
        self.yerr_ratio.SetFillColor(unc_fcolor)
        self.yerr_ratio.GetYaxis().SetRangeUser(self.yrange_ratio[0],self.yrange_ratio[1])
        self.yerr_ratio.GetXaxis().SetLimits(self.xrange[0],self.xrange[1])
        #self.yerr_ratio.GetXaxis().SetTickSize(0.1)

        if self.debug:
            print("h_ratio:",self.h_ratio)
            print("yerr_ratio:",self.yerr_ratio)
        
        self.h_ratio.DrawCopy("E1X0")
        self.yerr_ratio.Draw("E2 SAME")
        self.h_ratio.DrawCopy("E1X0 SAME")
        self.ratioPad.SetTickx(1)
        ROOT.gPad.RedrawAxis()
        self.ratioPad.Update()
        
        
        self.canvas.Update()
        self.canvas.Draw()
        
        
    def savefig(self,filename):
        self.canvas.Print(f"{filename}")
