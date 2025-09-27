from generator.dataset_generator import ConstructionDatasetGenerator

if __name__ == "__main__":
    generator = ConstructionDatasetGenerator(config_path="configs/default.yaml")
    generator.main()
