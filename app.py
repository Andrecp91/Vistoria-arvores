import streamlit as st
from datetime import date

# Configuração da página para parecer um app móvel
st.set_page_config(page_title="Vistoria MABOM - Árvores", layout="centered")

# --- CABEÇALHO ---
st.title("🚒 Vistoria de Risco Arbóreo")
st.caption("Baseado na Tabela MABOM - Vistoria, Poda e Corte de Árvores")

# --- DADOS DA OCORRÊNCIA ---
with st.expander("📝 Dados da Ocorrência", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        data_vistoria = st.date_input("Data", date.today())
        responsavel = st.text_input("Militar Responsável")
    with col2:
        local = st.text_input("Endereço / Local")
        especie = st.text_input("Espécie da Árvore (Opcional)")

st.divider()

# --- CÁLCULO DA PONTUAÇÃO ---
st.header("Avaliação de Risco")

# ITEM 1
st.subheader("Item 1: Avaliação dos Alvos")
st.info("Considere alvos dentro do raio de 1,5 x Altura da árvore.")
opcoes_item_1 = {
    "Há risco a pessoas (ocupação frequente)": 3,
    "Há risco eventual a pessoas (ocupação ocasional)": 2,
    "NÃO há risco a pessoas. Há risco a bens/propriedades": 1,
    "NÃO há risco a pessoas. NÃO há risco bens/propriedades": 0
}
item_1_label = st.radio("Selecione a situação do alvo:", list(opcoes_item_1.keys()))
pontos_item_1 = opcoes_item_1[item_1_label]
st.write(f"**Pontos Item 1:** {pontos_item_1}")

st.divider()

# ITEM 2
st.subheader("Item 2: Avaliação da Árvore (Tronco e Galhos)")
st.warning("Selecione a situação de PIOR cenário encontrada.")

# Dicionário com as descrições completas da tabela MABOM
opcoes_item_2 = {
    "4 pts - SITUAÇÃO DE RISCO EXTREMAMENTE ALTO": {
        "pontos": 4,
        "desc": """
        - Tronco degradado/cavidade excedendo limites + rachadura severa.
        - Rachaduras: tronco ou galho rachado ao meio.
        - Defeito afetando >= 40% da circunferência ou RCR + degradação extensa.
        - União fraca de galho com fissura + degradação.
        - Inclinação com rachaduras/elevação de solo recentes + Rachadura ou degradação extensa.
        - Galhos mortos: quebrados ou com rachaduras.
        - Árvores mortas: morta + outros defeitos, como fissuras, galhos dependurados, degradação extensa ou danos à raiz.
        - Obstrução física ao tráfego de pedestres e/ou veículos.
        """
    },
    "3 pts - SITUAÇÃO DE RISCO ALTO": {
        "pontos": 3,
        "desc": """
        - Tronco degradado ou cavidade > 30% da circunferência ou igual/excedendo o limite de segurança.
        - Rachaduras em contato com solo ou associadas a defeitos.
        - Defeito afetando > 40% da circunferência do tronco/galho.
        - Copa quebrada ou danificada > 50%; pinheiros > 30%.
        - União fraca do galho com rachaduras ou degradação.
        - Acinturamento de raízes >= 40% do tronco.
        - Danos à raiz >= 40% dentro do RCR.
        - Inclinação da árvore com fissuras no solo/elevação recente ou rachaduras na madeira ou degradação extensa.
        - Árvore morta SEM outros defeitos significativos.
        """
    },
    "2 pts - SITUAÇÃO DE RISCO MODERADO": {
        "pontos": 2,
        "desc": """
        - Tronco pouco degradado ou cavidade dentro dos limites.
        - Rachaduras sem processo de degradação extensa.
        - Defeito afetando 30-40% da circunferência.
        - Copa quebrada ou danificada < 50%; pinheiros > 30%.
        - União fraca do galho presente em galhos grandes ou em  troncos codominantes com casca inclusa.
        - Acinturamento do tronco pelas raízes , 40% da circunferência do tronco estrangulado.
        - Danos à raiz < 40% das raízes dentro do RCR.
        """
    },
    "1 pt - SITUAÇÃO DE RISCO BAIXO": {
        "pontos": 1,
        "desc": """
        - Perda de vigor menos intensa da copa ou de galhos.
        - Pequenos defeitos ou ferimentos/cancros.

        """
    }
}

item_2_select = st.selectbox("Classificação do defeito:", list(opcoes_item_2.keys()))
pontos_item_2 = opcoes_item_2[item_2_select]["pontos"]

# Mostra os detalhes técnicos para ajudar o militar a decidir
st.markdown(f"**Critérios para esta seleção:** {opcoes_item_2[item_2_select]['desc']}")

st.divider()

# ITEM 3
st.subheader("Item 3: Maior Diâmetro da Parte Defeituosa")
opcoes_item_3 = {
    "Diâmetro > 51 cm": 3,
    "Diâmetro de 10 a 51 cm": 2,
    "Diâmetro < 10 cm": 1
}
item_3_label = st.radio("Selecione o diâmetro:", list(opcoes_item_3.keys()))
pontos_item_3 = opcoes_item_3[item_3_label]

st.divider()

# ITEM 4
st.subheader("Item 4: Outros Fatores (Opcional)")
pontos_item_4 = st.slider("Acréscimo a critério do avaliador:", 0, 2, 0)

# --- RESULTADO FINAL ---
st.divider()
soma_total = pontos_item_1 + pontos_item_2 + pontos_item_3 + pontos_item_4

# Lógica do MABOM: "O risco será iminente se o somatório >= 9 pts"
st.header("📊 Resultado Final")

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.metric("SOMA TOTAL", f"{soma_total} pts")

with col_res2:
    if soma_total >= 9:
        st.error("🚨 RISCO IMINENTE! (>= 9 pts)")
        st.markdown("**Ação Sugerida:** Supressão ou eliminação imediata do risco.")
    elif soma_total >= 7:
        st.warning("⚠️ Risco Alto. Requer intervenção prioritária.")
    else:
        st.success("✅ Risco Moderado/Baixo. Monitoramento.")

# Botão de Gerar Texto para Relatório (útil para copiar e colar no REDS ou relatório)
if st.button("Gerar Texto para Relatório"):
    texto_relatorio = f"""
    VISTORIA TÉCNICA DE ÁRVORE - MABOM
    ----------------------------------
    Local: {local}
    Data: {data_vistoria}
    Responsável: {responsavel}
    
    PONTUAÇÃO TÉCNICA:
    Item 1 (Alvos): {pontos_item_1} pts
    Item 2 (Árvore): {pontos_item_2} pts
    Item 3 (Diâmetro): {pontos_item_3} pts
    Item 4 (Extras): {pontos_item_4} pts
    
    SOMA TOTAL: {soma_total} pontos
    RESULTADO: {'RISCO IMINENTE' if soma_total >= 9 else 'Risco Não Iminente'}
    """
    st.code(texto_relatorio)
