# 安装
```bash
cd MinerU
uv pip install -e .[core] -i https://mirrors.aliyun.com/pypi/simple
```

# 模型
```python
class ModelPath:
    vlm_root_hf = "opendatalab/MinerU2.0-2505-0.9B"
    vlm_root_modelscope = "OpenDataLab/MinerU2.0-2505-0.9B"
    pipeline_root_modelscope = "OpenDataLab/PDF-Extract-Kit-1.0"
    pipeline_root_hf = "opendatalab/PDF-Extract-Kit-1.0"
    doclayout_yolo = "models/Layout/YOLO/doclayout_yolo_docstructbench_imgsz1280_2501.pt"
    yolo_v8_mfd = "models/MFD/YOLO/yolo_v8_ft.pt"
    unimernet_small = "models/MFR/unimernet_hf_small_2503"
    pytorch_paddle = "models/OCR/paddleocr_torch"
    layout_reader = "models/ReadingOrder/layout_reader"
    slanet_plus = "models/TabRec/SlanetPlus/slanet-plus.onnx"
```

## 使用cuda
```bash
uv pip uninstall torch torchvision
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```