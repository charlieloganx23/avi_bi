"""
Script para obter o nome correto do dataset conectando e listando databases
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("="*60)
    print("🔍 DESCOBRINDO DATABASES DISPONÍVEIS")
    print("="*60)
    
    try:
        import clr
        
        # Adicionar caminhos das DLLs
        dll_paths = [
            r"C:\Program Files\Microsoft.NET\ADOMD.NET\160",
            r"C:\Program Files (x86)\Microsoft SQL Server Management Studio 20\Common7\IDE",
            r"C:\Program Files\Microsoft SQL Server\160\DTS\Binn",
        ]
        
        for dll_path in dll_paths:
            if os.path.exists(dll_path) and dll_path not in sys.path:
                sys.path.append(dll_path)
                os.environ['PATH'] = dll_path + os.pathsep + os.environ.get('PATH', '')
        
        # Carregar TOM (Tabular Object Model)
        clr.AddReference("Microsoft.AnalysisServices.Tabular")
        from Microsoft.AnalysisServices.Tabular import Server
        
        print("\n✅ Tabular Object Model carregado")
        
        # Conectar ao servidor sem especificar database
        port = 56495
        print(f"\n🔌 Conectando a localhost:{port}...")
        
        server = Server()
        server.Connect(f"DataSource=localhost:{port}")
        
        print(f"\n📊 Databases disponíveis: {server.Databases.Count}")
        for i in range(server.Databases.Count):
            db = server.Databases[i]
            print(f"   {i+1}. {db.Name} (ID: {db.ID})")
            
            if hasattr(db, 'Model'):
                model = db.Model
                if hasattr(model, 'Tables'):
                    print(f"      └─ Tabelas: {model.Tables.Count}")
        
        server.Disconnect()
        print("\n✅ Sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
