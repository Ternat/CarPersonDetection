# 行人 · 车辆检测系统（CarPersonDetection）

基于 [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) 与 **PyQt5** 的行人 / 车辆目标检测系统，提供图形化界面，支持**图片、视频、摄像头与批量文件夹检测**，并可导出检测结果。

> English version: [README.en.md](README.en.md)

## 功能特性

- **图片检测**：打开单张图片，实时显示检测框、类别、置信度与目标数量
- **视频检测**：对本地视频逐帧检测并实时显示
- **摄像头检测**：调用电脑摄像头进行实时检测
- **批量检测**：对文件夹内所有图片批量检测，结果汇总到表格
- **结果表格**：展示序号、文件路径、类别、置信度、目标框坐标
- **结果保存**：将检测结果保存为图片（jpg）或视频（avi）
- 支持 **行人 / 汽车** 两类目标，置信度与 IoU 阈值可调

## 个人贡献

本项目由作者独立完成，核心工作包括：

- **检测系统设计与实现**：基于 PyQt5 从零搭建图形化检测界面，实现图片 / 视频 / 摄像头 / 批量文件夹四种检测模式（`MainProgram.py`）
- **推理流程封装**：将 YOLOv8 推理、结果解析、目标框绘制、中文标签渲染、结果保存封装为完整流程（`detect_tools.py`）
- **结果可视化**：实现检测结果表格（序号、路径、类别、置信度、坐标）与目标数量统计，支持按目标筛选查看
- **模型训练与调优**：基于行人 / 车辆二分类数据集完成 YOLOv8n 模型微调（250 epochs），最终 mAP50 达 94.0%（`train.py`）
- **训练分析工具**：编写自定义训练结果分析脚本 `analysis/visual.py`，自动生成损失 / 指标曲线、相关性热力图与分析报告
- **工程问题解决**：定位并修复 Windows 下 PyQt5 与 torch 的 DLL 加载冲突（`c10.dll` 初始化失败）

## 效果展示

<div align="center">
  <img src="assets/demo_both.jpg" width="32%" alt="行人与车辆同时检测" />
  <img src="assets/demo_persons.jpg" width="32%" alt="行人检测" />
</div>

## 快速开始

### 环境要求

- Python 3.8 及以上
- 推荐在虚拟环境中安装依赖：

```bash
pip install -r requirements.txt
```

> 说明：`ultralytics` 会自动安装 `torch` / `torchvision`。如需 GPU 加速，请到 [PyTorch 官网](https://pytorch.org/) 安装对应 CUDA 版本的 torch。

### 启动图形界面

```bash
python MainProgram.py
```

### 命令行快速检测（无需 GUI）

```bash
python imgTest.py      # 图片检测
python VideoTest.py    # 视频检测
python CameraTest.py   # 摄像头检测
```

## 使用说明

1. 点击「图片」选择单张图片，或点击「文件夹」批量检测；
2. 选择「视频」或「摄像头」进行实时检测；
3. 在界面右侧表格查看每个目标的类别、置信度与坐标；
4. 点击「保存」将检测结果保存到 `save_data/` 目录。

## 模型训练

本项目模型基于 YOLOv8n 预训练权重微调，训练脚本见 `train.py`：

```bash
python train.py
```

训练配置（`train.py`）：

| 配置项 | 值 |
| --- | --- |
| 预训练模型 | `yolov8n.pt` |
| 数据集 | `datasets/CarPersonData/data.yaml`（需自行准备） |
| 训练轮数 | 250 epochs |
| batch size | 4 |

训练完成后，将新权重替换 `models/best.pt` 即可。

## 数据与评估

### 数据集

- 目标类别：`person`（行人）、`car`（车辆）
- 标注格式：YOLO 格式
- 标签分布（类别数量、目标框尺寸与位置）见下方 `labels.jpg`

### 训练配置

基于 YOLOv8n 预训练权重微调：

| 配置项 | 值 |
| --- | --- |
| 基础模型 | YOLOv8n |
| 输入尺寸 | 640×640 |
| 训练轮数 | 250 epochs |
| batch size | 4 |
| 优化器 | auto (SGD) |

### 评估指标（验证集）

| 指标 | 初始值 | 最终值 |
| --- | --- | --- |
| Precision | 81.7% | **89.6%** |
| Recall | 77.4% | **87.6%** |
| mAP50 | 86.1% | **94.0%** |
| mAP50-95 | 62.6% | **76.1%** |

> 最佳 mAP50 出现在第 217 轮（94.08%）；mAP50-95 较初始提升 21.6%。

### 评估可视化

<div align="center">
  <img src="assets/eval/results.png" width="45%" alt="训练过程损失与指标曲线" />
  <img src="assets/eval/PR_curve.png" width="45%" alt="PR 曲线" />
</div>

<div align="center">
  <img src="assets/eval/confusion_matrix.png" width="30%" alt="混淆矩阵" />
  <img src="assets/eval/labels.jpg" width="30%" alt="数据标签分布" />
</div>

## 运行验证

模型在**验证集**与**真实场景**上均已验证：

- **验证集预测**：模型在未参与训练数据上的预测效果（下图为预测结果与真实标注对比）
- **真实场景检测**：对真实图片 / 视频 / 摄像头画面的检测结果见上文「效果展示」

<div align="center">
  <img src="assets/eval/val_batch0_pred.jpg" width="45%" alt="验证集预测结果" />
  <img src="assets/eval/val_batch0_labels.jpg" width="45%" alt="验证集真实标注" />
</div>

复现方式：按上文「快速开始」安装依赖后，运行 `python MainProgram.py` 或 `python imgTest.py` 即可。

## 项目结构

```
CarPersonDetection/
├── MainProgram.py        # 主程序（PyQt5 图形界面）
├── Config.py             # 配置（模型路径、类别名、保存路径）
├── detect_tools.py       # 检测工具（画框、中文绘制、坐标转换）
├── train.py              # 模型训练脚本
├── imgTest.py            # 图片检测脚本（无 GUI）
├── VideoTest.py          # 视频检测脚本（无 GUI）
├── CameraTest.py         # 摄像头检测脚本（无 GUI）
├── installPackages.py    # 依赖安装辅助脚本
├── models/
│   └── best.pt           # 自训练的行人 / 车辆检测模型
├── yolov8n.pt            # YOLOv8n 预训练权重（训练用）
├── analysis/             # 训练结果分析
│   ├── visual.py         # 自定义分析脚本（生成曲线与报告）
│   └── results.csv       # 训练过程逐轮指标
├── UIProgram/            # 界面资源（.ui / .qss / 图标等）
├── Font/                 # 中文字体
├── TestFiles/            # 测试图片
├── assets/               # README 示例图与评估图
├── requirements.txt      # 依赖清单
└── LICENSE               # 许可证（AGPL-3.0）
```

## 常见问题

- **Windows 下启动报 `c10.dll` 错误**：这是 PyQt5 与 torch 的 DLL 加载顺序冲突，已在 `MainProgram.py` 中通过「先导入 ultralytics 再导入 PyQt5」解决。
- **检测不到目标**：可在 `MainProgram.py` 中调整 `conf`（置信度阈值，默认 0.25）与 `iou`（IoU 阈值，默认 0.7）。

## 许可证

本项目基于 [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)（AGPL-3.0），采用 **[AGPL-3.0](LICENSE)** 许可证发布。

## 致谢

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) —— 目标检测框架与预训练模型
