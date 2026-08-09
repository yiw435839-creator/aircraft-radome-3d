"""
设计引擎 - 离线版，基于工程模板生成整流罩设计方案
"""

class DesignEngine:
    def __init__(self):
        pass

    def generate_fairing_design(
        self,
        aircraft_model="DA42",
        component="机翼顶部 GPS 天线整流罩",
        antenna_type="GPS 天线",
        material="碳纤维复合材料",
        requirements="低阻力、防水、轻量化",
    ):
        # 根据材料调整参数
        if "碳纤维" in material:
            wall_thickness = "1.5mm"
            weight = "约 45g"
            layers = "3 层碳纤维布 + 1 层玻璃纤维隔离层"
        elif "玻璃纤维" in material:
            wall_thickness = "2.0mm"
            weight = "约 60g"
            layers = "4 层玻璃纤维布"
        elif "ABS" in material or "尼龙" in material:
            wall_thickness = "2.5mm"
            weight = "约 80g"
            layers = "3D 打印一体化成型"
        else:
            wall_thickness = "2.0mm"
            weight = "约 70g"
            layers = "标准工艺"

        # 根据天线类型调整尺寸
        if "GPS" in antenna_type or "北斗" in antenna_type:
            length = 180
            width = 80
            height = 60
        elif "VHF" in antenna_type:
            length = 300
            width = 60
            height = 40
        else:
            length = 150
            width = 70
            height = 50

        return {
            "设计概述": f"为 {aircraft_model} 设计的 {component}，采用 {material} 制造，满足 {requirements} 要求。",
            "几何参数": {
                "总长度": f"{length}mm",
                "最大宽度": f"{width}mm",
                "最大高度": f"{height}mm",
                "壁厚": wall_thickness,
                "底部法兰宽度": "10mm",
                "前缘曲率半径": f"{length//4}mm",
            },
            "结构方案": {
                "主体结构": "流线型椭球壳体",
                "材料分层": layers,
                "加强方式": "内部纵向加强筋 2 条",
                "安装方式": "4 孔法兰固定，M3 螺丝",
                "重量预估": weight,
            },
            "气动优化要点": [
                "采用对称翼型剖面，降低气动阻力",
                "前缘圆润过渡，避免气流分离",
                "后缘缓慢收窄，减小尾迹湍流",
                "最大厚度位置位于 40% 弦长处",
            ],
            "制造工艺": {
                "路线": "3D打印原型 → 模具翻制 → 复合材料铺层 → 真空固化 → 后处理",
                "步骤": [
                    "1. 3D 打印验证模型，检查安装尺寸",
                    "2. 用原型翻制玻璃钢阴模",
                    "3. 模具表面抛光，涂脱模剂",
                    "4. 手工铺层：先胶衣，再增强层",
                    "5. 真空袋抽真空，室温固化 24 小时",
                    "6. 脱模后修边、钻孔、打磨",
                    "7. 表面喷漆，安装密封件",
                ],
            },
            "注意事项": [
                "天线正上方不得使用金属材料，避免电磁屏蔽",
                "安装孔位需与机翼内部结构对齐",
                "防水等级建议达到 IP67",
                "需考虑热胀冷缩对安装的影响",
            ],
        }

    def print_design(self, design):
        """格式化打印设计方案"""
        print("=" * 60)
        print(f"  🛩️  {design['设计概述']}")
        print("=" * 60)
        print()

        print("📐 【几何参数】")
        for k, v in design["几何参数"].items():
            print(f"   {k}: {v}")
        print()

        print("🏗️ 【结构方案】")
        for k, v in design["结构方案"].items():
            print(f"   {k}: {v}")
        print()

        print("🌬️ 【气动优化要点】")
        for i, point in enumerate(design["气动优化要点"], 1):
            print(f"   {i}. {point}")
        print()

        print("🔧 【制造工艺】")
        print(f"   路线: {design['制造工艺']['路线']}")
        print()
        for step in design["制造工艺"]["步骤"]:
            print(f"   {step}")
        print()

        print("⚠️ 【注意事项】")
        for i, note in enumerate(design["注意事项"], 1):
            print(f"   {i}. {note}")
        print()
        print("=" * 60)