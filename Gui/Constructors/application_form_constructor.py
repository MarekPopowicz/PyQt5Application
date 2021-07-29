import os

import pyperclip
from PyQt5.QtGui import QIcon, QTextDocument
from PyQt5.QtPrintSupport import QPrinter

from PyQt5.QtWidgets import QDialog, QPushButton, QTextEdit, QFileDialog
from Gui.Components.button_panel import ButtonPanel
from Gui.Components.msg_dialogs import MsgBox
from Logic.main_window_logic import MainWindowLogic
import Gui.Components.constants as Const
from Logic.tools import data_export_prepare, resource_path


class ApplicationFormConstructor:
    def __init__(self, form: QDialog, operation: str, parent):
        self.parent = parent
        self.parent_logic = MainWindowLogic(self.parent)
        self.form = form
        qss_dir = resource_path("Gui\\QSS\\")
        with open(qss_dir + 'project_form.qss', 'r') as f:
            self.form.setStyleSheet(f.read())
        self.operation = operation
        self.document = QTextDocument()
        self.current_project = ''
        self.create_text_view()
        self.create_app_print_button()
        self.exec_project_form()

    def exec_project_form(self):
        self.form.adjustSize()
        current_width = self.form.width()
        current_height = self.form.height()
        self.form.setFixedSize(current_width, current_height)
        self.form.exec_()

    def create_text_view(self):
        textEdit = QTextEdit()
        textEdit.setMinimumWidth(700)
        textEdit.setMinimumHeight(900)
        self.form.layout().addWidget(textEdit)
        self.set_data(textEdit)

    def create_app_print_button(self):
        button_panel = ButtonPanel(self.form)
        self.form = button_panel.form
        print_button = self.form.findChild(QPushButton, "Zapisz")
        print_button.setIcon(QIcon(Const.PRINT_PDF_ICON))
        print_button.setText('Drukuj')
        print_button.setToolTip("Zapisz do pliku PDF")
        print_button.clicked.connect(self.save_button_clicked)

    def set_data(self, editor):
        user_data = self.parent_logic.user_logic.get_current_user()
        project_data = self.parent_logic.project_logic.get_project_data(self.parent.current_project_id)
        editor.setReadOnly(True)
        user = user_data[0][0].split()
        user_initials = user[0][:3] + user[1][:3]

        application = data_export_prepare(
            self.parent_logic.project_logic.get_project_data(self.parent.current_project_id),
            self.parent_logic.task_logic.get_tasks_list(self.parent.current_project_id),
            self.parent_logic.attachment_logic.get_attachment_data(self.parent.current_project_id))

        self.current_project = application["projekt"][0][0]

        message_text = f"Witam.\n\n" \
                       f"W załączeniu przekazuję wniosek nr {user_initials.upper()}/{self.parent.current_project_id}/{project_data[0][9][:4]}, " \
                       f"z dn. {project_data[0][9]}, o regulację terenowo-prawną\nwraz z załącznikami oraz plikiem danych dla " \
                       f"zadania: {self.current_project}.\n\nProszę o informację komu imiennie została przydzielona do realizacji " \
                       f"wnioskowana sprawa.\n\nPozdrawiam. "
        pyperclip.copy(message_text)

        html_header = f"""
               <table  width=100% >
                   <tr>
                       <td>
                           <img width="100" src="{Const.TAURON_LOGO}"/>
                       </td>
                       <td style="vertical-align: middle; ">
                           <div style="text-align: center; font-weight: bold;">
                               Wniosek nr 
                               <span style="color: red">
                                    {user_initials.upper()}/{self.parent.current_project_id}/{project_data[0][9][:4]}</span>, z dn. {project_data[0][9]}<br>
                               <span style="font-weight: normal">o regulację praw do nieruchomości pod infrastrukturą elektroenergetyczną.</span>
                               <span style="font-weight: normal"> 
                                   <strong><hr/>Wnioskujący/a: </strong><span style="color: darkblue">{project_data[0][8]}</span>, 
                                   tel.: {user_data[0][3]}
                               </span>
                           </div>

                       </td>
                   </tr>
               </table>
           """
        # <div style=\"page-break-after:always\"></div>

        if application['projekt'][0][3] == 1:
            priorytet = "Tak"
        else:
            priorytet = "Nie"

        html_project = f""" 
        <table width=100% style="margin-top:5px;"> 
        <tr> 
            <td width=65% style = 'text-align: left; padding-right: 20px '>
                    <strong>Nr inwestycji: </strong>
                <span style="color: #BF1363">
                    <strong>{application['projekt'][0][0]}</strong>
                </span>\t-\t
                    {application['projekt'][0][1]}
                    \t|\t{application['projekt'][0][2]}
            </td> 
            <td width=35% style = 'text-align: right; padding-right: 20px '>
                <strong>Priorytet: </strong>{priorytet}</td>
        </tr>
            <tr>
                <td width=65%><strong>Urządzenie: </strong>{application['projekt'][0][4]}</td>
                <td width=35%><strong>Zakres: </strong>{application['projekt'][0][5]}</td>
            </tr>
            <tr>
                <td><strong>Lokalizacja: </strong>{application['projekt'][0][6]}</td>
                <td><strong>Ulica: </strong>{application['projekt'][0][7]}</td>
            </tr>
            <tr>
                <td colspan="2">
                    <strong>Podstawa: </strong>{application['projekt'][0][10]} nr {application['projekt'][0][11]}
                    , z dn. {application['projekt'][0][12]}
                </td>
            </tr>
            <tr>
                <td colspan="2" style="font-style: italic;">
                    <strong>Uwagi: </strong>{application['projekt'][0][13]}
            </td>
        </tr>
        </table>
        """

        task_list = []
        device_list = []
        attachment_list = []
        counter = 1
        for attachment in application['zalaczniki']:

            oryginal = 'Nie'
            if attachment[1] == 1:
                oryginal = 'Tak'

            html_attachment = f"""
                                    <tr>
                                        <td style="padding-left: 10px;">{str(counter)}. {attachment[0]}</td> 
                                        <td width=10% style="text-align:center"><span style='font-weight: bold; '>Org.: </span> {oryginal}</td>
                                        <td width=10% style="text-align:center"><span style='font-weight: bold; '>Szt.: </span> {attachment[2]}</td>
                                    </tr>
                                    <tr>     
                                        <td style="font-style: italic; padding-left: 25px;" colspan="3"><span style='font-weight: bold;'>Uwagi: </span>{attachment[3]}</td> 
                                    </tr>
                           """
            counter += 1
            attachment_list.append(html_attachment)

        html_attach = ''.join(map(str, attachment_list))
        attachment_html = """<div style="width:100%">
                            <table width=100%>
                            <caption style='font-weight: bold;'><span style="color: darkblue; text-decoration: underline;">Załączniki:</span></caption>
                            """ + html_attach + """</table> 
                            </div>
                           """

        for item in application['dzialki']:

            dz = f"""<table width=100% border = '1' bordercolor = '#B2B1B9' cellpadding = '2'
                    style="border-collapse:collapse; margin-top:10px;">
                     <tr>
                        <td width=40% style="padding-left: 10px; background:#DDDDDD"><strong>Księga Wieczysta: </strong><span style="background: yellow">{item[1]}</span></td>
                        <td width=20% style="text-align:center; background:#DDDDDD"><strong>Dz. </strong>{item[2]},\t<strong>AM-</strong>{item[3]}</td>
                        <td style="text-align:center; background:#DDDDDD"><strong>Obręb: </strong>{item[4]}</td>
                     </tr>
                     <tr>
                        <td style="padding-left: 10px;" colspan="3"><strong>Właścicel: </strong>{item[5]}</td>
                     </tr>
                     <tr>
                        <td style="padding-left: 10px; font-style: italic;" colspan="3"><strong>Uwagi: </strong>{item[6]}</td>
                     </tr>
                     </table>
                     """

            for device in application['urzadzenia']:
                for dev in device:
                    if dev[0] == item[0]:
                        a = float(dev[2].replace(',', '.')) * float(dev[3].replace(',', '.'))
                        area = str("%.2f" % round(a, 2)).replace('.', ',')
                        urz = f"""<tr>
                                    <td width=50% style="padding-left: 10px; background: #E1E8EB;"><span style='color:red;'>\u26A1</span> {dev[1]}</td>
                                    <td style="text-align:center; background: #E1E8EB"><strong>Dł.: </strong>{dev[2]} m.\t<strong>Szer.: </strong>{dev[3]} m.\t<strong>Pow.: </strong>{area} m2</td>
                                </tr>
                                <tr>
                                    <td style="padding-left: 10px;" colspan="2"><strong>Regulacja: </strong>{dev[4]}</td>
                                </tr>
                                <tr>
                                    <td style="padding-left: 10px; font-style: italic;" colspan="2"><strong>Uwagi: </strong>{dev[5]}</td>
                                </tr>"""

                        device_list.append(urz)

            html_dev = ''.join(map(str, device_list))
            html_device = """<table width=100% border = '1'  
                bordercolor='#B2B1B9' cellpadding = '2' 
                style=" border-collapse:collapse; 
                margin-bottom:5px; margin-top:3px;">""" + html_dev + """</table>"""
            device_list.clear()
            html_task = dz + html_device
            task_list.append(html_task)

            task_html = ''.join(map(str, task_list))

        html_order = """<div style="width:90%; margin: 15px; text-align: center; color: #194350; font-weight: bold"> 
            Wnoszę o uregulowanie praw do nieruchomości według załączonej formuły uprawnień\n
            dla urządzeń zlokalizowanych na działkach gruntu jak poniżej:
        </div>"""

        html = html_header + html_project + html_order + task_html + attachment_html
        self.document.setHtml(html)
        editor.setDocument(self.document)

    def save_button_clicked(self):
        printer = QPrinter()
        printer.setFullPage(True)

        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPaperSize(QPrinter.A4)
        printer.setPageMargins(20, 20, 20, 20, QPrinter.Millimeter)
        printer.setColorMode(QPrinter.Color)
        printer.setResolution(300)
        printer.setOrientation(QPrinter.Portrait)
        # self.document.setPageSize(QSizeF(printer.pageRect().size()))
        #
        # self.document.setPageSize(printer.paperSize(QPrinter.Millimeter))
        # self.document.setDefaultFont(QFont("Tahoma", 4))

        filename, _ = QFileDialog.getSaveFileName(None, "Wybierz lokalizację zapisu",
                                                  os.path.expanduser(
                                                      "~/Desktop/Wniosek o regulację praw do nieruchomości nr " + self.current_project),
                                                  "PDF (*.pdf)")
        if not filename:
            return

        printer.setOutputFileName(filename)
        self.document.print_(printer)
        MsgBox("ok_dialog", "Wydruk wniosku", f"Wniosek został zapisany do pliku:\n {filename}",
               QIcon(Const.APP_ICON))
        self.form.close()
