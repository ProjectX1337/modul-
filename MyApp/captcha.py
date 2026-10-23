import random
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize, Qt


class PuzzleCaptcha(QWidget):
    def __init__(self, image_paths, tile_size=100, parent=None):
        super().__init__(parent)
        self.tile_size = tile_size
        self.image_paths = image_paths
        self.tiles = []
        self.current_order = [0, 1, 2, 3]
        self.selected_index = -1
        self.init_ui()
        self.shuffle()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(2)
        self.setLayout(layout)

        self.image_parts = []
        for path in self.image_paths:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                pixmap = QPixmap(self.tile_size, self.tile_size)
                pixmap.fill(Qt.GlobalColor.lightGray)
            pixmap = pixmap.scaled(
                self.tile_size,
                self.tile_size,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_parts.append(pixmap)

        for i in range(4):
            btn = QPushButton()
            btn.setFixedSize(QSize(self.tile_size, self.tile_size))
            btn.setIconSize(QSize(self.tile_size, self.tile_size))
            btn.clicked.connect(lambda _, idx=i: self.on_tile_clicked(idx))
            self.tiles.append(btn)
            layout.addWidget(btn, i // 2, i % 2)

        self.update_tiles()

    def on_tile_clicked(self, index):
        if self.selected_index == -1:
            self.selected_index = index
            self.tiles[index].setStyleSheet("border: 3px solid red;")
        elif self.selected_index == index:
            self.tiles[index].setStyleSheet("")
            self.selected_index = -1
        else:
            self.swap_tiles(self.selected_index, index)
            self.tiles[self.selected_index].setStyleSheet("")
            self.selected_index = -1
            self.update_tiles()

    def swap_tiles(self, i, j):
        self.current_order[i], self.current_order[j] = self.current_order[j], self.current_order[i]

    def shuffle(self):
        random.shuffle(self.current_order)
        if self.is_solved():
            self.swap_tiles(0, 1)
        self.update_tiles()
        self.selected_index = -1

    def update_tiles(self):
        for i in range(4):
            image_index = self.current_order[i]
            self.tiles[i].setIcon(QIcon(self.image_parts[image_index]))

    def is_solved(self):
        return self.current_order == [0, 1, 2, 3]

    def reset(self):
        for tile in self.tiles:
            tile.setStyleSheet("")
        self.shuffle()