# Bio-Inspired Codec

A bio-inspired video **CODEC** built from a custom **Spiking Neural Network (SNN)** in [NEST Simulator](https://www.nest-simulator.org/). A video is split into image frames and an audio track, both are encoded into spike trains, passed through multiple layers with an injected noise layer and lateral inhibition, and then decoded back into frames and audio. Reconstruction error is quantified with spike metrics.

Built for **COMP40731 – Artificial Cognitive Systems** (Nottingham Trent University).
Author: Bhagyesh Chaudhari

---

## How it works

```
Video (.mp4)
   ├─ Frames (.png) ──► Image encoding (RGB, 3 layers) ──► spikes ─┐
   └─ Audio (.mp3)  ──► Sound encoding (left/right)    ──► spikes ─┤
                                                                   ▼
                          Noise layer (Poisson) + lateral inhibition + learning (STDP / ReSuMe)
                                                                   ▼
                       Spike normalisation ──► Image / sound decoding ──► reconstructed_video.mp4
```

- **Neuron model:** `iaf_psc_alpha` throughout.
- **Image encoding:** frames resized to 200×300; each pixel intensity is mapped to an input current (`I_e = intensity + 380`) and encoded by one neuron per pixel per colour channel (B, G, R) across three layers with one-to-one connections.
- **Sound encoding:** audio is cut into 1/30 s chunks (one per video frame), with separate neuron populations for the left and right channels, simulated for 50 ms per chunk.
- **Noise:** a `poisson_generator` noise layer (10 Hz) is injected after encoding.
- **Learning:** lateral inhibition with static synapses, STDP synapses, and ReSuMe-style supervised training with a teaching layer (`stdp_triplet_synapse`).
- **Error measurement:** a Victor–Purpura-style spike-train distance.

## Repository contents

The full pipeline is in the notebook, and the same code is also split into one script per stage.

| File | Purpose |
| --- | --- |
| `COMP40731 - ACS - CWK - N1218683.ipynb` | **Main notebook** containing the complete pipeline end to end |
| `Assessment.py` | Opens the source video with OpenCV and reads it frame by frame (a quick check that the video loads; press `q` to stop) |
| `Split_Video_audio.py` | Extracts frames and the audio track from the video |
| `audio.mp3` | Audio extracted from the source video |
| `COMP40731_video.mp4/` | Folder containing the source video |
| `image_encoding.py` | Encodes frames into spikes (HDF5 + NPY output) |
| `sound_encoding.py` | Encodes audio chunks into spikes (HDF5 + NPY output) |
| `current_spikes_values.py` | Builds the current-to-spike-count lookup table used for sound |
| `propagation_delay.py` | Measures the delay through the three-layer chain |
| `image_normalise_2d.py` / `img_normalise_3d.py` | Convert image spikes into binary spike-pattern matrices |
| `image_decoding.py` | Recovers pixel intensities from spike patterns |
| `sound_decoding.py` | Recovers audio amplitudes from spike counts |
| `snn_architecture.py`, `snn_stdp_synapses.py`, `snn_without_enhibition_static-synapses.py`, `snn_WLH_raster_plot.py` | Network variants with/without lateral inhibition, static and STDP synapses, with raster plots |
| `snn_without_LH_ReSuMe.py`, `snn_LH_trainin-ReSuMe.py` | ReSuMe training without and with lateral inhibition |
| `inference_using_pretrained.py` | Runs the network with saved, pre-trained weights |
| `reconstructed_video.py` | Writes the reconstructed frames to an MP4 |

## Data formats

| Format | Used for |
| --- | --- |
| HDF5 (`.h5`) | Encoded spike senders and times for images and sound |
| NPY (`.npy`) | Audio data, calibration table, normalised spike matrices, trained SNN weights |
| PNG / MP3 / MP4 | Extracted frames, audio, and the reconstructed video |

## Requirements

- Python 3.8+
- [NEST Simulator](https://nest-simulator.readthedocs.io/) 3.x (PyNEST)
- `numpy`, `matplotlib`, `h5py`, `opencv-python`, `pydub`, `scipy`, `tqdm`
- `ffmpeg` (used by `pydub` for audio)
- Jupyter Notebook or JupyterLab

```bash
pip install numpy matplotlib h5py opencv-python pydub scipy tqdm jupyter
conda install -c conda-forge nest-simulator
```

## Getting started

```bash
git clone https://github.com/bhagyotic15/Bio-Inspired-Codec.git
cd Bio-Inspired-Codec
```

1. **Update the video path.** The notebook and scripts use a hard-coded local path (`/home/ntu-user/PycharmProjects/...`). Change it to the location of `COMP40731_video.mp4` on your machine.
2. Create the output folders the code writes to:
   ```bash
   mkdir -p frames sounds sound_results image_encoding_results raster_plots_img \
            normalised_mat_results sound_normalise_3d snn_architecture_result \
            reconstructed_video
   ```
3. Run the notebook top to bottom, or run the scripts in this order:
   1. `Split_Video_audio.py`
   2. `image_encoding.py`, `current_spikes_values.py`, `sound_encoding.py`
   3. `image_normalise_2d.py`, `img_normalise_3d.py`
   4. SNN scripts (`snn_*.py`)
   5. `image_decoding.py`, `sound_decoding.py`
   6. `reconstructed_video.py`

> Encoding every pixel as a spiking neuron is slow and memory-heavy, so the code processes a limited number of frames (e.g. `frame_021`–`frame_030`) and the first 10 audio chunks by default.

## Acknowledgements

Simulation by [NEST Simulator](https://www.nest-simulator.org/). Developed as coursework for COMP40731 Artificial Cognitive Systems.
