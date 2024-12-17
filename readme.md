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
for out in out.000*.c4; do cfour_parser -j $out | jq > ${out%%.c4}.json; done
for out in out.000*.c4; do cfour_proc/print_roots.py -j ${out%%.c4}.json | jq > ${out%%.c4}.roots.json; done
```
Run
```bash
python src/get_points.py out*.roots.json --pick_states <state_name>=<state_number>... | jq > sample_data/model_mode_raw.json
python src/sanitize_points.py sample_data/model_mode_raw.json | jq > sample_data/model_mode.json
```
You can view the adiabatic surfaces using 
```bash
python src/plot_points.py <model_mode.json>
```
To find the diabatic expansion parameters use
```bash
# Before use edit the value of the diabatic coupling in the fit_kdc file
# lambda1AB
python ./src/fit_kdc.py <model_mode.json> --verbose
# or 
python ./src/fit_kdc.py <model_mode.json> --json | jq > sample_data/model_mode_kappas.json
```
If you use the second option, you can view the fitting resutls with
```bash
python src/plot_points.py --kappas sample_data/model_kappas.json sample_data/model.json
```

## Example
Using the sample data for pyrazine coupling the first and second bright excited
states
```bash
python src/fit_kdc.py --json ./sample_data/pyrazine/1B3u+1B2u+nu8/1B3u+1B2u+nu8.json
```
the model produces the fitted diabatic expansion coefficies
```json
{
  "kappa1A": 0.0006979295527113924,
  "kappa2A": 651.9440166138535,
  "kappa1B": 0.0008868137608524403,
  "kappa2B": 861.3966128591228
}
```
The fitting-quality can be easily checked using 
```bash
python src/plot_points.py --kappas_json sample_data/pyrazine/1B3u+1B2u+nu8/1B3u+1B2u+nu8_kappas.json sample_data/pyrazine/1B3u+1B2u+nu8/1B3u+1B2u+nu8.json
```
The above commond produces the figure below, which shows the ab initio data
(solid lines) agains the fitted potential (dots)
[Only one coupling mode](sample_data/pyrazine/1B3u+1B2u+nu8/scan_vs_fit.pdf)
