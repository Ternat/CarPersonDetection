# Car & Person Detection (CarPersonDetection)

A car / person object detection system built on [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) and **PyQt5**, featuring a graphical interface for **image, video, webcam, and batch-folder detection**, with exportable results.

> 中文版请见：[README.md](README.md)

## ✨ Features

- 🖼️ **Image detection** — open a single image and show bounding boxes, class, confidence, and object counts in real time
- 🎥 **Video detection** — run frame-by-frame detection on local videos
- 📷 **Webcam detection** — real-time detection using your computer's camera
- 📁 **Batch detection** — detect all images in a folder and aggregate results into a table
- 📊 **Results table** — shows index, file path, class, confidence, and bounding-box coordinates
- 💾 **Result export** — save results as image (jpg) or video (avi)
- 🎯 Detects **person / car** classes, with adjustable confidence and IoU thresholds

## 📸 Demo

<div align="center">
  <img src="assets/demo_both.jpg" width="32%" alt="Cars and persons detected" />
  <img src="assets/demo_persons.jpg" width="32%" alt="Persons detected" />
</div>

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Install dependencies (a virtual environment is recommended):

```bash
pip install -r requirements.txt
```

> Note: `ultralytics` installs `torch` / `torchvision` automatically. For GPU acceleration, install a CUDA-compatible `torch` from the [PyTorch website](https://pytorch.org/).

### Launch the GUI

```bash
python MainProgram.py
```

### Command-line detection (no GUI)

```bash
python imgTest.py      # image detection
python VideoTest.py    # video detection
python CameraTest.py   # webcam detection
```

## 🖱️ Usage

1. Click the **Image** button to pick a single image, or **Folder** for batch detection;
2. Choose **Video** or **Webcam** for real-time detection;
3. View each object's class, confidence, and coordinates in the table on the right;
4. Click **Save** to export results to the `save_data/` directory.

## 🧠 Model Training

The model is fine-tuned from YOLOv8n pretrained weights; the training script is `train.py`:

```bash
python train.py
```

Training configuration (`train.py`):

| Setting | Value |
| --- | --- |
| Pretrained model | `yolov8n.pt` |
| Dataset | `datasets/CarPersonData/data.yaml` (prepare it yourself) |
| Epochs | 250 |
| Batch size | 4 |

After training, replace `models/best.pt` with the new weights.

## 📁 Project Structure

```
CarPersonDetection/
├── MainProgram.py        # Main program (PyQt5 GUI)
├── Config.py             # Configuration (model path, class names, save path)
├── detect_tools.py       # Detection utilities (drawing, Chinese text, coordinate conversion)
├── train.py              # Model training script
├── imgTest.py            # Image detection script (no GUI)
├── VideoTest.py          # Video detection script (no GUI)
├── CameraTest.py         # Webcam detection script (no GUI)
├── installPackages.py    # Dependency installation helper
├── models/
│   └── best.pt           # Fine-tuned car / person detection model
├── yolov8n.pt            # YOLOv8n pretrained weights (for training)
├── UIProgram/            # UI resources (.ui / .qss / icons, etc.)
├── Font/                 # Chinese font
├── TestFiles/            # Sample images
├── assets/               # README demo images
├── requirements.txt      # Dependency list
└── LICENSE               # License (AGPL-3.0)
```

## ❓ FAQ

- **`c10.dll` error on Windows startup**: caused by a DLL loading-order conflict between PyQt5 and torch; already fixed in `MainProgram.py` by importing `ultralytics` before `PyQt5`.
- **No objects detected**: adjust `conf` (confidence threshold, default 0.25) and `iou` (IoU threshold, default 0.7) in `MainProgram.py`.

## 📄 License

Built on [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) (AGPL-3.0). This project is released under the **[AGPL-3.0](LICENSE)** license.

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) — detection framework and pretrained models
