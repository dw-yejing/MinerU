import os
import gradio as gr
from demo import do_parse
import zipfile

# Helper function to compress directory to zip (copied from server.py)
def compress_directory_to_zip(directory_path, output_zip_path):
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, arcname)
        return 0
    except Exception as e:
        print(f"Error compressing directory: {e}")
        return -1

def parse_and_zip(files, id,
                  f_draw_layout_bbox, f_draw_span_bbox, f_dump_md, f_dump_middle_json,
                  f_dump_model_output, f_dump_orig_pdf, f_dump_content_list):
    output_dir = os.path.join("demo", "output", id)
    os.makedirs(output_dir, exist_ok=True)
    lang = "ch"
    backend = "pipeline"
    method = "auto"
    server_url = None
    start_page_id = 0
    end_page_id = None

    file_name_list = []
    pdf_bytes_list = []
    lang_list = []
    for file in files:
        file_name = os.path.basename(file)
        with open(file, 'rb') as f:
            pdf_bytes = f.read()
        # file_name = file.name
        # pdf_bytes = file.read()
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
        f_draw_layout_bbox=f_draw_layout_bbox,
        f_draw_span_bbox=f_draw_span_bbox,
        f_dump_md=f_dump_md,
        f_dump_middle_json=f_dump_middle_json,
        f_dump_model_output=f_dump_model_output,
        f_dump_orig_pdf=f_dump_orig_pdf,
        f_dump_content_list=f_dump_content_list,
    )
    zipfile_path = f"{output_dir}.zip"
    compress_directory_to_zip(output_dir, zipfile_path)
    return zipfile_path

def gradio_interface(files, id,
                     f_draw_layout_bbox, f_draw_span_bbox, f_dump_md, f_dump_middle_json,
                     f_dump_model_output, f_dump_orig_pdf, f_dump_content_list):
    zip_path = parse_and_zip(files, id,
                            f_draw_layout_bbox, f_draw_span_bbox, f_dump_md, f_dump_middle_json,
                            f_dump_model_output, f_dump_orig_pdf, f_dump_content_list)
    return zip_path

with gr.Blocks() as demo:
    gr.Markdown("# PDF Parser GUI (MinerU)")
    with gr.Row():
        files = gr.File(label="Upload PDF(s)", file_count="multiple")
        id = gr.Textbox(label="ID", value="demo1")
    with gr.Row():
        f_draw_layout_bbox = gr.Checkbox(label="Draw Layout BBox", value=False)
        f_draw_span_bbox = gr.Checkbox(label="Draw Span BBox", value=False)
        f_dump_md = gr.Checkbox(label="Dump Markdown", value=True)
        f_dump_middle_json = gr.Checkbox(label="Dump Middle JSON", value=False)
        f_dump_model_output = gr.Checkbox(label="Dump Model Output", value=False)
        f_dump_orig_pdf = gr.Checkbox(label="Dump Original PDF", value=False)
        f_dump_content_list = gr.Checkbox(label="Dump Content List", value=False)
    submit_btn = gr.Button("Parse and Download Zip", variant="primary")
    output = gr.File(label="Download Result Zip")

    submit_btn.click(
        gradio_interface,
        inputs=[files, id, f_draw_layout_bbox, f_draw_span_bbox, f_dump_md, f_dump_middle_json,
                f_dump_model_output, f_dump_orig_pdf, f_dump_content_list],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8003, share=True)