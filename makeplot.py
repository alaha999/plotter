import pyplotlib.pyplot as plot
import ROOT
import random,math
from collections import defaultdict
import yaml
import os,sys,argparse

## no-runtime-window-display
ROOT.gROOT.SetBatch(True)

## read yaml file
def read_yaml_file(filename):
    with open(f'{filename}', 'r') as file:
        yaml_data = yaml.safe_load(file)
        
    return yaml_data

## fetch histogams
def get_histograms(filename,samplename,histoname):
    print("############ processing sample : ",samplename)
    print("############ processing file   : ",filename)
    print("############ processing histo  : ",histoname)
    print()
    rootfile = ROOT.TFile.Open(filename,'READ')
    histo = rootfile.Get(f"{histoname}")
    histo.SetDirectory(0)
    histo.SetName(samplename)
    rootfile.Close()
    return histo.Clone()

## prepare data for plotting
def preprocess_info(yaml_data,variable_name):
    histogramdir = yaml_data["general"]["input_path_histograms"]
    plotdict=defaultdict(dict)
    for item in yaml_data["samples"]:
        processname = item["name"]
        if processname in yaml_data["samples_to_run"]:
            filepath = item["file_path"]
            if filepath == "auto":
                filepath = f"{processname}.root"
            color_opt  = item["color"]
            fill_opt   = item["fill"]
            stack_opt  = item["stack"]
            isData_opt = item["isData"]
            legend_name= item["legend_name"]
            histo = get_histograms(f"{histogramdir}{filepath}",processname,variable_name)
            plotdict[f"{processname}"]=[filepath,color_opt,fill_opt,stack_opt,isData_opt,legend_name,processname,histo.Clone()]

    return plotdict

## plot SoverRootB
def get_significance_hist(h_sig,h_bkg):
    h_sb = h_sig.Clone(f"h_sb_{h_sig.GetName()}")
    nbins = h_sb.GetNbinsX()
    for binno in range(1,nbins+1):
        h_sb.SetBinContent(binno,0)
        h_sb.SetBinError(binno,0)
        #compute S/rootB
        if(h_bkg.Integral(binno,nbins)):
            value_sb = h_sig.Integral(binno,nbins)/math.sqrt(h_bkg.Integral(binno,nbins))
        else:
            value_sb = 0

        #fill the bins with s/rootB value    
        h_sb.SetBinContent(binno,value_sb)

    return h_sb

