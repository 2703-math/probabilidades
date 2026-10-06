"""
🔺 Triângulo de Pascal e Binômio de Newton Visual
===================================================
Executar com: streamlit run pascal_binomial.py

Seis módulos didáticos interativos:
  1. O Triângulo de Pascal – construção n x k e Relação de Stifel
  2. Padrões Visuais – Sierpinski (pares/ímpares), Soma das linhas e Teorema do Hóquei
  3. Binômio de Newton – expansão algébrica de (ax + b)ⁿ e triângulo de coeficientes
  4. Termo Geral – busca por termo independente, termo em xᵖ e termo central
  5. Conexão com Probabilidade – ensaios de Bernoulli e Distribuição Binomial
  6. Aplicação na Genética – 1ª e 2ª Leis de Mendel e Herança Quantitativa (Poligenia)
"""

import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pascal & Binômio de Newton Visual",
    page_icon="🔺",
    layout="wide"
)

st.markdown("""
<style>
.main-title { font-size: 2.2rem; font-weight: 800; color: #0f172a; text-align: center; margin-bottom: .3rem; }
.subtitle { font-size: 1.05rem; color: #64748b; text-align: center; margin-bottom: 1.4rem; }
.card { background: #f8fafc; border-radius: 12px; padding: 1.1rem 1.3rem; border-left: 4px solid #3b82f6; margin-bottom: .9rem; color: #334155; line-height: 1.6; }
.form { background: #f0fdf4; border-radius: 10px; padding: .7rem 1.2rem; border-left: 4px solid #10b981; margin: .5rem 0; color: #065f46; font-size: 1.05rem; }
.warn { background: #fffbeb; border-radius: 10px; padding: .7rem 1.2rem; border-left: 4px solid #f59e0b; margin: .5rem 0; color: #78350f; }
.highlight { background: #eff6ff; border-radius: 8px; padding: .8rem; border: 1px solid #bfdbfe; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
# UTILITÁRIOS
# ────────────────────────────────────────────────────────────
def mostrar(fig, h=460):
    fig.update_layout(
        height=h,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(family="sans-serif", size=13)
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def formula(latex_str):
    st.latex(latex_str)

def quiz(chave, enunciado, opcoes, correta, explicacao):
    with st.expander("🎯 Teste sua intuição"):
        r = st.radio(enunciado, opcoes, index=None, key=f"q_{chave}")
        if r is not None:
            if opcoes.index(r) == correta:
                st.success(f"✅ {explicacao}")
            else:
                st.warning("🤔 Não ainda — observe as propriedades no gráfico e tente novamente.")

def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)

# ────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configurações")
    mostrar_formulas = st.checkbox("Mostrar fórmulas e demonstrações", value=True)
    st.markdown("---")
    st.subheader("🧑‍🏫 Roteiro sugerido")
    st.markdown(
        "**1. Pascal:** Explore a relação de Stifel e a simetria.\n\n"
        "**2. Padrões:** Ative a paridade para ver o Fractal de Sierpinski.\n\n"
        "**3. Binômio:** Conecte os coeficientes binomiais à expansão de $(a+b)^n$.\n\n"
        "**4. Termo Geral:** Calcule termos específicos sem expandir tudo.\n\n"
        "**5. Probabilidade:** Veja como o triângulo distribui as chances de moedas.\n\n"
        "**6. Genética:** Aplique o binômio em Mendel e na Herança Quantitativa."
    )
    st.markdown("---")
    st.caption("Desenvolvido para Ensino Médio e Pré-Vestibular")

# ────────────────────────────────────────────────────────────
# TÍTULO
# ────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🔺 Triângulo de Pascal & Binômio de Newton</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Propriedades combinatórias, expansões algébricas, fractais e genético-estatística</div>', unsafe_allow_html=True)

tabs = st.tabs([
    "1. O Triângulo de Pascal",
    "2. Padrões & Curiosidades",
    "3. Binômio de Newton",
    "4. Termo Geral",
    "5. Conexão com Probabilidade",
    "6. Aplicação na Genética"
])

# ══════════════════════════════════════════════════════════════
# ABA 1 — O TRIÂNGULO DE PASCAL E STIFEL
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""<div class="card">
    O <b>Triângulo de Pascal</b> é uma tabela triangular infinita de números onde o elemento na linha <i>n</i>
    e coluna <i>k</i> representa a combinação <b>C(n, k) = binom(n, k)</b>.<br>
    <b>Relação de Stifel:</b> Todo elemento interno é igual à soma do elemento diretamente acima com o elemento imediatamente à esquerda dele na linha anterior.
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            n_linhas = st.slider("Número de linhas (n)", 3, 12, 7, key="n_pascal")
            modo_exib = st.radio("Modo de exibição das células", ["Valores C(n,k)", "Notação Binomial binom(n,k)"], key="modo_pascal")
            destacar_stifel = st.checkbox("Destacar Relação de Stifel", value=True, key="stifel_chk")

            if destacar_stifel and n_linhas >= 2:
                st.markdown("**Selecione um elemento para aplicar Stifel:**")
                stifel_n = st.slider("Linha destino (n)", 2, n_linhas, min(3, n_linhas), key="stifel_n")
                stifel_k = st.slider("Coluna destino (k)", 1, stifel_n - 1, min(1, stifel_n - 1), key="stifel_k")

        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"\binom{n}{k} = \frac{n!}{k!(n-k)!}")
            st.markdown("**Relação de Stifel:**")
            formula(r"\binom{n-1}{k-1} + \binom{n-1}{k} = \binom{n}{k}")
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        xs, ys, textos, cores, hover_txt = [], [], [], [], []

        for i in range(n_linhas + 1):
            for j in range(i + 1):
                x_pos = j - i / 2.0
                y_pos = -i
                val = nCr(i, j)

                xs.append(x_pos)
                ys.append(y_pos)

                if modo_exib == "Valores C(n,k)":
                    textos.append(str(val))
                else:
                    textos.append(f"({i}<br>{j})")

                if destacar_stifel and n_linhas >= 2:
                    if i == stifel_n and j == stifel_k:
                        cores.append("#ef4444")
                    elif i == stifel_n - 1 and j == stifel_k - 1:
                        cores.append("#3b82f6")
                    elif i == stifel_n - 1 and j == stifel_k:
                        cores.append("#10b981")
                    else:
                        cores.append("#f1f5f9")
                else:
                    cores.append("#f1f5f9")

                hover_txt.append(f"Linha n={i}, Coluna k={j}<br>C({i},{j}) = {val}")

        fig_pascal = go.Figure()

        if destacar_stifel and n_linhas >= 2:
            x_dest = stifel_k - stifel_n / 2.0
            y_dest = -stifel_n
            x_p1 = (stifel_k - 1) - (stifel_n - 1) / 2.0
            y_p1 = -(stifel_n - 1)
            x_p2 = stifel_k - (stifel_n - 1) / 2.0
            y_p2 = -(stifel_n - 1)

            fig_pascal.add_trace(go.Scatter(
                x=[x_p1, x_dest], y=[y_p1, y_dest], mode="lines",
                line=dict(color="#3b82f6", width=3), hoverinfo="skip", showlegend=False
            ))
            fig_pascal.add_trace(go.Scatter(
                x=[x_p2, x_dest], y=[y_p2, y_dest], mode="lines",
                line=dict(color="#10b981", width=3), hoverinfo="skip", showlegend=False
            ))

        fig_pascal.add_trace(go.Scatter(
            x=xs, y=ys, mode="markers+text",
            text=textos, textposition="middle center",
            textfont=dict(size=12, color="#0f172a"),
            marker=dict(size=36, color=cores, line=dict(color="#94a3b8", width=1.5)),
            hovertext=hover_txt, hoverinfo="text", showlegend=False
        ))

        fig_pascal.update_xaxes(visible=False)
        fig_pascal.update_yaxes(visible=False)
        fig_pascal.update_layout(title="Triângulo de Pascal (Representação Piramidal)")
        mostrar(fig_pascal, 480)

        if destacar_stifel and n_linhas >= 2:
            p1_val = nCr(stifel_n - 1, stifel_k - 1)
            p2_val = nCr(stifel_n - 1, stifel_k)
            res_val = nCr(stifel_n, stifel_k)
            st.info(f"🔵 **C({stifel_n-1}, {stifel_k-1}) = {p1_val}** + 🟢 **C({stifel_n-1}, {stifel_k}) = {p2_val}** ⟹ 🔴 **C({stifel_n}, {stifel_k}) = {res_val}**")

    quiz("stifel1", "Qual é o valor do elemento C(6, 3) sabendo que C(5, 2) = 10 e C(5, 3) = 10?",
         ["15", "20", "25", "30"], 1,
         "Pela Relação de Stifel: C(6, 3) = C(5, 2) + C(5, 3) = 10 + 10 = 20.")

# ══════════════════════════════════════════════════════════════
# ABA 2 — PADRÕES & CURIOSIDADES VISUAIS
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("""<div class="card">
    O Triângulo de Pascal esconde propriedades matemáticas fascinantes:
    <b>Soma das Linhas (2ⁿ)</b>, <b>Fractal de Sierpinski (Pares vs Ímpares)</b>, <b>Sequência de Fibonacci</b> e o <b>Teorema do Hóquei</b>.
    </div>""", unsafe_allow_html=True)

    padrao = st.selectbox("Selecione o Padrão para Visualizar", [
        "1. Paridade & Fractal de Sierpinski",
        "2. Soma das Linhas (Potências de 2)",
        "3. Teorema do Hóquei (Hockey-Stick Identity)",
        "4. Diagonais e Sequência de Fibonacci"
    ], key="padrao_sel")

    if padrao.startswith("1."):
        c1, c2 = st.columns([1, 2.5])
        with c1:
            n_f = st.slider("Número de linhas", 8, 32, 16, key="n_sierp")
            mod_val = st.radio("Destacar divisibilidade por", [2, 3, 5], format_func=lambda x: f"Múltiplos de {x}" if x > 2 else "Números Pares (mod 2)", key="mod_sierp")
            st.caption("Ao colorir os números ímpares (ou não múltiplos), emerge o padrão fractal do Triângulo de Sierpinski!")
        with c2:
            grid = np.zeros((n_f + 1, n_f + 1))
            for i in range(n_f + 1):
                for j in range(i + 1):
                    val = nCr(i, j)
                    grid[i, j] = 1 if val % mod_val == 0 else 2

            fig_sierp = go.Figure(go.Heatmap(
                z=grid, x=list(range(n_f + 1)), y=list(range(n_f + 1)),
                colorscale=[[0, "#ffffff"], [0.5, "#e2e8f0"], [1.0, "#3b82f6"]],
                showscale=False, hovertemplate="Linha %{y}, Coluna %{x}<extra></extra>"
            ))
            fig_sierp.update_yaxes(autorange="reversed", title="Linha (n)")
            fig_sierp.update_xaxes(title="Coluna (k)")
            fig_sierp.update_layout(title=f"Matriz do Triângulo mod {mod_val} (Fractal de Sierpinski)")
            mostrar(fig_sierp, 420)

    elif padrao.startswith("2."):
        c1, c2 = st.columns([1, 2.5])
        with c1:
            n_pow = st.slider("Número de linhas", 3, 15, 8, key="n_pow")
            st.markdown("A soma dos elementos da linha *n* é sempre **2ⁿ**:")
            for i in range(min(n_pow + 1, 6)):
                st.write(f"Linha {i}: soma = {2**i}")
        with c2:
            xs_p = list(range(n_pow + 1))
            ys_p = [2**i for i in xs_p]
            fig_pow = go.Figure(go.Bar(
                x=xs_p, y=ys_p, text=[f"2^{i} = {v}" for i, v in zip(xs_p, ys_p)],
                textposition="outside", marker_color="#3b82f6"
            ))
            fig_pow.update_layout(
                title="Soma dos Elementos da Linha n: ∑ C(n, k) = 2ⁿ",
                xaxis=dict(title="Linha (n)", dtick=1),
                yaxis=dict(title="Soma total")
            )
            mostrar(fig_pow, 400)

    elif padrao.startswith("3."):
        st.markdown("**Teorema do Hóquei:** A soma dos elementos de uma diagonal, começando da borda (k=0 ou k=n), é igual ao elemento na linha seguinte, na coluna logo abaixo do último somado.")
        c1, c2 = st.columns([1, 2.5])
        with c1:
            diag_k = st.slider("Escolha a coluna diagonal (k)", 0, 4, 1, key="hoquei_k")
            len_diag = st.slider("Tamanho da haste do taco", 2, 6, 4, key="hoquei_len")
            r_start = diag_k
            r_end = r_start + len_diag - 1

            soma_h = sum(nCr(r, diag_k) for r in range(r_start, r_end + 1))
            res_r, res_k = r_end + 1, diag_k + 1

            st.success(f"Soma da haste: **{soma_h}**\n\nElemento do cabo C({res_r}, {res_k}): **{nCr(res_r, res_k)}**")

        with c2:
            n_h = res_r + 1
            xs_h, ys_h, txt_h, colors_h = [], [], [], []
            for i in range(n_h + 1):
                for j in range(i + 1):
                    x_pos = j - i / 2.0
                    y_pos = -i
                    val = nCr(i, j)
                    xs_h.append(x_pos)
                    ys_h.append(y_pos)
                    txt_h.append(str(val))

                    if diag_k <= j <= diag_k and r_start <= i <= r_end:
                        colors_h.append("#3b82f6")
                    elif i == res_r and j == res_k:
                        colors_h.append("#ef4444")
                    else:
                        colors_h.append("#f1f5f9")

            fig_hoquei = go.Figure(go.Scatter(
                x=xs_h, y=ys_h, mode="markers+text",
                text=txt_h, textposition="middle center",
                marker=dict(size=32, color=colors_h, line=dict(color="#94a3b8", width=1.5)),
                showlegend=False
            ))
            fig_hoquei.update_xaxes(visible=False)
            fig_hoquei.update_yaxes(visible=False)
            fig_hoquei.update_layout(title="Teorema do Hóquei (Células Azuis somam a Célula Vermelha)")
            mostrar(fig_hoquei, 420)

    else:
        st.markdown("**Diagonais Rasas e Fibonacci:** Somando os elementos ao longo das diagonais rasas do Triângulo de Pascal, obtemos a Sequência de Fibonacci (1, 1, 2, 3, 5, 8, 13...).")
        n_fib = st.slider("Termos de Fibonacci para gerar", 4, 10, 6, key="n_fib")
        fibs = []
        for n in range(n_fib):
            val = sum(nCr(n - k, k) for k in range(n // 2 + 1))
            fibs.append(val)

        df_fib = pd.DataFrame({
            "Termo (F_n)": [f"F_{i+1}" for i in range(n_fib)],
            "Soma das Diagonais Rasas": [f"∑ C({i}-k, k)" for i in range(n_fib)],
            "Valor de Fibonacci": fibs
        })
        st.dataframe(df_fib, use_container_width=True, hide_index=True)

    quiz("pad2", "Qual é a soma dos elementos da linha 5 do Triângulo de Pascal (n=5)?",
         ["16", "32", "64", "128"], 1,
         "A soma dos elementos da linha n é 2ⁿ. Para n=5, 2⁵ = 32.")

# ══════════════════════════════════════════════════════════════
# ABA 3 — BINÔMIO DE NEWTON
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""<div class="card">
    O <b>Binômio de Newton</b> estabelece a fórmula de expansão para a potência de um binômio:
    <b>(a + b)ⁿ = ∑ C(n, k) · aⁿ⁻ᵏ · bᵏ</b>.<br>
    Os coeficientes do desenvolvimento são exatamente os números da linha <i>n</i> do Triângulo de Pascal!
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            coef_a = st.number_input("Coeficiente 'a'", value=1, step=1, key="bin_a")
            coef_b = st.number_input("Coeficiente 'b'", value=1, step=1, key="bin_b")
            exp_n = st.slider("Expoente (n)", 0, 10, 3, key="bin_n")

        soma_coef = (coef_a + coef_b)**exp_n
        st.metric("Soma dos Coeficientes (x=1)", f"{soma_coef:,}".replace(",", "."))

        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k")
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        termos_str = []
        valores_termos = []
        labels_termos = []

        for k in range(exp_n + 1):
            cnk = nCr(exp_n, k)
            val_coef = cnk * (coef_a**(exp_n - k)) * (coef_b**k)
            valores_termos.append(val_coef)

            pow_a = exp_n - k
            pow_b = k

            t_str = f"{val_coef}" if val_coef != 1 or (pow_a == 0 and pow_b == 0) else ""
            if pow_a > 0:
                t_str += "x" if pow_a == 1 else f"x^{{{pow_a}}}"
            if pow_b > 0:
                t_str += "y" if pow_b == 1 else f"y^{{{pow_b}}}"

            termos_str.append(t_str)
            labels_termos.append(f"k={k}")

        st.markdown("#### Expansão Algébrica Completa:")
        expansao_latex = f"({coef_a}x + {coef_b}y)^{{{exp_n}}} = " + " + ".join(termos_str)
        expansao_latex = expansao_latex.replace("+ -", "- ")
        st.latex(expansao_latex)

        fig_bin = go.Figure(go.Bar(
            x=labels_termos, y=valores_termos,
            text=[f"{v}" for v in valores_termos], textposition="outside",
            marker_color="#10b981"
        ))
        fig_bin.update_layout(
            title=f"Valores dos Coeficientes Expandidos de ({coef_a}x + {coef_b}y)^{exp_n}",
            xaxis_title="Índice do Termo (k)",
            yaxis_title="Valor do Coeficiente"
        )
        mostrar(fig_bin, 360)

    quiz("bin1", "Qual é a soma de todos os coeficientes da expansão de (2x + 1)⁵?",
         ["32", "243", "64", "100"], 1,
         "Para encontrar a soma dos coeficientes, fazemos x = 1: (2(1) + 1)⁵ = 3⁵ = 243.")

# ══════════════════════════════════════════════════════════════
# ABA 4 — TERMO GERAL DO BINÔMIO
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("""<div class="card">
    O <b>Termo Geral</b> permite encontrar qualquer termo específico do desenvolvimento sem precisar expandir todo o binômio:<br>
    <b>T_{k+1} = binom(n, k) · (A)^n-k · (B)^k</b>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2.2])
    with c1:
        with st.container(border=True):
            st.markdown("**Binômio da forma: (c₁ · xᵖ¹ + c₂ · xᵖ²)ⁿ**")
            c1_val = st.number_input("Coeficiente c₁", value=1, key="tg_c1")
            p1_val = st.number_input("Expoente p₁ de x no 1º termo", value=1, key="tg_p1")
            c2_val = st.number_input("Coeficiente c₂", value=1, key="tg_c2")
            p2_val = st.number_input("Expoente p₂ de x no 2º termo", value=-1, key="tg_p2")
            n_tg = st.slider("Expoente n", 1, 15, 6, key="tg_n")

        k_sel = st.slider("Escolha a posição k (para T_{k+1})", 0, n_tg, min(2, n_tg), key="tg_k")

        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"T_{k+1} = \binom{n}{k} A^{n-k} B^k")
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        passos = []
        for k in range(n_tg + 1):
            cnk = nCr(n_tg, k)
            coef_num = cnk * (c1_val**(n_tg - k)) * (c2_val**k)
            exp_x = p1_val * (n_tg - k) + p2_val * k
            is_indep = (exp_x == 0)
            passos.append({
                "Posição": f"T_{k+1} (k={k})",
                "Binomial C(n,k)": cnk,
                "Coeficiente": coef_num,
                "Expoente de x": exp_x,
                "Termo Independente?": "⭐ SIM" if is_indep else "Não"
            })

        df_tg = pd.DataFrame(passos)
        st.markdown("#### Análise de todos os termos do Binômio:")
        st.dataframe(df_tg, use_container_width=True, hide_index=True)

        sel_row = df_tg.iloc[k_sel]
        st.success(
            f"🎯 **Termo T_{k_sel+1} (k={k_sel}):** \n"
            f"Valor = **{sel_row['Coeficiente']} · x^{{{sel_row['Expoente de x']}}}**"
        )

        indep_row = df_tg[df_tg["Expoente de x"] == 0]
        if not indep_row.empty:
            st.info(f"💡 **Termo Independente de x encontrado:** {indep_row.iloc[0]['Posição']} com valor **{indep_row.iloc[0]['Coeficiente']}**")
        else:
            st.warning("ℹ️ Esta expansão não possui termo independente de x (expoente 0).")

    quiz("tg_q1", "No desenvolvimento de (x + 2)⁴, qual é o 3º termo T₃ (k=2)?",
         ["6x²", "12x²", "24x²", "8x³"], 2,
         "T₃ = C(4, 2) · x⁴⁻² · 2² = 6 · x² · 4 = 24x².")

