import sqlite3
import pandas as pd
from database.db_manager import connect_db


class Reports:
    """Gera relatórios de atividades e presença para prestação de contas."""

    @staticmethod
    def generate_presence_summary(start_date=None, end_date=None):
        """
        Gera um resumo da presença dos alunos em um período,
        agrupando por aluno e contando o total de presenças.
        """
        conn = connect_db()

        # Consulta SQL para buscar os dados de presença junto com o nome do aluno
        query = """
                SELECT s.name  AS student_name, \
                       r.date, \
                       a.title AS activity_title, \
                       r.is_present
                FROM presence_records r
                         JOIN students s ON r.student_id = s.id
                         JOIN activities a ON r.activity_id = a.id
                WHERE r.is_present = 1 \
                """

        # Adiciona filtros de data se fornecidos
        date_filters = []
        params = []
        if start_date:
            date_filters.append("r.date >= ?")
            params.append(start_date)
        if end_date:
            date_filters.append("r.date <= ?")
            params.append(end_date)

        if date_filters:
            query += " AND " + " AND ".join(date_filters)

        query += " ORDER BY s.name, r.date"

        # Lê os dados no DataFrame
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        if df.empty:
            return None

        # Processamento com Pandas: conta o total de presenças por aluno
        summary_df = df.groupby('student_name').agg(
            total_presences=('student_name', 'count'),
            first_activity=('date', 'min'),
            last_activity=('date', 'max')
        ).reset_index()

        summary_df.columns = ['Aluno', 'Total de Presenças', 'Primeira Atividade', 'Última Atividade']

        return summary_df

    @staticmethod
    def export_report(dataframe, file_path, format='excel'):
        """Exporta o DataFrame gerado para Excel ou CSV."""
        if dataframe is None or dataframe.empty:
            return False

        try:
            if format.lower() == 'excel':
                # Requer a biblioteca openpyxl ou xlsxwriter para exportar para .xlsx
                dataframe.to_excel(file_path + '.xlsx', index=False)
            elif format.lower() == 'csv':
                dataframe.to_csv(file_path + '.csv', index=False, sep=';')
            elif format.lower() == 'pdf':
                # Nota: A exportação para PDF é complexa com Pandas e Kivy.
                # Geralmente requer bibliotecas adicionais (como ReportLab) ou
                # a conversão de HTML intermediária, sendo mais simples
                # exportar para Excel/CSV para a maioria das prestações de contas.
                return False  # Não suportado nativamente pelo modelo simplificado
            return True
        except Exception as e:
            print(f"Erro ao exportar relatório: {e}")
            return False