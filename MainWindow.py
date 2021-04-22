import os

from MainWindowUI import Ui_MainWindow as MainWindowUI
from game import Game, GameState, Element

from PyQt5 import QtSvg
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QModelIndex, QRectF, QTimer, Qt


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("My Tetris")

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
                self.parent().on_item_paint(0, idx, painter, option)
                self.parent().on_item_paint(1, idx, painter, option)
                self.parent().on_item_paint(2, idx, painter, option)
                self.parent().on_item_paint(3, idx, painter, option)
                painter.restore()

        class MyD1(MyDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                super(MyD1, self).paint(painter, option, idx)

        self.field.setItemDelegate(MyDelegate(self))
        self.elem1.setItemDelegate(MyD1(self))
        self.elem2.setItemDelegate(MyD1(self))
        self.elem3.setItemDelegate(MyD1(self))

        # такие ухищрения, т.к. не предусмотрено сигналов для правой кнопки мыши
        #       def new_mouse_press_event(e: QMouseEvent) -> None:
        #          idx = self.gameFieldTableView.indexAt(e.pos())
        #         self.on_item_clicked(idx, e)
        #    self.gameFieldTableView.mousePressEvent = new_mouse_press_event
        #
        #       self.newGamePushButton.clicked.connect(self.on_new_game)

        self.new_game()

    def game_resize(self, game: Game) -> None:
        model = QStandardItemModel(game.row_count, game.col_count)
        self.field.setModel(model)
        self.elem1.setModel(QStandardItemModel(len(self._game.kit[0].it), len(self._game.kit[0].it[0])))
        self.elem2.setModel(QStandardItemModel(len(self._game.kit[1].it), len(self._game.kit[1].it[0])))
        self.elem3.setModel(QStandardItemModel(len(self._game.kit[2].it), len(self._game.kit[2].it[0])))
        self.update_view()

    def update_view(self):
        self.field.viewport().update()
        self.elem1.viewport().update()
        self.elem2.viewport().update()
        self.elem3.viewport().update()

    def new_game(self):
        self._game.new_game()
        self.game_resize(self._game)
        self.update_view()

    def on_new_game(self):
        self.new_game()

    def on_item_paint(self, m, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem):
        if m == 0:
            item = self._game.field[e.row()][e.column()]
            if item == 1:
                img = self._images['square']
                img.render(painter, QRectF(option.rect))
        else:
            tmp = self._game.kit[m - 1].it
            if e.row() < len(tmp) and e.column() < len(tmp[0]):
                item = tmp[e.row()][e.column()]
                if item == 1:
                    img = self._images['square']
                    img.render(painter, QRectF(option.rect))

    #  def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
    #     item = self._game[e.row(), e.column()]
    #    if item.state == SapperCellState.FLAG:
    #       img = self._images['flag']
    #  elif item.state == SapperCellState.PROBLEM:
    #     img = self._images['problem']
    # elif item.state == SapperCellState.OPENED and item.mine:
    #    img = self._images['mine_red']
    # elif self._game.state == SapperGameState.FAIL and item.mine:
    #    img = self._images['mine']
    # elif item.state == SapperCellState.OPENED:
    #    img = self._images['type' + str(item.around)]
    # else:
    #   img = self._images['closed']
    # img.render(painter, QRectF(option.rect))

    def on_item_clicked(self, e: QModelIndex, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton:
            self._game.left_mouse_click(e.row(), e.column())
        elif me.button() == Qt.RightButton:
            self._game.right_mouse_click(e.row(), e.column())
        self.update_view()
