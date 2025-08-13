#!/usr/bin/env python3
"""
Sistema de Bioprospecção de Cogumelos Nativos
Arquivo de execução simplificado
"""

import os
import sys
from app import app, db

def create_directories():
    """Cria diretórios necessários se não existirem"""
    directories = ['uploads']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Diretório '{directory}' criado com sucesso")

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_migrate
        import PIL
        print("✓ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"✗ Erro: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def init_database():
    """Inicializa o banco de dados"""
    try:
        with app.app_context():
            db.create_all()
            print("✓ Banco de dados inicializado com sucesso")
    except Exception as e:
        print(f"✗ Erro ao inicializar banco de dados: {e}")
        return False
    return True

def main():
    """Função principal"""
    print("🍄 Sistema para Bioprospecção de Cogumelos Nativos")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Criar diretórios
    create_directories()
    
    # Inicializar banco de dados
    if not init_database():
        sys.exit(1)
    
    print("\n🚀 Iniciando o sistema...")
    print("📱 Acesse: http://localhost:5000")
    print("🛑 Pressione Ctrl+C para parar")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"\n✗ Erro ao executar o sistema: {e}")

if __name__ == '__main__':
    main()
