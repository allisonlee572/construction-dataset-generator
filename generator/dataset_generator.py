import blenderproc as bproc
import numpy as np
import os
from pathlib import Path
from .config import load_config
from .utils import convert_relative_to_absolute


class ConstructionDatasetGenerator:
    def __init__(self, config_path: str = "configs/default.yaml"):
        self.config = load_config(config_path)
        self.scene_objects = []

        self.label_id_mapping = bproc.utility.LabelIdMapping.from_dict(self.config["labels"])
        bproc.init()
        self.load_assets()
        self.setup()

    def load_single_asset(self, obj_file, category_id, scale=1.0):
        convert_relative_to_absolute(obj_file)
        objs = bproc.loader.load_obj(obj_file)

        for obj in objs:
            obj.set_cp("category_id", category_id)
            obj.set_scale([scale, scale, scale])

        self.scene_objects.append(objs)

    def load_assets(self):
        for asset in self.config["assets"]:
            self.load_single_asset(asset["path"], asset["category_id"], asset.get("scale", 1.0))

    def setup(self):
        ground = bproc.object.create_primitive('PLANE', scale=[20, 20, 1])
        ground.set_location([0, 0, 0])
        ground.set_cp("category_id", 0)

        light = bproc.types.Light()
        light.set_location([2, -2, 0])
        light.set_energy(self.config["lighting"]["energy"])

        cam_pose = bproc.math.build_transformation_mat(
            self.config["camera"]["location"],
            self.config["camera"]["rotation"]
        )
        bproc.camera.add_camera_pose(cam_pose)

        bproc.renderer.enable_segmentation_output(map_by=["category_id", "instance", "name"])

    def place_assets_randomly(self):
        for objs in self.scene_objects:
            x = np.random.uniform(-2, 2)
            y = np.random.uniform(-2, 2)
            rotation = np.random.uniform(0, 2 * np.pi, size=3)
            size = np.random.uniform(0.5, 1.5, size=3)

            for obj in objs:
                obj.set_location([x, y, 0])
                obj.set_rotation_euler(rotation)
                obj.set_scale(size)

    def main(self):
        data = bproc.renderer.render()
        output_dir = os.path.join("output", "0001")

        bproc.writer.write_coco_annotations(
            output_dir,
            instance_segmaps=data["instance_segmaps"],
            instance_attribute_maps=data["instance_attribute_maps"],
            colors=data["colors"],
            color_file_format="PNG",
            label_mapping=self.label_id_mapping,
            append_to_existing_output=True
        )

        bproc.writer.write_hdf5(output_dir, data)
        print(f"[INFO] Dataset written to {output_dir}")
