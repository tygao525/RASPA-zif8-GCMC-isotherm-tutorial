# Ethane Adsorption Isotherm in ZIF-8

This tutorial records GCMC workflow on macOS: adapting Widom inputs, calculating four pressure points at 303 K (0.1, 0.2, 0.5, and 1 bar), plotting an absolute adsorption isotherm, and checking longer sampling at 0.5 bar.

**These are preliminary simulations over 0.1–1 bar, not an isotherm covering saturation or a validated reproduction of the published research.**

The figure above shows a Python/Matplotlib plot of the four short runs; the 0.5 bar data point has not been updated to the longer-run result.

## 1. Objective

At a fixed temperature, vary the gas-reservoir pressure and measure the mean ethane uptake in ZIF-8. GCMC allows insertion, deletion, translation, rotation, and reinsertion moves; the number of adsorbed molecules fluctuates.

| Item | Setting |
| --- | --- |
| Framework | ZIF-8，rigid framework |
| Adsorbate | ethane |
| Temperature | 303 K |
| Supercell | 2 × 2 × 2 |
| Short-run initialization | 5,000 cycles |
| Short-run production | 10,000 cycles |
| 0.5 bar Long-run initialization | 50,000 cycles |
| 0.5 bar Long-run production | 100,000 cycles |
| van der Waals cutoff | 12 Å |
| Uptake type | absolute uptake |

Monte Carlo cycles do not represent physical time. `Movies` saves sampled configurations, not a molecular dynamics trajectory.

## 2. Create a folder for each pressure

```text
RASPA/
└── ZIF8_乙烷_GCMC/
    ├── P_0.1bar/
    ├── P_0.2bar/
    ├── P_0.5bar/
    ├── P_1bar/
    └── P_0.5bar_long/
```

First create `P_0.1bar` in Finder. Download the following five files from the original project and create a plain-text `simulation.input` in the same folder:

| File |
| --- | --- |
| `ZIF_08.cif` |
| `ethane.def` |
| `pseudo_atoms.def` |
| `force_field_mixing_rules.def` |
| `force_field.def` |
| `simulation.input` |

## 3. Configure the first pressure point

Open `simulation.input` in VS Code, enter the following, and save.

```text
SimulationType                MonteCarlo
NumberOfCycles                10000
NumberOfInitializationCycles  5000
PrintEvery                    1000
RestartFile                   no

Forcefield                    Local
RemoveAtomNumberCodeFromLabel no
CutOffVDW                     12.0
ChargeMethod                  ewald
EwaldPrecision                1e-6
OmitAdsorbateAdsorbateCoulombInteractions no

Framework 0
FrameworkName                 ZIF_08
UnitCells                     2 2 2

ExternalTemperature           303.0
ExternalPressure              10000

Movies                        yes
WriteMoviesEvery               1000

Component 0 MoleculeName       ethane
            MoleculeDefinition       Local
            TranslationProbability   0.5
            ReinsertionProbability   0.5
            RotationProbability      0.5
            SwapProbability          1.0
            CreateNumberOfMolecules  0
```

| Key setting | Meaning |
| --- | --- |
| `ExternalPressure 10000` | Pressure is in Pa; 10,000 Pa = 0.1 bar |
| `Forcefield Local` | Read the force field from the current folder |
| `MoleculeDefinition Local` | Read the local molecule definition |
| `SwapProbability 1.0` | Enable insertion and deletion moves |
| `CreateNumberOfMolecules 0` | Start without adsorbate molecules; GCMC inserts them |
| `PrintEvery 1000` | Report progress every 1,000 cycles |

Move-probability parameters are relative selection weights, not direct percentages. Initialization helps the system approach equilibrium, but a specified cycle count does not guarantee equilibration.

## 4. Activate the environment and run

In every new terminal session, activate the environment and set the data directory. Confirm that the six input files are present, then execute each line:

```bash
conda activate raspa2
export RASPA_DIR="$CONDA_PREFIX"
cd "$HOME/Desktop/姑苏实验室/RASPA/ZIF8_乙烷_GCMC/P_0.1bar"
```

If `cd` fails, correct the path first. Confirm the prompt starts with `(raspa2)` and the directory is correct, then launch once:

```bash
simulate > run.log 2>&1
```

It is normal to see no terminal output because it is redirected to `run.log`. The prompt returning means the process has exited; check the output to determine whether it succeeded.

