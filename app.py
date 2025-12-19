import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import pytz

# Configuração da Página
st.set_page_config(
    page_title="Sorteio Profissional",
    page_icon="🎰",
    layout="wide"
)

# --- Funções Auxiliares ---

def carregar_dados_exemplo():
    """Gera dados de exemplo com NOME e CIDADE, incluindo repetições (chances)."""
    dados = [
        {"NOME": "2000 COM DE MAT PARA CONST LTD", "CIDADE": "FORMIGA"},
        {"NOME": "2000 COM DE MAT PARA CONST LTD", "CIDADE": "FORMIGA"},
        {"NOME": "2N PLANEJADOS LTDA", "CIDADE": "OURO PRETO"},
        {"NOME": "2N PLANEJADOS LTDA", "CIDADE": "OURO PRETO"},
        {"NOME": "2N PLANEJADOS LTDA", "CIDADE": "OURO PRETO"},
        {"NOME": "ABEL GOMES DA SILVA", "CIDADE": "VIÇOSA"},
        {"NOME": "ABEL GOMES DA SILVA", "CIDADE": "VIÇOSA"},
        {"NOME": "JOAO DA SILVA", "CIDADE": "BELO HORIZONTE"},
        {"NOME": "JOAO DA SILVA", "CIDADE": "BELO HORIZONTE"},
        {"NOME": "JOAO DA SILVA", "CIDADE": "BELO HORIZONTE"},
        {"NOME": "MARIA OLIVEIRA", "CIDADE": "CONTAGEM"}
    ]
    return pd.DataFrame(dados)

def processar_upload(df):
    """
    Padroniza o DataFrame para ter colunas NOME e CIDADE.
    Remove colunas extras e padroniza texto.
    """
    if df is not None:
        # Padronizar nomes das colunas para maiúsculo e remover espaços
        df.columns = [c.upper().strip() for c in df.columns]
        
        # Tentar identificar colunas alvo
        col_nome = None
        col_cidade = None
        
        # Busca colunas compatíveis
        for col in df.columns:
            if col in ['NOME', 'PARTICIPANTE', 'CLIENTE', 'NAME']:
                col_nome = col
            elif col in ['CIDADE', 'CITY', 'LOCAL']:
                col_cidade = col
        
        # Se não achou colunas exatas, tenta pegar pela posição (1ª nome, 2ª cidade)
        if not col_nome and len(df.columns) >= 1:
            col_nome = df.columns[0]
        if not col_cidade and len(df.columns) >= 2:
            col_cidade = df.columns[1]
            
        if col_nome:
            novo_df = pd.DataFrame()
            novo_df['NOME'] = df[col_nome].astype(str).str.strip().str.upper()
            
            if col_cidade:
                novo_df['CIDADE'] = df[col_cidade].astype(str).str.strip().str.upper()
            else:
                novo_df['CIDADE'] = "NÃO INFORMADA"
                
            return novo_df
            
    return None

def calcular_probabilidades(df):
    """Agrupa por Nome/Cidade e calcula chances."""
    if df is None or df.empty:
        return pd.DataFrame()
    
    total_entradas = len(df)
    
    # Agrupar e contar
    df_agrupado = df.groupby(['NOME', 'CIDADE']).size().reset_index(name='Total de Entradas')
    
    # Calcular %
    df_agrupado['Probabilidade (%)'] = (df_agrupado['Total de Entradas'] / total_entradas) * 100
    df_agrupado['Probabilidade (%)'] = df_agrupado['Probabilidade (%)'].map('{:.2f}%'.format)
    
    return df_agrupado.sort_values(by='Total de Entradas', ascending=False)

# --- Inicialização do Session State ---

if 'df_tickets' not in st.session_state:
    st.session_state.df_tickets = carregar_dados_exemplo()

if 'lista_premios' not in st.session_state:
    st.session_state.lista_premios = ["Vale Compras R$ 500", "Kit Ferramentas", "Smart TV 50"]

if 'historico_sorteios' not in st.session_state:
    st.session_state.historico_sorteios = []

# --- Sidebar (Menu) ---
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", ["Cadastro e Dados", "Sorteio"])
st.sidebar.markdown("---")
st.sidebar.info("Modo: Padrão Streamlit (Alto Contraste)")

# --- Página 1: Cadastro e Dados ---
if pagina == "Cadastro e Dados":
    st.title("📂 Cadastro e Dados")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("1. Upload de Participantes")
        st.write("Formato esperado: CSV com colunas **NOME** e **CIDADE**.")
        uploaded_file = st.file_uploader("Carregar arquivo CSV", type=['csv'])
        
        # Seletor de Separador (Correção solicitada)
        separador = st.radio("Qual o separador do arquivo?", ["Ponto e Vírgula (;)", "Vírgula (,)"], index=0, horizontal=True)
        sep_char = ";" if "Ponto" in separador else ","
        
        if uploaded_file:
            try:
                df_raw = pd.read_csv(uploaded_file, sep=sep_char)
                df_proc = processar_upload(df_raw)
                
                if df_proc is not None and not df_proc.empty:
                    st.session_state.df_tickets = df_proc
                    st.success(f"✅ Arquivo carregado! {len(df_proc)} entradas processadas.")
                else:
                    st.error("⚠️ Não encontramos as colunas NOME e CIDADE.")
                    st.warning(f"Dica: Tente mudar o separador acima para '{'Vírgula' if sep_char == ';' else 'Ponto e Vírgula'}'. Verifique também se o cabeçalho do CSV está correto.")
                    st.write("Colunas lidas:", list(df_raw.columns))
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
        
        st.markdown("---")
        st.subheader("2. Cadastro de Prêmios")
        novo_premio = st.text_input("Nome do Prêmios")
        if st.button("Adicionar Prêmio"):
            if novo_premio:
                st.session_state.lista_premios.append(novo_premio)
                st.success(f"Prêmio '{novo_premio}' adicionado!")
                st.rerun()
        
        if st.session_state.lista_premios:
            st.write("### 📋 Lista de Prêmios")
            for p in st.session_state.lista_premios:
                st.text(f"• {p}")
            
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
            df_display = calcular_probabilidades(st.session_state.df_tickets)
            
            total_tickets = len(st.session_state.df_tickets)
            total_pessoas = len(df_display)
            
            # Cards Nativos
            k1, k2 = st.columns(2)
            k1.metric("Total de Entradas (Chances)", total_tickets)
            k2.metric("Pessoas Únicas", total_pessoas)
            
            st.write("### Tabela de Probabilidades")
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum dado carregado.")