## draw histograms
def make_plot(plotdict,yaml_data,region_config,plot_config):
    plt = plot.Plotter()
    plt.setExperiment(yaml_data["general"]["experiment"])
    plt.setExtraText(yaml_data["general"]["extratext"])
    plt.setEnergy(yaml_data["general"]["energy"])
    plt.setYear(yaml_data["general"]["year"])
    plt.setLumi(yaml_data["general"]["lumi"])
    plt.setPubStyle(yaml_data["general"]["pubstyle"])
    plt.debug=yaml_data["general"]["debug_level"]
    plt.print_info=yaml_data["general"]["print_info_table"]
    if plt.debug:plt.show()
    
    #canvas
    plt.figure(canvName="example_atlas_plot")    

    #histograms
    for key,item in plotdict.items():
        color_opt   = item[1]
        fill_opt    = item[2]
        stack_opt   = item[3]
        isData_opt  = item[4]
        legend_name = item[5]
        process     = item[6]
        histo       = item[-1]
    
        if not isData_opt:
            plt.hist(histo,color=color_opt,label=legend_name,fill=fill_opt,stack=stack_opt,isData=isData_opt,density=plot_config["density"])
        if isData_opt and plot_config["plotdata"]:
            plt.hist(histo,color=color_opt,label=legend_name,lwidth=1,ls=0.7,fill=fill_opt,stack=stack_opt,isData=isData_opt,density=plot_config["density"])

    ##plot-cosmetics
    plt.set_xaxis(plot_config["xlabel"],xrange=tuple(plot_config["xrange"]))
    plt.set_yaxis(plot_config["ylabel"],yrange=tuple(plot_config["yrange"]))
    plt.set_yaxis_ratio(plot_config["ratio_ylabel"],yrange=tuple(plot_config["ratio_yrange"]))
    plt.legend(plot_config["legend_position"],fontsize=plot_config["legend_fontsize"],col=plot_config["legend_column"])
    for extra_text in (plot_config["extra_text"]+region_config["extra_text"]):
        plt.set_extraTextCaption(extra_text)
        
    plt.Draw(
        logY=plot_config["logy"],
        rebin=plot_config["rebin"],
        unc_fstyle=plot_config["unc_fstyle"],
        unc_fcolor=eval(plot_config["unc_fcolor"]),
        extraTextOffset=plot_config["extraTextOffset"],
        sortLegend=plot_config["sortLegend"]
    )

    ##plot significance
    if yaml_data["general"]["plot_ratio_significance"]:
        plt.ratioPad.cd()
        for i,item in enumerate(plt.histogram):
            if not item[1] and not item[2]:
                h_sig = item[-1]
                h_bkg = plt.h_totbkg
                h_sb  = get_significance_hist(h_sig,h_bkg)
                h_sb.DrawCopy("HIST SAME")
                
                
                
    ##store output
    output_folder= region_config["output_folder"]
    if plot_config["savefig"]:
        plt.savefig(output_folder+"/"+"example_"+plot_config["name"]+'_'+region_config["name"]+".png")
        plt.savefig(output_folder+"/"+"example_"+plot_config["name"]+'_'+region_config["name"]+".pdf")


    print("DONE!")
    #display(Image(f"output_plotter/histogramsv4/example_{variable_name}_tagger_stack.png"))
            

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config"                   ,help="configuration file for plotting")
    parser.add_argument("--inputdir" ,default = None , help="input path of the directory containing files")
    parser.add_argument("--samples"  ,default = None , help="string separated samples list")
    parser.add_argument("--test"     ,default = False,help="test the script for a few plots")
    args = parser.parse_args()
    return args

if __name__=="__main__":

    #parse args
    args=argument_parser()
    
    #read yaml data
    yaml_data = read_yaml_file(args.config)
    #print(yaml_data)

    #overwrite yaml_data from args
    if args.inputdir is not None:
        yaml_data["general"]["input_path_histograms"] = args.inputdir
    if args.samples is not None:
        yaml_data["samples_to_run"]= args.samples.strip(" ").split(",")
    else:
        yaml_data["samples_to_run"]=[item["name"] for item in yaml_data["samples"]]

    print()
    print("############ samples to run: ",yaml_data["samples_to_run"])
        
    ##create output folder
    input_folder_name = yaml_data["general"]["input_path_histograms"].split("/")[-2]
    output_folder=yaml_data["general"]["output_path_plots"]+"/"+input_folder_name+"/"+yaml_data["general"]["output_subfolder"]
    yaml_data["general"]["output_folder"]=output_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    ##plot variables and regions
    for region_config in yaml_data["region"]:
        print()
        ##save plots in per region subfolder
        region_config["output_folder"]=yaml_data["general"]["output_folder"]+f"/{region_config['name']}/"
        if not os.path.exists(region_config["output_folder"]):
            os.makedirs(region_config["output_folder"])
            
        print(f"############ plotting for region : {region_config['name']} {region_config['extra_text']}")
        for histogram_config in yaml_data["variable"]:
            print("############ fetching histogram : ",histogram_config["name"])
            histoname=os.path.join(histogram_config["root_file_folder"],histogram_config["name"])
            plotdict=preprocess_info(yaml_data,histoname+"_"+region_config["name"])
            #print(plotdict)
            make_plot(plotdict,yaml_data,region_config,histogram_config)
            if args.test: break
            
    print("ALL DONE!")
    print("SUCCESS!")
