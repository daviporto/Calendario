from PyQt5 import QtCore, QtGui, QtWidgets
import pickle
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(668, 609)
        self.save_file = os.path.join("save", "save.pkl")
        self.eventos = {}
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.calendario = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendario.setObjectName("calendario")
        self.gridLayout.addWidget(self.calendario, 0, 0, 1, 4)
        self.lbl_eventos = QtWidgets.QLabel(self.centralwidget)
        self.lbl_eventos.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_eventos.setText("eventos hoje ")
        self.lbl_eventos.setObjectName("label")
        self.gridLayout.addWidget(self.lbl_eventos, 1, 0, 1, 1)
        self.entry_titulo = QtWidgets.QLineEdit(self.centralwidget)
        self.entry_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.entry_titulo.setObjectName("entry")
        self.entry_titulo.setText("titulo")
        self.gridLayout.addWidget(self.entry_titulo, 1, 1, 1, 3)
        self.list_events = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_events.sizePolicy().hasHeightForWidth())
        self.list_events.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(13)
        self.list_events.setFont(font)
        self.list_events.setObjectName("list_events")
        self.gridLayout.addWidget(self.list_events, 2, 0, 3, 1)
        self.tags = QtWidgets.QComboBox(self.centralwidget)
        self.tags.setObjectName("tags")
        self.tags.addItem("reuniao")
        self.tags.addItem("prova")
        self.tags.addItem("aniversario")
        self.tags.addItem("outros...")
        self.gridLayout.addWidget(self.tags, 2, 1, 1, 1)
        self.time_event = QtWidgets.QTimeEdit(self.centralwidget)
        self.time_event.setObjectName("time_event")
        self.gridLayout.addWidget(self.time_event, 2, 2, 1, 1)
        self.cb_allDay = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_allDay.setObjectName("cb_allDay")
        self.cb_allDay.setText("dia todo")
        self.gridLayout.addWidget(self.cb_allDay, 2, 3, 1, 1)
        self.txt_event = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(13)
        self.txt_event.setFont(font)
        self.txt_event.setObjectName("txt_event")
        self.gridLayout.addWidget(self.txt_event, 3, 1, 1, 3)
        self.btn_adicionar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_adicionar.setText("adicionar/atualizar")
        self.gridLayout.addWidget(self.btn_adicionar, 4, 1, 1, 1)
        self.btn_remover = QtWidgets.QPushButton(self.centralwidget)
        self.btn_remover.setText("remover")
        self.gridLayout.addWidget(self.btn_remover, 4, 2, 1, 1)
        self.btn_resetar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_resetar.setText("resetar")
        self.btn_resetar.setToolTip("esquece o save")
        self.gridLayout.addWidget(self.btn_resetar, 4, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 668, 22))
        self.menubar.setObjectName("menubar")
        self.menusalvar = QtWidgets.QMenu(self.menubar)
        self.menusalvar.setObjectName("menusalvar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsalvar = QtWidgets.QAction(MainWindow)
        self.actionsalvar.setObjectName("actionsalvar")
        self.actioncarregar = QtWidgets.QAction(MainWindow)
        self.actioncarregar.setObjectName("actioncarregar")
        self.menusalvar.addAction(self.actionsalvar)
        self.menusalvar.addAction(self.actioncarregar)
        self.menubar.addAction(self.menusalvar.menuAction())

        self.calendario.selectionChanged.connect(self.preenche_eventos_dia)
        self.cb_allDay.toggled.connect(self.time_event.setDisabled)
        self.list_events.itemSelectionChanged.connect(self.preencher_descricao)
        self.btn_adicionar.clicked.connect(self.salvar_evento)
        self.list_events.itemSelectionChanged.connect(self.ha_evento_para_deletar)
        self.ha_evento_para_deletar()
        self.btn_remover.clicked.connect(self.excluir_evento)
        self.btn_resetar.clicked.connect(self.resetar)

    def preenche_eventos_dia(self):
        self.list_events.clear()
        data = self.calendario.selectedDate()
        self.limpar_dados()

        for evento in self.eventos.get(data, []):
            time = (
                evento['time'].toString('hh:mm')
                if evento['time']
                else 'All Day'
            )
            self.list_events.addItem(f"{time}: {evento['titulo']}")

    def preencher_descricao(self):
        self.txt_event.clear()
        data = self.calendario.selectedDate()
        numero_evento = self.list_events.currentRow()
        if numero_evento == -1:
            return
        try:
            dados_evento = self.eventos.get(data)[numero_evento]
            # se tentar mudar de dia com um evento selecionado
        except:
            return
        self.tags.setCurrentText(dados_evento['tag'])
        if dados_evento['time']:
            self.time_event.setTime(dados_evento['time'])
        else:
            self.cb_allDay.setChecked(True)

        self.entry_titulo.setText(dados_evento['titulo'])
        self.txt_event.setPlainText(dados_evento['descricao'])

    def limpar_dados(self):
        self.entry_titulo.clear()
        self.tags.setCurrentIndex(0)
        self.time_event.setTime(QtCore.QTime(8, 0))
        self.cb_allDay.setChecked(False)
        self.txt_event.setPlainText('')

    def salvar_evento(self):
        evento = {
            'tag': self.tags.currentText(),
            'time': (
                None
                if self.cb_allDay.isChecked()
                else self.time_event.time()
            ),
            'titulo': self.entry_titulo.text(),
            'descricao': self.txt_event.toPlainText()
        }

        date = self.calendario.selectedDate()
        lista_eventos = self.eventos.get(date, [])
        event_number = self.list_events.currentRow()

        if event_number == -1:
            lista_eventos.append(evento)
        else:
            lista_eventos[event_number] = evento

        lista_eventos.sort(key=lambda x: x['time'] or QtCore.QTime(0, 0))
        self.eventos[date] = lista_eventos
        self.preenche_eventos_dia()
        self.save()

    def excluir_evento(self):
        dados = self.calendario.selectedDate()
        row = self.list_events.currentRow()
        del (self.eventos[dados][row])
        self.list_events.setCurrentRow(-1)
        self.limpar_dados()
        self.preenche_eventos_dia()
        self.save()

    def ha_evento_para_deletar(self):
        self.btn_remover.setDisabled(
            self.list_events.currentRow() == -1)

    def save(self):
        pickle_dict = pickle.dumps(self.eventos)
        with open(self.save_file, 'wb') as file:
            file.write(pickle_dict)

    def load(self):
        try:
            file = open(self.save_file, 'rb')
            self.eventos = pickle.load(file)
            self.preenche_eventos_dia()
        except:
            pass
            #nothing to be load

    def resetar(self):
        self.eventos = {}
        self.preenche_eventos_dia()
        self.save()
