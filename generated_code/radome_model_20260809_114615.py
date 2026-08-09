import FreeCAD as App
import FreeCADGui as Gui
import Part
import math
import os

# 创建新文档
doc = App.newDocument("DA42_GPS_Radome")

# 参数定义（单位：mm）
radius_x = 120.0      # 长轴半径
radius_y = 80.0       # 短轴半径
radius_z = 60.0       # 高度半径
wall_thickness = 2.0  # 壁厚
flange_length = 100.0 # 法兰长度
flange_width = 100.0  # 法兰宽度
flange_height = 10.0  # 法兰厚度
hole_radius = 3.0     # 安装孔半径（M6螺栓）
hole_count = 6        # 安装孔数量
hole_circle_radius = 35.0  # 安装孔分布圆半径

# 1. 创建外椭球（中心在Z=radius_z，底部在Z=0）
outer_ellipsoid = doc.addObject("Part::Ellipsoid", "OuterEllipsoid")
outer_ellipsoid.Radius1 = radius_x
outer_ellipsoid.Radius2 = radius_y
outer_ellipsoid.Radius3 = radius_z
outer_ellipsoid.Placement = App.Placement(
    App.Vector(0, 0, radius_z),
    App.Rotation(0, 0, 0, 1)
)
doc.recompute()

# 2. 创建内椭球（缩小壁厚，中心在Z=radius_z）
inner_ellipsoid = doc.addObject("Part::Ellipsoid", "InnerEllipsoid")
inner_ellipsoid.Radius1 = radius_x - wall_thickness
inner_ellipsoid.Radius2 = radius_y - wall_thickness
inner_ellipsoid.Radius3 = radius_z - wall_thickness
inner_ellipsoid.Placement = App.Placement(
    App.Vector(0, 0, radius_z),
    App.Rotation(0, 0, 0, 1)
)
doc.recompute()

# 3. 创建法兰（长方体，顶面在Z=0，向下延伸）
flange = doc.addObject("Part::Box", "Flange")
flange.Length = flange_length
flange.Width = flange_width
flange.Height = flange_height
flange.Placement = App.Placement(
    App.Vector(-flange_length/2, -flange_width/2, -flange_height),
    App.Rotation(0, 0, 0, 1)
)
doc.recompute()

# 4. 布尔运算：外椭球 - 内椭球 = 壳体
shell = doc.addObject("Part::Cut", "Shell")
shell.Base = outer_ellipsoid
shell.Tool = inner_ellipsoid
doc.recompute()

# 5. 布尔合并：壳体 + 法兰
body = doc.addObject("Part::Fuse", "Body")
body.Base = shell
body.Tool = flange
doc.recompute()

# 6. 创建安装孔（垂直方向，从下往上贯穿）
holes = []
for i in range(hole_count):
    angle = 2 * math.pi * i / hole_count
    x = hole_circle_radius * math.cos(angle)
    y = hole_circle_radius * math.sin(angle)
    
    hole = doc.addObject("Part::Cylinder", f"Hole_{i+1}")
    hole.Radius = hole_radius
    hole.Height = radius_z + flange_height + 10  # 足够长以贯穿
    hole.Placement = App.Placement(
        App.Vector(x, y, -(flange_height + 5)),
        App.Rotation(0, 0, 0, 1)  # 垂直方向，不旋转
    )
    doc.recompute()
    holes.append(hole)

# 7. 逐个切除安装孔
current_body = body
for i, hole in enumerate(holes):
    cut = doc.addObject("Part::Cut", f"Cut_Hole_{i+1}")
    cut.Base = current_body
    cut.Tool = hole
    doc.recompute()
    current_body = cut

# 8. 隐藏所有中间特征
for obj in doc.Objects:
    if obj.Name not in ["Cut_Hole_6"]:  # 只保留最终结果
        obj.ViewObject.Visibility = False

# 9. 设置最终模型显示
final_model = doc.getObject("Cut_Hole_6")
final_model.ViewObject.Visibility = True
final_model.ViewObject.ShapeColor = (0.8, 0.8, 0.8)  # 灰色玻璃钢外观

# 10. 保存文件
output_dir = r"D:\AI_UAV_Radome\output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

step_file = os.path.join(output_dir, "DA42_GPS_Radome.step")
doc.saveAs(step_file)
print(f"STEP文件已保存至: {step_file}")

# 11. 视图调整
Gui.activeView().viewAxonometric()
Gui.SendMsgToActiveView("ViewFit")

print("DA42机载GPS天线罩建模完成")
print(f"外形尺寸: {radius_x*2} x {radius_y*2} x {radius_z*2} mm")
print(f"壁厚: {wall_thickness} mm")
print(f"法兰尺寸: {flange_length} x {flange_width} x {flange_height} mm")
print(f"安装孔: {hole_count}个, 直径{hole_radius*2}mm, 分布圆半径{hole_circle_radius}mm")