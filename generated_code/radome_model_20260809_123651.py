import FreeCAD as App
import FreeCADGui as Gui
import Part
import math
import os

# 创建新文档
doc = App.newDocument("DA42_GPS_Radome")

# ========== 设计参数 ==========
# 椭球尺寸 (mm)
radius_x = 150.0    # 长半轴
radius_y = 100.0    # 短半轴
radius_z = 80.0     # 高度半轴
wall_thickness = 2.0  # 壁厚

# 法兰参数
flange_width = 25.0   # 法兰宽度 (20-30mm)
flange_height = 10.0  # 法兰厚度 (8-15mm)
flange_length = 200.0 # 法兰边长 (方形)

# 安装孔参数
hole_count = 6        # 孔数量
hole_diameter = 6.0   # M6螺栓
hole_radius = 80.0    # 分布圆半径

# 材料参数
density = 1.9e-6      # 玻璃钢密度 kg/mm³ (1.9g/cm³)

# ========== 1. 创建椭球基体 ==========
outer_ellipsoid = doc.addObject("Part::Ellipsoid", "OuterEllipsoid")
outer_ellipsoid.Radius1 = radius_x
outer_ellipsoid.Radius2 = radius_y
outer_ellipsoid.Radius3 = radius_z
outer_ellipsoid.Placement = App.Placement(
    App.Vector(0, 0, radius_z),  # 底部落在Z=0
    App.Rotation(0, 0, 0, 1)
)
doc.recompute()

# ========== 2. 创建内椭球 (用于抽壳) ==========
inner_ellipsoid = doc.addObject("Part::Ellipsoid", "InnerEllipsoid")
inner_ellipsoid.Radius1 = radius_x - wall_thickness
inner_ellipsoid.Radius2 = radius_y - wall_thickness
inner_ellipsoid.Radius3 = radius_z - wall_thickness
inner_ellipsoid.Placement = App.Placement(
    App.Vector(0, 0, radius_z),
    App.Rotation(0, 0, 0, 1)
)
doc.recompute()

# ========== 3. 创建法兰 ==========
flange = doc.addObject("Part::Box", "Flange")
flange.Length = flange_length
flange.Width = flange_length
flange.Height = flange_height
flange.Placement = App.Placement(
    App.Vector(-flange_length/2, -flange_length/2, -flange_height),
    App.Rotation(0, 0, 0, 1)
)
doc.recompute()

# ========== 4. 创建安装孔 ==========
holes = []
for i in range(hole_count):
    angle = 2 * math.pi * i / hole_count
    x = hole_radius * math.cos(angle)
    y = hole_radius * math.sin(angle)
    
    hole = doc.addObject("Part::Cylinder", f"Hole_{i+1}")
    hole.Radius = hole_diameter / 2
    hole.Height = flange_height + radius_z + 20  # 贯穿法兰和壳体
    hole.Placement = App.Placement(
        App.Vector(x, y, -flange_height - 10),
        App.Rotation(0, 0, 0, 1)  # 垂直方向
    )
    doc.recompute()
    holes.append(hole)

# ========== 5. 布尔运算 ==========
# 外壳 = 外椭球 - 内椭球
shell = doc.addObject("Part::Cut", "Shell")
shell.Base = outer_ellipsoid
shell.Tool = inner_ellipsoid
doc.recompute()

# 合并壳体与法兰
fused = doc.addObject("Part::Fuse", "FusedBody")
fused.Base = shell
fused.Tool = flange
doc.recompute()

# 切除安装孔
final_body = fused
for hole in holes:
    cut = doc.addObject("Part::Cut", f"Cut_{hole.Name}")
    cut.Base = final_body
    cut.Tool = hole
    doc.recompute()
    final_body = cut

# 重命名最终模型
final_body.Label = "DA42_GPS_Radome_Final"

# ========== 6. 工程计算 ==========
# 计算体积 (通过形状属性)
shape = final_body.Shape
volume = shape.Volume  # mm³

# 计算重量 (kg)
weight_kg = volume * density

# 计算外表面积 (mm²)
surface_area = shape.Area

# 转换为常用单位
weight_g = weight_kg * 1000
surface_area_cm2 = surface_area / 100

# ========== 7. 显示设置 ==========
# 隐藏所有中间特征
for obj in doc.Objects:
    if obj.Name != final_body.Name:
        obj.ViewObject.Visibility = False

# 设置最终模型显示
final_body.ViewObject.Visibility = True
final_body.ViewObject.ShapeColor = (0.8, 0.8, 0.8)  # 灰色

# 视图调整
Gui.activeView().viewAxonometric()
Gui.SendMsgToActiveView("ViewFit")

# ========== 8. 输出工程参数 ==========
print("=" * 50)
print("DA42 GPS天线罩设计参数")
print("=" * 50)
print(f"椭球尺寸: {radius_x} x {radius_y} x {radius_z} mm")
print(f"壁厚: {wall_thickness} mm")
print(f"法兰尺寸: {flange_length} x {flange_length} x {flange_height} mm")
print(f"安装孔: {hole_count}个, 直径{hole_diameter}mm, 分布圆半径{hole_radius}mm")
print("-" * 50)
print(f"模型体积: {volume:.2f} mm³")
print(f"模型重量: {weight_g:.2f} g ({weight_kg:.4f} kg)")
print(f"外表面积: {surface_area:.2f} mm² ({surface_area_cm2:.2f} cm²)")
print("=" * 50)

# ========== 9. 保存文件 ==========
output_dir = r"D:\AI_UAV_Radome\output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

step_file = os.path.join(output_dir, "DA42_GPS_Radome.step")
Part.export([final_body], step_file)
print(f"STEP文件已保存: {step_file}")

fcstd_file = os.path.join(output_dir, "DA42_GPS_Radome.FCStd")
doc.saveAs(fcstd_file)
print(f"FCStd文件已保存: {fcstd_file}")

print("\n建模完成！")