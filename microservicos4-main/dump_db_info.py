import os
import sqlite3

SERVICOS = {
    "Gerenciamento": "./app1_gerenciamento/db/app.db",
    "Atividades": "./app2_atividades/db/app.db",
    "Reservas": "./app3_reservas/db/app.db",
}

OUTPUT_DIR = "./db_relatorios"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]

def get_columns(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()

def get_row_count(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]

def gerar_relatorio(servico, db_path):
    arquivo_saida = os.path.join(OUTPUT_DIR, f"{servico}_relatorio.txt")

    if not os.path.exists(db_path):
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write(f"Banco NÃO encontrado: {db_path}\n")
        print(f"[!] Banco não encontrado para {servico}")
        return

    conn = sqlite3.connect(db_path)

    texto = []
    texto.append(f"=== RELATÓRIO DO SERVIÇO: {servico} ===")
    texto.append(f"Banco: {db_path}\n")

    tabelas = get_tables(conn)

    if not tabelas:
        texto.append("Nenhuma tabela encontrada!\n")
    else:
        for tabela in tabelas:
            texto.append(f"\nTabela: {tabela}")
            colunas = get_columns(conn, tabela)
            texto.append("  Colunas:")
            for col in colunas:
                cid, nome, tipo, notnull, dflt, pk = col
                texto.append(f"    - {nome} ({tipo}){' [PK]' if pk else ''}")

            total = get_row_count(conn, tabela)
            texto.append(f"  Linhas: {total}")

    conn.close()

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(texto))

    print(f"[OK] Arquivo gerado: {arquivo_saida}")


if __name__ == "__main__":
    print("\nGerando relatórios dos bancos...\n")
    for servico, db_path in SERVICOS.items():
        gerar_relatorio(servico, db_path)
    print("\nConcluído!\n")
