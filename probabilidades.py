"""
🎲 Probabilidade Visual — Do clássico à Teoria dos Jogos
=========================================================
Executar com:   streamlit run probabilidades.py

Sete módulos didáticos:
  1. Fundamentos     – espaço amostral, tipos de evento, Lei dos Grandes Números
  2. Árvore          – experimentos compostos animados
  3. Eventos Suces.  – produto de probabilidades, caminho na árvore
  4. Complementar    – P(A') = 1 – P(A), paradoxo do aniversário
  5. Condicional     – P(A|B), Bayes, tabela de contingência interativa
  6. União           – P(A∪B), diagrama de Venn animado
  7. Teoria dos      – Dilema do Prisioneiro, Pedra-Papel-Tesoura, Equilíbrio de Nash
     Jogos

Roteiro: Prever → Observar → Explicar (caixas "Teste sua intuição")
"""
import math
import random
import itertools
from fractions import Fraction
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ────────────────────────────────────────────
# PÁGINA
# ────────────────────────────────────────────
st.set_page_config(page_title="Probabilidade Visual", page_icon="🎲", layout="wide")
st.markdown("""
<style>
.main-title{font-size:2.2rem;font-weight:800;color:#0f172a;text-align:center;margin-bottom:.3rem}
.subtitle{font-size:1.1rem;color:#64748b;text-align:center;margin-bottom:1.5rem}
.card{background:#f8fafc;border-radius:12px;padding:1.2rem;border-left:4px solid #3b82f6;
      margin-bottom:1rem;color:#334155}
.warn{background:#fffbeb;border-radius:12px;padding:1.2rem;border-left:4px solid #f59e0b;
      margin-bottom:1rem;color:#334155}
.formula{background:#f0fdf4;border-radius:10px;padding:.8rem 1.2rem;border-left:4px solid #10b981;
         margin:.6rem 0;color:#065f46;font-size:1.05rem}
</style>
""", unsafe_allow_html=True)

CORES = ["#3b82f6","#ef4444","#10b981","#f59e0b","#8b5cf6","#06b6d4","#f97316"]

# ────────────────────────────────────────────
# UTILITÁRIOS
# ────────────────────────────────────────────
def mostrar(fig, h=None):
    kw = dict(use_container_width=True, config={"displayModeBar": False})
    if h: fig.update_layout(height=h)
    st.plotly_chart(fig, **kw)

def quiz(chave, enunciado, opcoes, correta, explicacao):
    with st.expander("🎯 Teste sua intuição"):
        r = st.radio(enunciado, opcoes, index=None, key=f"q_{chave}")
        if r is not None:
            if opcoes.index(r) == correta:
                st.success(f"✅ Isso mesmo! {explicacao}")
            else:
                st.warning("🤔 Não ainda. Observe os gráficos, mexa nos controles e tente de novo.")

def frac_str(n, d):
    """Retorna string de fração irredutível."""
    g = math.gcd(int(n), int(d))
    return f"{n//g}/{d//g}" if g else f"{n}/{d}"

# ────────────────────────────────────────────
# ABA 1 — FUNDAMENTOS E LEI DOS GRANDES NÚMEROS
# ────────────────────────────────────────────
def fig_fundamentos(lados, n_sim, seed):
    rng = np.random.default_rng(seed)
    rolls = rng.integers(1, lados + 1, size=n_sim)
    p_teo = 1 / lados

    fig = make_subplots(1, 2,
        subplot_titles=("Frequência relativa acumulada (Lei dos Grandes Números)",
                        f"Histograma de {n_sim:,} lançamentos".replace(",", ".")),
        horizontal_spacing=.1)

    for face in range(1, lados + 1):
        hits = (rolls == face).cumsum()
        freq = hits / np.arange(1, n_sim + 1)
        xs = np.arange(1, n_sim + 1)
        fig.add_trace(go.Scatter(x=xs, y=freq, mode="lines",
            line=dict(color=CORES[(face-1) % len(CORES)], width=1.4),
            name=f"Face {face}",
            hovertemplate="n=%{x}<br>freq=%{y:.4f}<extra></extra>"), 1, 1)

    fig.add_hline(y=p_teo, line=dict(color="#0f172a", dash="dash", width=2),
                  annotation_text=f"P teórico = {frac_str(1,lados)}",
                  annotation_position="top right", row=1, col=1)

    counts = [(rolls == f).sum() for f in range(1, lados + 1)]
    fig.add_trace(go.Bar(x=[str(f) for f in range(1, lados + 1)], y=counts,
        marker_color=CORES[:lados],
        text=[f"{c/n_sim*100:.1f}%" for c in counts], textposition="outside",
        hovertemplate="face %{x}<br>%{y} vezes<extra></extra>"), 1, 2)
    fig.add_hline(y=n_sim * p_teo, line=dict(color="#0f172a", dash="dash", width=2),
                  annotation_text="esperado", annotation_position="top right", row=1, col=2)

    fig.update_xaxes(type="log", title_text="n (lançamentos)", row=1, col=1)
    fig.update_yaxes(range=[0, 1], title_text="frequência relativa", row=1, col=1)
    fig.update_xaxes(title_text="face", row=1, col=2)
    fig.update_yaxes(title_text="contagem", row=1, col=2)
    fig.update_layout(showlegend=True, plot_bgcolor="white", paper_bgcolor="white",
                      margin=dict(l=10,r=10,t=70,b=10), legend=dict(orientation="h", y=-.15))
    return fig

def fig_espaco_amostral(lados):
    if lados > 6:
        return None
    n = lados
    xs, ys, txts, cors = [], [], [], []
    for i in range(1, n+1):
        for j in range(1, n+1):
            xs.append(i); ys.append(j)
            txts.append(f"({i},{j})")
            s = i + j
            cors.append(s)
    fig = go.Figure(go.Scatter(x=xs, y=ys, mode="markers+text",
        text=txts, textposition="top center",
        marker=dict(size=28, color=cors, colorscale="RdYlGn", showscale=True,
                    colorbar=dict(title="Soma")),
        hovertemplate="(%{x},%{y})<br>soma=%{marker.color}<extra></extra>"))
    fig.update_layout(title=f"Espaço amostral: dois dados de {n} lados ({n*n} resultados)",
        xaxis=dict(title="Dado 1", dtick=1), yaxis=dict(title="Dado 2", dtick=1),
        plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=10,t=60,b=10))
    return fig

# ────────────────────────────────────────────
# ABA 2 — ÁRVORE DE PROBABILIDADES
# ────────────────────────────────────────────
def construir_arvore(etapas):
    nodes = [{"id": "R", "label": "Início", "prob": 1.0, "nivel": 0, "pos_y": 0.5}]
    edges = []
    nivel_nos = {"R": nodes[0]}
    proximo_id = [0]

    def novo_id():
        proximo_id[0] += 1
        return f"N{proximo_id[0]}"

    nos_atuais = ["R"]
    for k, opcoes in enumerate(etapas):
        nos_novos = []
        grupos = []
        for pai_id in nos_atuais:
            filhos = []
            for lbl, p in opcoes:
                nid = novo_id()
                p_acum = nivel_nos[pai_id]["prob"] * p
                filhos.append({"id": nid, "label": lbl, "prob": p_acum,
                                "nivel": k+1, "prob_ramo": p, "pai": pai_id})
                nos_novos.append(nid)
            grupos.append(filhos)

        total = sum(len(g) for g in grupos)
        for g in grupos:
            pai_y = nivel_nos[g[0]["pai"]]["pos_y"] if g else 0.5
            n = len(g)
            span = 1.0 / max(total, 1)
            start = pai_y - (n - 1) * span / 2
            for i, no in enumerate(g):
                no["pos_y"] = start + i * span
                nodes.append(no)
                nivel_nos[no["id"]] = no
                edges.append((no["pai"], no["id"], no["prob_ramo"]))
        nos_atuais = nos_novos

    n_niveis = len(etapas) + 1
    for no in nodes:
        no["pos_x"] = no["nivel"] / max(n_niveis - 1, 1)

    return nodes, edges

