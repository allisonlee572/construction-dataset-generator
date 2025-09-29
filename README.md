
# Construction Dataset Generator

A **BlenderProc-based synthetic dataset generator** for construction site objects such as workers, helmets, and equipment.

## Project Structure

construction-dataset-generator/

│── scripts/ # Script to run the generator

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
blenderproc run scripts/run_generator.py
### 4. Outputs
* RGB images (.png)
* Segmentation maps
* COCO annotations
* HDF5 files
* To visualize: blenderproc vis coco -i [image_index] -c coco_annotations.json -b output/0001

Generated datasets will appear under output/0001/

## Next Steps
* Create config, utilities, other files to clean code structure
* Support for background buildings
* Add Dockerfile for reproducibility 
* CI/CD piepline for automated testing