# --- Página 2: Sorteio ---
elif pagina == "Sorteio":
    st.title("🎯 Realizar Sorteio")
    
    if st.session_state.df_tickets.empty:
        st.warning("⚠️ Não há participantes cadastrados. Vá para a página de Cadastro.")
    else:
        # Configuração do Sorteio
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
            botao_sortear = st.button("� SORTEAR", type="primary", use_container_width=True)
        
        with c2:
            st.write("### Resultado")
            
            if botao_sortear:
                # 1. Definir Ganhador Real e Dados ANTES da animação
                df_atual = st.session_state.df_tickets
                lista_nomes_unicos = df_atual['NOME'].unique().tolist()
                
                indice_sorteado = random.choice(df_atual.index)
                ganhador_dados = df_atual.loc[indice_sorteado]
                
                nome_ganhador = ganhador_dados['NOME']
                cidade_ganhador = ganhador_dados['CIDADE']
                premio = st.session_state.premio_selecionado
                # Define o fuso horário do Brasil
                fuso_brasil = pytz.timezone('America/Sao_Paulo')
                # Pega a hora atual JÁ convertida para o Brasil
                hora_sorteio = datetime.now(fuso_brasil).strftime('%d/%m/%Y %H:%M:%S')
                # 2. Animação de Suspense (Roleta)
                placeholder = st.empty()
                # 2. Animação de Suspense (Roleta) - Duração Aprox. 5s
                placeholder = st.empty()
                tempo_espera = 0.03
                loops = 70 # Aumentado para durar mais
                
                # Garante que temos nomes suficientes para "piscar"
                nomes_animacao = lista_nomes_unicos if len(lista_nomes_unicos) > 5 else lista_nomes_unicos * 10
                
                for i in range(loops):
                    # Nome aleatório APENAS para visual
                    nome_flash = random.choice(nomes_animacao)
                    
                    # COR: Alterar cor aleatoriamente para efeito visual dinâmico
                    cor_flash = random.choice(["#FF4B4B", "#1C83E1", "#FFA421", "#555"])
                    
                    placeholder.markdown(
                        f"""
                        <div style="text-align: center; padding: 20px; border: 2px dashed #ddd; border-radius: 10px; background-color: #f9f9f9;">
                            <h3 style="color: #666; margin:0;">Sorteando...</h3>
                            <h1 style="color: {cor_flash}; font-size: 40px; margin: 10px 0;">{nome_flash}</h1>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    time.sleep(tempo_espera)
                    
                    # Lógica Progressiva para durar ~5s
                    # Começa rápido (0.03s) e vai desacelerando
                    if i > loops - 20: 
                        tempo_espera += 0.01 
                    if i > loops - 10:
                        tempo_espera += 0.03
                    if i > loops - 5:
                        tempo_espera += 0.05

                # 3. Exibição da Revelação Final
                placeholder.empty()
                
                st.balloons()
                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 30px; border-radius: 15px; background-color: #d4edda; border: 2px solid #28a745; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: #155724; text-transform: uppercase; letter-spacing: 2px;">🏆 Ganhador Confirmado �</h4>
                        <h1 style="color: #28a745; font-size: 55px; font-weight: 800; margin: 15px 0;">{nome_ganhador}</h1>
                        <h3 style="color: #333; margin-bottom: 5px;">📍 {cidade_ganhador}</h3>
                        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #c3e6cb;">
                            <p style="font-size: 18px; color: #555;"><b>🎁 Prêmio:</b> {premio}</p>
                            <p style="font-size: 14px; color: #777;">� Sorteado em: {hora_sorteio}</p>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Salvar Histórico
                registro = {
                    "Data/Hora": hora_sorteio,
                    "Prêmio": premio,
                    "Ganhador": nome_ganhador,
                    "Cidade": cidade_ganhador
                }
                st.session_state.historico_sorteios.append(registro)
                
                # Remover Ganhador (todas as entradas desse nome)
                if remover_ganhador:
                    st.session_state.df_tickets = df_atual[df_atual['NOME'] != nome_ganhador]
                    st.info(f"ℹ️ Todas as entradas de {nome_ganhador} foram removidas dos próximos sorteios.")

    st.markdown("---")
    st.subheader("📜 Últimos Ganhadores")
    if st.session_state.historico_sorteios:
        df_hist = pd.DataFrame(st.session_state.historico_sorteios)
        st.table(df_hist) # st.table é mais limpo para listas simples
    else:
        st.info("Nenhum sorteio realizado ainda hoje.")

