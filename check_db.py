# check_db.py


import os
import sqlite3

# Serviços e caminhos relativos dentro do projeto
services = {
    "Gerenciamento": "./app1_gerenciamento/db/app.db",
    "Atividades": "./app2_atividades/db/app.db",
    "Reservas": "./app3_reservas/db/app.db"
}

for service_name, db_path in services.items():
    print(f"\nVerificando serviço: {service_name}")
    
    if not os.path.exists(db_path):
        print(f"  Banco não encontrado em: {db_path}")
        continue

    print(f"  Banco encontrado em: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("  Tabelas encontradas:")
            for table in tables:
                print("   -", table[0])
        else:
            print("  Nenhuma tabela encontrada.")
    except Exception as e:
        print("  Erro ao acessar o banco:", e)
    finally:
        if 'conn' in locals():
            conn.close()
