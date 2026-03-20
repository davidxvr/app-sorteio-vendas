import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import pytz
import base64
import os

# Configuração da Página
st.set_page_config(
    page_title="Sorteio JR Ferragens e Madeiras",
    page_icon="🏆",
    layout="wide"
)

# --- Cores da Marca JR ---
COR_VERMELHO   = "#C41230"
COR_VERMELHO_CLARO = "#E63946"
COR_AZUL       = "#1A2B6B"
COR_AZUL_CLARO = "#2D5A8C"
COR_BRANCO     = "#FFFFFF"
COR_CINZA_BG   = "#F8F9FA"
COR_CINZA_BORDA = "#E0E0E0"
COR_DESTAQUE   = "#FF6B35"

# --- Carregar Logo como Base64 ---
def carregar_logo_base64(caminho: str) -> str:
    """Lê um arquivo de imagem e retorna string base64."""
    try:
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

# Tenta carregar logos (coloque os arquivos PNG na mesma pasta do script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logo_lateral_b64  = carregar_logo_base64(os.path.join(BASE_DIR, "JR NOVA Logo-04 - lateral.png"))  # Horizontal branco
logo_vertical_b64 = carregar_logo_base64(os.path.join(BASE_DIR, "JR NOVA Logo-03.png"))             # Vertical
logo_principal_b64 = carregar_logo_base64(os.path.join(BASE_DIR, "JR NOVA Logo-02.png"))            # Principal (páginas)
logo_icone_b64    = carregar_logo_base64(os.path.join(BASE_DIR, "JR NOVA Logo-05.png"))             # Ícone

def img_tag(b64: str, width: str = "100%") -> str:
    if b64:
        return f'<img src="data:image/png;base64,{b64}" style="width:{width}; display:block; margin:auto;">'
    return ""

