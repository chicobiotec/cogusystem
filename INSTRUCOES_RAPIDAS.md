# 🚀 Instruções Rápidas - Sistema de Cogumelos

## ⚡ Instalação e Execução

### 1. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 2. **Executar o Sistema**
```bash
python run.py
```

### 3. **Acessar**
Abra o navegador e acesse: **http://localhost:5000**

---

## 🆕 Funcionalidade: Múltiplas Imagens por Coleta

### ✨ **O que mudou:**
- **Antes**: Uma imagem por coleta
- **Agora**: **Múltiplas imagens** por coleta com descrições individuais

### 📸 **Como usar:**

#### **Cadastrando Nova Coleta:**
1. Vá em **"Coletas" → "Nova Coleta"**
2. Preencha os dados básicos
3. Na seção **"Imagens da Coleta"**:
   - Selecione **uma ou mais imagens** (Ctrl+click para múltiplas)
   - Adicione uma **descrição geral** para todas as imagens
4. Clique em **"Cadastrar Coleta"**

#### **Visualizando Imagens:**
1. Acesse os **detalhes de uma coleta**
2. Veja a **galeria de imagens** organizada
3. Clique em qualquer imagem para **visualização em modal**
4. Cada imagem mostra sua **descrição e data de upload**

#### **Na Lista de Coletas:**
- **Preview** da primeira imagem de cada coleta
- **Contador** de imagens por coleta
- **Badge** mostrando número de imagens
- **Botão de exclusão** rápido em cada card

#### **Editando Coletas:**
1. **Na lista**: Clique no botão ✏️ (editar) em qualquer coleta
2. **Nos detalhes**: Use o botão "Editar Coleta" na sidebar
3. **Formulário**: Todos os campos são editáveis e preenchidos com dados atuais
4. **Imagens**: Visualize as existentes e adicione novas

#### **Excluindo Coletas:**
1. **Na lista**: Clique no botão 🗑️ (lixeira) em qualquer coleta
2. **Nos detalhes**: Use o botão "Excluir Coleta" na sidebar
3. **Confirmação**: Modal mostra todos os dados que serão removidos
4. **Segurança**: Cascade delete remove imagens, isolados e experimentos relacionados

---

## 🔧 **Configurações Importantes**

### **Upload de Imagens:**
- **Formatos aceitos**: JPG, PNG, GIF
- **Tamanho máximo**: 16MB por arquivo
- **Nomes únicos**: Sistema adiciona timestamp automaticamente
- **Pasta**: `uploads/` (criada automaticamente)

### **Banco de Dados:**
- **Arquivo**: `cogumelos.db` (SQLite)
- **Criação**: Automática na primeira execução
- **Migrações**: Suporte a atualizações futuras

---

## 📊 **Dados de Exemplo (Opcional)**

### **Para testar o sistema:**
```bash
python exemplo_dados.py
```

### **O que será criado:**
- **5 coletas** com diferentes espécies
- **10 imagens** distribuídas entre as coletas
- **4 isolados** com dados técnicos
- **4 repiques** com histórico
- **3 experimentos** com metodologias

---

## 🎯 **Fluxo de Trabalho Recomendado**

### **1. Primeira Coleta:**
1. **Cadastre a coleta** com múltiplas imagens
2. **Adicione descrições** para cada imagem
3. **Verifique** se todas as imagens foram salvas

### **2. Isolado Micelial:**
1. **Crie um isolado** vinculado à coleta
2. **Configure** meio de cultura e temperatura
3. **Registre** observações do crescimento

### **3. Repiques:**
1. **Faça repiques** para manter o isolado ativo
2. **Controle** número de placas e datas
3. **Documente** mudanças no meio de cultura

### **4. Experimentos:**
1. **Registre experimentos** científicos
2. **Vincule** com coleta e/ou isolado
3. **Documente** metodologia e resultados

---

## 🔍 **Dicas de Uso**

### **Para Múltiplas Imagens:**
- **Tire fotos** de diferentes ângulos
- **Documente** características específicas
- **Use descrições** claras e objetivas
- **Organize** por data ou característica

### **Para Melhor Organização:**
- **Use códigos** consistentes para coletas
- **Mantenha** histórico de repiques
- **Documente** todas as observações
- **Vincule** experimentos às coletas

---

## 🐛 **Solução de Problemas**

### **Erro: "No module named 'flask'"**
```bash
pip install -r requirements.txt
```

### **Erro: "Database is locked"**
- Feche o sistema (Ctrl+C)
- Aguarde alguns segundos
- Execute novamente

### **Imagens não aparecem:**
- Verifique se a pasta `uploads/` existe
- Confirme permissões de escrita
- Verifique se os arquivos foram salvos

### **Sistema não inicia:**
- Verifique se a porta 5000 está livre
- Confirme se Python 3.8+ está instalado
- Verifique logs de erro no terminal

---

## 📱 **Acesso e Navegação**

### **URLs Principais:**
- **Dashboard**: `/` (página inicial)
- **Coletas**: `/coletas`
- **Nova Coleta**: `/coleta/nova`
- **Isolados**: `/isolados`
- **Experimentos**: `/experimentos`
- **Busca**: `/busca`

### **Navegação:**
- **Menu superior** para módulos principais
- **Breadcrumbs** para orientação
- **Links relacionados** para navegação cruzada
- **Botões de ação** para operações rápidas

---

## 🎉 **Pronto para Usar!**

O sistema está configurado com:
- ✅ **Múltiplas imagens** por coleta
- ✅ **Interface responsiva** e moderna
- ✅ **Banco de dados** integrado
- ✅ **Sistema de busca** avançado
- ✅ **Relacionamentos** entre entidades
- ✅ **Dados de exemplo** para teste
- ✅ **Exclusão segura** de coletas
- ✅ **Edição completa** de coletas

**🚀 Comece cadastrando sua primeira coleta com múltiplas imagens!**
