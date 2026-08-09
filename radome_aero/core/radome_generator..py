# radome_gen.py 修复版，旋转轮廓生成天线罩
import FreeCAD
import Part
import os

def generate_radome(out_step_path: str = "da42_radome.step"):
    doc = FreeCAD.newDocument("RadomeDoc")

    # --------参数，可根据需求修改----------
    length = 120.0      # X向长轴 mm
    width  = 80.0       # Y向短轴 mm
    height = 60.0       # Z向罩体高度
    wall_thick = 2.0    # 壳体壁厚
    flange_w = 10.0     # 法兰宽度
    # ------------------------------------
    rx = length / 2.0
    ry = width / 2.0

    # 构造封闭的旋转截面轮廓（2D，X‑Z平面）
    pts = []
    # 法兰外端点
    pts.append(FreeCAD.Vector(rx + flange_w, 0, -wall_thick))
    pts.append(FreeCAD.Vector(rx + flange_w, 0, 0))
    # 沿着椭球外轮廓到顶点，椭圆方程 x²/rx² + z²/rz² =1
    import math
    num_seg = 40
    for i in range(num_seg,-1,-1):
        t = i/num_seg
        z = height * t
        x = rx * math.sqrt(1.0 - t*t)
        pts.append(FreeCAD.Vector(x,0,z))
    # 向内到内壁
    for i in range(0,num_seg+1):
        t = i/num_seg
        z = height * t
        x = (rx-wall_thick) * math.sqrt(1.0 - t*t)
        pts.append(FreeCAD.Vector(x,0,z))
    pts.append(FreeCAD.Vector(rx-wall_thick,0,0))
    pts.append(FreeCAD.Vector(rx+flange_w,0,-wall_thick))

    wire = Part.makePolygon(pts)
    face = Part.Face(wire)
    # 绕Z轴旋转360°得到完整回转实体
    solid = face.revolve(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), 360.0)
    solid = solid.removeSplitter()

    obj = doc.addObject("Part::Feature","Radome")
    obj.Shape = solid
    doc.recompute()

    Part.export([obj], out_step_path)
    print(f"✅天线罩模型已输出: {os.path.abspath(out_step_path)}")
    return out_step_path

if __name__ == "__main__":
    generate_radome()