# --- CSS Customizado com Paleta JR ---
st.markdown(f"""
<style>
    /* ── Importar fonte ── */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Montserrat', sans-serif;
    }}

    /* ── Fundo geral ── */
    .stApp {{
        background-color: {COR_CINZA_BG};
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COR_AZUL} 0%, {COR_AZUL_CLARO} 100%) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {COR_BRANCO} !important;
    }}
    [data-testid="stSidebar"] .stRadio label {{
        color: {COR_BRANCO} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] .stRadio {{
        color: {COR_BRANCO} !important;
    }}
    [data-testid="stSidebar"] .stRadio span {{
        color: {COR_BRANCO} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] {{
        color: {COR_BRANCO} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] * {{
        color: {COR_BRANCO} !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.2) !important;
    }}
    [data-testid="stSidebar"] .stInfo {{
        background-color: rgba({220,18,48},0.15) !important;
        color: {COR_BRANCO} !important;
        border: 1px solid {COR_VERMELHO} !important;
    }}

    /* ── Títulos de página ── */
    h1 {{
        color: {COR_AZUL} !important;
        font-weight: 800 !important;
        border-bottom: 4px solid {COR_VERMELHO};
        padding-bottom: 12px;
        margin-bottom: 24px;
    }}
    h2, h3 {{
        color: {COR_AZUL} !important;
        font-weight: 700 !important;
        border-left: 4px solid {COR_VERMELHO};
        padding-left: 12px;
    }}

    /* ── Botão primário → Vermelho JR ── */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {COR_VERMELHO} 0%, {COR_VERMELHO_CLARO} 100%) !important;
        color: {COR_BRANCO} !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 1px;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(196,18,48,0.3);
    }}
    .stButton > button[kind="primary"]:hover {{
        filter: brightness(1.15) !important;
        box-shadow: 0 6px 18px rgba(196,18,48,0.5);
    }}

    /* ── Botão secundário → Azul JR ── */
    .stButton > button[kind="secondary"] {{
        background-color: transparent !important;
        color: {COR_AZUL} !important;
        border: 2px solid {COR_AZUL} !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, {COR_AZUL} 0%, {COR_AZUL_CLARO} 100%) !important;
        color: {COR_BRANCO} !important;
    }}

    /* ── Métricas (cards de KPI) ── */
    [data-testid="stMetric"] {{
        background: linear-gradient(135deg, {COR_BRANCO} 0%, rgba({26,43,107},0.03) 100%);
        border: 1px solid {COR_CINZA_BORDA};
        border-top: 5px solid {COR_VERMELHO};
        border-radius: 12px;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    [data-testid="stMetricLabel"] {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {COR_VERMELHO} !important;
        font-weight: 800 !important;
    }}

    /* ── Tabs / Upload / Select ── */
    .stSelectbox label, .stRadio legend, .stCheckbox label,
    .stFileUploader label, .stTextInput label {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}

    /* ── Radio Button ── */
    [data-testid="stRadio"] {{
        color: {COR_AZUL} !important;
    }}
    [data-testid="stRadio"] label {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stRadio"] span {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stRadio"] * {{
        color: {COR_AZUL} !important;
    }}
    .stRadio > div {{
        color: {COR_AZUL} !important;
    }}
    .stRadio > div > label {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}
    .stRadio {{
        color: {COR_AZUL} !important;
    }}
    .stRadio label {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}
    .stRadio span {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}
    .stRadio p {{
        color: {COR_AZUL} !important;
        font-weight: 600 !important;
    }}
    /* ── Force Text Color in Radio ── */
    [role="radiogroup"] {{
        color: {COR_AZUL} !important;
    }}
    [role="radio"] {{
        color: {COR_AZUL} !important;
    }}
    [role="radio"] * {{
        color: {COR_AZUL} !important;
    }}

    /* ── Input e Textbox ── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {{
        background-color: {COR_BRANCO} !important;
        color: {COR_AZUL} !important;
        border: 1px solid {COR_CINZA_BORDA} !important;
    }}

    /* ── File Uploader ── */
    [data-testid="stFileUploadDropzone"] {{
        background-color: {COR_BRANCO} !important;
        border: 2px dashed {COR_VERMELHO} !important;
    }}
    .stFileUploader > div {{
        background-color: {COR_BRANCO} !important;
    }}

    /* ── Dataframe / tabela ── */
    [data-testid="stDataFrame"] {{
        background-color: {COR_BRANCO} !important;
    }}
    [data-testid="stDataFrame"] th {{
        background: linear-gradient(90deg, {COR_AZUL} 0%, {COR_AZUL_CLARO} 100%) !important;
        color: {COR_BRANCO} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stDataFrame"] tr {{
        background-color: {COR_BRANCO} !important;
    }}
    [data-testid="stDataFrame"] tr:hover {{
        background-color: rgba({26,43,107},0.05) !important;
    }}
    [data-testid="stDataFrame"] td {{
        color: {COR_AZUL} !important;
        font-weight: 500 !important;
    }}

    /* ── Texto em tabelas/elementos ── */
    .stDataFrame {{
        color: {COR_AZUL} !important;
    }}
    .stDataFrame * {{
        color: {COR_AZUL} !important;
    }}
    table td {{
        color: {COR_AZUL} !important;
    }}

    /* ── Barra superior (header) ── */
    header[data-testid="stHeader"] {{
        background-color: {COR_BRANCO};
        border-bottom: 4px solid {COR_VERMELHO};
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}

    /* ── Divisor ── */
    hr {{
        border-color: {COR_CINZA_BORDA} !important;
    }}

    /* ── Info Box ── */
    .stInfo {{
        background-color: rgba({26,43,107},0.08) !important;
        border-left: 4px solid {COR_VERMELHO} !important;
    }}
</style>
""", unsafe_allow_html=True)


# --- Funções Auxiliares ---

