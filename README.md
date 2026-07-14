# SALT3-model-Calibration-Systematics
Propagating photometric calibration systematics through SALT3 training to dark energy constraints for LSST and Roman (Stage IV) supernova surveys.

This repo contains the pipeline, configuration files, and analysis scripts used to propagate photometric calibration uncertainties through SALT3 light-curve model training and subsequent cosmological inference, for simulated LSST and Roman (Stage IV) supernova surveys. This work is part of the Roman Supernova Project Infrastructure Team (SNPIT) effort to optimize the dark energy figure of merit (FoM).


***A note on the computing environment*** 

The instructions in this repository assume you are running on the University of Chicago Research Computing Center's Midway cluster, where SNANA — along with SALT3, Pippin, and their dependencies — is already installed and configured for general use. We do not provide installation instructions for other systems; if you are working outside Midway, please refer to the SNANA documentation for setup on your own system.


***Overview***


Most previous forecasts propagate calibration systematics only through light-curve fitting. Here, we additionally propagate calibration uncertainties through the SALT3 training step itself, training a new SALT3 model from simulated data rather than reusing a fixed model throughout.

The cosmological analysis itself is run with Pippin, the SNANA pipeline driver. SALT3 training with perturbed photometric calibration is done as an external step before Pippin is invoked, and the resulting trained models are passed in as inputs to Pippin's LCFIT stage as fitting options (FITOPTS). This repository documents both halves: the external calibration/training step, and the Pippin configuration used for everything downstream.

Pipeline Overview:

This repository documents the full analysis pipeline used in the paper, split into two stages:

1. SALT3 model realizations training (see instructions in SALT3_training_file attached)
2. Full analysis pipeline via Pippin (see guidelines in pippin_pipeline_file attached) 