## 5. Check completion and uptake

Open the pressure-specific `.data` file in `Output/System_0`. For 0.1 bar it is:

```text
output_ZIF_08_2.2.2_303.000000_10000.data
```

First search for the completion marker, then for uptake:

```text
Simulation finished,  0 warnings
Average loading absolute [mol/kg framework]
```

All four short runs and the latest long run at 0.5 bar reported normal completion with zero warnings. This does not establish model accuracy or sampling convergence.

**1 mol/kg = 1 mmol/g, so the numerical value is unchanged.** Mean molecule counts per simulation box or unit cell may be fractional because they are averages over configurations.

Record **absolute uptake** consistently. `HeliumVoidFraction` was not set; identical excess and absolute values in the output do not establish physical equivalence. Before comparing with experiments, check the reported uptake convention and the relevant pore-volume definition.

## 6. Extend to four pressures

Create a separate folder for each new pressure. Copy only the six inputs, not old `Output`, `Movies`, or `Restart` folders. Change only `ExternalPressure`, retaining the same short-run settings.

| Folder | Pressure (bar) | `ExternalPressure` (Pa) |
| --- | ---: | ---: |
| `P_0.1bar` | 0.1 | 10000 |
| `P_0.2bar` | 0.2 | 20000 |
| `P_0.5bar` | 0.5 | 50000 |
| `P_1bar` | 1.0 | 100000 |

Replace the final folder in the `cd` command with the corresponding pressure folder.

## 7. Four short-run results

These values were checked against the complete local outputs. Error estimates are recorded as reported by RASPA, without relabeling them as standard deviations or standard errors.

| Pressure (bar) | Absolute uptake (mmol/g) | Reported error (mmol/g) |
| --- | ---: | ---: |
| 0.1 | 0.2337928953 | 0.0046151920 |
| 0.2 | 0.4576176813 | 0.0149769379 |
| 0.5 | 1.0999474480 | 0.0435223571 |
| 1.0 | 2.0705703488 | 0.0317378951 |

Data file: [results/isotherm_short.csv](results/isotherm_short.csv).

Uptake increases with pressure without a clear saturation plateau. The earlier Widom coefficient of 2.27757 mol/(kg·bar) gives a linear estimate of 0.227757 mmol/g at 0.1 bar, close to the GCMC value of 0.233793 mmol/g. This is only a low-pressure consistency check.

## 8. Plot with Python

Save the following as `plot_isotherm.py` and run it in a Python environment with Matplotlib installed; the RASPA2 environment need not be modified. Plot absolute uptake on the y-axis with errors in the same units.

```python
import matplotlib.pyplot as plt

pressure = [0.1, 0.2, 0.5, 1.0]
uptake = [0.2337928953, 0.4576176813, 1.0999474480, 2.0705703488]
error = [0.0046151920, 0.0149769379, 0.0435223571, 0.0317378951]

fig, ax = plt.subplots(figsize=(7, 5))
ax.errorbar(pressure, uptake, yerr=error, fmt="s--",
            capsize=4, label="GCMC, 303 K")
ax.set(xlabel="Pressure (bar)", ylabel="Absolute uptake (mmol/g)",
       title="Ethane adsorption in ZIF-8\nPreliminary GCMC results")
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()
fig.savefig("ethane_isotherm_short.png", dpi=300)
plt.show()
```

## 9. Longer sampling at 0.5 bar

Create `P_0.5bar_long`, copy only the inputs, keep pressure at `50000` Pa, and change:

```text
NumberOfCycles                100000
NumberOfInitializationCycles  50000
```

This means 50,000 initialization cycles followed by 100,000 production cycles, totaling 150,000 cycles. 

| 0.5 bar Run | Uptake (mmol/g) | Reported error (mmol/g) | Record |
| --- | ---: | ---: | --- |
| Short run | 1.0999474480 | 0.0435223571 | Complete output |
| First long run | 1.1147051010 | 0.0051439116 | Screenshot only; output overwritten by rerun |
| Latest long run | 1.1116739354 | 0.0057693073 | Complete output |

Data file: [results/convergence_0.5bar.csv](results/convergence_0.5bar.csv).

The latest long run has a relative reported error of approximately 0.52%; the two long-run means differ by approximately 0.27%. This supports preliminary repeatability, but a single-pressure check does not establish convergence of the entire isotherm. Random seeds were not recorded, so these runs are not a documented independent-replicate design.