def fig_arvore(nodes, edges, destacar=None):
    fig = go.Figure()
    for pai_id, filho_id, p_ramo in edges:
        pai  = next(n for n in nodes if n["id"] == pai_id)
        filho = next(n for n in nodes if n["id"] == filho_id)
        cor = "#ef4444" if destacar and filho_id in destacar else "#94a3b8"
        larg = 4 if destacar and filho_id in destacar else 1.5
        mx = (pai["pos_x"] + filho["pos_x"]) / 2
        my = (pai["pos_y"] + filho["pos_y"]) / 2
        fig.add_trace(go.Scatter(
            x=[pai["pos_x"], filho["pos_x"]], y=[pai["pos_y"], filho["pos_y"]],
            mode="lines", line=dict(color=cor, width=larg), hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(
            x=[mx], y=[my], mode="text",
            text=[f"p={frac_str(round(p_ramo*100), 100) if p_ramo not in (0.5,1/3,1/4,1/6,2/3,3/4) else str(Fraction(p_ramo).limit_denominator(20))}"],
            textfont=dict(size=11, color=cor), hoverinfo="skip", showlegend=False))

    xs = [n["pos_x"] for n in nodes]
    ys = [n["pos_y"] for n in nodes]
    txts = [f"{n['label']}<br>{n['prob']:.3f}" if n["id"] != "R" else "Início" for n in nodes]
    cors = ["#ef4444" if destacar and n["id"] in destacar else
            ("#0f172a" if n["id"] == "R" else "#3b82f6") for n in nodes]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers+text",
        text=txts, textposition="middle right",
        textfont=dict(size=12, color="#0f172a"),
        marker=dict(size=18, color=cors, line=dict(color="white", width=2)),
        hovertemplate="%{text}<extra></extra>", showlegend=False))

    fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(visible=False, range=[-0.05, 1.35]),
        yaxis=dict(visible=False, range=[-0.05, 1.05]),
        margin=dict(l=10, r=10, t=20, b=10))
    return fig

# ────────────────────────────────────────────
# ABA 5 — CONDICIONAL e BAYES
# ────────────────────────────────────────────
def fig_contingencia(a, b, ab):
    nao_ab = a - ab
    b_nao_a = b - ab
    nem = 100 - a - b + ab
    fig = go.Figure()
    cats = ["Em A (não B)", "Em A∩B", "Em B (não A)", "Nem A nem B"]
    vals = [nao_ab, ab, b_nao_a, nem]
    cors2 = ["#60a5fa","#8b5cf6","#34d399","#94a3b8"]
    for c, v, cor in zip(cats, vals, cors2):
        fig.add_trace(go.Bar(name=c, x=["Total"], y=[v],
            marker_color=cor, text=[f"{v}%"], textposition="inside"))
    fig.update_layout(barmode="stack", height=280,
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10,r=10,t=30,b=10),
        yaxis=dict(title="%", range=[0,100], gridcolor="#e2e8f0"),
        legend=dict(orientation="h", y=-.3))
    return fig

def fig_venn_cond(a, b, ab):
    fig = go.Figure()
    theta = np.linspace(0, 2*np.pi, 200)
    cx_a, cx_b = -1.0, 1.0
    for cx, label, cor in [(cx_a,"A","rgba(59,130,246,.35)"),
                            (cx_b,"B","rgba(16,185,129,.35)")]:
        fig.add_trace(go.Scatter(x=cx+1.5*np.cos(theta), y=1.5*np.sin(theta),
            fill="toself", fillcolor=cor, line=dict(color=cor.replace(".35","1").replace("rgba","rgb").split(",")[0]+")"),
            mode="lines", hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=[cx*1.8], y=[0], mode="text",
            text=[label], textfont=dict(size=22, color="#0f172a"),
            hoverinfo="skip", showlegend=False))
    for x, y, txt in [(cx_a-.6, 0, f"só A\n{a-ab}%"),
                       (0, 0, f"A∩B\n{ab}%"),
                       (cx_b+.6, 0, f"só B\n{b-ab}%"),
                       (0, -2.2, f"fora: {100-a-b+ab}%")]:
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="text",
            text=[txt], textfont=dict(size=13, color="#0f172a"),
            hoverinfo="skip", showlegend=False))
    fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(visible=False, range=[-4,4]),
        yaxis=dict(visible=False, range=[-3,3], scaleanchor="x", scaleratio=1),
        margin=dict(l=10,r=10,t=20,b=10), height=280)
    return fig

# ────────────────────────────────────────────
# ABA 6 — UNIÃO DE EVENTOS (Venn animado)
# ────────────────────────────────────────────
def fig_uniao_animado(pa, pb, pab):
    theta = np.linspace(0, 2*np.pi, 200)
    dist = 2.5 * (1 - pab / max(pa, pb, 0.01))
    dist = max(0.1, min(dist, 3.0))
    cx_a, cx_b = -dist/2, dist/2

    N_F = 20
    fases = np.linspace(0, 1, N_F)

    def cor_blend(base, alpha):
        r,g,b = int(base[1:3],16),int(base[3:5],16),int(base[5:7],16)
        return f"rgba({r},{g},{b},{alpha:.2f})"

    frames = []
    for alpha in fases:
        data = []
        for cx, label, hex_cor in [(cx_a,"A","#3b82f6"),(cx_b,"B","#10b981")]:
            data.append(go.Scatter(x=cx+1.5*np.cos(theta), y=1.5*np.sin(theta),
                fill="toself", fillcolor=cor_blend(hex_cor, alpha*.55),
                line=dict(color=hex_cor, width=2),
                mode="lines", hoverinfo="skip"))
        frames.append(go.Frame(data=data, name=str(round(alpha,2))))

    fig = go.Figure(data=frames[0].data, frames=frames)
    puniao = pa + pb - pab
    for x, y, txt, sz in [
        (cx_a-.5, 0, f"A\n{pa*100:.0f}%", 16),
        (cx_b+.5, 0, f"B\n{pb*100:.0f}%", 16),
        (0, 0,  f"A∩B\n{pab*100:.0f}%", 13),
        (0,-2.5, f"P(A∪B) = {pa:.2f}+{pb:.2f}−{pab:.2f} = {puniao:.3f}", 14),
    ]:
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="text",
            text=[txt], textfont=dict(size=sz, color="#0f172a"), hoverinfo="skip"))

    fig.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(visible=False, range=[-4.5,4.5]),
        yaxis=dict(visible=False, range=[-3.2,3.2], scaleanchor="x", scaleratio=1),
        margin=dict(l=10,r=10,t=40,b=10), height=340,
        updatemenus=[{"type":"buttons","showactive":False,"x":0,"y":1.15,
            "buttons":[
                {"label":"▶ Animar","method":"animate","args":[None,
                    {"frame":{"duration":120,"redraw":True},"fromcurrent":True,"mode":"immediate"}]},
                {"label":"❚❚ Pausar","method":"animate","args":[[None],
                    {"frame":{"duration":0},"mode":"immediate"}]}]}])
    return fig

