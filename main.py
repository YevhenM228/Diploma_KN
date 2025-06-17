import json
import os
import gradio as gr
from tracker import detection_on_image, detection_on_video

APP_TITLE = "Автоматизована система виявлення об'єктів"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), title="Аналіз зображень та відео") as demo:
    gr.Markdown(f"""
    <h1 style='text-align:center'>{APP_TITLE}</h1>
    <p style='text-align:center'>Цей застосунок дозволяє проводити виявлення об'єктів на зображеннях та у відео. Оберіть файл, і ми зробимо решту.</p>
    """)

    with gr.Row(variant='panel'):
        with gr.Column(scale=1):
            with gr.Tabs():
                with gr.TabItem("🖼️ Зображення"):
                    image_input = gr.Image(type="numpy", label="Зображення")
                    button_image = gr.Button("Почати розпізнавання", variant="primary")

                with gr.TabItem("🎬 Відео"):
                    video_input = gr.File(label="Відео файл", file_types=[".mp4", ".avi", ".mov"])
                    button_video = gr.Button("Почати розпізнавання", variant="primary")
            
            status_message = gr.Textbox(label="Стан розпізнавання", interactive=False, visible=False)

        with gr.Column(scale=1):
            gr.Label("Результати")
            output_image = gr.Image()
            download_image = gr.File(label="Завантажити зображення", visible=False)
            output_video = gr.Video(visible=False)
            download_video = gr.File(label="Завантажити відео", visible=False)   # <-- Додаємо для завантаження відео

            with gr.Accordion("📊 Додаткові файли", open=False):
                json_result = gr.JSON(label="Дані у форматі JSON")
                with gr.Row():
                    download_json = gr.File(label="Завантажити JSON")
                    download_csv = gr.File(label="Завантажити CSV")

    def process_image(img):
        if img is None:
            raise gr.Error("Завантажте зображення для початку аналізу.")
        yield {status_message: gr.update(value="Обробляємо зображення...", visible=True)}

        try:
            result_img, json_path, csv_path, img_path = detection_on_image(img)
            with open(json_path, 'r', encoding='utf-8') as f:
                json_content = json.load(f)

            yield {
                output_image: gr.update(value=result_img),
                output_video: gr.update(visible=False),
                download_image: gr.update(value=img_path, visible=True),
                download_video: gr.update(visible=False, value=None),
                json_result: gr.update(value=json_content),
                download_json: gr.update(value=json_path, visible=True),
                download_csv: gr.update(value=csv_path, visible=True),
                status_message: gr.update(visible=False)
            }
        except Exception as error:
            print(f"Помилка під час обробки зображення: {error}")
            raise gr.Error("Виникла проблема при аналізі зображення. Будь ласка, спробуйте ще раз або завантажте інший файл.")

    def process_video(vid):
        if vid is None:
            raise gr.Error("Завантажте відео перед запуском аналізу.")

        yield {status_message: gr.update(value="Йде обробка відео, будь ласка зачекайте...", visible=True)}

        try:
            first_frame, json_path, csv_path, video_path = detection_on_video(vid)
            with open(json_path, 'r', encoding='utf-8') as f:
                json_content = json.load(f)

            yield {
                output_image: gr.update(value=first_frame),
                # output_video: gr.update(value=video_path, visible=True),
                download_image: gr.update(visible=False, value=None),
                download_video: gr.update(value=video_path, visible=True),
                json_result: gr.update(value=json_content),
                download_json: gr.update(value=json_path, visible=True),
                download_csv: gr.update(value=csv_path, visible=True),
                status_message: gr.update(visible=False)
            }
        except Exception as error:
            print(f"Помилка під час обробки відео: {error}")
            raise gr.Error("Під час обробки відео виникла помилка. Спробуйте ще раз або перевірте формат файлу.")

    all_outputs = [
        output_image,
        output_video,
        download_image,
        download_video,    
        json_result,
        download_json,
        download_csv,
        status_message
    ]
    button_image.click(fn=process_image, inputs=image_input, outputs=all_outputs)
    button_video.click(fn=process_video, inputs=video_input, outputs=all_outputs)

if __name__ == "__main__":
    demo.launch(debug=True)
