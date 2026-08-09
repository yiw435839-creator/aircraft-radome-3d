"""
离线版 Demo - 直接运行，无需 API Key
"""

import sys
import os

# 让 Python 能找到 src 文件夹
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.design_engine import DesignEngine


def main():
    print()
    print("=" * 60)
    print("     AeroCAD Copilot - 整流罩智能设计助手 (离线版)")
    print("=" * 60)
    print()

    # 初始化设计引擎
    engine = DesignEngine()

    # 生成设计方案
    print("📋 正在生成 DA42 机翼顶部 GPS 天线整流罩设计方案...")
    print()

    design = engine.generate_fairing_design(
        aircraft_model="DA42",
        component="机翼顶部 GPS 天线整流罩",
        antenna_type="GPS 天线",
        material="碳纤维复合材料",
        requirements="低阻力、防水、轻量化、可 3D 打印验证",
    )

    # 打印结果
    engine.print_design(design)

    print()
    print("✅ 设计方案生成完成！")
    print()


if __name__ == "__main__":
    main()