# ────────────────────────────────────────────
# ABA 7 — TEORIA DOS JOGOS
# ────────────────────────────────────────────
PAYOFF_PRISIONEIRO = {
    ("Cooperar","Cooperar"):   (-1,-1),
    ("Cooperar","Trair"):      (-5, 0),
    ("Trair",   "Cooperar"):   ( 0,-5),
    ("Trair",   "Trair"):      (-3,-3),
}
PAYOFF_PPT = {
    ("Pedra","Pedra"):    (0,0),("Pedra","Papel"):   (-1,1),("Pedra","Tesoura"): (1,-1),
    ("Papel","Pedra"):    (1,-1),("Papel","Papel"):   (0,0),("Papel","Tesoura"): (-1,1),
    ("Tesoura","Pedra"):  (-1,1),("Tesoura","Papel"): (1,-1),("Tesoura","Tesoura"): (0,0),
}

def fig_matriz_jogo(payoff, jogadores=("Jogador A","Jogador B"), destaque=None):
    acoes_A = list(dict.fromkeys(k[0] for k in payoff))
    acoes_B = list(dict.fromkeys(k[1] for k in payoff))
    nA, nB = len(acoes_A), len(acoes_B)
    zA = [[payoff[(a,b)][0] for b in acoes_B] for a in acoes_A]
    zB = [[payoff[(a,b)][1] for b in acoes_B] for a in acoes_A]
    textos = [[f"({zA[i][j]}, {zB[i][j]})" for j in range(nB)] for i in range(nA)]

    cors = np.array(zA, dtype=float)
    fig = go.Figure(go.Heatmap(z=cors, x=acoes_B, y=acoes_A,
        text=textos, texttemplate="%{text}", textfont=dict(size=18),
        colorscale="RdYlGn", showscale=False,
        hovertemplate=f"{jogadores[0]}=%{{y}}<br>{jogadores[1]}=%{{x}}<br>Resultado=%{{text}}<extra></extra>"))

    if destaque:
        xa, yb = destaque
        fig.add_shape(type="rect",
            x0=acoes_B.index(yb)-.5, x1=acoes_B.index(yb)+.5,
            y0=acoes_A.index(xa)-.5, y1=acoes_A.index(xa)+.5,
            line=dict(color="#0f172a", width=4))

    fig.update_layout(
        xaxis=dict(title=jogadores[1], side="top"),
        yaxis=dict(title=jogadores[0], autorange="reversed"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10,r=10,t=60,b=10), height=300)
    return fig

def simular_iterado(n_rodadas, est_A, est_B, seed=42):
    rng = random.Random(seed)
    hist_A, hist_B, pts_A, pts_B = [], [], 0, 0
    ult_A, ult_B = "Cooperar", "Cooperar"

    def escolha(est, ult_proprio, ult_oponente):
        if est == "Sempre cooperar": return "Cooperar"
        if est == "Sempre trair":    return "Trair"
        if est == "Olho por olho":   return ult_oponente
        if est == "Aleatório":       return rng.choice(["Cooperar","Trair"])
        if est == "Olho por olho (generoso)":
            return "Cooperar" if ult_oponente=="Cooperar" or rng.random()<.1 else "Trair"
        return "Cooperar"

    for _ in range(n_rodadas):
        ca = escolha(est_A, ult_A, ult_B)
        cb = escolha(est_B, ult_B, ult_A)
        ga, gb = PAYOFF_PRISIONEIRO[(ca, cb)]
        pts_A += ga; pts_B += gb
        hist_A.append(ca); hist_B.append(cb)
        ult_A, ult_B = ca, cb
    return hist_A, hist_B, pts_A, pts_B

def fig_iterado(hist_A, hist_B, pts_A, pts_B, est_A, est_B):
    n = len(hist_A)
    x = list(range(1, n+1))
    ca = np.array([0 if h=="Cooperar" else 1 for h in hist_A])
    cb = np.array([0 if h=="Cooperar" else 1 for h in hist_B])
    cum_A = np.cumsum([PAYOFF_PRISIONEIRO[(a,b)][0] for a,b in zip(hist_A,hist_B)])
    cum_B = np.cumsum([PAYOFF_PRISIONEIRO[(a,b)][1] for a,b in zip(hist_A,hist_B)])

    fig = make_subplots(2, 1, subplot_titles=("Decisões por rodada","Pontuação acumulada (anos de cadeia)"),
        vertical_spacing=.18)
    fig.add_trace(go.Scatter(x=x, y=ca, mode="lines+markers",
        marker=dict(color=[CORES[0] if v==0 else CORES[1] for v in ca], size=8),
        line=dict(color="#94a3b8", width=1), name=est_A,
        hovertemplate="Rodada %{x}<br>"+est_A+"=%{customdata}<extra></extra>",
        customdata=hist_A), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=cb+1.5, mode="lines+markers",
        marker=dict(color=[CORES[0] if v==0 else CORES[1] for v in cb], size=8),
        line=dict(color="#e2e8f0", width=1), name=est_B,
        hovertemplate="Rodada %{x}<br>"+est_B+"=%{customdata}<extra></extra>",
        customdata=hist_B), 1, 1)
    fig.update_yaxes(tickvals=[0,1.5], ticktext=[est_A,est_B], row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=cum_A, mode="lines", line=dict(color=CORES[0],width=3), name=est_A), 2, 1)
    fig.add_trace(go.Scatter(x=x, y=cum_B, mode="lines", line=dict(color=CORES[1],width=3), name=est_B), 2, 1)
    fig.update_xaxes(title_text="Rodada", row=2, col=1)
    fig.update_yaxes(title_text="pontos (neg = menos cadeia)", row=2, col=1)
    fig.update_layout(showlegend=True, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10,r=10,t=70,b=10), height=480,
        legend=dict(orientation="h", y=-.12))
    return fig

def fig_nash_ppt():
    ps = np.linspace(0,1,50)
    qs = np.linspace(0,1,50)
    U = np.zeros((50,50))
    for i,p in enumerate(ps):
        for j,q in enumerate(qs):
            pA = np.array([p, (1-p)/2, (1-p)/2])
            pB = np.array([q, (1-q)/2, (1-q)/2])
            M = np.array([[PAYOFF_PPT[(a,b)][0] for b in ["Pedra","Papel","Tesoura"]]
                           for a in ["Pedra","Papel","Tesoura"]])
            U[i,j] = pA @ M @ pB

    fig = go.Figure(go.Heatmap(z=U, x=np.round(qs,2), y=np.round(ps,2),
        colorscale="RdBu", zmid=0, showscale=True,
        colorbar=dict(title="Utilidade A"),
        hovertemplate="P(Pedra)_A=%{y}<br>P(Pedra)_B=%{x}<br>U_A=%{z:.3f}<extra></extra>"))
    fig.add_scatter(x=[1/3], y=[1/3], mode="markers+text",
        text=["Nash (1/3,1/3)"], textposition="top right",
        marker=dict(size=14, color="#0f172a", symbol="star"),
        showlegend=False)
    fig.update_layout(xaxis_title="P(Pedra) — Jogador B",
        yaxis_title="P(Pedra) — Jogador A",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10,r=10,t=40,b=10), height=360,
        title="Utilidade esperada de A em estratégias mistas (Pedra-Papel-Tesoura)")
    return fig

# ────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configurações gerais")
    avancado = st.checkbox("Mostrar fórmulas matemáticas", value=True,
        help="Exibe as equações por trás de cada conceito.")
    st.markdown("---")
    st.subheader("🧑‍🏫 Roteiro sugerido")
    st.markdown("**1. Prever** – pergunte o que os alunos esperam ver.\n\n"
                "**2. Observar** – explore os controles e a animação.\n\n"
                "**3. Explicar** – relacione o resultado com a fórmula.\n\n"
                "Use as caixas *Teste sua intuição* para verificar o entendimento.")
    st.markdown("---")
    st.caption("Cada aba é independente; você pode usar só a parte que precisar na aula.")

