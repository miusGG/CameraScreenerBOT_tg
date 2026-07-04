import os
import cv2
from datetime import datetime
import logging


class WebcamSaver:
    def __init__(self, output_dir="screenshot", camera_index=0):
        self.output_dir = output_dir
        self.camera_index = camera_index

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"Создана директория для скриншотов: {self.output_dir}")

    def take_screenshot(self):
        cap = cv2.VideoCapture(self.camera_index)

        if not cap.isOpened():
            logging.error("Не удалось подключиться к веб-камере.")
            return None

        cap.read()
        ret, frame = cap.read()

        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shot_{timestamp}.jpg"
            full_path = os.path.join(self.output_dir, filename)

            cv2.imwrite(full_path, frame)
            logging.info(f"Скриншот успешно сделан. Файл сохранен как: [ {filename} ] по пути: {full_path}")
            result = full_path
        else:
            logging.error("Не удалось захватить кадр с камеры.")
            result = None

        cap.release()
        return result


if __name__ == "__main__":
    camera_manager = WebcamSaver(output_dir="screenshot")
    print("Делаем снимок...")
    path = camera_manager.take_screenshot()
