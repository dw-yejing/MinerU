# 使用 fastapi 开发一个post接口
import os
from typing import List
import zipfile

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse

from demo.demo import do_parse

app = FastAPI()

@app.post("/parse")
async def submit_data(files: List[UploadFile] = File(...), 
    id: str = Form(...),
    f_draw_layout_bbox: bool = Form(default=False),  # Whether to draw layout bounding boxes
    f_draw_span_bbox: bool = Form(default=False),  # Whether to draw span bounding boxes
    f_dump_md: bool = Form(default=True),  # Whether to dump markdown files
    f_dump_middle_json: bool = Form(default=False),  # Whether to dump middle JSON files
    f_dump_model_output: bool = Form(default=False),  # Whether to dump model output files
    f_dump_orig_pdf: bool = Form(default=False),  # Whether to dump original PDF files
    f_dump_content_list: bool = Form(default=False),  # Whether to dump content list files
    ):
    
    output_dir = r"D:\github\MinerU-master\nexus"
    output_dir = f"{output_dir}/{id}"
    lang="ch"
    backend="pipeline"
    method="auto"
    server_url=None
    start_page_id=0
    end_page_id=None
    
    
    file_name_list = []
    pdf_bytes_list = []
    lang_list = []
    for file in files:
        file_name = file.filename
        pdf_bytes = file.file
        file_name_list.append(file_name)
        pdf_bytes_list.append(pdf_bytes)
        lang_list.append(lang)
        
    do_parse(
        output_dir=output_dir,
        pdf_file_names=file_name_list,
        pdf_bytes_list=pdf_bytes_list,
        p_lang_list=lang_list,
        backend=backend,
        parse_method=method,
        server_url=server_url,
        start_page_id=start_page_id,
        end_page_id=end_page_id,
        f_draw_layout_bbox=f_draw_layout_bbox,  # Whether to draw layout bounding boxes
        f_draw_span_bbox=f_draw_span_bbox,  # Whether to draw span bounding boxes
        f_dump_md=f_dump_md,  # Whether to dump markdown files
        f_dump_middle_json=f_dump_middle_json,  # Whether to dump middle JSON files
        f_dump_model_output=f_dump_model_output,  # Whether to dump model output files
        f_dump_orig_pdf=f_dump_orig_pdf,  # Whether to dump original PDF files
        f_dump_content_list=f_dump_content_list,  # Whether to dump content list files
    )
    zipfile_path = f"{output_dir}.zip"
    compress_directory_to_zip(output_dir, zipfile_path)
    
    headers = {
        "Content-Disposition": f"attachment; filename={id}.zip",
        "Content-Type": "application/octet-stream"
    }
    return FileResponse(zipfile_path, headers=headers, media_type="application/octet-stream")
    
def compress_directory_to_zip(directory_path, output_zip_path):
    """压缩指定目录到一个 ZIP 文件。

    :param directory_path: 要压缩的目录路径
    :param output_zip_path: 输出的 ZIP 文件路径
    """
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:

            # 遍历目录中的所有文件和子目录
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    # 构建完整的文件路径
                    file_path = os.path.join(root, file)
                    # 计算相对路径
                    arcname = os.path.relpath(file_path, directory_path)
                    # 添加文件到 ZIP 文件
                    zipf.write(file_path, arcname)
        return 0
    except Exception as e:
        print(f"Error compressing directory: {e}")
        return -1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)