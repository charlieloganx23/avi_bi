# Features v1.3.0 - Média Prioridade

Versão: **1.3.0**  
Data: **28 de dezembro de 2025**

## 🎯 Visão Geral

Esta versão implementa três funcionalidades importantes para gestão avançada de modelos Power BI:
- 🎨 **Aplicação de Temas via TMSL**
- 🔗 **Gestão de Relacionamentos**
- ⚡ **Análise de Performance de Medidas**

---

## 🎨 Aplicação de Temas via TMSL

### Funcionalidade
Aplica temas de cores diretamente no modelo Power BI Desktop através de comandos TMSL (Tabular Model Scripting Language).

### Como Usar

1. **Conecte ao Power BI Desktop**
   - Vá para "🔌 Conectar ao Power BI"
   - Selecione a instância ativa

2. **Acesse o Menu de Temas**
   - Selecione "🎨 Aplicar Tema" no menu lateral

3. **Escolha ou Crie um Tema**
   
   **Opção A - Temas Predefinidos:**
   - **Corporativo Azul**: Paleta profissional com tons de azul
   - **Moderno Escuro**: Design dark mode com cores vibrantes
   - **Natura Verde**: Tons naturais de verde
   
   **Opção B - Tema Personalizado:**
   - Defina 5 cores personalizadas usando o color picker
   - Configure cor de background
   - Nomeie seu tema

4. **Aplicar**
   - Clique em "🎨 Aplicar Tema"
   - Aguarde confirmação
   - Atualize os visuais no Power BI Desktop

### Estrutura do Tema

```json
{
  "name": "Nome do Tema",
  "dataColors": ["#cor1", "#cor2", "#cor3", "#cor4", "#cor5"],
  "background": "#FFFFFF",
  "foreground": "#000000",
  "tableAccent": "#cor1"
}
```

### Benefícios

✅ Aplica tema instantaneamente sem copiar/colar JSON  
✅ Padronização rápida de múltiplos relatórios  
✅ Preview visual antes de aplicar  
✅ Temas predefinidos profissionais  
✅ Criação de temas personalizados  

### Limitações

⚠️ Requer Power BI Desktop aberto  
⚠️ Modifica o modelo (faça backup)  
⚠️ Alguns visuais podem não suportar todas as cores  
⚠️ Necessário XMLA write access  

### Troubleshooting

**Erro: "XMLA write access"**
- Power BI Desktop não permite modificações via XMLA por padrão
- Solução: Use Power BI Service com Premium ou Premium Per User

**Tema não aparece nos visuais**
- Atualize manualmente os visuais no Power BI Desktop
- Vá em Visualizações > Formatar > Cores

---

## 🔗 Gestão de Relacionamentos

### Funcionalidade
Interface completa para visualizar, criar e analisar relacionamentos entre tabelas do modelo.

### Como Usar

1. **Conecte ao Power BI Desktop**

2. **Acesse Relacionamentos**
   - Selecione "🔗 Relacionamentos" no menu lateral

3. **Visualizar Relacionamentos Existentes**
   
   - **Aba: 📊 Relacionamentos Existentes**
   - Clique em "🔄 Atualizar Lista"
   - Veja todos os relacionamentos com detalhes:
     - Tabela e coluna de origem
     - Tabela e coluna de destino
     - Tipo de filtro cruzado
     - Status (ativo/inativo)

4. **Criar Novo Relacionamento**
   
   - **Aba: ➕ Criar Novo**
   - Selecione tabela e coluna de origem
   - Selecione tabela e coluna de destino
   - Configure:
     - **Cardinalidade**: ManyToOne, OneToMany, OneToOne, ManyToMany
     - **Direção do Filtro**: SingleDirection, BothDirections
   - Clique em "➕ Criar Relacionamento"

5. **Análise de Grafo**
   
   - **Aba: 📈 Análise de Grafo**
   - Veja estatísticas:
     - Total de relacionamentos
     - Relacionamentos ativos
     - Relacionamentos bidirecionais
     - Tabelas envolvidas

### Tipos de Cardinalidade

| Tipo | Descrição | Uso Típico |
|------|-----------|------------|
| **ManyToOne** | N:1 - Múltiplos registros para um | Fato → Dimensão |
| **OneToMany** | 1:N - Um registro para múltiplos | Dimensão → Fato |
| **OneToOne** | 1:1 - Único registro para único | Tabelas complementares |
| **ManyToMany** | N:N - Múltiplos para múltiplos | Requer tabela ponte |