def carregar_dados_exemplo():
    """Gera dados de exemplo com NOME e CIDADE, incluindo repetições (chances)."""
    dados = [
        {"NOME": "2000 COM DE MAT PARA CONST LTD", "CIDADE": "FORMIGA"},
        {"NOME": "2000 COM DE MAT PARA CONST LTD", "CIDADE": "FORMIGA"},
        {"NOME": "2N PLANEJADOS LTDA",              "CIDADE": "OURO PRETO"},
        {"NOME": "2N PLANEJADOS LTDA",              "CIDADE": "OURO PRETO"},
        {"NOME": "2N PLANEJADOS LTDA",              "CIDADE": "OURO PRETO"},
        {"NOME": "ABEL GOMES DA SILVA",             "CIDADE": "VIÇOSA"},
        {"NOME": "ABEL GOMES DA SILVA",             "CIDADE": "VIÇOSA"},
        {"NOME": "JOAO DA SILVA",                   "CIDADE": "BELO HORIZONTE"},
        {"NOME": "JOAO DA SILVA",                   "CIDADE": "BELO HORIZONTE"},
        {"NOME": "JOAO DA SILVA",                   "CIDADE": "BELO HORIZONTE"},
        {"NOME": "MARIA OLIVEIRA",                  "CIDADE": "CONTAGEM"},
    ]
    return pd.DataFrame(dados)


def processar_upload(df):
    """Padroniza o DataFrame para ter colunas NOME e CIDADE."""
    if df is not None:
        df.columns = [c.upper().strip() for c in df.columns]
        col_nome = col_cidade = None

        for col in df.columns:
            if col in ['NOME', 'PARTICIPANTE', 'CLIENTE', 'NAME']:
                col_nome = col
            elif col in ['CIDADE', 'CITY', 'LOCAL']:
                col_cidade = col

        if not col_nome and len(df.columns) >= 1:
            col_nome = df.columns[0]
        if not col_cidade and len(df.columns) >= 2:
            col_cidade = df.columns[1]

        if col_nome:
            novo_df = pd.DataFrame()
            novo_df['NOME'] = df[col_nome].astype(str).str.strip().str.upper()
            novo_df['CIDADE'] = df[col_cidade].astype(str).str.strip().str.upper() if col_cidade else "NÃO INFORMADA"
            return novo_df

    return None


def calcular_probabilidades(df):
    """Agrupa por Nome/Cidade e calcula chances."""
    if df is None or df.empty:
        return pd.DataFrame()

    total_entradas = len(df)
    df_agrupado = df.groupby(['NOME', 'CIDADE']).size().reset_index(name='Total de Entradas')
    df_agrupado['Probabilidade (%)'] = (df_agrupado['Total de Entradas'] / total_entradas * 100).map('{:.2f}%'.format)
    return df_agrupado.sort_values(by='Total de Entradas', ascending=False)


# --- Inicialização do Session State ---
if 'df_tickets' not in st.session_state:
    st.session_state.df_tickets = carregar_dados_exemplo()

if 'lista_premios' not in st.session_state:
    st.session_state.lista_premios = ["Vale Compras R$ 500", "Kit Ferramentas", "Smart TV 50"]

if 'historico_sorteios' not in st.session_state:
    st.session_state.historico_sorteios = []


# ════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════
with st.sidebar:
    # Logo na sidebar (versão lateral branca, ou vertical)
    if logo_lateral_b64:
        st.markdown(img_tag(logo_lateral_b64, "95%"), unsafe_allow_html=True)
    else:
        st.markdown(
            f'<p style="font-size:24px; font-weight:800; color:white; text-align:center;">JR<br>'
            f'<span style="font-size:14px; font-weight:500;">Ferragens e Madeiras</span></p>',
            unsafe_allow_html=True
        )

    st.markdown(f'<hr style="border-top: 2px solid rgba(255,255,255,0.3);">', unsafe_allow_html=True)
    
    st.markdown('<p style="font-weight:700; font-size:16px; margin:16px 0 8px 0; color:white; letter-spacing:0.5px;">📍 NAVEGAÇÃO</p>',
                unsafe_allow_html=True)
    pagina = st.radio("Ir para:", ["Cadastro e Dados", "Sorteio"], label_visibility="collapsed")
    
    st.markdown(f'<hr style="border-top: 2px solid rgba(255,255,255,0.3); margin:16px 0;">', unsafe_allow_html=True)
    
    st.info(f"ℹ️ **Sistema de Sorteio Profissional**\n\nJR Ferragens e Madeiras — Sorteios com Integridade")
    
    st.markdown(f'<hr style="border-top: 2px solid rgba(255,255,255,0.3);">', unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align:center; font-size:12px; color:rgba(255,255,255,0.7); margin-top:20px;">'
        f'<b>Versão 2.0</b></p>',
        unsafe_allow_html=True
    )


