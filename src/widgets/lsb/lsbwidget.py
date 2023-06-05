from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QFileDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from modules.lsb import message_encode, message_decode
from utils.appstate import AppState

BUTTON_WIDTH = 200
BUTTON_STYLES = "margin: 40px 0; height: 40px"

class LSBWidget(QWidget):
    changed_state = Signal(AppState)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.row = QHBoxLayout()

        self.header_lbl = QLabel("LSB")
        self.header_lbl.setAlignment(Qt.AlignCenter)
        self.header_lbl.setMargin(20)
        self.layout.addWidget(self.header_lbl)

        self.bytes_cycle = ''

        self.bytes_cycle_lbl = QLabel("Bytes cycle")
        self.layout.addWidget(self.bytes_cycle_lbl)

        self.bytes_cycle_input = QLineEdit()
        self.bytes_cycle_input.textChanged.connect(self.bytes_cycle_changed)
        self.bytes_cycle_input.setFixedWidth(BUTTON_WIDTH)
        self.layout.addWidget(self.bytes_cycle_input)

        self.bits_per_char = ''

        self.bits_per_char_lbl = QLabel("Bits for char")
        self.layout.addWidget(self.bits_per_char_lbl)

        self.bits_per_char_input = QLineEdit()
        self.bits_per_char_input.textChanged.connect(self.bits_per_char_changed)
        self.bits_per_char_input.setFixedWidth(BUTTON_WIDTH)
        self.layout.addWidget(self.bits_per_char_input)

        ##########################
        # Encode
        ##########################

        self.file_to_encode = ''

        self.encode_layout = QVBoxLayout()
        self.encode_layout.setAlignment(Qt.AlignTop)

        self.encode_header_lbl = QLabel("Encode message")

        self.load_file_to_encode_btn = QPushButton("Load audio file")
        self.load_file_to_encode_btn.setFixedWidth(BUTTON_WIDTH)
        self.load_file_to_encode_btn.clicked.connect(self.load_file_to_encode)

        self.loaded_file_to_encode_lbl = QLabel(f"Not loaded file!")

        self.encode_layout.addWidget(self.encode_header_lbl)
        self.encode_layout.addWidget(self.load_file_to_encode_btn)
        self.encode_layout.addWidget(self.loaded_file_to_encode_lbl)

        self.message_text_file =''

        self.load_text_file_btn = QPushButton("Load message text file")
        self.load_text_file_btn.setFixedWidth(BUTTON_WIDTH)
        self.load_text_file_btn.clicked.connect(self.load_file_with_message)
        self.encode_layout.addWidget(self.load_text_file_btn)

        self.load_text_file_lbl = QLabel(f"Not loaded file!")
        self.encode_layout.addWidget(self.load_text_file_lbl)

        self.encoded_file = ''

        self.audio_file_to_save_btn = QPushButton("Choose place to save encoded audio")
        self.audio_file_to_save_btn.setFixedWidth(BUTTON_WIDTH)
        self.audio_file_to_save_btn.clicked.connect(self.load_audio_file_to_save)
        self.encode_layout.addWidget(self.audio_file_to_save_btn)

        self.audio_file_to_save_lbl = QLabel(f"Not loaded file!")
        self.encode_layout.addWidget(self.audio_file_to_save_lbl)

        self.encode_btn = QPushButton("Code message")
        self.encode_btn.setFixedWidth(BUTTON_WIDTH)
        self.encode_btn.setStyleSheet(BUTTON_STYLES)
        self.encode_btn.clicked.connect(self.encode)
        self.encode_layout.addWidget(self.encode_btn)


        self.row.addLayout(self.encode_layout)

        ##########################
        # decode
        ##########################

        self.file_to_decode = ''

        self.decode_layout = QVBoxLayout()
        self.decode_layout.setAlignment(Qt.AlignTop)

        self.decode_header = QLabel("Decode message")

        self.load_file_to_decode_btn = QPushButton("Load audio file")
        self.load_file_to_decode_btn.setFixedWidth(BUTTON_WIDTH)
        self.load_file_to_decode_btn.clicked.connect(self.load_file_to_decode)

        self.loaded_file_to_decode_lbl = QLabel(f"Not loaded file!")

        self.file_to_save = ''

        self.message_to_save_btn = QPushButton("Choise place to save message")
        self.message_to_save_btn.setFixedWidth(BUTTON_WIDTH)
        self.message_to_save_btn.clicked.connect(self.load_file_to_save)

        self.message_lbl = QLabel(f"Not loaded file!")

        self.decode_btn = QPushButton("Decode message")
        self.decode_btn.setFixedWidth(BUTTON_WIDTH)
        self.decode_btn.setStyleSheet(BUTTON_STYLES)
        self.decode_btn.clicked.connect(self.decode)

        self.decode_layout.addWidget(self.decode_header)
        self.decode_layout.addWidget(self.load_file_to_decode_btn)
        self.decode_layout.addWidget(self.loaded_file_to_decode_lbl)
        self.decode_layout.addWidget(self.message_to_save_btn)
        self.decode_layout.addWidget(self.message_lbl)
        self.decode_layout.addWidget(self.decode_btn)


        self.row.addLayout(self.decode_layout)


        self.go_back = QPushButton("Go back")
        self.go_back.setFixedWidth(BUTTON_WIDTH)
        self.go_back.clicked.connect(lambda: self.changed_state.emit(AppState.MainMenu))


        self.layout.addLayout(self.row)
        self.layout.addWidget(self.go_back)

    def load_file_to_encode(self):
        file_name = QFileDialog.getOpenFileName()[0]
        self.file_to_encode = file_name
        self.loaded_file_to_encode_lbl.setText(f"Loaded file: {file_name}")

    def load_file_to_decode(self):
        file_name = QFileDialog.getOpenFileName()[0]
        self.file_to_decode = file_name
        self.loaded_file_to_decode_lbl.setText(f"Loaded file: {file_name}")

    def load_file_with_message(self):
        file_name = QFileDialog.getOpenFileName()[0]
        self.message_text_file = file_name
        self.load_text_file_lbl.setText(f"Loaded file: {file_name}")

    def load_file_to_save(self):
        file_name = QFileDialog.getSaveFileUrl()[0].toLocalFile()
        self.file_to_save = file_name
        self.message_lbl.setText(f"Save location: {file_name}")

    def load_audio_file_to_save(self):
        file_name = QFileDialog.getSaveFileUrl()[0].toLocalFile()
        self.encoded_file = file_name
        self.audio_file_to_save_lbl.setText(f"Save location: {file_name}")

    def bytes_cycle_changed(self):
        if str(self.bytes_cycle) == self.bytes_cycle_input.text():
            return
        try:
            self.bytes_cycle = int(self.bytes_cycle_input.text())
        except Exception as e:
            print(e)
        finally:
            self.bytes_cycle_input.setText(str(self.bytes_cycle))

    def bits_per_char_changed(self):
        if str(self.bits_per_char) == self.bits_per_char_input.text():
            return
        try:
            self.bits_per_char = int(self.bits_per_char_input.text())
        except Exception as e:
            print(e)
        finally:
            self.bits_per_char_input.setText(str(self.bits_per_char))

    def change_state(self, state):
        self.changed_state.emit(state)

    def encode(self):
        message_encode(self.file_to_encode, self.message_text_file, self.encoded_file, self.bytes_cycle, self.bits_per_char)

    def decode(self):
        message_decode(self.file_to_decode, self.file_to_save, self.bytes_cycle, self.bits_per_char)