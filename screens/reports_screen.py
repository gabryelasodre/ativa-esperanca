import datetime

from kivy.uix.screenmanager import Screen
from models.reports_model import Reports
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App


class ReportsScreen(Screen):
    """Tela para seleção de filtros e geração de relatórios."""

    def imprimir_relatorio(self):
        # Acesso ao usuário logado para verificar permissões
        app = App.get_running_app()

        if app.logged_user is None or app.logged_user['role'] != 'coordinator':  # [4] é o índice da role no tuplo retornado
            self.show_popup('Acesso Negado', 'Somente a Coordenação pode gerar relatórios.')
            return

        start_date = self.ids.start_date.text  # TextInput format YYYY-MM-DD
        end_date = self.ids.end_date.text  # TextInput format YYYY-MM-DD

        # O caminho de saída deve ser ajustado para o sistema de arquivos do dispositivo
        # Usando um nome simples por enquanto.
        file_name = 'Relatorio_Presenca_' + datetime.datetime.now().strftime("%Y%m%d")

        report_df = Reports.generate_presence_summary(start_date, end_date)

        if report_df is None:
            self.show_popup('Relatório Vazio', 'Não foram encontrados registros para o período selecionado.')
            return

        # Exporta como Excel
        success = Reports.export_report(report_df, file_name, format='excel')

        if success:
            self.show_popup('Sucesso', f'Relatório exportado para {file_name}.xlsx')
        else:
            self.show_popup('Erro', 'Falha na exportação do arquivo. Verifique se o Pandas/openpyxl estão instalados.')

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.4)).open()