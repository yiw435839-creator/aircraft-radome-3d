# FreeCAD天线罩建模代码规范
## 1. 统一单位
所有尺寸单位统一为毫米（mm）

## 2. 建模顺序
1. 创建椭球基体
2. 抽壳生成薄壁壳体
3. 创建底部安装法兰
4. 布尔合并壳体与法兰
5. 打安装孔
6. 导出STEP文件

## 3. 参数命名规范
- radius_x：X轴半径（长轴）
- radius_y：Y轴半径（短轴）
- radius_z：Z轴半径（高度）
- wall_thickness：壁厚
- flange_length：法兰长度
- flange_width：法兰宽度
- flange_height：法兰厚度
- hole_radius：安装孔半径
- hole_count：安装孔数量