# ────────────────────────────────────────────
# TÍTULO
# ────────────────────────────────────────────
st.markdown('<div class="main-title">🎲 Probabilidade Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dos fundamentos clássicos à estratégia: sete módulos didáticos interativos</div>',
    unsafe_allow_html=True)

tabs = st.tabs([
    "1. Fundamentos",
    "2. Árvore",
    "3. Eventos Sucessivos",
    "4. Complementar",
    "5. Condicional & Bayes",
    "6. União de Eventos",
    "7. Teoria dos Jogos",
])

# ══════════════════════════════════════════════════════════════
# ABA 1 — FUNDAMENTOS
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""<div class="card">
        <b>Probabilidade clássica:</b> quando todos os resultados têm a mesma chance,
        P(A) = (casos favoráveis) ÷ (casos possíveis).<br>
        <b>Lei dos Grandes Números:</b> à medida que o experimento é repetido muitas vezes,
        a frequência relativa converge para a probabilidade teórica.
    </div>""", unsafe_allow_html=True)
    with st.expander("💡 Analogia: a eleição na sala"):
        st.markdown("Imagine uma turma de 30 alunos. Se pedirmos a 3 deles suas opiniões, o resultado pode ser "
                    "muito diferente do da turma toda. Se perguntarmos a 28, ficará perto da realidade. "
                    "**A amostra grande converge para o resultado verdadeiro** — é exatamente o que a "
                    "Lei dos Grandes Números diz.")

    c1, c2 = st.columns([1, 2.5])
    with c1:
        with st.container(border=True):
            lados = st.slider("Lados do dado", 2, 12, 6, key="lados_f")
            n_sim = st.select_slider("Lançamentos simulados", [100,500,1000,5000,10000,50000], 1000, key="nsim_f")
            seed = st.number_input("Semente (reprodutibilidade)", 0, 9999, 42, key="seed_f")
            st.caption(f"P(qualquer face) = {frac_str(1,lados)} ≈ {1/lados:.4f}")
        if avancado:
            st.markdown('<div class="formula">P(A) = n(A) / n(Ω)</div>', unsafe_allow_html=True)
            st.caption("n(A) = casos favoráveis, n(Ω) = total de casos no espaço amostral Ω")
    with c2:
        mostrar(fig_fundamentos(lados, n_sim, int(seed)))

    if lados <= 6:
        st.markdown("#### 🗺️ Espaço amostral — dois dados")
        mostrar(fig_espaco_amostral(lados), 350)

    quiz("fund1",
         "Com um dado de 6 lados, qual é a probabilidade de sair um número par?",
         ["1/3","1/2","2/3","1/6"], 1,
         "Pares: {2,4,6} → 3 casos favoráveis de 6 → P = 3/6 = 1/2.")
    quiz("fund2",
         "Se um dado é lançado 6 vezes e sai 1 todas as vezes, a próxima jogada tem P(1) = ?",
         ["Maior que 1/6 (o dado está 'quente')",
          "1/6 — cada lançamento é independente",
          "Menor que 1/6 (está 'na hora' de outra face sair)"], 1,
         "Dado honesto: cada lançamento é independente. O dado não tem memória.")

# ══════════════════════════════════════════════════════════════
# ABA 2 — ÁRVORE DE PROBABILIDADES
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("""<div class="card">
        A <b>árvore de probabilidades</b> organiza experimentos compostos em etapas.
        Cada ramo representa um resultado possível, e a <b>probabilidade do caminho</b>
        é o produto das probabilidades de cada ramo percorrido.
    </div>""", unsafe_allow_html=True)
    with st.expander("💡 Analogia: o GPS das possibilidades"):
        st.markdown("A árvore é como um GPS que mostra **todos os caminhos possíveis** em uma viagem com várias "
                    "encruzilhadas. Em cada encruzilhada você escolhe uma direção (resultado), e a probabilidade "
                    "do caminho completo é o produto de todas as probabilidades nas encruzilhadas que você atravessou.")

    ct1, ct2 = st.columns([1, 2.8])
    with ct1:
        with st.container(border=True):
            cenario = st.selectbox("Cenário", [
                "Moeda (2 lançamentos)",
                "Moeda (3 lançamentos)",
                "Urna: 3 azuis, 2 vermelhas (com reposição)",
                "Urna: 3 azuis, 2 vermelhas (sem reposição)",
                "Dado par/ímpar → moeda",
                "Personalizado",
            ], key="cen_arv")

        if cenario == "Moeda (2 lançamentos)":
            etapas = [[("K",0.5),("C",0.5)],[("K",0.5),("C",0.5)]]
            desc = "K = Cara, C = Coroa"
        elif cenario == "Moeda (3 lançamentos)":
            etapas = [[("K",0.5),("C",0.5)],[("K",0.5),("C",0.5)],[("K",0.5),("C",0.5)]]
            desc = "K = Cara, C = Coroa"
        elif cenario == "Urna: 3 azuis, 2 vermelhas (com reposição)":
            etapas = [[("Azul",3/5),("Verm",2/5)],[("Azul",3/5),("Verm",2/5)]]
            desc = "Cada extração tem as mesmas probabilidades (bola devolvida)"
        elif cenario == "Urna: 3 azuis, 2 vermelhas (sem reposição)":
            etapas = [[("Azul",3/5),("Verm",2/5)],
                      [("Azul",2/4),("Verm",2/4)]]
            desc = "Sem reposição: após tirar uma azul, restam 2 azuis e 2 vermelhas de 4"
        elif cenario == "Dado par/ímpar → moeda":
            etapas = [[("Par",0.5),("Ímpar",0.5)],[("K",0.5),("C",0.5)]]
            desc = "Primeiro: dado (par ou ímpar). Depois: moeda."
        else:
            st.markdown("**Etapa 1**")
            n1 = st.slider("Nº de ramos na etapa 1", 2, 4, 2, key="n1_p")
            ramos1 = []
            tot = 0.0
            for i in range(n1):
                lb = st.text_input(f"Label {i+1}", value=chr(65+i), key=f"lb1_{i}")
                p = st.slider(f"P({lb})", 0.01, 1.0-tot, round(1/n1,2), key=f"p1_{i}")
                ramos1.append((lb, p)); tot += p
            etapas = [ramos1]
            if st.checkbox("Adicionar etapa 2", key="et2_p"):
                st.markdown("**Etapa 2** (igual para todos os nós)")
                n2 = st.slider("Nº de ramos na etapa 2", 2, 3, 2, key="n2_p")
                ramos2 = []
                tot2 = 0.0
                for i in range(n2):
                    lb = st.text_input(f"Label 2-{i+1}", value=chr(88+i), key=f"lb2_{i}")
                    p = st.slider(f"P({lb})", 0.01, 1.0-tot2, round(1/n2,2), key=f"p2_{i}")
                    ramos2.append((lb, p)); tot2 += p
                etapas.append(ramos2)
            desc = "Cenário personalizado"

        st.caption(desc)

    with ct2:
        nodes, edges = construir_arvore(etapas)
        st.markdown("#### 🌳 Árvore completa")
        mostrar(fig_arvore(nodes, edges), 380)

        st.markdown("#### 🔎 Qual caminho me interessa?")
        folhas_reais = [n for n in nodes if n["nivel"] == len(etapas)]
        if folhas_reais:
            opcoes = [n["label"] + f"  (P = {n['prob']:.4f})" for n in folhas_reais]
            sel = st.selectbox("Selecione um resultado final:", opcoes, key="sel_folha")
            idx_sel = opcoes.index(sel)
            folha_id = folhas_reais[idx_sel]["id"]
            caminho = set()
            nid = folha_id
            caminho.add(nid)
            for _ in range(10):
                pais = [e[0] for e in edges if e[1] == nid]
                if not pais: break
                nid = pais[0]; caminho.add(nid)
            mostrar(fig_arvore(nodes, edges, destacar=caminho), 380)
            st.success(f"Probabilidade desse caminho: **{folhas_reais[idx_sel]['prob']:.6f}** "
                       f"≈ {folhas_reais[idx_sel]['prob']*100:.2f}%")

    quiz("arv1",
         "Na árvore de uma moeda lançada 2 vezes, qual é P(KK)?",
         ["1/4","1/2","1/8","3/4"], 0,
         "P(K)·P(K) = 1/2 · 1/2 = 1/4. Multiplicamos as probabilidades dos ramos do caminho.")

# ══════════════════════════════════════════════════════════════
# ABA 3 — EVENTOS SUCESSIVOS
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""<div class="card">
        <b>Eventos sucessivos independentes:</b> a probabilidade de uma sequência de eventos
        independentes ocorrer é o <b>produto</b> das probabilidades individuais.<br>
        <b>Eventos dependentes:</b> a segunda probabilidade muda conforme o resultado do primeiro
        (sem reposição, por exemplo).
    </div>""", unsafe_allow_html=True)
    if avancado:
        st.markdown('<div class="formula">P(A₁ ∩ A₂ ∩ … ∩ Aₙ) = P(A₁) · P(A₂) · … · P(Aₙ)    (independentes)</div>',
                    unsafe_allow_html=True)

    with st.expander("💡 Analogia: senha de cofre"):
        st.markdown("Cada dígito de uma senha de 4 algarismos (0–9) é escolhido independentemente. "
                    "P(acertar 1 dígito) = 1/10. P(acertar todos os 4) = (1/10)⁴ = 1/10 000. "
                    "**Eventos independentes multiplicam** — por isso senhas longas são tão seguras!")

    ce1, ce2 = st.columns([1, 2.5])
    with ce1:
        with st.container(border=True):
            tipo_ev = st.radio("Tipo de experimento", ["Moeda","Dado","Urna personalizada","Senha numérica"], key="tipo_suc")
            if tipo_ev == "Moeda":
                n_ev = st.slider("Quantos lançamentos?", 1, 10, 3, key="nev_moeda")
                p_unit = 0.5
                eventos = [("Cara", 0.5)] * n_ev
                prob_seq = 0.5 ** n_ev
                desc_ev = f"P(tudo cara em {n_ev} lançamentos)"
            elif tipo_ev == "Dado":
                lados_ev = st.slider("Lados do dado", 2, 12, 6, key="lados_ev")
                face_ev = st.slider("Face de interesse", 1, lados_ev, 6, key="face_ev")
                n_ev = st.slider("Quantos lançamentos?", 1, 8, 3, key="nev_dado")
                p_unit = 1/lados_ev
                eventos = [(f"Face {face_ev}", p_unit)] * n_ev
                prob_seq = p_unit ** n_ev
                desc_ev = f"P(face {face_ev} em todos os {n_ev} lançamentos)"
            elif tipo_ev == "Urna personalizada":
                n_azuis = st.slider("Bolas azuis", 1, 10, 3, key="naz_ev")
                n_verm  = st.slider("Bolas vermelhas", 1, 10, 2, key="nverm_ev")
                reposicao = st.checkbox("Com reposição", True, key="rep_ev")
                n_ev = st.slider("Extrações", 1, min(5, n_azuis+n_verm), 2, key="nev_urna")
                total = n_azuis + n_verm
                eventos = []
                prob_seq = 1.0
                az_rest, tot_rest = n_azuis, total
                for k in range(n_ev):
                    p = az_rest / tot_rest
                    eventos.append((f"Azul({k+1})", p))
                    prob_seq *= p
                    if not reposicao:
                        az_rest = max(az_rest - 1, 0)
                        tot_rest -= 1
                desc_ev = f"P({n_ev} azuis consecutivas)"
            else:
                n_dig = st.slider("Dígitos da senha", 1, 8, 4, key="ndig_ev")
                base = st.slider("Base (0 a N-1)", 2, 16, 10, key="base_ev")
                n_ev = n_dig
                p_unit = 1/base
                eventos = [(f"Dígito {k+1}", p_unit) for k in range(n_dig)]
                prob_seq = p_unit ** n_dig
                desc_ev = f"P(acertar todos os {n_dig} dígitos)"

    with ce2:
        etapas_suc = [[ev] for ev in eventos[:4]]
        if len(etapas_suc) > 0:
            nodes_s, edges_s = construir_arvore(etapas_suc)
            folha_dest = {n["id"] for n in nodes_s if n["nivel"] == len(etapas_suc)}
            caminho_d = set(folha_dest)
            nid = list(folha_dest)[0] if folha_dest else None
            if nid:
                while True:
                    pais = [e[0] for e in edges_s if e[1]==nid]
                    if not pais: break
                    nid = pais[0]; caminho_d.add(nid)
            st.markdown("#### Caminho da sequência desejada (até 4 etapas)")
            mostrar(fig_arvore(nodes_s, edges_s, destacar=caminho_d), 320)

        st.markdown("#### 📐 Cálculo passo a passo")
        passos = []
        prod = 1.0
        for k, (lbl, p) in enumerate(eventos):
            prod *= p
            passos.append({"Etapa": k+1, "Evento": lbl, "P individual": f"{p:.6f}",
                           "Produto acumulado": f"{prod:.8f}"})
        st.dataframe(pd.DataFrame(passos), use_container_width=True, hide_index=True)
        st.info(f"**{desc_ev} = {prob_seq:.8f}** = {prob_seq*100:.4f}%  "
                f"→ em média 1 vez a cada **{1/prob_seq:,.0f}** tentativas".replace(",","."))

    quiz("suc1",
         "P(tirar cara 5 vezes seguidas com moeda honesta) = ?",
         ["1/10","1/25","1/32","1/16"], 2,
         "(1/2)⁵ = 1/32 ≈ 3,1%. Cada lançamento é independente; multiplicamos.")
    quiz("suc2",
         "Numa urna com 5 bolas (3 azuis, 2 vermelhas), sem reposição, P(2 azuis seguidas) = ?",
         ["9/25","3/10","6/20","9/20"], 1,
         "P(1ª azul) = 3/5. Após retirar 1 azul, restam 2 de 4: P(2ª azul) = 2/4 = 1/2. Produto: 3/5 · 1/2 = 3/10.")

