SALT3 Model Realization Training

The goal of this stage is to produce a nominal SALT3 model (SALT3.MODEL000) along with a set of intentionally biased model realizations, 
each trained under a different random photometric calibration perturbation. These biased realizations are later propagated through the Pippin
pipeline as fitting options (FITOPTS) to estimate calibration-driven systematic uncertainties.

1.1 Generating Calibration Shift Files

Before any training happens, the calibration systematics that will be applied to each biased SALT3 model realization is generated with 

create_calib_shift_file.py

The script uses the following templates as input: 
  1. calib_saltshaker_template.txt  (for combined LSST + Roman calibration template)
  2. calib_saltshaker_template_roman_only.txt (for Roman-only calibration template)
  3. calib_saltshaker_template_lsst_only.txt  (for LSST-only calibration template)

Running create_calib_shift_file.py on these templates produces the full set of calib_nominal_*.txt SHIFTLIST_FILEs (one per biased realization) each
containing a random MAGSHIFT/WAVESHIFT combination for the relevant survey/band. These are the files referenced later under the TRAINOPT block of

Submit_trainsalt3.config 



1.2 GENERATING SALT3 MODEL TRAINING DATASETS (Light curves as well as prism spectra)

To simulate LSST SNe, do

   snlc_sim.exe SIMGEN_LSST.input   (see further instructions in SIMGEN_LSST.input)

To simulate Roman SNe (both light curves and prism spectra)

    snlc_sim.exe SIMGEN_Roman.input   (further instructions in SIMGEN_Roman.input)

The above will produce LSST_LC_simulations.LIST and Roman_LC_simulations.LIST which will be input lists for 'snlists' in SALTShaker_main_file.config (see below).

SALTShaker also requires some initial guesses for 'tmaxlist' and 'snparlist' keys in SALTShaker_main_file.config. 

To generate the file for tmaxlist and snparlist, run:
   snlc_fit.exe FIT_LSST.nml
   snlc_fit.exe FIT_Roman.nml

The nml files will reference the version photometry generated for each survey. The runs above will output FIT_LSST.FIRES and FIT_Roman.FITRES files, from which one can
use 'tmax_extractor.py' and 'snparlist_extractor.py' scripts to extract the lists for 'SN_peak_MJD.list' and 'SN_params.list' keys in SALTShaker_main_file.config. Note 
that both extractor files can take one or more surveys and give a combined SN_peak_MJD.list and SN_params.list for the surveys. The extractor scripts also reference

fitres_utils



1.3 TRAINING CONFIGURATION

The training run is launched from Submit_trainsalt3.config, SNANA-style batch submission file that wraps the actual SALTShaker config file - SALTShaker_main_file.config

Before running Submit_trainsalt3.config, ensure that:

  a. The calib_nominal_*.txt files from 1.1 above are attached (see example in Submit_trainsalt.config)
  b. SALTShaker_main_file.config exists  (Further required files within SALTShaker_main_file.config are indicated with $directory_of_SALTShaker_main_file) 
  c. Necessary snlists exist. 'snlists' key in SALTShaker_main_file.config takes in photometric/spectroscopic data required for training.
  d. The right conda environment is activated: 
  
         conda activate SALTShaker_kene_mod   (or any other SALTShaker environment)
  
To submit Submit_trainsalt3.config, do:

      submit_batch_jobs.sh Submit_trainsalt3.config

At the end of the job, there should be a new directory (SALT3.SYS in the sample attached) containing the newly trained nominal model with all the biased model realizations.
