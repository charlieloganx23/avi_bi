"""
Script de teste para verificar conexão com Power BI Desktop
"""
from modules.powerbi_connector import PowerBIConnector
import subprocess

def test_powerbi_detection():
    """Testa detecção do Power BI Desktop"""
    print("=" * 60)
    print("TESTE: Detecção do Power BI Desktop")
    print("=" * 60)
    
    # 1. Verifica se o processo está rodando
    print("\n📋 Verificando processos do Power BI...")
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Process | Where-Object {$_.ProcessName -like "*PBIDesktop*"} | Select-Object Id, ProcessName, MainWindowTitle'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            if "PBIDesktop" in result.stdout:
                print("✅ Power BI Desktop está rodando!")
                print(result.stdout)
            else:
                print("⚠️ Nenhum processo do Power BI encontrado")
                print("💡 Certifique-se de que o Power BI Desktop está aberto")
        else:
            print(f"❌ Erro ao executar comando: {result.stderr}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 2. Tenta listar instâncias
    print("\n🔍 Listando instâncias disponíveis...")
    connector = PowerBIConnector()
    instances = connector.list_local_instances()
    
    if instances:
        print(f"✅ Encontradas {len(instances)} instância(s):")
        for idx, instance in enumerate(instances, 1):
            print(f"   {idx}. {instance.get('name')} (Porta: {instance.get('port')})")
    else:
        print("⚠️ Nenhuma instância detectada")
        print("\n💡 Dicas de solução:")
        print("   1. Abra o Power BI Desktop")
        print("   2. Carregue ou crie um arquivo .pbix")
        print("   3. Certifique-se de que o arquivo está completamente carregado")
        print("   4. O Power BI Desktop precisa estar com um modelo ativo")
    
    # 3. Testa portas específicas
    print("\n🔌 Testando portas comuns do Power BI...")
    common_ports = [49152, 50000, 51000, 52000, 53000, 54000, 55000]
    
    for port in common_ports:
        if connector._is_port_open('localhost', port):
            print(f"   ✅ Porta {port} está aberta!")
        else:
            print(f"   ❌ Porta {port} não está acessível")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO")
    print("=" * 60)

if __name__ == "__main__":
    test_powerbi_detection()
