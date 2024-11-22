# KDC Hamitonian parameters
These scripts find the diabatic potential along coupling modes in the KDC
Hamiltonian. The input requires the linear diabatic coupling (lambda) and the
adiabatic surfaces along both of the coupled states.

## How to use this

Run the pes with cfour as described in the templates/cfour/pes_something.c4
file.

Get as the outcome a series of out.xxxxx.c4 files with the enrgies. Run them
through the `cfour_parser -j` and `cfour_proc/print_roots.py -j` to get a set
of `out.xxxxx.root.json` files. 
```bash
for out in  out.000*.c4; do cfour_parser -j $out | jq >  ${out%%.c4}.json; done
for out in  out.000*.c4; do cfour_proc/print_roots.py -j ${out%%.c4}.json | jq > ${out%%.c4}.roots.json; done
```
Run
```bash
python src/get_points.py out*.root.json | jq > sample_data/model_mode.json
python src/sanitize_points.py sample_data/model_mode.json | jq > sample_data/model_mode_cm.json
```
Feed the last file to the `src/fit_kdc.py` script. Other scripts in `src` can
disply the outcome.

## Adiabatic surface for pyrazine
[Only one coupling mode](sample_data/pyrazine/nu8.pdf)
