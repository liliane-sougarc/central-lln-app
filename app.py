
import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Central de Projetos LLN", layout="wide")
st.title("🧠 Central LLN – Painel de Controle de Projetos")

st.markdown("""
**Criado por:** Liliane de Souza Garcia  
**Marca:** LLN Automações  
**Missão:** Automatizar, organizar e potencializar ideias com dados, propósito e inteligência.

---
""")

# Inicializar sessão
if "projetos" not in st.session_state:
    st.session_state.projetos = {
        "Radar Climático – LLN": "Ativo",
        "CRM de Bolso": "Ativo",
        "UTM Link Builder": "Ativo",
        "Tendda101": "Ativo",
        "Blog “E se eu te contar...”": "Ativo",
        "LLN Automações": "Ativo"
    }
if "tempos" not in st.session_state:
    st.session_state.tempos = {}

# Gerenciamento de projetos
st.sidebar.subheader("📋 Gerenciar Projetos")
novo_projeto = st.sidebar.text_input("Adicionar novo projeto")
status_novo = st.sidebar.selectbox("Status", ["Ativo", "Hibernando", "Em Espera", "Arquivado"], key="novo_status")
if st.sidebar.button("➕ Adicionar") and novo_projeto:
    st.session_state.projetos[novo_projeto] = status_novo
    st.success(f"Projeto '{novo_projeto}' adicionado com status '{status_novo}'.")

# Filtro de visualização
visualizar_todos = st.sidebar.checkbox("👁️ Ver todos os projetos", value=False)

# Atualizar status
st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Editar Status de Projeto")
projeto_editar = st.sidebar.selectbox("Escolha o projeto", list(st.session_state.projetos.keys()))
novo_status = st.sidebar.selectbox("Novo status", ["Ativo", "Hibernando", "Em Espera", "Arquivado"], key="status_edicao")
if st.sidebar.button("💾 Atualizar Status"):
    st.session_state.projetos[projeto_editar] = novo_status
    st.success(f"Status do projeto '{projeto_editar}' atualizado para '{novo_status}'.")

# Filtrar projetos para exibição
projetos_visiveis = [p for p, s in st.session_state.projetos.items() if visualizar_todos or s == "Ativo"]

# Menu lateral principal
projeto = st.sidebar.selectbox("📌 Selecione o projeto:", projetos_visiveis)
status_atual = st.session_state.projetos.get(projeto, "Ativo")

# Relógio-ponto
st.sidebar.markdown("---")
st.sidebar.subheader("⏱️ Relógio-Ponto")
if f"inicio_{projeto}" not in st.session_state:
    st.session_state[f"inicio_{projeto}"] = None

if st.sidebar.button("Iniciar Sessão"):
    st.session_state[f"inicio_{projeto}"] = time.time()
    st.success(f"Sessão iniciada para {projeto} em {datetime.now().strftime('%H:%M:%S')}")

if st.sidebar.button("Encerrar Sessão") and st.session_state[f"inicio_{projeto}"]:
    fim = time.time()
    duracao = round((fim - st.session_state[f"inicio_{projeto}"]) / 60, 2)
    st.session_state.tempos.setdefault(projeto, []).append(duracao)
    st.session_state[f"inicio_{projeto}"] = None
    st.success(f"Sessão encerrada! Tempo registrado: {duracao} min")

total = sum(st.session_state.tempos.get(projeto, []))
st.sidebar.markdown(f"**⏳ Tempo acumulado hoje:** {total:.2f} min")

# Conteúdo principal
tarefas_padrao = [
    "Planejar próximos passos",
    "Atualizar documentação",
    "Testar novas funcionalidades",
    "Publicar atualizações"
]

st.markdown(f"## 📂 {projeto}  ")
st.markdown(f"**Status atual:** `{status_atual}`")

def checklist(tarefas):
    concluido = []
    for tarefa in tarefas:
        if st.checkbox(tarefa, key=f"{projeto}-{tarefa}"):
            concluido.append(tarefa)
    st.success(f"{len(concluido)} de {len(tarefas)} tarefas concluídas.")

# Checklists por projeto
if projeto == "Radar Climático – LLN":
    checklist([
        "Buscar e limpar dados reais (chuvas, população, ocorrências)",
        "Substituir dataset de cidades no app",
        "Adicionar cores por intensidade de risco",
        "Validar primeiros testes com mapas reais"
    ])
elif projeto == "CRM de Bolso":
    checklist([
        "Criar modelo de pedidos no WhatsApp com respostas",
        "Simular fechamento de caixa automático",
        "Organizar categorias e estoques",
        "Teste com base da Tendda101"
    ])
elif projeto == "UTM Link Builder":
    checklist([
        "Finalizar exportação de links com QR Code",
        "Melhorar instruções visuais no app",
        "Conectar com planilha de histórico",
        "Publicar README estratégico no GitHub"
    ])
elif projeto == "Tendda101":
    checklist([
        "Organizar cronograma de postagens semanais",
        "Criar painel de pedidos ativos",
        "Incluir fotos reais dos produtos",
        "Testar fluxo de entrega com Noemi"
    ])
elif projeto == "Blog “E se eu te contar...”":
    checklist([
        "Montar lista de posts com potencial de viralização",
        "Organizar roteiro de Shorts/TikToks",
        "Integrar blog com newsletter",
        "Começar curadoria SEO com IA"
    ])
elif projeto == "LLN Automações":
    checklist([
        "Organizar todos os tokens e credenciais",
        "Criar painel visual com links de todos os apps",
        "Simular fluxos de automações completas por cliente",
        "Planejar lançamento do site institucional LLN"
    ])
else:
    checklist(tarefas_padrao)