# ══════════════════════════════════════════════════════════════
# ABA 4 — COMPLEMENTAR
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("""<div class="card">
        O <b>evento complementar</b> A' (lê-se "A complemento") é tudo o que <i>não</i> é A.
        Como A e A' cobrem todos os casos possíveis, P(A) + P(A') = 1.<br>
        <b>Estratégia do complementar:</b> calcular P(A') diretamente é muitas vezes <i>muito mais fácil</i>
        do que somar todas as formas de A acontecer.
    </div>""", unsafe_allow_html=True)
    if avancado:
        st.markdown('<div class="formula">P(A\') = 1 − P(A) &nbsp;⟹&nbsp; P(A) = 1 − P(A\')</div>',
                    unsafe_allow_html=True)

    with st.expander("💡 Analogia: a chance de NÃO ganhar na loteria"):
        st.markdown("É muito difícil listar **todas** as formas de ganhar (são poucas combinações vencedoras). "
                    "Mas é trivial saber que P(não ganhar) = 1 − P(ganhar). "
                    "**O complementar transforma um problema difícil num fácil.**")

    cc1, cc2 = st.columns([1, 2.5])
    with cc1:
        with st.container(border=True):
            st.markdown("**Paradoxo do Aniversário**")
            st.markdown("Qual é a probabilidade de que **ao menos duas pessoas** numa sala tenham o mesmo aniversário?")
            n_pessoas = st.slider("Pessoas na sala", 2, 70, 23, key="np_aniv")
            p_todos_dif = 1.0
            for k in range(n_pessoas):
                p_todos_dif *= (365 - k) / 365
            p_coincide = 1 - p_todos_dif
            st.metric("P(ao menos 2 mesmos aniversários)", f"{p_coincide*100:.1f}%")
            st.metric("P(todos diferentes) [complementar]", f"{p_todos_dif*100:.1f}%")

        with st.container(border=True):
            st.markdown("**Exemplo livre**")
            p_a = st.slider("P(A)", 0.01, 0.99, 0.30, 0.01, key="pa_comp")
            st.metric("P(A')", f"{1-p_a:.2f}")
            n_tent = st.slider("Tentativas independentes", 1, 20, 5, key="nt_comp")
            p_nenhuma = (1-p_a)**n_tent
            p_ao_menos = 1 - p_nenhuma
            st.metric(f"P(A ocorre ao menos 1x em {n_tent} tentativas)", f"{p_ao_menos*100:.2f}%")
            st.caption(f"Pela estratégia do complementar: 1 − P(A nunca ocorre) = 1 − {1-p_a:.2f}^{n_tent} = {p_ao_menos:.4f}")

    with cc2:
        ns = list(range(2, 71))
        probs = []
        p = 1.0
        for k in range(70):
            if k < 2:
                probs.append(0.0) if k==0 else probs.append(1-p)
            else:
                p *= (365 - k) / 365
                probs.append(1 - p)

        fig_aniv = go.Figure()
        fig_aniv.add_trace(go.Scatter(x=ns, y=[probs[n-2]*100 for n in ns],
            mode="lines+markers", line=dict(color="#3b82f6", width=3),
            marker=dict(size=5), name="P(coincidência)",
            hovertemplate="n=%{x} pessoas<br>P=%{y:.1f}%<extra></extra>"))
        fig_aniv.add_hline(y=50, line=dict(color="#ef4444", dash="dash"),
                           annotation_text="50%", annotation_position="right")
        fig_aniv.add_vline(x=23, line=dict(color="#f59e0b", dash="dot"),
                           annotation_text="n=23", annotation_position="top right")
        fig_aniv.add_vline(x=n_pessoas, line=dict(color="#0f172a", width=2),
                           annotation_text=f"n={n_pessoas}", annotation_position="top left")
        fig_aniv.update_layout(title="Paradoxo do Aniversário", xaxis_title="pessoas na sala",
            yaxis_title="P(ao menos 2 mesmos aniversários) %",
            plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=10,t=60,b=10))
        mostrar(fig_aniv, 340)

        fig_pie = go.Figure(go.Pie(labels=["P(A)","P(A')"],
            values=[p_a, 1-p_a],
            marker=dict(colors=["#3b82f6","#e2e8f0"]),
            textinfo="label+percent", hole=.5))
        fig_pie.update_layout(title="Evento A e seu complemento",
            margin=dict(l=10,r=10,t=60,b=10), paper_bgcolor="white")
        mostrar(fig_pie, 280)

    quiz("comp1",
         "Numa turma de 23 pessoas, a probabilidade de ao menos dois fazerem aniversário no mesmo dia é:",
         ["Menor que 10%","Perto de 50%","Maior que 90%","Exatamente 23/365"], 1,
         "É ~50,7%! Parece pouco, mas há 253 pares possíveis, cada um com chance de coincidir.")
    quiz("comp2",
         "P(sair ao menos um 6 em 4 lançamentos de dado) é mais fácil calcular como:",
         ["Somar as probabilidades de sair 6 em cada lançamento",
          "1 − P(não sair nenhum 6)",
          "4 × 1/6"], 1,
         "1 − (5/6)⁴ ≈ 51,8%. O complementar evita contar sobreposições.")

