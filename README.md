Matplotlib style ROOT-backend plotting package

- YAML config based plotting
- minimal: `python3 makeplot.py --config configs/test_config.yaml`
- For more options check `makeplot.py` macro

Usage:

```
usage: makeplot.py [-h] [--config CONFIG] [--inputdir INPUTDIR] [--samples SAMPLES] [--test] [--stack]

options:
  -h, --help           show this help message and exit
  --config CONFIG      configuration file for plotting
  --inputdir INPUTDIR  input path of the directory containing files
  --samples SAMPLES    string separated samples list
  --test               test the script for a few plots
  --stack              enable stack plot settings with this flag

```

Unit-test:

- jupyter notebook: `unittest_pyplotlib.ipynb` (look at the demo! It is fun!)
- TODO: Github actions workflow or CI/CD pipeline

What you can do with it:

- publication level plot (CMS/ATLAS)
- overlay of any samples
- usual background stack, signal overlaid, data overlaid style plotting
- Flexible binning
- Signal significance study (S/rootB in ratio plot added now in `makeplot.py` macro!)

Wishlist:

- TGraph (limit plots!)
- anything else
- Improving coding style/pip installation may be

Example plot:

![example plot dummy variable](example_dummyvar_base.png)