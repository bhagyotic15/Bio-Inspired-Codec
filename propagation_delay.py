import matplotlib.pyplot as plt
import numpy as np
import nest

# Reset NEST kernel
nest.ResetKernel()

# Set simulation parameters
propagation_delay=13.0 #See below how to get the propagation delay
sim_time = 50.0+propagation_delay# in milliseconds
offset = 380  # Offset value for analog input
# Define the analog values from 0 to 255
min_analog_value = 0 + offset
max_analog_value = 255 + offset
num_neurons = 256

# Create neuron populations
L1_neurons = nest.Create("iaf_psc_alpha", num_neurons)
L2_neurons = nest.Create("iaf_psc_alpha", num_neurons)
L3_neurons = nest.Create("iaf_psc_alpha", num_neurons)

ind=0
for value in range(min_analog_value, max_analog_value):
    # Set current for each neuron
    nest.SetStatus(L1_neurons[ind], {"I_e": value})
    ind+=1

# Connect neurons with one-to-one connections
for idx in range(num_neurons):
    nest.Connect(L1_neurons[idx], L2_neurons[idx], "one_to_one", syn_spec={"weight": 1200.0})  # 800.0 is a high synaptic weight to perform by-pass
    nest.Connect(L2_neurons[idx], L3_neurons[idx], "one_to_one", syn_spec={"weight": 1200.0})

# Create spike recorder
spikerecorder_L1 = nest.Create("spike_recorder")
spikerecorder_L2 = nest.Create("spike_recorder")
spikerecorder_L3 = nest.Create("spike_recorder")

# Connect spike recorder to neurons
nest.Connect(L1_neurons, spikerecorder_L1)
nest.Connect(L2_neurons, spikerecorder_L2)
nest.Connect(L3_neurons, spikerecorder_L3)


# Simulate network
nest.Simulate(sim_time)


# Get spike events from spike recorders
spike_events_L1 = nest.GetStatus(spikerecorder_L1, "events")[0]
spike_events_L2 = nest.GetStatus(spikerecorder_L2, "events")[0]
spike_events_L3 = nest.GetStatus(spikerecorder_L3, "events")[0]
senders_L1 = spike_events_L1["senders"]
ts_L1 = spike_events_L1["times"]
senders_L2 = spike_events_L2["senders"]
ts_L2 = spike_events_L2["times"]
senders_L3 = spike_events_L3["senders"]
ts_L3 = spike_events_L3["times"]

print("Propagation delay between L1 and L2:",(ts_L2[0]-ts_L1[0]),"ms.")
print("Propagation delay between L2 and L3:",(ts_L3[0]-ts_L2[0]),"ms.")
print("Propagation delay between L1 and L3:",(ts_L3[0]-ts_L1[0]),"ms.")

# Output
# Propagation delay between L1 and L2: 7.0 ms.
# Propagation delay between L2 and L3: 6.0 ms.
# Propagation delay between L1 and L3: 13.0 ms.


# Plot raster plot with different colors per layer
plt.figure(figsize=(10, 6))

# Plot spikes for Layer 1
senders_L1 = spike_events_L1["senders"]
ts_L1 = spike_events_L1["times"]
plt.vlines(ts_L1, senders_L1, senders_L1 + 1, color='red', label='Layer 1')

# Plot spikes for Layer 2
senders_L2 = spike_events_L2["senders"]
ts_L2 = spike_events_L2["times"]
plt.vlines(ts_L2, senders_L2, senders_L2 + 1, color='green', label='Layer 2')

# Plot spikes for Layer 3
senders_L3 = spike_events_L3["senders"]
ts_L3 = spike_events_L3["times"]
plt.vlines(ts_L3, senders_L3, senders_L3 + 1, color='blue', label='Layer 3')

plt.xlabel('Time (ms)')
plt.ylabel('Neuron Index')
plt.title('Raster Plot')
plt.legend()
plt.grid()
plt.show()

