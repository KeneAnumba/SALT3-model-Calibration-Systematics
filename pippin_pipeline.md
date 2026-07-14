# Pippin

Pippin is the pipeline-orchestration tool used across the DES/Roman/LSST supernova-cosmology community to chain together 
the many individual SNANA jobs that turn a survey strategy into a cosmological measurement. Rather than manually scripting 
and sequencing each SNANA program, Pippin reads a single YAML "task" file that declares each stage of the analysis and how 
its outputs feed into the next stage, then handles job submission (SLURM sbatch), dependency tracking, and re-running only what's changed.

Pippin organizes the jobs and their outputs in different stages (1_SIM,2_LCFIT, 3_CLAS, 4_MERGE, 5_AGG, 6_BIASCOR, 7_COV, 8_COSMOFIT) under a single
run directory. Furthermore, later stages reference earlier ones by the task names defined in the YAML. Also, Pippin resolves the directory paths and job dependencies automatically.
For further details on pippin, see below:

[Pippin stages](https://github.com/dessn/PIPPIN)

## Pippin Input Files
The top level files are:
  1. pippin_config files - pippin_bcor_config.yml and pippin_analysis_config.yml
  2. inp_base_analysis.yml
  3. inp_base_bcor+train.yml
  4. inp_base_include.yml

To run the config files:

```bash
pippin.sh pippin_bcor_config.yml >& bcor.log &
```
```bash
pippin.sh pippin_analysis_config.yml >& analysis_config.log &
```
The above commands will give one back the control of their screen as well as output any errors in .log files.