# ════════════════════════════════════════
#  PÁGINA 1 — CADASTRO E DADOS
# ════════════════════════════════════════
if pagina == "Cadastro e Dados":

    # Cabeçalho com logo e título
    st.markdown(f'''
    <div style="
        background-color: {COR_BRANCO};
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        border-left: 5px solid {COR_VERMELHO};
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    ">
        <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
            {img_tag(logo_principal_b64, "150px") if logo_principal_b64 else '<h1 style="color:{COR_AZUL}; margin:0;">📂</h1>'}
            <div>
                <h1 style="color:{COR_AZUL}; margin:0; font-size:32px; border:none; padding-bottom:0;">📂 Cadastro e Dados</h1>
                <p style="color:#666; margin:8px 0 0 0; font-size:14px;">Gerencie participantes e prêmios para seus sorteios</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("1. Upload de Participantes")
        st.write("Formato esperado: CSV com colunas **NOME** e **CIDADE**.")
        uploaded_file = st.file_uploader("Carregar arquivo CSV", type=['csv'])

        separador = st.radio(
            "Qual o separador do arquivo?",
            ["Ponto e Vírgula (;)", "Vírgula (,)"],
            index=0,
            horizontal=True
        )
        sep_char = ";" if "Ponto" in separador else ","

        if uploaded_file:
            try:
                df_raw  = pd.read_csv(uploaded_file, sep=sep_char)
                df_proc = processar_upload(df_raw)

                if df_proc is not None and not df_proc.empty:
                    st.session_state.df_tickets = df_proc
                    st.success(f"✅ Arquivo carregado! {len(df_proc)} entradas processadas.")
                else:
                    st.error("⚠️ Não encontramos as colunas NOME e CIDADE.")
                    st.warning(
                        f"Dica: Tente mudar o separador para "
                        f"'{'Vírgula' if sep_char == ';' else 'Ponto e Vírgula'}'. "
                        f"Verifique também o cabeçalho do CSV."
                    )
                    st.write("Colunas lidas:", list(df_raw.columns))
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")

        st.markdown("---")
        st.subheader("2. Cadastro de Prêmios")
        novo_premio = st.text_input("Nome do Prêmio")
        if st.button("Adicionar Prêmio"):
            if novo_premio:
                st.session_state.lista_premios.append(novo_premio)
                st.success(f"Prêmio '{novo_premio}' adicionado!")
                st.rerun()

        if st.session_state.lista_premios:
            st.markdown(f'<h3 style="color:{COR_AZUL}; border-left:4px solid {COR_VERMELHO}; padding-left:12px;">📋 Lista de Prêmios</h3>', unsafe_allow_html=True)
            for p in st.session_state.lista_premios:
                st.markdown(f'<p style="color:{COR_AZUL}; font-size:16px; margin:8px 0;">• {p}</p>', unsafe_allow_html=True)

            st.markdown("---")
            st.write("🗑️ **Excluir Prêmio**")
            premio_para_remover = st.selectbox("Selecione um prêmio para remover", st.session_state.lista_premios)
            if st.button("Excluir Prêmio", type="secondary"):
                st.session_state.lista_premios.remove(premio_para_remover)
                st.warning(f"Prêmio '{premio_para_remover}' removido!")
                st.rerun()

    with col2:
        st.subheader("📊 Visão Geral dos Dados")

        if not st.session_state.df_tickets.empty:
            df_display    = calcular_probabilidades(st.session_state.df_tickets)
            total_tickets = len(st.session_state.df_tickets)
            total_pessoas = len(df_display)

            k1, k2 = st.columns(2)
            k1.metric("Total de Entradas (Chances)", total_tickets)
            k2.metric("Pessoas Únicas", total_pessoas)

            st.markdown(f'<h3 style="color:{COR_AZUL}; border-left:4px solid {COR_VERMELHO}; padding-left:12px;">📊 Tabela de Probabilidades</h3>', unsafe_allow_html=True)
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum dado carregado.")


# ════════════════════════════════════════
#  PÁGINA 2 — SORTEIO
# ════════════════════════════════════════
elif pagina == "Sorteio":

    # Cabeçalho com logo e título
    st.markdown(f'''
    <div style="
        background-color: {COR_BRANCO};
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        border-left: 5px solid {COR_VERMELHO};
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    ">
        <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
            {img_tag(logo_principal_b64, "150px") if logo_principal_b64 else '<h1 style="color:{COR_AZUL}; margin:0;">🎯</h1>'}
            <div>
                <h1 style="color:{COR_AZUL}; margin:0; font-size:32px; border:none; padding-bottom:0;">🎯 Realizar Sorteio</h1>
                <p style="color:#666; margin:8px 0 0 0; font-size:14px;">Sorteie seu ganhador com segurança e transparência</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if st.session_state.df_tickets.empty:
        st.warning("⚠️ Não há participantes cadastrados. Vá para a página de Cadastro.")
    else:
        c1, c2 = st.columns([1, 2])

        with c1:
            st.selectbox(
                "Escolha o Prêmio:",
                st.session_state.lista_premios,
                key="premio_selecionado"
            )

            remover_ganhador = st.checkbox(
                "Remover ganhador dos próximos sorteios?",
                value=True,
                help="Se marcado, remove todas as entradas da pessoa sorteada."
            )

            st.markdown("<br>", unsafe_allow_html=True)
            botao_sortear = st.button("🎰 SORTEAR", type="primary", use_container_width=True)

        with c2:
            st.write("### Resultado")

            if botao_sortear:
                df_atual          = st.session_state.df_tickets
                lista_nomes_unicos = df_atual['NOME'].unique().tolist()

                indice_sorteado   = random.choice(df_atual.index)
                ganhador_dados    = df_atual.loc[indice_sorteado]
                nome_ganhador     = ganhador_dados['NOME']
                cidade_ganhador   = ganhador_dados['CIDADE']
                premio            = st.session_state.premio_selecionado

                fuso_brasil  = pytz.timezone('America/Sao_Paulo')
                hora_sorteio = datetime.now(fuso_brasil).strftime('%d/%m/%Y %H:%M:%S')

                # ── Animação de suspense ──
                placeholder  = st.empty()
                tempo_espera = 0.03
                loops        = 70

                nomes_animacao = lista_nomes_unicos if len(lista_nomes_unicos) > 5 else lista_nomes_unicos * 10
                cores_animacao = [COR_VERMELHO, COR_AZUL, "#8B0000", "#0D1B55", "#333333"]

                for i in range(loops):
                    nome_flash = random.choice(nomes_animacao)
                    cor_flash  = random.choice(cores_animacao)

                    placeholder.markdown(
                        f"""
                        <div style="
                            text-align:center; padding:20px;
                            border:2px dashed {COR_CINZA_BORDA};
                            border-radius:10px;
                            background-color:{COR_BRANCO};
                        ">
                            <h3 style="color:{COR_AZUL}; margin:0; font-family:Montserrat,sans-serif;">
                                Sorteando...
                            </h3>
                            <h1 style="
                                color:{cor_flash}; font-size:36px;
                                margin:10px 0; font-family:Montserrat,sans-serif;
                                font-weight:800;
                            ">{nome_flash}</h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    time.sleep(tempo_espera)

                    if i > loops - 20:
                        tempo_espera += 0.01
                    if i > loops - 10:
                        tempo_espera += 0.03
                    if i > loops - 5:
                        tempo_espera += 0.05

                placeholder.empty()

                # ── Logo no card de resultado (ícone pequeno) ──
                logo_card = f'<img src="data:image/png;base64,{logo_icone_b64}" style="width:85px; margin-bottom:15px; filter:drop-shadow(0 2px 4px rgba(255,255,255,0.3));">' if logo_icone_b64 else "🏆"

                st.balloons()
                st.markdown(
                    f"""
                    <div style="
                        text-align:center; padding:40px 30px;
                        border-radius:16px;
                        background: linear-gradient(135deg, {COR_AZUL} 0%, {COR_AZUL_CLARO} 100%);
                        border: 3px solid {COR_VERMELHO};
                        box-shadow: 0 8px 32px rgba(196,18,48,0.35);
                        font-family: Montserrat, sans-serif;
                    ">
                        {logo_card}
                        <p style="
                            color:rgba(255,255,255,0.8);
                            text-transform:uppercase;
                            letter-spacing:4px;
                            font-size:13px;
                            margin:0 0 8px 0;
                            font-weight:700;
                        ">🏆 GANHADOR CONFIRMADO 🏆</p>
                        <div style="
                            color:#FFFFFF !important;
                            font-size:48px; font-weight:800;
                            margin:16px 0; line-height:1.1;
                            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        ">{nome_ganhador}</div>
                        <div style="color:rgba(255,255,255,0.95); margin-bottom:8px; font-size:18px;">
                            📍 {cidade_ganhador}</div>
                        <div style="
                            margin-top:24px; padding-top:24px;
                            border-top:2px solid rgba(255,255,255,0.2);
                        ">
                            <p style="font-size:18px; color:{COR_BRANCO}; margin:12px 0; font-weight:600;">
                                <span style="color:{COR_DESTAQUE}; font-size:20px;">🎁</span> <b>Prêmio:</b> {premio}
                            </p>
                            <p style="font-size:13px; color:rgba(255,255,255,0.75); margin:8px 0;">
                                🕐 Sorteado em: {hora_sorteio}
                            </p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ── Histórico ──
                registro = {
                    "Data/Hora": hora_sorteio,
                    "Prêmio":    premio,
                    "Ganhador":  nome_ganhador,
                    "Cidade":    cidade_ganhador,
                }
                st.session_state.historico_sorteios.append(registro)

                if remover_ganhador:
                    st.session_state.df_tickets = df_atual[df_atual['NOME'] != nome_ganhador]
                    st.info(f"ℹ️ Todas as entradas de {nome_ganhador} foram removidas dos próximos sorteios.")

    st.markdown("---")
    st.subheader("📜 Últimos Ganhadores")
    if st.session_state.historico_sorteios:
        df_hist = pd.DataFrame(st.session_state.historico_sorteios)
        df_hist.index = df_hist.index + 1
        st.table(df_hist)

# ════════════════════════════════════════
#  RODAPÉ COM LOGO
# ════════════════════════════════════════
st.markdown(f'''
<div style="
    text-align:center;
    padding:30px;
    margin-top:40px;
    border-top: 3px solid {COR_VERMELHO};
    background-color:rgba({26,43,107},0.05);
">
    <div style="margin-bottom:16px;">
        {img_tag(logo_vertical_b64, "80px") if logo_vertical_b64 else '<p style="font-size:20px;">JR Ferragens e Madeiras</p>'}
    </div>
    <p style="color:{COR_AZUL}; font-weight:700; margin:12px 0; font-size:16px;">JR Ferragens e Madeiras</p>
    <p style="color:#666; font-size:13px; margin:4px 0;">🏪 Qualidade, Confiança e Integridade em Sorteios</p>
    <p style="color:#999; font-size:11px; margin-top:16px;">© 2026 JR Ferragens e Madeiras. Todos os direitos reservados.</p>
</div>
''', unsafe_allow_html=True)
