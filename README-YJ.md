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

# MM_MD、NLP_MD、CONTENT_LIST 三种模式的区别
这三种模式是MinerU项目中用于解析PDF文档并生成不同格式输出的模式，它们在处理文档内容时有显著的区别：
1. MM_MD (mm_markdown) - 多媒体Markdown模式
特点：最完整的输出模式，保留所有多媒体内容
处理内容：
✅ 图片：保留图片引用 ![]({img_path})
✅ 表格：保留表格HTML结构或图片引用
✅ 公式：保留LaTeX公式
✅ 标题：转换为Markdown标题格式 # ## ###
✅ 文本：保留所有文本内容
✅ 图片/表格标题和脚注：完整保留
2. NLP_MD (nlp_markdown) - 自然语言处理Markdown模式
特点：专注于文本内容，适合NLP任务
处理内容：
❌ 图片：跳过图片内容 (continue)
❌ 表格：跳过表格内容 (continue)
✅ 公式：保留LaTeX公式
✅ 标题：转换为Markdown标题格式
✅ 文本：保留所有文本内容
❌ 图片/表格标题和脚注：不包含
3. CONTENT_LIST - 结构化内容列表模式
特点：生成结构化的JSON格式，便于程序处理
输出格式：返回JSON数组，每个元素包含：
Apply to glossary.txt
```json
  {
    "type": "text|image|table|equation",
    "text": "内容文本",
    "text_level": 1,  // 标题级别（仅标题）
    "img_path": "图片路径",  // 图片/表格
    "image_caption": ["标题1", "标题2"],  // 图片标题
    "image_footnote": ["脚注1"],  // 图片脚注
    "table_caption": ["表格标题"],
    "table_footnote": ["表格脚注"],
    "page_idx": 0  // 页码
  }
  ```
  主要区别总结：

<table> <tr> <th>特性</th> <th>MM_MD</th> <th>NLP_MD</th> <th>CONTENT_LIST</th> </tr> <tr> <td>图片处理</td> <td>✅ 保留图片引用</td> <td>❌ 跳过</td> <td>✅ 结构化存储</td> </tr> <tr> <td>表格处理</td> <td>✅ 保留HTML/图片</td> <td>❌ 跳过</td> <td>✅ 结构化存储</td> </tr> <tr> <td>公式处理</td> <td>✅ LaTeX格式</td> <td>✅ LaTeX格式</td> <td>✅ 结构化存储</td> </tr> <tr> <td>标题处理</td> <td>✅ Markdown格式</td> <td>✅ Markdown格式</td> <td>✅ 带级别信息</td> </tr> <tr> <td>输出格式</td> <td>纯文本Markdown</td> <td>纯文本Markdown</td> <td>JSON结构化数据</td> </tr> <tr> <td>适用场景</td> <td>完整文档展示</td> <td>NLP文本分析</td> <td>程序化处理</td> </tr> </table>

# abandon region
根据文档说明，Abandon = 2 包括：
页眉 (Headers)
页脚 (Footers)
页码 (Page Numbers)
页面注释 (Page Annotations)

# ocr
主入口类
文件：mineru/model/ocr/paddleocr2pytorch/pytorch_paddle.py
类：PytorchPaddleOCR
方法：ocr 和 __call__
ocr 方法负责整体的检测与识别流程（检测文本框+识别文本内容）。
__call__ 方法内部调用检测器（self.text_detector）和识别器（self.text_recognizer）完成文本识别。
2. 文本识别器实现
文件：mineru/model/ocr/paddleocr2pytorch/tools/infer/predict_rec.py
类：TextRecognizer
方法：__call__
输入为图片块列表，输出为识别出的文本内容和置信度分数。
3. 检测器实现
文件：mineru/model/ocr/paddleocr2pytorch/tools/infer/predict_det.py
类：TextDetector
方法：__call__
负责检测图片中的文本框区域。
4. 流程简述
检测：self.text_detector(img) 检测文本框。
裁剪：对每个检测到的文本框裁剪图片块。
识别：self.text_recognizer(img_crop_list) 对每个图片块做文本识别，输出文本内容和置信度。

```python
# 入口
ocr_engine = PytorchPaddleOCR()
dt_boxes, rec_res = ocr_engine(img)  # dt_boxes为检测框，rec_res为识别结果
```