import blenderproc as bproc
import numpy as np 
import os 
from pathlib import Path

class ConstructionDatasetGenerator:
    def __init__(self):
        self.scene_objects = []
        self.label_id_mapping = bproc.utility.LabelIdMapping.from_dict({
            "background": 0, 
            "buildings": 1,
            "helmet": 2, 
            "worker": 3 ,
            "bgchar": 4,
            "equipement": 5
        })

        bproc.init()
        self.load_assets()
        self.setup()  
        # self.place_assets_randomly()


    def load_single_asset(self, obj_file, category_id, scale=1):
        self.relative_to_absolute(obj_file)
        objs = bproc.loader.load_obj(obj_file)

        for obj in objs:
            obj.set_cp("category_id", category_id)
            obj.set_scale([scale, scale, scale])


        self.scene_objects.append(objs)


    def load_assets(self):
        # for i in range(np.random.randint(1, 5)):
        self.load_single_asset("assets/helmet1/helmet.obj", 2, 1)
            
  
    def setup(self):
        ground = bproc.object.create_primitive('PLANE', scale=[20, 20, 1])
        ground.set_location([0, 0, 0])
        ground.set_cp("category_id", 0)  # Background category
        
        light = bproc.types.Light() # Create a point light next to it
        light.set_location([2, -2, 0])
        light.set_energy(300) #brightness of light
        cam_pose = bproc.math.build_transformation_mat([0, -5, 0], [np.pi / 2, 0, 0])
        bproc.camera.add_camera_pose(cam_pose)
        bproc.renderer.enable_segmentation_output(map_by=["category_id", "instance", "name"])

    def place_assets_randomly(self) -> None:
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
        print(data.keys())

        bproc.writer.write_coco_annotations(
            os.path.join("output", "0001"), # -> output\\0001
            instance_segmaps=data["instance_segmaps"], #segmentation mask that was rendered earlier 
            instance_attribute_maps=data["instance_attribute_maps"], # contains info about each instance (category_id, name, etc)
            colors=data["colors"], # actual rendered RGB image
            color_file_format="PNG", # format for RGB image.
            label_mapping=self.label_id_mapping, 
            append_to_existing_output=True # If the output folder already has COCO annotations, append to them instead of overwriting
        )

        bproc.writer.write_hdf5(f"output/0001/", data)


    def relative_to_absolute(self, obj_path: str):
        obj_path = Path(obj_path)
        mtl_file = obj_path.with_suffix(".mtl")

        if not mtl_file.exists():
            print(f"[WARNING] No .mtl file found for {obj_path}")
            return

        text = mtl_file.read_text()
        base_dir = mtl_file.parent

        new_lines = []
        for line in text.splitlines():
            parts = line.strip().split()
            if not parts:
                continue

            key = parts[0].lower()

            if key in ["map_Kd", "map_ns", "refl", "bump", "map_bump"]:
                # default: last token is the filename
                rel_path = parts[-1]
                abs_path = (base_dir / rel_path).resolve()

                # rebuild line keeping any options before the filename
                options = " ".join(parts[1:-1])  # e.g. "-bm 0.3000"
                if options:
                    line = f"{key} {options} {abs_path.as_posix()}"
                else:
                    line = f"{key} {abs_path.as_posix()}"

            new_lines.append(line)

        mtl_file.write_text("\n".join(new_lines))
        print(f"[INFO] Converted texture paths in {mtl_file} to absolute.")

        mtl_file.write_text("\n".join(new_lines))
        print(f"[INFO] Converted texture paths in {mtl_file} to absolute.")


if __name__ == "__main__":
    generator = ConstructionDatasetGenerator()
    generator.main()