### Tipos de Filtro Cruzado

| Tipo | Descrição | Impacto |
|------|-----------|---------|
| **SingleDirection** | Filtro em uma direção | Performance melhor |
| **BothDirections** | Filtro bidirecional | Pode causar ambiguidade |

### Benefícios

✅ Visualização clara de todos os relacionamentos  
✅ Criação rápida sem sair da ferramenta  
✅ Detecção de cardinalidade sugerida  
✅ Análise de conectividade do modelo  
✅ Identificação de relacionamentos problemáticos  

### Limitações

⚠️ Não exclui relacionamentos (apenas criação)  
⚠️ Visualização gráfica em desenvolvimento  
⚠️ Requer XMLA write access para criar  

### Melhores Práticas

1. **Use SingleDirection sempre que possível**
   - Melhor performance
   - Evita ambiguidade

2. **Evite ManyToMany direto**
   - Crie tabela ponte
   - Use SingleDirection em ambas as pontas

3. **Nomeie relacionamentos claramente**
   - Ex: `Vendas_Produto` em vez de `Relationship1`

4. **Valide após criar**
   - Teste filtros no Power BI Desktop
   - Verifique se DAX funciona corretamente

---

## ⚡ Análise de Performance de Medidas

### Funcionalidade
Avalia o tempo de execução de medidas DAX e identifica gargalos de performance.

### Como Usar

1. **Conecte ao Power BI Desktop**

2. **Acesse Análise de Performance**
   - Selecione "⚡ Performance" no menu lateral

3. **Analisar Medida Individual**
   
   - **Aba: 🔍 Análise Individual**
   - Selecione uma medida do dropdown
   - Configure número de execuções (1-10)
     - Mais execuções = resultado mais preciso
     - Menos execuções = análise mais rápida
   - Clique em "⚡ Analisar Performance"

4. **Interpretar Resultados**

   **Métricas Principais:**
   - **Tempo Médio**: Média de todas as execuções
   - **Tempo Mínimo**: Melhor tempo registrado
   - **Tempo Máximo**: Pior tempo registrado
   - **Performance Rating**: Classificação automática

   **Cold Start vs Warm:**
   - **Cold Start**: Primeira execução (sem cache)
   - **Warm Avg**: Média das execuções seguintes (com cache)
   - **Cache Improvement**: % de melhoria com cache

### Classificação de Performance

| Rating | Tempo Médio | Emoji | Ação Recomendada |
|--------|-------------|-------|------------------|
| **Excelente** | < 100ms | 🚀 | Nenhuma otimização necessária |
| **Boa** | 100-500ms | ✅ | Otimizar se usada intensivamente |
| **Aceitável** | 500-2000ms | ⚠️ | Considerar otimização |
| **Lenta** | > 2000ms | 🐌 | Otimização urgente requerida |

### Recomendações de Otimização

#### Para Medidas Lentas (> 2s)

1. **Evite FILTER quando possível**
   ```dax
   // ❌ Lento
   CALCULATE(SUM(Vendas[Valor]), FILTER(Produtos, Produtos[Categoria] = "A"))
   
   // ✅ Rápido
   CALCULATE(SUM(Vendas[Valor]), Produtos[Categoria] = "A")
   ```

2. **Use variáveis para cálculos repetidos**
   ```dax
   // ❌ Lento (calcula 3 vezes)
   Total Vendas = 
   IF(SUM(Vendas[Valor]) > 1000,
      SUM(Vendas[Valor]) * 1.1,
      SUM(Vendas[Valor]))
   
   // ✅ Rápido (calcula 1 vez)
   Total Vendas = 
   VAR _Valor = SUM(Vendas[Valor])
   RETURN IF(_Valor > 1000, _Valor * 1.1, _Valor)
   ```

3. **Evite iteradores quando possível**
   ```dax
   // ❌ Lento
   SUMX(Vendas, Vendas[Quantidade] * Vendas[Preco])
   
   // ✅ Rápido (se houver coluna calculada)
   SUM(Vendas[Total])
   ```

4. **Simplifique relacionamentos**
   - Use relacionamentos diretos em vez de USERELATIONSHIP múltiplo
   - Evite relacionamentos bidirecionais

