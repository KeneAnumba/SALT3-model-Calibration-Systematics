# SALT3-model-Calibration-Systematics
Propagating photometric calibration systematics through SALT3 training to dark energy constraints for LSST and Roman (Stage IV) supernova surveys.

This repo contains the pipeline, configuration files, and analysis scripts used to propagate photometric calibration uncertainties through SALT3 light-curve model training and subsequent cosmological inference, for simulated LSST and Roman (Stage IV) supernova surveys. This work is part of the Roman Supernova Project Infrastructure Team (SNPIT) effort to optimize the dark energy figure of merit (FoM).

Overview

Most previous forecasts propagate calibration systematics only through light-curve fitting. Here, we additionally propagate calibration uncertainties through the SALT3 training step itself, training a new SALT3 model (an empirical model for standardizing Type Ia supernovae light curves) from simulated data at each stage of the pipeline rather than reusing a fixed model throughout. We trace the impact of these systematics from SALT3 training → light-curve fitting → BBC bias correction → constraints on the dark energy equation of state (w0​,wa​).


Pipeline stages:
Simulated photometry (SNANA)
        │
        ▼
Photometric calibration perturbation  ──►  [see pipeline/prism_calibration/]
        │
        ▼
SALT3 model training  ──►  [see pipeline/training/]
        │
        ▼
Light-curve fitting (SALT3)
        │
        ▼
BBC bias correction  ──►  [see pipeline/cosmology_fit/]
        │
        ▼
w0, wa constraints / FoM


Repository structure:
├── configs/
│   ├── salt3_training/      # Exact configuration files used to train SALT3 at each iteration
│   ├── snana_sim/           # SNANA simulation input files for LSST and Roman
│   └── bbc/                 # BBC configuration for bias corrections
├── pipeline/
│   ├── prism_calibration/   # Treatment of Roman prism spectrophotometric calibration
│   ├── training/            # Scripts orchestrating SALT3 training runs
│   └── cosmology_fit/       # BBC + cosmology fitting scripts
├── figures/                 # Scripts to regenerate every paper figure from saved outputs
├── docs/
│   └── reproducibility.md   # Step-by-step reproduction guide, figure-by-figure
├── environment.yml
└── README.md


