# config.py 项目统一配置
import os
from pathlib import Path

# 项目根目录（固定D盘路径）
ROOT_DIR = Path(r"D:\AI_UAV_Radome")

# 各目录路径
KNOWLEDGE_DIR = ROOT_DIR / "knowledge"
OUTPUT_DIR = ROOT_DIR / "output"
GENERATED_CODE_DIR = ROOT_DIR / "generated_code"
EXAMPLES_DIR = ROOT_DIR / "examples"

# 确保目录存在
for d in [OUTPUT_DIR, GENERATED_CODE_DIR, EXAMPLES_DIR]:
    d.mkdir(exist_ok=True)

# 默认建模参数
DEFAULT_PARAMS = {
    "radius_x": 150.0,
    "radius_y": 100.0,
    "radius_z": 80.0,
    "wall_thickness": 2.0,
    "flange_length": 250.0,
    "flange_width": 200.0,
    "flange_height": 10.0,
    "hole_radius": 3.0,
    "hole_count": 6,
    "hole_circle_r": 90.0,
}

# 材料密度表（g/cm³）
MATERIAL_DENSITY = {
    "玻璃钢": 1.9,
    "聚四氟乙烯": 2.15,
    "石英纤维复合材料": 1.8,
}