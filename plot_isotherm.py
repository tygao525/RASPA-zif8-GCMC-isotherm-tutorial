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