5. **Crie agregações**
   - Para grandes volumes, crie tabelas agregadas
   - Use agregações automáticas do Power BI

### Benefícios

✅ Identifica medidas problemáticas rapidamente  
✅ Compara impacto de otimizações  
✅ Mostra diferença entre cold start e cache  
✅ Fornece recomendações específicas  
✅ Ajuda a definir SLAs de performance  

### Limitações

⚠️ Tempo pode variar por carga do sistema  
⚠️ Não analisa queries de visuais  
⚠️ Cache do Analysis Services pode afetar resultados  
⚠️ Comparação entre medidas em desenvolvimento  

### Melhores Práticas

1. **Execute múltiplas iterações (5+)**
   - Resultados mais confiáveis
   - Média elimina outliers

2. **Analise em diferentes horários**
   - Carga do sistema varia
   - Teste em horário de pico

3. **Compare antes e depois**
   - Salve resultados antes de otimizar
   - Documente melhorias

4. **Foque nas mais usadas**
   - Priorize medidas em visuais principais
   - Ignore medidas auxiliares rápidas

---

## 📊 Fluxo de Trabalho Recomendado

### 1. Configuração Inicial
```
Conectar → Aplicar Tema → Verificar Relacionamentos
```

### 2. Desenvolvimento
```
Criar Medidas → Validar DAX → Testar Performance
```

### 3. Otimização
```
Analisar Performance → Identificar Lentas → Otimizar → Re-analisar
```

### 4. Auditoria
```
Listar Relacionamentos → Validar Estrutura → Documentar
```

---

## 🔧 Requisitos Técnicos

### Software
- Power BI Desktop (qualquer versão)
- Python 3.12+
- pythonnet 3.0.0+
- Microsoft.AnalysisServices.AdomdClient (incluído no SQL Server)

### Permissões
- ✅ **Leitura**: Todas as funcionalidades de consulta funcionam
- ⚠️ **Escrita**: Aplicar tema e criar relacionamentos requerem XMLA write access

### XMLA Write Access

**Power BI Desktop**: Não suporta escrita via XMLA  
**Power BI Service**: Requer Premium ou Premium Per User

---

## 🐛 Troubleshooting

### "Não conectado ao Analysis Services"
- Verifique se Power BI Desktop está aberto
- Vá em "🔌 Conectar ao Power BI" e reconecte

### "Erro ao aplicar tema"
- Power BI Desktop não permite modificações via TMSL
- Use Power BI Service com workspace Premium

### "Erro ao criar relacionamento"
- Verifique se colunas existem
- Confirme tipos de dados compatíveis
- Evite criar relacionamento duplicado

### Performance Analysis retorna erro
- Medida pode ter erro de sintaxe
- Valide medida antes de analisar performance
- Use "✅ Validar DAX" primeiro

---

## 📈 Próximas Melhorias (v1.4)

### 🔗 Relacionamentos
- ❌ Excluir relacionamentos
- 🔄 Editar relacionamentos existentes
- 📊 Visualização gráfica (diagrama interativo)
- 🤖 Sugestão automática de relacionamentos

### ⚡ Performance
- 📊 Comparação de múltiplas medidas
- 🏆 Ranking automático de todas as medidas
- 📉 Gráficos de tendência de performance
- 💾 Histórico de análises

### 🎨 Temas
- 📥 Importar tema de arquivo JSON
- 💾 Salvar tema personalizado
- 🎨 Mais temas predefinidos
- 🔄 Aplicar tema em batch para múltiplos relatórios

---

## 📝 Notas da Versão

**v1.3.0** (28/12/2025)
- ➕ Aplicação de temas via TMSL
- ➕ Gestão de relacionamentos com UI completa
- ➕ Análise de performance de medidas
- ➕ Três temas predefinidos
- ➕ Editor de tema personalizado
- ➕ Estatísticas de cold start vs warm
- ➕ Recomendações de otimização automáticas

---

## 🆘 Suporte

Em caso de dúvidas ou problemas:
1. Consulte a seção de Troubleshooting
2. Verifique os logs no terminal
3. Teste em modelo de exemplo primeiro
4. Documente erro e contexto para suporte

---

**Desenvolvido com ❤️ para a comunidade Power BI**
