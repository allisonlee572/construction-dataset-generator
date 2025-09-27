from pathlib import Path

def convert_relative_to_absolute(obj_path: str):
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

        if key in ["map_kd", "map_ns", "refl", "bump", "map_bump"]:
            rel_path = parts[-1]
            abs_path = (base_dir / rel_path).resolve()
            options = " ".join(parts[1:-1])
            line = f"{key} {options} {abs_path.as_posix()}" if options else f"{key} {abs_path.as_posix()}"
        new_lines.append(line)

    mtl_file.write_text("\n".join(new_lines))
    print(f"[INFO] Converted texture paths in {mtl_file} to absolute.")