# ══════════════════════════════════════════════════════════════
# ABA 5 — CONEXÃO COM PROBABILIDADE
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""<div class="card">
    A <b>Distribuição Binomial</b> modela experimentos com <i>n</i> ensaios independentes de Bernoulli (sucesso/fracasso).<br>
    A probabilidade de obter exatamente <i>k</i> sucessos é: 
    <b>P(X = k) = binom(n, k) · pᵏ · (1 - p)ⁿ⁻ᵏ</b>.<br>
    O Triângulo de Pascal fornece diretamente o número de maneiras favoráveis de combinar os sucessos!
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            n_moedas = st.slider("Número de lançamentos de moeda (n)", 1, 12, 6, key="pb_n")
            p_sucesso = st.slider("Probabilidade de Cara (p)", 0.05, 0.95, 0.50, 0.05, key="pb_p")
            k_desejado = st.slider("Número de Caras desejadas (k)", 0, n_moedas, min(3, n_moedas), key="pb_k")

        p_k = nCr(n_moedas, k_desejado) * (p_sucesso**k_desejado) * ((1 - p_sucesso)**(n_moedas - k_desejado))
        st.metric(f"P(X = {k_desejado} caras)", f"{p_k * 100:.2f}%")

        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}")
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        ks = list(range(n_moedas + 1))
        probs = [nCr(n_moedas, k) * (p_sucesso**k) * ((1 - p_sucesso)**(n_moedas - k)) for k in ks]
        cores_b = ["#ef4444" if k == k_desejado else "#3b82f6" for k in ks]

        fig_prob = go.Figure(go.Bar(
            x=[f"{k} caras" for k in ks], y=[p * 100 for p in probs],
            text=[f"{p*100:.1f}%<br>(C={nCr(n_moedas,k)})" for p, k in zip(probs, ks)],
            textposition="outside", marker_color=cores_b
        ))

        fig_prob.update_layout(
            title=f"Distribuição Binomial para {n_moedas} Lançamentos (p = {p_sucesso:.2f})",
            xaxis_title="Resultado (k sucessos)",
            yaxis_title="Probabilidade (%)"
        )
        mostrar(fig_prob, 400)

        st.info(f"De todas as **2^{n_moedas} = {2**n_moedas}** sequências possíveis, exatamente **C({n_moedas}, {k_desejado}) = {nCr(n_moedas, k_desejado)}** resultam em {k_desejado} caras.")

    quiz("pb1", "Lançando 4 moedas honestas (p=0.5), qual a probabilidade de obter exatamente 2 caras?",
         ["25%", "37,5%", "50%", "12,5%"], 1,
         "P(X=2) = C(4,2) · (0,5)² · (0,5)² = 6 · (1/16) = 6/16 = 37,5%.")

