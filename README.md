# 🍄 Sistema de Bioprospecção de Cogumelos Nativos

Sistema web completo para administração de projetos de bioprospecção de cogumelos nativos em busca de pigmentos. Desenvolvido com Flask, SQLAlchemy e Bootstrap 5.

## ✨ Funcionalidades Principais

### 📸 Gestão de Coletas com Múltiplas Imagens
- **Cadastro completo** de coletas com informações detalhadas
- **Múltiplas imagens por coleta** com descrições individuais
- **Upload de imagens** em lote com preview em tempo real
- **Galeria de imagens** organizada e responsiva
- **Modal de visualização** para imagens em alta resolução
- **Filtros avançados** por substrato, coletor e busca textual
- **Paginação** para melhor performance
- **Exclusão segura** com confirmação e cascade delete
- **Edição completa** de coletas existentes

### 🧫 Banco de Culturas Miceliais (Isolados)
- **Registro de isolados** com dados técnicos completos
- **Controle de repiques** com datas e número de placas
- **Meios de cultura** personalizáveis
- **Temperatura de incubação** configurável
- **Observações detalhadas** para cada isolado

### 🔬 Repositório de Experimentos
- **Formulário completo** com todos os campos essenciais
- **Materiais e métodos** estruturados
- **Resultados e discussão** organizados
- **Status de acompanhamento** (Em andamento, Concluído, etc.)
- **Vinculação** com coletas e isolados

### 🔗 Integração entre Bancos de Dados
- **Relacionamentos cruzados** entre coletas, isolados e experimentos
- **Navegação intuitiva** entre entidades relacionadas
- **Estatísticas integradas** em tempo real
- **Busca unificada** em todos os dados

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.8+, Flask 2.3.3
- **Banco de Dados**: SQLite com Flask-SQLAlchemy 3.0.5
- **Migrações**: Flask-Migrate 4.0.5
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Processamento de Imagens**: Pillow 10.0.1
- **Upload de Arquivos**: Werkzeug 2.3.7

## 📁 Estrutura do Projeto

```
utfpr_cogumelos_bancodedados/
├── app.py                      # Aplicação principal Flask
├── config.py                   # Configurações do sistema
├── run.py                      # Script de execução
├── requirements.txt            # Dependências Python
├── exemplo_dados.py            # Script para dados de exemplo
├── INSTRUCOES_RAPIDAS.md      # Guia rápido de uso
├── README.md                   # Documentação completa
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Dashboard principal
│   ├── coletas.html           # Lista de coletas
│   ├── nova_coleta.html       # Formulário de nova coleta
│   ├── coleta_detalhe.html    # Detalhes da coleta
│   ├── isolados.html          # Lista de isolados
│   ├── novo_isolado.html      # Formulário de novo isolado
│   ├── isolado_detalhe.html   # Detalhes do isolado
│   ├── novo_repique.html      # Formulário de novo repique
│   ├── experimentos.html      # Lista de experimentos
│   ├── novo_experimento.html  # Formulário de novo experimento
│   ├── experimento_detalhe.html # Detalhes do experimento
│   └── busca.html             # Sistema de busca
├── uploads/                    # Pasta para imagens (criada automaticamente)
└── cogumelos.db               # Banco de dados SQLite (criado automaticamente)
```

## 🗄️ Modelos de Dados

### Coleta
- **Identificação**: código único, nome científico/popular
- **Localização**: local, coordenadas geográficas
- **Características**: substrato, coletor, data
- **Mídia**: múltiplas imagens com descrições
- **Relacionamentos**: isolados, experimentos

### ImagemColeta (Novo!)
- **Vinculação**: ID da coleta
- **Arquivo**: nome do arquivo de imagem
- **Descrição**: descrição individual da imagem
- **Metadados**: data de upload

### Isolado
- **Identificação**: código único, vinculação à coleta
- **Cultivo**: meio de cultura, temperatura, data
- **Relacionamentos**: repiques, experimentos

### Repique
- **Controle**: data, número de placas, meio
- **Observações**: detalhes do processo

### Experimento
- **Estrutura**: título, objetivo, materiais/métodos
- **Resultados**: dados, discussão, conclusões
- **Vinculação**: coleta e/ou isolado relacionados

## 🔍 Sistema de Busca e Filtros

### Busca Integrada
- **Busca textual** em coletas, isolados e experimentos
- **Resultados categorizados** por tipo de entidade
- **Filtros específicos** para cada entidade