# ══════════════════════════════════════════════════════════════
# ABA 5 — CONDICIONAL & BAYES
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""<div class="card">
        <b>Probabilidade condicional P(A|B):</b> a probabilidade de A ocorrer,
        <i>sabendo que B já ocorreu</i>. Restringimos o espaço amostral a B.<br>
        <b>Teorema de Bayes:</b> permite <i>inverter</i> a condicional —
        calcular P(causa | efeito) a partir de P(efeito | causa).
    </div>""", unsafe_allow_html=True)
    if avancado:
        st.markdown("""<div class="formula">
        P(A|B) = P(A∩B) / P(B) &nbsp;&nbsp;&nbsp;
        P(A|B) = P(B|A)·P(A) / P(B)  <span style="color:#64748b">(Bayes)</span>
        </div>""", unsafe_allow_html=True)

    with st.expander("💡 Analogia: resultado de exame médico"):
        st.markdown("Uma doença afeta 1% da população. Um teste é 95% preciso (positivo em doentes) "
                    "e tem 5% de falso-positivo. Se você testar positivo, qual a chance de estar doente? "
                    "**Resposta intuitiva: 95%. Resposta real (Bayes): ~16%.** "
                    "A prevalência baixa da doença é crucial e Bayes captura isso.")

    cb1, cb2 = st.columns([1, 2.5])
    with cb1:
        with st.container(border=True):
            st.markdown("**Tabela de contingência interativa**")
            st.markdown("Defina as porcentagens da população (total = 100%)")
            pa_c = st.slider("P(A) — % da população em A", 5, 90, 40, key="pa_c")
            pb_c = st.slider("P(B) — % da população em B", 5, 90, 50, key="pb_c")
            max_ab = min(pa_c, pb_c)
            pab_c = st.slider("P(A∩B) — % em ambos", 0, max_ab, min(20, max_ab), key="pab_c")
            if pa_c + pb_c - pab_c > 100:
                st.error("Configuração impossível: P(A∪B) > 100%. Reduza P(A) ou P(B).")
            else:
                p_a_dado_b = pab_c / pb_c if pb_c > 0 else 0
                p_b_dado_a = pab_c / pa_c if pa_c > 0 else 0
                st.metric("P(A|B)", f"{p_a_dado_b*100:.1f}%",
                    help="Prob. de estar em A, dado que estamos em B")
                st.metric("P(B|A)", f"{p_b_dado_a*100:.1f}%",
                    help="Prob. de estar em B, dado que estamos em A")

        with st.container(border=True):
            st.markdown("**Simulação de Bayes: teste diagnóstico**")
            prev = st.slider("Prevalência da doença (%)", 1, 50, 5, key="prev_b") / 100
            sens = st.slider("Sensibilidade (P(+|doente) %)", 50, 100, 95, key="sens_b") / 100
            espec = st.slider("Especificidade (P(−|saudável) %)", 50, 100, 95, key="espec_b") / 100
            p_pos = sens*prev + (1-espec)*(1-prev)
            p_doente_pos = sens*prev / p_pos if p_pos>0 else 0
            st.metric("P(doente | teste +)", f"{p_doente_pos*100:.1f}%")
            st.caption("Mesmo com teste 95% preciso, a prevalência baixa domina o resultado.")

    with cb2:
        if pa_c + pb_c - pab_c <= 100:
            mostrar(fig_venn_cond(pa_c, pb_c, pab_c), 280)
            mostrar(fig_contingencia(pa_c, pb_c, pab_c), 260)

        prevs = np.linspace(0.01, 0.5, 100)
        vpp = sens * prevs / (sens*prevs + (1-espec)*(1-prevs))
        fig_vpp = go.Figure()
        fig_vpp.add_trace(go.Scatter(x=prevs*100, y=vpp*100, mode="lines",
            line=dict(color="#8b5cf6", width=3),
            hovertemplate="Prevalência=%{x:.1f}%<br>P(doente|+)=%{y:.1f}%<extra></extra>"))
        fig_vpp.add_vline(x=prev*100, line=dict(color="#0f172a", dash="dot", width=2),
                          annotation_text=f"{prev*100:.0f}%")
        fig_vpp.add_scatter(x=[prev*100], y=[p_doente_pos*100], mode="markers",
            marker=dict(size=14, color="#ef4444", line=dict(color="white", width=2)), showlegend=False)
        fig_vpp.update_layout(title="Valor preditivo positivo × prevalência (Bayes)",
            xaxis_title="Prevalência (%)", yaxis_title="P(doente | teste positivo) %",
            plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=10,t=60,b=10))
        mostrar(fig_vpp, 280)

    quiz("cond1",
         "P(A|B) = P(A) sempre que:",
         ["A e B são mutuamente exclusivos","A e B são independentes","A está contido em B"], 1,
         "Independência significa que saber B não muda a probabilidade de A: P(A|B) = P(A).")
    quiz("cond2",
         "Num baralho de 52 cartas, P(Ás | carta de espadas) = ?",
         ["1/52","1/13","1/4","4/13"], 1,
         "Há 13 espadas. Delas, 1 é ás. P = 1/13.")

# ══════════════════════════════════════════════════════════════
# ABA 6 — UNIÃO DE EVENTOS
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("""<div class="card">
        P(A∪B) é a probabilidade de <b>A ou B</b> (ou ambos) ocorrerem.
        A fórmula subtrai P(A∩B) para não contar duas vezes o que está em ambos.<br>
        Eventos <b>mutuamente exclusivos</b>: não podem ocorrer juntos → P(A∩B)=0 → P(A∪B) = P(A)+P(B).
    </div>""", unsafe_allow_html=True)
    if avancado:
        st.markdown("""<div class="formula">
        P(A∪B) = P(A) + P(B) − P(A∩B)
        </div>""", unsafe_allow_html=True)

    with st.expander("💡 Analogia: contar alunos em clubes"):
        st.markdown("Numa escola, 30 alunos estão no clube de Xadrez, 20 no de Robótica, e 10 estão nos dois. "
                    "Quantos estão em **ao menos um** clube? Não é 50 — senão contaríamos os 10 duas vezes. "
                    "Correto: 30 + 20 − 10 = **40**. É exatamente P(A∪B) = P(A)+P(B)−P(A∩B).")

    cu1, cu2 = st.columns([1, 2.5])
    with cu1:
        with st.container(border=True):
            pa_u = st.slider("P(A)", 0.05, 0.95, 0.50, 0.05, key="pa_u")
            pb_u = st.slider("P(B)", 0.05, 0.95, 0.40, 0.05, key="pb_u")
            max_pab = min(pa_u, pb_u)
            pab_u = st.slider("P(A∩B)", 0.0, max_pab, min(0.20, max_pab), 0.05, key="pab_u")
            excl = st.checkbox("Forçar mutuamente exclusivos (P(A∩B)=0)", key="excl_u")
            if excl:
                pab_u = 0.0
            puniao = pa_u + pb_u - pab_u
            if puniao > 1:
                st.error("P(A∪B) > 1: combinação impossível.")
            else:
                st.metric("P(A∪B)", f"{puniao:.3f}")
                st.metric("P(nenhum)", f"{1-puniao:.3f}")
                if pab_u == 0:
                    st.info("Mutuamente exclusivos: A e B não podem ocorrer juntos.")

        st.markdown("**Decomposição:**")
        st.dataframe({
            "Região": ["Só A","Só B","A∩B","Nenhum"],
            "Probabilidade": [f"{pa_u-pab_u:.3f}",f"{pb_u-pab_u:.3f}",f"{pab_u:.3f}",f"{1-puniao:.3f}"]
        }, hide_index=True, use_container_width=True)

    with cu2:
        mostrar(fig_uniao_animado(pa_u, pb_u, pab_u), 340)

        st.markdown("#### 🔢 Generalização: 3 eventos")
        st.latex(r"P(A\cup B\cup C) = P(A)+P(B)+P(C)-P(A\cap B)-P(A\cap C)-P(B\cap C)+P(A\cap B\cap C)")
        pc_u = st.slider("P(C)", 0.05, 0.80, 0.30, 0.05, key="pc_u")
        pabc = st.slider("P(A∩B∩C)", 0.0, min(pab_u, pc_u), min(0.05, pab_u, pc_u), 0.01, key="pabc_u")
        pac = st.slider("P(A∩C)", 0.0, min(pa_u,pc_u), min(0.10, pa_u, pc_u), 0.05, key="pac_u")
        pbc = st.slider("P(B∩C)", 0.0, min(pb_u,pc_u), min(0.10, pb_u, pc_u), 0.05, key="pbc_u")
        p3 = pa_u+pb_u+pc_u - pab_u-pac-pbc + pabc
        if 0 <= p3 <= 1:
            st.success(f"P(A∪B∪C) = **{p3:.4f}**")
        else:
            st.warning(f"Configuração gera P(A∪B∪C) = {p3:.4f} — ajuste os controles.")

    quiz("uni1",
         "A e B são mutuamente exclusivos com P(A)=0,3 e P(B)=0,5. P(A∪B) = ?",
         ["0,15","0,65","0,80","0,85"], 2,
         "Exclusivos → P(A∩B)=0 → P(A∪B)=0,3+0,5=0,8.")
    quiz("uni2",
         "P(A)=0,6, P(B)=0,5, P(A∩B)=0,3. P(A∪B) = ?",
         ["1,10","0,80","0,60","0,90"], 1,
         "P(A∪B)=0,6+0,5−0,3=0,8.")

# ══════════════════════════════════════════════════════════════
# ABA 7 — TEORIA DOS JOGOS
# ══════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("""<div class="card">
        A <b>Teoria dos Jogos</b> estuda decisões estratégicas entre agentes racionais.
        Um <b>Equilíbrio de Nash</b> é uma combinação de estratégias em que nenhum jogador
        melhora mudando sozinho de escolha — dado o que o outro faz.<br>
        Conecta-se à probabilidade porque jogadores às vezes usam <b>estratégias mistas</b>
        (escolhas aleatórias com probabilidades ótimas).
    </div>""", unsafe_allow_html=True)

    with st.expander("💡 Analogia: pedra-papel-tesoura"):
        st.markdown("Se você sempre jogar Pedra, seu oponente aprenderá e sempre jogará Papel. "
                    "A única estratégia que não pode ser explorada é jogar **aleatoriamente com p=1/3 para cada opção** — "
                    "o Equilíbrio de Nash em estratégias mistas.")

    tj1, tj2 = st.tabs(["🔒 Dilema do Prisioneiro", "✂️ Pedra-Papel-Tesoura"])

    with tj1:
        st.markdown("""<div class="warn">
            <b>Contexto:</b> dois suspeitos são interrogados separadamente. Cada um pode <b>Cooperar</b>
            (ficar calado) ou <b>Trair</b> (delatar o outro). Os anos de cadeia dependem das escolhas <i>combinadas</i>.
            </div>""", unsafe_allow_html=True)

        dp1, dp2 = st.columns([1, 2.2])
        with dp1:
            with st.container(border=True):
                st.markdown("#### 🎮 Jogue uma rodada")
                esc_A = st.radio("Escolha do Suspeito A", ["Cooperar","Trair"], key="esca_d")
                esc_B = st.radio("Escolha do Suspeito B", ["Cooperar","Trair"], key="escb_d")
                ga, gb = PAYOFF_PRISIONEIRO[(esc_A, esc_B)]
                st.markdown(f"**Resultado:** A recebe **{ga} ano(s)**, B recebe **{gb} ano(s)**")
                st.caption("(negativo = anos de prisão — quanto menor, pior)")

            with st.container(border=True):
                st.markdown("#### 🔁 Dilema iterado")
                est_A_it = st.selectbox("Estratégia do Suspeito A", ["Sempre cooperar","Sempre trair","Olho por olho","Aleatório","Olho por olho (generoso)"], key="esta_it")
                est_B_it = st.selectbox("Estratégia do Suspeito B", ["Sempre cooperar","Sempre trair","Olho por olho","Aleatório","Olho por olho (generoso)"], index=2, key="estb_it")
                n_rod = st.slider("Rodadas", 10, 200, 50, key="nrod_it")

        with dp2:
            mostrar(fig_matriz_jogo(PAYOFF_PRISIONEIRO,
                                    ("Suspeito A","Suspeito B"),
                                    destaque=(esc_A, esc_B)), 300)
            st.markdown("""
            **Leitura:** linha = escolha de A, coluna = escolha de B. Valor = (anos A, anos B).
            🟩 = melhor resultado individual · 🟥 = pior.

            **Por que Trair é sempre tentador?** Qualquer que seja a escolha de B,
            trair dá um resultado melhor *para A individualmente* — mas se ambos trairem, ambos ficam em (-3,-3),
            pior do que cooperar mutuamente (-1,-1). Isso é a **tragédia dos comuns**.
            """)

        hist_A, hist_B, pts_A, pts_B = simular_iterado(n_rod, est_A_it, est_B_it)
        m1,m2,m3 = st.columns(3)
        m1.metric(f"Pontos A ({est_A_it})", str(pts_A))
        m2.metric(f"Pontos B ({est_B_it})", str(pts_B))
        m3.metric("Cooperação de A", f"{hist_A.count('Cooperar')/n_rod*100:.0f}%")
        mostrar(fig_iterado(hist_A, hist_B, pts_A, pts_B, est_A_it, est_B_it))

        st.markdown("#### 🏆 Resultado do torneio de estratégias")
        est_todas = ["Sempre cooperar","Sempre trair","Olho por olho","Aleatório","Olho por olho (generoso)"]
        placar = {e: 0 for e in est_todas}
        for eA, eB in itertools.combinations(est_todas, 2):
            _, _, pA, pB = simular_iterado(100, eA, eB, seed=1)
            placar[eA] += pA; placar[eB] += pB
        fig_rank = go.Figure(go.Bar(
            x=list(placar.keys()), y=list(placar.values()),
            marker_color=[CORES[i] for i in range(len(placar))],
            text=[str(v) for v in placar.values()], textposition="outside"))
        fig_rank.update_layout(title="Pontuação total (100 rodadas vs cada oponente — menor = melhor)",
            yaxis_title="anos de cadeia (total)", plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10,r=10,t=60,b=10))
        mostrar(fig_rank, 300)

        quiz("tg1",
             "No Dilema do Prisioneiro de rodada única, o Equilíbrio de Nash é:",
             ["Ambos cooperam","Ambos traem","Um trai e o outro coopera","Depende da personalidade"], 1,
             "Trair é a estratégia dominante: independente do outro, trair é sempre melhor individualmente. Nash: ambos traem.")
        quiz("tg2",
             "No dilema iterado, a estratégia 'Olho por olho' tende a ir bem porque:",
             ["Nunca trai, então nunca é punido",
              "Incentiva cooperação e pune a traição imediatamente",
              "Aleatória é sempre eficiente"], 1,
             "Simples, clara e recíproca: coopera enquanto o outro coopera, mas responde com traição na mesma hora.")

    with tj2:
        st.markdown("""<div class="card">
            Pedra-Papel-Tesoura é um <b>jogo de soma zero</b>: o ganho de A é exatamente a perda de B.
            Não existe Equilíbrio de Nash em estratégias puras (sempre haverá uma resposta melhor).
            O equilíbrio em <b>estratégias mistas</b> é jogar cada opção com probabilidade <b>1/3</b>.
        </div>""", unsafe_allow_html=True)

        pp1, pp2 = st.columns([1, 2.2])
        with pp1:
            with st.container(border=True):
                st.markdown("#### 🎮 Jogue contra o computador")
                p_ped = st.slider("P(Pedra) — Jogador A", 0.0, 1.0, 1/3, 0.05, key="p_ped")
                p_pap = st.slider("P(Papel) — Jogador A", 0.0, 1-p_ped, (1-p_ped)/2, 0.05, key="p_pap")
                p_tes = 1 - p_ped - p_pap
                st.caption(f"P(Tesoura) = {p_tes:.2f}")
                q_ped = st.slider("P(Pedra) — Jogador B", 0.0, 1.0, 1/3, 0.05, key="q_ped")
                q_pap = st.slider("P(Papel) — Jogador B", 0.0, 1-q_ped, (1-q_ped)/2, 0.05, key="q_pap")
                q_tes = 1 - q_ped - q_pap
                st.caption(f"P(Tesoura) = {q_tes:.2f}")
                pA = np.array([p_ped, p_pap, p_tes])
                pB = np.array([q_ped, q_pap, q_tes])
                M = np.array([[PAYOFF_PPT[(a,b)][0] for b in ["Pedra","Papel","Tesoura"]]
                               for a in ["Pedra","Papel","Tesoura"]])
                u_A = float(pA @ M @ pB)
                u_B = -u_A
                st.metric("Utilidade esperada A", f"{u_A:+.4f}")
                st.metric("Utilidade esperada B", f"{u_B:+.4f}")
                if abs(p_ped-1/3)<.03 and abs(p_pap-1/3)<.03 and abs(q_ped-1/3)<.03 and abs(q_pap-1/3)<.03:
                    st.success("✅ Ambos no Equilíbrio de Nash! U_A = U_B = 0.")
                elif abs(u_A) < 0.01:
                    st.info("A estratégia de A é ótima contra B (U_A ≈ 0).")
                else:
                    venc = "A" if u_A > 0 else "B"
                    st.warning(f"Jogador {venc} tem vantagem. Alguém pode melhorar mudando sua estratégia.")

        with pp2:
            mostrar(fig_matriz_jogo(PAYOFF_PPT, ("Jogador A","Jogador B")), 300)
            mostrar(fig_nash_ppt(), 360)

        quiz("ppt1",
             "No Pedra-Papel-Tesoura, jogar sempre Pedra é uma boa estratégia contra um adversário racional porque:",
             ["Pedra é a opção mais forte","Não é boa — o adversário aprenderá e sempre jogará Papel",
              "Depende do número de rodadas"], 1,
             "Estratégias puras (fixas) sempre têm uma resposta ótima do oponente. O equilíbrio exige mistura 1/3-1/3-1/3.")

# RODAPÉ
st.markdown("---")
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:.85rem;padding:1rem;">'
    '🎲 <b>Probabilidade Visual</b> — fundamentos clássicos · árvores · eventos · Bayes · Teoria dos Jogos</div>',
    unsafe_allow_html=True)