# ══════════════════════════════════════════════════════════════
# ABA 6 — APLICAÇÃO NA GENÉTICA (MENDEL & POLIGENIA)
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("""<div class="card">
    <b>A Genética de Mendel e o Triângulo de Pascal:</b><br>
    A distribuição dos genótipos e fenótipos na genética segue rigorosamente as leis binomiais!<br>
    • <b>1ª Lei de Mendel:</b> O cruzamento Aa x Aa produz a proporção genotípica 1 AA : 2 Aa : 1 aa (linha 2 de Pascal).<br>
    • <b>Cálculo de Proles:</b> A probabilidade de um casal ter k filhos com determinado fenótipo em N nascimentos é dada pela expansão binomial (p + q)ⁿ.<br>
    • <b>2ª Lei de Mendel:</b> A combinação de dois genes independentes (3+1)² = 9 : 3 : 3 : 1 é o quadrado do binômio fenotípico.<br>
    • <b>Herança Quantitativa (Poligenia):</b> A frequência dos fenótipos para N pares de alelos segue a linha 2N de Pascal, formando a curva normal em sino.
    </div>""", unsafe_allow_html=True)

    modo_genetica = st.radio("Selecione o conceito genético:", [
        "1. Probabilidade na Família (1ª Lei em Proles)",
        "2. Dihibridismo (2ª Lei de Mendel)",
        "3. Herança Quantitativa / Poligenia"
    ], key="gen_modo")

    if modo_genetica.startswith("1."):
        st.markdown("### 🧬 Probabilidade de Fenótipos em uma Família")
        st.caption("Exemplo: Casal heterozigoto (Aa x Aa) para um caráter autossômico recessivo (ex: Albinismo).")

        cg1, cg2 = st.columns([1, 2.3])
        with cg1:
            with st.container(border=True):
                n_filhos = st.slider("Número de filhos do casal (N)", 1, 10, 4, key="gen_n")
                p_fenotipo = st.radio("Fenótipo desejado:", [
                    "Dominante (Normal) - P = 3/4",
                    "Recessivo (Afetado) - P = 1/4"
                ], key="gen_p_type")

                p_val = 0.75 if "Dominante" in p_fenotipo else 0.25
                q_val = 1 - p_val

                k_filhos = st.slider("Quantidade exata de filhos com esse fenótipo (k)", 0, n_filhos, min(3 if p_val == 0.75 else 1, n_filhos), key="gen_k")

            p_exata = nCr(n_filhos, k_filhos) * (p_val**k_filhos) * (q_val**(n_filhos - k_filhos))
            st.metric(f"P(exatamente {k_filhos} filhos)", f"{p_exata*100:.2f}%")

            if mostrar_formulas:
                st.markdown('<div class="form">', unsafe_allow_html=True)
                formula(r"P(X = k) = \binom{N}{k} \left(\frac{3}{4}\right)^k \left(\frac{1}{4}\right)^{N-k}")
                st.markdown('</div>', unsafe_allow_html=True)

        with cg2:
            ks = list(range(n_filhos + 1))
            probs = [nCr(n_filhos, k) * (p_val**k) * (q_val**(n_filhos - k)) for k in ks]
            cores_g = ["#ef4444" if k == k_filhos else "#3b82f6" for k in ks]

            lbl_fen = "Dominante(s)" if p_val == 0.75 else "Recessivo(s)"

            fig_gen1 = go.Figure(go.Bar(
                x=[f"{k} {lbl_fen}" for k in ks],
                y=[p * 100 for p in probs],
                text=[f"{p*100:.1f}%<br>(Termo C={nCr(n_filhos, k)})" for p, k in zip(probs, ks)],
                textposition="outside", marker_color=cores_g
            ))
            fig_gen1.update_layout(
                title=f"Distribuição Binomial para Família de {n_filhos} Filhos",
                xaxis_title="Número de filhos com a característica",
                yaxis_title="Probabilidade (%)"
            )
            mostrar(fig_gen1, 380)

    elif modo_genetica.startswith("2."):
        st.markdown("### 🧬 2ª Lei de Mendel (Dihibridismo)")
        st.markdown(
            "No cruzamento $AaBb \\times AaBb$, a segregação de cada par de alelos é independente ($3:1$).\n"
            "A combinação dos dois pares equivale ao quadrado do binômio fenotípico:"
        )
        st.latex(r"(3\text{ Dominantes} + 1\text{ Recessivo})^2 = 9\text{ A\_B\_} + 3\text{ A\_bb} + 3\text{ aaB\_} + 1\text{ aabb}")

        df_mendel2 = pd.DataFrame({
            "Fenótipo": ["Dominante / Dominante (A_B_)", "Dominante / Recessivo (A_bb)", "Recessivo / Dominante (aaB_)", "Recessivo / Recessivo (aabb)"],
            "Proporção": ["9/16 (56,25%)", "3/16 (18,75%)", "3/16 (18,75%)", "1/16 (6,25%)"],
            "Origem Binomial": ["(3/4) × (3/4) = 9/16", "(3/4) × (1/4) = 3/16", "(1/4) × (3/4) = 3/16", "(1/4) × (1/4) = 1/16"]
        })
        st.table(df_mendel2)

        fig_m2 = go.Figure(go.Pie(
            labels=["A_B_ (9)", "A_bb (3)", "aaB_ (3)", "aabb (1)"],
            values=[9, 3, 3, 1],
            marker=dict(colors=["#3b82f6", "#10b981", "#f59e0b", "#ef4444"]),
            textinfo="label+percent"
        ))
        fig_m2.update_layout(title="Proporção Fenotípica da 2ª Lei de Mendel (9 : 3 : 3 : 1)")
        mostrar(fig_m2, 360)

    else:
        st.markdown("### 🧬 Herança Quantitativa (Poligenia)")
        st.markdown(
            "Em características influenciadas por múltiplos pares de genes com efeito aditivo (ex: cor da pele, altura, teor de óleo em sementes):\n\n"
            "Para **$N$ pares de alelos** em genitores heterozigotos ($AaBbCc... \\times AaBbCc...$), existem **$2N$ alelos aditivos**.\n"
            "A quantidade de alelos aditivos segue exatamente a **linha $2N$ do Triângulo de Pascal**!"
        )

        cg1, cg2 = st.columns([1, 2.3])
        with cg1:
            n_pares = st.slider("Número de pares de alelos (N)", 1, 5, 2, key="pol_n")
            tot_alelos = 2 * n_pares
            st.info(f"**Pares de genes:** {n_pares} \n**Total de alelos aditivos:** {tot_alelos} \n**Linha do Triângulo de Pascal:** n = {tot_alelos}")
            st.metric("Total de combinações de gametas", f"4^{n_pares} = {4**n_pares}")

        with cg2:
            ks_p = list(range(tot_alelos + 1))
            comb_p = [nCr(tot_alelos, k) for k in ks_p]
            pcts_p = [c / (2**tot_alelos) * 100 for c in comb_p]

            fig_poli = go.Figure(go.Bar(
                x=[f"{k} aditivos" for k in ks_p],
                y=pcts_p,
                text=[f"{c}/{2**tot_alelos}<br>({p:.1f}%)" for c, p in zip(comb_p, pcts_p)],
                textposition="outside",
                marker_color="#8b5cf6"
            ))
            fig_poli.update_layout(
                title=f"Distribuição Fenotípica para Poligenia com {n_pares} Par(es) de Genes (Curva Normal)",
                xaxis_title="Número de Alelos Aditivos",
                yaxis_title="Frequência na Prole (%)"
            )
            mostrar(fig_poli, 400)

    quiz("gen_q1", "Em um caso de herança quantitativa com 2 pares de genes (4 alelos no total), qual linha do Triângulo de Pascal define as proporções fenotípicas?",
         ["Linha 2 (1, 2, 1)", "Linha 4 (1, 4, 6, 4, 1)", "Linha 8 (1, 8, 28...)", "Linha 16"], 1,
         "Com 2 pares de genes heterozigotos (AaBb x AaBb), o total de alelos aditivos varia de 0 a 4. As proporções fenotípicas correspondem à linha 4 do Triângulo de Pascal: 1:4:6:4:1 (com um total de 16 combinações).")

# RODAPÉ
st.markdown("---")
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:.85rem;padding:1rem;">'
    '🔺 <b>Triângulo de Pascal & Binômio de Newton Visual</b> — combinações · Stifel · Sierpinski · termo geral · distribuição binomial · genética mendeliana</div>',
    unsafe_allow_html=True)