### Filtros Avançados
- **Coletas**: substrato, coletor, busca textual
- **Isolados**: meio de cultura, data de isolamento
- **Experimentos**: status, período, vinculação

## 🎨 Interface do Usuário

### Design Responsivo
- **Bootstrap 5** para layout moderno e responsivo
- **Componentes interativos** com JavaScript
- **Ícones FontAwesome** para melhor usabilidade
- **Temas consistentes** em todas as páginas

### Funcionalidades de Imagem
- **Upload múltiplo** com drag & drop
- **Preview em tempo real** das imagens selecionadas
- **Galeria organizada** com cards responsivos
- **Modal de visualização** para imagens grandes
- **Contador de imagens** por coleta

### Navegação Intuitiva
- **Breadcrumbs** para orientação do usuário
- **Menu de navegação** organizado por funcionalidade
- **Ações rápidas** em cada página de detalhes
- **Links contextuais** entre entidades relacionadas

## ⚙️ Configuração e Instalação

### Requisitos do Sistema
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno

### Instalação Rápida
```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd utfpr_cogumelos_bancodedados

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o sistema
python run.py
```

### Configurações Avançadas
- **Arquivo config.py**: configurações de ambiente
- **Variáveis de ambiente**: chaves secretas e configurações sensíveis
- **Banco de dados**: configuração de conexão e migrações

## 🚀 Execução do Sistema

### Modo Desenvolvimento
```bash
python run.py
```
- **URL de acesso**: http://localhost:5000
- **Modo debug**: ativado para desenvolvimento
- **Recarregamento automático**: em caso de alterações

### Modo Produção
```bash
# Configure variáveis de ambiente
export FLASK_ENV=production
export SECRET_KEY=sua_chave_secreta_aqui

# Execute com gunicorn (recomendado)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 Dados de Exemplo

### Populando o Banco
```bash
python exemplo_dados.py
```

### Conteúdo dos Dados
- **5 coletas** com diferentes espécies de cogumelos
- **10 imagens** distribuídas entre as coletas
- **4 isolados** com dados técnicos completos
- **4 repiques** com histórico de manutenção
- **3 experimentos** com metodologias detalhadas

## 🔧 Funcionalidades Avançadas

### Sistema de Migrações
- **Flask-Migrate** para controle de versão do banco
- **Comandos de migração** para atualizações
- **Rollback** para versões anteriores

### API JSON
- **Endpoints REST** para integração externa
- **Dados em formato JSON** para aplicações móveis
- **Documentação da API** incluída

### Upload de Imagens
- **Validação de arquivos** (tipo, tamanho)
- **Processamento seguro** com nomes únicos
- **Organização automática** por data/hora
- **Suporte a múltiplos formatos** (JPG, PNG, GIF)

## 🐛 Solução de Problemas

### Problemas Comuns
1. **Erro de dependências**: Execute `pip install -r requirements.txt`
2. **Erro de banco**: Delete `cogumelos.db` e reinicie
3. **Erro de uploads**: Verifique permissões da pasta `uploads/`

### Logs e Debug
- **Modo debug** ativado por padrão
- **Logs detalhados** no console
- **Tratamento de erros** com mensagens amigáveis

## 📈 Próximas Funcionalidades

### Planejadas
- **Sistema de usuários** com autenticação
- **Relatórios e exportação** de dados
- **Dashboard analítico** com gráficos
- **API completa** para integração externa
- **Sistema de notificações** para experimentos

### Melhorias Técnicas
- **Cache Redis** para melhor performance
- **Testes automatizados** com pytest
- **CI/CD** com GitHub Actions
- **Containerização** com Docker

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o repositório
2. **Crie uma branch** para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra um Pull Request**

### Padrões de Código
- **PEP 8** para estilo Python
- **Docstrings** para documentação
- **Type hints** para melhor legibilidade
- **Testes** para novas funcionalidades

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Equipe de Desenvolvimento** - UTFPR
- **Orientadores** - Professores do curso
- **Alunos** - Participantes do projeto

## 📞 Suporte

Para dúvidas, sugestões ou problemas:
- **Issues**: Abra uma issue no GitHub
- **Email**: contato@utfpr.edu.br
- **Documentação**: Consulte este README

---

**🍄 Sistema desenvolvido para o projeto de Bioprospecção de Cogumelos Nativos da UTFPR**
