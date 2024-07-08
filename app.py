import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget
import cv2
import numpy as np
from paddleocr import PaddleOCR

class ImageProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')

    def process_image(self, image_path):
        # 读取图像
        image = cv2.imread(image_path)
        
        # 使用PaddleOCR检测文字
        result, = self.ocr.ocr(image, cls=True)
        
        # 找到最右下的文本框
        if result:
            bottom_right_box = max(result, key=lambda x: x[0][2][0] + x[0][2][1])
            
            # 获取文本框坐标
            box = np.array(bottom_right_box[0], dtype=np.int32)
            
            # 创建mask
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [box], (255, 255, 255))
            
            # 使用inpaint去除水印
            image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
        
        return image

class ImageViewer:
    def __init__(self, image):
        self.image = image.copy()
        self.drawing = False
        self.mask = np.zeros(image.shape[:2], dtype=np.uint8)
        self.overlay = np.zeros_like(self.image, dtype=np.uint8)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                cv2.circle(self.mask, (x, y), 20, (255, 255, 255), -1)
                cv2.circle(self.overlay, (x, y), 20, (0, 0, 255, 0.5), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False

    def show(self):
        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.setWindowTitle('Image', "Mouse Select & Erase, Enter Apply, Q Save")
        cv2.setMouseCallback('Image', self.mouse_callback)

        while True:
            overlayed_image = cv2.addWeighted(self.image, 1, self.overlay, 0.5, 0)
            cv2.imshow('Image', overlayed_image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == 13:  # Enter key
                self.image = cv2.inpaint(self.image, self.mask, 3, cv2.INPAINT_TELEA)
                self.mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
                self.overlay = np.zeros_like(self.image, dtype=np.uint8)

        cv2.destroyAllWindows()
        return self.image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()
        
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_processing)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_processor = ImageProcessor()

    def start_processing(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.png *.webp *.jpg *.jpeg)")

        for file_path in file_paths:
            # 处理图像
            processed_image = self.image_processor.process_image(file_path)

            # 显示图像并允许进一步编辑
            viewer = ImageViewer(processed_image)
            final_image = viewer.show()

            # 保存处理后的图像并删除原图
            file_name, file_extension = os.path.splitext(file_path)
            new_file_path = f"{file_name}_fixed.jpg"
            cv2.imwrite(new_file_path, final_image)
            os.remove(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
