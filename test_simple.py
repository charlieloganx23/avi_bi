"""
Teste simples de conexão
"""
import sys
sys.path.append('.')

from modules.powerbi_connector import PowerBIConnector

print("=" * 60)
print("TESTE DE CONEXÃO")
print("=" * 60)

# 1. Listar instâncias
connector = PowerBIConnector()
instances = connector.list_local_instances()

if not instances:
    print("❌ Nenhuma instância encontrada")
    sys.exit(1)

print(f"\n✅ Encontradas {len(instances)} instância(s)")

# 2. Conectar
print("\n🔌 Tentando conectar...")
port = instances[0]['port']
dataset = instances[0].get('dataset', 'Model')

success = connector.connect_to_desktop(port=port, dataset_name=dataset)

if success:
    print("\n✅ CONEXÃO BEM SUCEDIDA!")
    print(f"   Porta: {port}")
    print(f"   Dataset: {dataset}")
    print(f"   Conectado: {connector.is_connected()}")
    
    # Desconectar
    connector.disconnect()
    print("\n🔌 Desconectado")
else:
    print("\n❌ FALHA NA CONEXÃO")
    sys.exit(1)

print("\n" + "=" * 60)
print("TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 60)
