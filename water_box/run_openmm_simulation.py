# This script was generated by OpenMM-Setup on 2022-04-13.

from openmm import *
from openmm.app import *
from openmm.unit import *

# Input Files

pdb = PDBFile('water-processed.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

# System Configuration

nonbondedMethod = CutoffPeriodic
nonbondedCutoff = 1*nanometers
constraints = None
rigidWater = False

# Integration Options

dt = 0.001*picoseconds
temperature = 300*kelvin
friction = 1/picosecond
pressure = 1*atmospheres
barostatInterval = 10

# Simulation Options

steps = 50000
equilibrationSteps = 100
platform = Platform.getPlatformByName('CPU')
dcdReporter = DCDReporter('water.dcd', 10)
dataReporter = StateDataReporter('water.out', 10, totalSteps=steps,
    step=True, time=True, potentialEnergy=True, kineticEnergy=True, totalEnergy=True, temperature=True, volume=True, density=True, separator='\t')

# Prepare the Simulation

print('Building system...')
topology = pdb.topology
positions = pdb.positions
system = forcefield.createSystem(topology, nonbondedMethod=nonbondedMethod, nonbondedCutoff=nonbondedCutoff,
    constraints=constraints, rigidWater=rigidWater)
system.addForce(MonteCarloBarostat(pressure, temperature, barostatInterval))
integrator = LangevinMiddleIntegrator(temperature, friction, dt)
simulation = Simulation(topology, system, integrator, platform)
simulation.context.setPositions(positions)

# Write XML serialized objects

with open("waterxml", mode="w") as file:
    file.write(XmlSerializer.serialize(system))

# Minimize and Equilibrate

print('Performing energy minimization...')
simulation.minimizeEnergy()
print('Equilibrating...')
simulation.context.setVelocitiesToTemperature(temperature)
simulation.step(equilibrationSteps)

# Simulate

print('Simulating...')
simulation.reporters.append(dcdReporter)
simulation.reporters.append(dataReporter)
simulation.currentStep = 0
simulation.step(steps)

# Write file with final simulation state

simulation.saveState("final")