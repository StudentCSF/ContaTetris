import os

from MainWindowUI import Ui_MainWindow as MainWindowUI
from game import Game, GameState

from PyQt5 import QtSvg
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem, QMessageBox
from PyQt5.QtCore import QModelIndex, QRectF, Qt


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("My Tetris")
        self._pressed = False
        self._ready = False
        self._kit_i = -1
        self._pos = []

        self.dialog = QMessageBox()
        self.dialog.setWindowTitle('Oops')
        self.dialog.setText('Game over')

        self.actionQuit.triggered.connect(self.close)

        self.actionNew_game.triggered.connect(self.on_new_game)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self._game = Game(10, 10)
        self.game_resize(self._game)

        class MyDelegate(QItemDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_field_paint(idx, painter, option)
                painter.restore()

        class MyD1(MyDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_elem_paint(0, idx, painter, option)
                painter.restore()

        class MyD2(MyDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_elem_paint(1, idx, painter, option)
                painter.restore()

        class MyD3(MyDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_elem_paint(2, idx, painter, option)
                painter.restore()

        self.field.setItemDelegate(MyDelegate(self))
        self.elem1.setItemDelegate(MyD1(self))
        self.elem2.setItemDelegate(MyD2(self))
        self.elem3.setItemDelegate(MyD3(self))

        def field_mouse_press_event(e: QMouseEvent) -> None:
            idx = self.field.indexAt(e.pos())
            self.on_field_clicked(idx, e)

        def elem1_mouse_press_event(e: QMouseEvent) -> None:
            self._kit_i = 0
            self.on_elem_clicked(e)

        def elem2_mouse_press_event(e: QMouseEvent) -> None:
            self._kit_i = 1
            self.on_elem_clicked(e)

        def elem3_mouse_press_event(e: QMouseEvent) -> None:
            self._kit_i = 2
            self.on_elem_clicked(e)

        self.field.mousePressEvent = field_mouse_press_event
        self.elem1.mousePressEvent = elem1_mouse_press_event
        self.elem2.mousePressEvent = elem2_mouse_press_event
        self.elem3.mousePressEvent = elem3_mouse_press_event

    def game_resize(self, game: Game) -> None:
        model = QStandardItemModel(game.row_count, game.col_count)
        self.field.setModel(model)
        self.elem1.setModel(QStandardItemModel(4, 4))
        self.elem2.setModel(QStandardItemModel(4, 4))
        self.elem3.setModel(QStandardItemModel(4, 4))
        self.update_view()

    def update_view(self):
        self.field.viewport().update()
        self.elem1.viewport().update()
        self.elem2.viewport().update()
        self.elem3.viewport().update()
        if self._game.state == GameState.LOSE:
            self.dialog.show()

    def new_game(self):
        self._game.new_game()
        self.game_resize(self._game)
        self.update_view()

    def on_new_game(self):
        self.new_game()

    def on_field_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem):
        item = self._game.field[e.row()][e.column()]
        if item == 1:
            img = self._images['red']
            img.render(painter, QRectF(option.rect))
        if item == -1:
            img = self._images['blue']
            img.render(painter, QRectF(option.rect))

    def on_elem_paint(self, m: int, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem):
        tmp = self._game.kit[m].it
        if e.row() < len(tmp) and e.column() < len(tmp[0]):
            item = tmp[e.row()][e.column()]
            if item == 1:
                img = self._images['red']
                img.render(painter, QRectF(option.rect))

    def on_elem_clicked(self, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton:
            self._game.clear_opp()
            self._pressed = True
            self._game.elem_left_mouse_click(self._kit_i)
        self.update_view()

    def on_field_clicked(self, e: QModelIndex, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton:
            if self._ready and e.row() == self._pos[0] and e.column() == self._pos[1]:
                self._game.field_left_mouse_click(e.row(), e.column(), True)
                self._pressed = False
                self._ready = False
                self._pos = []
            elif self._pressed:
                self._game.clear_opp()
                self._ready = self._game.field_left_mouse_click(e.row(), e.column(), False)
                self._pos = [e.row(), e.column()]
        self.update_view()
