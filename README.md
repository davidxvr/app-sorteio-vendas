# 🏆 Sistema de Sorteio JR Ferragens e Madeiras

Aplicação web profissional para gerenciar e realizar sorteios com transparência e integridade. Desenvolvida com **Streamlit** para facilitar o cadastro de participantes, prêmios e execução de sorteios.

## ✨ Características

- 📂 **Cadastro de Participantes**: Upload de CSV com participantes e cidades
- 🎁 **Gerenciamento de Prêmios**: Adicione, visualize e remova prêmios
- 📊 **Análise de Probabilidades**: Visualize chances de cada participante
- 🎯 **Sorteios ao Vivo**: Animação de suspense com seleção aleatória
- 📜 **Histórico**: Registro completo de todos os sorteios realizados
- 🎨 **Design Profissional**: Paleta de cores da marca JR com logos integradas
- 📱 **Interface Responsiva**: Funciona em desktop e móvel

## 🚀 Como Usar

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Preparar Arquivos de Logo

Coloque os seguintes arquivos PNG na mesma pasta do script (z:\JR FERRAGENS\a\):
- `JR NOVA Logo-03.png` (Logo vertical)
- `JR NOVA Logo-04 - lateral.png` (Logo horizontal/lateral)
- `JR NOVA Logo-05.png` (Logo ícone)

### 3. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
z:\JR FERRAGENS\a\
├── app.py                          # Arquivo principal da aplicação
├── requirements.txt                # Dependências do projeto
├── .gitignore                      # Configuração Git
├── README.md                       # Este arquivo
├── JR NOVA Logo-03.png             # Logo vertical
├── JR NOVA Logo-04 - lateral.png   # Logo horizontal
└── JR NOVA Logo-05.png             # Logo ícone
```

## 📊 Formato do CSV de Entrada

O arquivo CSV deve conter duas colunas principais:

```csv
NOME,CIDADE
2000 COM DE MAT PARA CONST LTD,FORMIGA
2N PLANEJADOS LTDA,OURO PRETO
ABEL GOMES DA SILVA,VIÇOSA
```

**Separadores Aceitos:**
- `;` (Ponto e Vírgula) - Padrão
- `,` (Vírgula)

## 🎨 Paleta de Cores

A aplicação utiliza a paleta oficial da marca JR:

| Cor | Código | Uso |
|-----|--------|-----|
| Vermelho JR | `#C41230` | Destaque principal |
| Azul JR | `#1A2B6B` | Secundário |
| Branco | `#FFFFFF` | Fundo componentes |
| Cinza | `#F8F9FA` | Fundo geral |

## 🛠️ Funcionalidades Principais

### 📂 Página: Cadastro e Dados

- Upload de arquivo CSV com participantes
- Seleção automática de separador (`;` ou `,`)
- Validação de colunas NOME e CIDADE
- Cadastro manual de prêmios
- Visualização de probabilidades por participante
- Métricas: Total de entradas e pessoas únicas

### 🎯 Página: Realizar Sorteio

- Seleção do prêmio para sorteio
- Opção de remover ganhador dos próximos sorteios
- Animação de suspense ao sortear
- Exibição em card destacado do ganhador
- Histórico completo de sorteios realizados

## 💾 Session State

A aplicação mantém em memória:
- `df_tickets`: DataFrame com todos os participantes
- `lista_premios`: Lista de prêmios disponíveis
- `historico_sorteios`: Histórico de ganhadores

## ⚙️ Requisitos

- **Python**: 3.8+
- **Streamlit**: 1.28.1+
- **Pandas**: 2.0.0+
- **Pytz**: 2023.3+

## 🚀 Deploy

### Streamlit Cloud

1. Faça push do repositório para GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em "Create app"
4. Selecione seu repositório
5. Configure o arquivo principal (`app.py`)

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

## 📝 Notas Importantes

- **Logos**: A aplicação busca os arquivos PNG automaticamente. Se não encontrar, exibe um fallback com emojis.
- **Fusos Horários**: O horário dos sorteios usa fuso de São Paulo (America/Sao_Paulo)
- **Segurança**: Não compartilhe dados sensíveis via upload direto; use em ambiente seguro

## 👨‍💻 Desenvolvimento

### Estrutura do Código

1. **Configuração Inicial**: Paleta de cores e carregamento de logos
2. **Funções Auxiliares**: Processamento de dados e cálculos
3. **Session State**: Inicialização de variáveis persistentes
4. **UI Principal**: Sidebar e páginas (Cadastro/Sorteio)

### Melhorias Futuras

- [ ] Backup automático em banco de dados
- [ ] Relatórios em PDF
- [ ] Autenticação de usuários
- [ ] Sorteios agendados
- [ ] Integração com WhatsApp/Email

## 📄 Licença

Todos os direitos reservados © 2026 JR Ferragens e Madeiras

## 📞 Suporte

Para dúvidas ou sugestões, entre em contato com a equipe JR Ferragens.

---

**Desenvolvido com ❤️ para JR Ferragens e Madeiras**
