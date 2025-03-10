import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QListWidget, QFileDialog
)

class INCARGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tags = {
            "离子步参数": ["EDIFFG", "IBRION", "POTIM", "NSW", "ISIF", "NFREE"],
            "电子步参数": ["ENCUT", "ISMEAR", "SIGMA", "EDIFF", "NELMIN", "NELMDL", "NELM", 
                         "PREC", "NGX", "NGY", "NGZ", "NGXF", "NGYF", "NGZF", "ADDGRID", "LREAL"],
            "其他参数": ["ISPIN", "MAGMOM", "NBANDS", "NEDOS", "EMIN", "EMAX", "LDAU", "LDAUL",
                        "LDAUU", "LDAUJ", "IVDW", "VDW_RADIUS", "GGA", "LHFCALC", "HFSCREEN"]
        }
        self.populate_categories()
    
    def initUI(self):
        layout = QVBoxLayout()

        # 分类选择
        category_layout = QHBoxLayout()
        self.category_label = QLabel("选择类别:")
        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self.populate_tags)
        category_layout.addWidget(self.category_label)
        category_layout.addWidget(self.category_combo)
        
        # Tag 选择
        tag_layout = QHBoxLayout()
        self.tag_label = QLabel("选择Tag:")
        self.tag_combo = QComboBox()
        tag_layout.addWidget(self.tag_label)
        tag_layout.addWidget(self.tag_combo)

        # Value 输入
        input_layout = QHBoxLayout()
        self.value_label = QLabel("输入Value:")
        self.value_input = QLineEdit()
        self.add_button = QPushButton("添加")
        self.add_button.clicked.connect(self.add_tag_value)
        input_layout.addWidget(self.value_label)
        input_layout.addWidget(self.value_input)
        input_layout.addWidget(self.add_button)

        # 列表展示已添加内容
        self.list_widget = QListWidget()
        
        # 删除按钮
        self.delete_button = QPushButton("删除选中项")
        self.delete_button.clicked.connect(self.delete_selected_item)

        # 保存和加载按钮
        self.save_button = QPushButton("导出INCAR")
        self.save_button.clicked.connect(self.export_incar)
        self.load_config_button = QPushButton("加载配置")
        self.load_config_button.clicked.connect(self.load_config)

        # 布局管理
        layout.addLayout(category_layout)
        layout.addLayout(tag_layout)
        layout.addLayout(input_layout)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_config_button)

        self.setLayout(layout)
        self.setWindowTitle("INCAR 生成器")

    def populate_categories(self):
        self.category_combo.addItems(self.tags.keys())
        self.populate_tags()

    def populate_tags(self):
        self.tag_combo.clear()
        category = self.category_combo.currentText()
        if category in self.tags:
            self.tag_combo.addItems(self.tags[category])

    def add_tag_value(self):
        tag = self.tag_combo.currentText()
        value = self.value_input.text()
        if tag and value:
            self.list_widget.addItem(f"{tag} = {value}")
            self.value_input.clear()

    def delete_selected_item(self):
        selected_item = self.list_widget.currentRow()
        if selected_item >= 0:
            self.list_widget.takeItem(selected_item)

    def export_incar(self):
        filename, _ = QFileDialog.getSaveFileName(self, "保存 INCAR", "INCAR", "All Files (*)")
        if filename:
            with open(filename, "w") as f:
                for i in range(self.list_widget.count()):
                    f.write(self.list_widget.item(i).text() + "\n")

    def load_config(self):
        filename, _ = QFileDialog.getOpenFileName(self, "加载配置", "", "JSON Files (*.json)")
        if filename:
            with open(filename, "r") as f:
                config = json.load(f)
                self.list_widget.clear()
                for tag, value in config.items():
                    self.list_widget.addItem(f"{tag} = {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = INCARGenerator()
    window.show()
    sys.exit(app.exec())
