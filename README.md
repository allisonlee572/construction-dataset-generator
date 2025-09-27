
# Construction Dataset Generator

A **BlenderProc-based synthetic dataset generator** for construction site objects such as workers, helmets, and equipment.

## Project Structure

construction-dataset-generator/

│── configs/ # YAML config files for assets, labels, lighting, camera

│── generator/ # Core generator code

│── scripts/ # Scripts to run the generator

│── assets/ # Place your 3D models here

│── output/ # Generated datasets (COCO + HDF5)


## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Place assets
Put your .obj models under assets/models/...
### 3. Run generator
python scripts/run_generator.py
### 4. Outputs
* RGB images (.png)
* Segmentation maps
* COCO annotations
* HDF5 files

Generated datasets will appear under output/0001/


## Configuration
Modify configs/default.yaml to:
* Add/remove assets
* Adjust scales
* Configure lighting and camera parameters
*  Extend label mappings

## Accomplishments
* Modularized the dataset generator
* Configurable asset loading and rendering
* Automatic COCO + HDF5 output
* Utility for absolute texture path conversion
* Clean, reusable project layout

## Next Steps
* Support for background buildings
* Add Dockerfile for reproducibility 
* CI/CD piepline for automated testing