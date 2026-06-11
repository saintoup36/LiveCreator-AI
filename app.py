
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except Exception:
    create_client = None
    SUPABASE_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


# ============================================================
# LIVECREATOR AI — SAFE ELITE VERSION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="LiveCreator AI",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None
if SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        supabase = None
        
def is_premium_user():
    return False
        

# ============================================================
# TRANSLATION SYSTEM — SAFE, NO MONKEY PATCHING
# ============================================================

LANGUAGES = [
    "English",
    "French",
    "Haitian Creole",
    "Spanish",
    "Portuguese",
    "Arabic",
    "Mandarin Chinese",
    "Hindi",
]

UI_TRANSLATIONS = {
    "English": {},

    "French": {
        "LiveCreator AI": "LiveCreator AI",
        "Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.": "Préparez des titres de live, des accroches, des plans, des légendes, des hashtags, des appels à l’action et des idées de contenu en quelques minutes.",
        "Never go live unprepared again.": "Ne lancez plus jamais un live sans préparation.",
        "⚡ Full live plans": "⚡ Plans de live complets",
        "🔥 Viral hooks": "🔥 Accroches virales",
        "🌍 Multilingual": "🌍 Multilingue",
        "💎 Creator SaaS": "💎 SaaS pour créateurs",
        "This language controls both the app interface and the AI-generated content.": "Cette langue contrôle à la fois l’interface de l’application et le contenu généré par l’IA.",
        "Language Settings": "Paramètres de langue",
        "App Language": "Langue de l’application",
        "Apply Language": "Appliquer la langue",
        "Account Access": "Accès au compte",
        "Create Account": "Créer un compte",
        "Login": "Connexion",
        "Logout": "Déconnexion",
        "Email": "E-mail",
        "Password": "Mot de passe",
        "Logged in as": "Connecté en tant que",
        "Creator Studio": "Studio Créateur",
        "Choose what you want LiveCreator AI to build.": "Choisissez ce que LiveCreator AI doit créer.",
        "Choose AI tool": "Choisissez un outil IA",
        "Complete Live Pack": "Pack live complet",
        "Viral Hooks": "Accroches virales",
        "Captions": "Légendes",
        "Repurpose Live": "Réutiliser le live",
        "Audience Retention": "Rétention d’audience",
        "Debate Engine": "Moteur de débat",
        "Creator Brand Voice": "Voix de marque du créateur",
        "Trend Radar": "Radar de tendances",
        "Live Simulator": "Simulateur de live",
        "Teleprompter": "Téléprompteur",
        "Translate": "Traduire",
        "Saved Packs": "Packs sauvegardés",
        "Premium": "Premium",
        "Create a complete livestream pack": "Créer un pack complet de livestream",
        "Enter your live idea. The AI prepares your title, hook, outline, prompts, captions, hashtags, and closing script.": "Entrez votre idée de live. L’IA prépare votre titre, accroche, plan, prompts, légendes, hashtags et script de clôture.",
        "Livestream topic": "Sujet du livestream",
        "Goal of the live": "Objectif du live",
        "Niche": "Niche",
        "Platform": "Plateforme",
        "Language": "Langue",
        "Duration": "Durée",
        "Tone": "Ton",
        "Creator mode": "Mode créateur",
        "Target audience": "Public cible",
        "Include product / affiliate promotion section": "Inclure une section produit / affiliation",
        "Generate Complete Live Pack": "Générer le pack live complet",
        "Go Live in 60 Seconds": "Aller en live en 60 secondes",
        "Please enter a livestream topic first.": "Veuillez d’abord entrer un sujet de livestream.",
        "LiveCreator AI is preparing your live pack...": "LiveCreator AI prépare votre pack de live...",
        "Copy your full live pack": "Copiez votre pack complet",
        "Download Live Pack": "Télécharger le pack live",
        "Saved Creator Packs": "Packs créateur sauvegardés",
        "No saved packs yet.": "Aucun pack sauvegardé pour le moment.",
        "Open Pack": "Ouvrir le pack",
        "Hook topic": "Sujet des accroches",
        "Hook niche": "Niche des accroches",
        "Hook language": "Langue des accroches",
        "Hook tone": "Ton des accroches",
        "Generate Viral Hooks": "Générer des accroches virales",
        "Please enter a hook topic.": "Veuillez entrer un sujet d’accroche.",
        "Caption Bundle Generator": "Générateur de légendes",
        "Caption topic": "Sujet des légendes",
        "Caption platform": "Plateforme des légendes",
        "Caption language": "Langue des légendes",
        "Caption tone": "Ton des légendes",
        "Generate Caption Bundle": "Générer les légendes",
        "Translation Tool": "Outil de traduction",
        "Text to translate": "Texte à traduire",
        "Translate into": "Traduire en",
        "Translation style": "Style de traduction",
        "Translate Content": "Traduire le contenu",
        "Premium Plan": "Plan Premium",
        "Upgrade Coming Soon": "Mise à niveau bientôt disponible",
    },

    "Haitian Creole": {
        "LiveCreator AI": "LiveCreator AI",
        "Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.": "Prepare tit live, fraz pou atire moun, plan, caption, hashtag, CTA, ak ide kontni an kèk minit.",
        "Never go live unprepared again.": "Pa janm antre live san preparasyon ankò.",
        "⚡ Full live plans": "⚡ Plan live konplè",
        "🔥 Viral hooks": "🔥 Fraz viral",
        "🌍 Multilingual": "🌍 Plizyè lang",
        "💎 Creator SaaS": "💎 SaaS pou kreyatè",
        "This language controls both the app interface and the AI-generated content.": "Lang sa a kontwole ni aplikasyon an ni kontni AI a kreye.",
        "Language Settings": "Paramèt lang",
        "App Language": "Lang aplikasyon an",
        "Apply Language": "Aplike lang lan",
        "Account Access": "Aksè kont",
        "Create Account": "Kreye kont",
        "Login": "Konekte",
        "Logout": "Dekonekte",
        "Email": "Imèl",
        "Password": "Modpas",
        "Logged in as": "Konekte kòm",
        "Creator Studio": "Estidyo Kreyatè",
        "Choose what you want LiveCreator AI to build.": "Chwazi sa ou vle LiveCreator AI kreye.",
        "Choose AI tool": "Chwazi zouti AI a",
        "Complete Live Pack": "Pake live konplè",
        "Viral Hooks": "Fraz viral",
        "Captions": "Caption",
        "Repurpose Live": "Re-itilize live",
        "Audience Retention": "Kenbe odyans",
        "Debate Engine": "Motè deba",
        "Creator Brand Voice": "Vwa mak kreyatè",
        "Trend Radar": "Rada tandans",
        "Live Simulator": "Similatè live",
        "Teleprompter": "Teleprompter",
        "Translate": "Tradui",
        "Saved Packs": "Pake ki sove",
        "Premium": "Premium",
        "Create a complete livestream pack": "Kreye yon pake livestream konplè",
        "Livestream topic": "Sijè live la",
        "Goal of the live": "Objektif live la",
        "Niche": "Domèn",
        "Platform": "Platfòm",
        "Language": "Lang",
        "Duration": "Dire",
        "Tone": "Ton",
        "Creator mode": "Mòd kreyatè",
        "Target audience": "Odyans sib",
        "Generate Complete Live Pack": "Kreye pake live konplè",
        "Go Live in 60 Seconds": "Pare pou live nan 60 segonn",
        "Please enter a livestream topic first.": "Tanpri antre sijè live la anvan.",
        "Saved Creator Packs": "Pake kreyatè ki sove",
        "No saved packs yet.": "Pa gen pake ki sove ankò.",
        "Open Pack": "Louvri pake a",
        "Hook topic": "Sijè fraz yo",
        "Generate Viral Hooks": "Kreye fraz viral",
        "Caption Bundle Generator": "Dèlko caption",
        "Translation Tool": "Zouti tradiksyon",
        "Text to translate": "Tèks pou tradui",
        "Translate into": "Tradui an",
        "Translate Content": "Tradui kontni an",
        "Premium Plan": "Plan Premium",
    },

    "Spanish": {
        "LiveCreator AI": "LiveCreator AI",
        "Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.": "Prepara títulos de live, ganchos, esquemas, captions, hashtags, llamadas a la acción e ideas de contenido en minutos.",
        "Never go live unprepared again.": "Nunca vuelvas a salir en vivo sin preparación.",
        "⚡ Full live plans": "⚡ Planes completos de live",
        "🔥 Viral hooks": "🔥 Ganchos virales",
        "🌍 Multilingual": "🌍 Multilingüe",
        "💎 Creator SaaS": "💎 SaaS para creadores",
        "This language controls both the app interface and the AI-generated content.": "Este idioma controla tanto la interfaz de la app como el contenido generado por IA.",
        "Language Settings": "Configuración de idioma",
        "App Language": "Idioma de la app",
        "Apply Language": "Aplicar idioma",
        "Account Access": "Acceso a la cuenta",
        "Create Account": "Crear cuenta",
        "Login": "Iniciar sesión",
        "Logout": "Cerrar sesión",
        "Email": "Correo",
        "Password": "Contraseña",
        "Logged in as": "Conectado como",
        "Creator Studio": "Estudio del Creador",
        "Choose what you want LiveCreator AI to build.": "Elige lo que quieres que LiveCreator AI cree.",
        "Choose AI tool": "Elige una herramienta IA",
        "Complete Live Pack": "Paquete completo de live",
        "Viral Hooks": "Ganchos virales",
        "Captions": "Subtítulos",
        "Repurpose Live": "Reutilizar live",
        "Audience Retention": "Retención de audiencia",
        "Debate Engine": "Motor de debate",
        "Creator Brand Voice": "Voz de marca",
        "Trend Radar": "Radar de tendencias",
        "Live Simulator": "Simulador de live",
        "Teleprompter": "Teleprompter",
        "Translate": "Traducir",
        "Saved Packs": "Paquetes guardados",
        "Premium": "Premium",
        "Livestream topic": "Tema del livestream",
        "Goal of the live": "Objetivo del live",
        "Niche": "Nicho",
        "Platform": "Plataforma",
        "Language": "Idioma",
        "Duration": "Duración",
        "Tone": "Tono",
        "Creator mode": "Modo creador",
        "Target audience": "Audiencia objetivo",
        "Generate Complete Live Pack": "Generar paquete completo",
        "Go Live in 60 Seconds": "Salir en vivo en 60 segundos",
        "Please enter a livestream topic first.": "Primero ingresa un tema.",
        "Saved Creator Packs": "Paquetes guardados",
        "No saved packs yet.": "Aún no hay paquetes guardados.",
        "Open Pack": "Abrir paquete",
        "Hook topic": "Tema de ganchos",
        "Generate Viral Hooks": "Generar ganchos virales",
        "Caption Bundle Generator": "Generador de captions",
        "Translation Tool": "Herramienta de traducción",
        "Text to translate": "Texto para traducir",
        "Translate into": "Traducir a",
        "Translate Content": "Traducir contenido",
        "Premium Plan": "Plan Premium",
    },

    "Portuguese": {
        "LiveCreator AI": "LiveCreator AI",
        "Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.": "Prepare títulos de live, ganchos, roteiros, legendas, hashtags, chamadas para ação e ideias de conteúdo em minutos.",
        "Never go live unprepared again.": "Nunca mais entre ao vivo despreparado.",
        "⚡ Full live plans": "⚡ Planos completos de live",
        "🔥 Viral hooks": "🔥 Ganchos virais",
        "🌍 Multilingual": "🌍 Multilíngue",
        "💎 Creator SaaS": "💎 SaaS para criadores",
        "This language controls both the app interface and the AI-generated content.": "Este idioma controla tanto a interface do app quanto o conteúdo gerado pela IA.",
        "Language Settings": "Configurações de idioma",
        "App Language": "Idioma do app",
        "Apply Language": "Aplicar idioma",
        "Creator Studio": "Estúdio do Criador",
        "Choose AI tool": "Escolha uma ferramenta IA",
        "Livestream topic": "Tema da live",
        "Goal of the live": "Objetivo da live",
        "Language": "Idioma",
        "Generate Complete Live Pack": "Gerar pacote completo",
        "Go Live in 60 Seconds": "Entrar ao vivo em 60 segundos",
        "Premium Plan": "Plano Premium",
    },

    "Arabic": {
        "LiveCreator AI": "LiveCreator AI",
        "Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.": "حضّر عناوين البث المباشر، والافتتاحيات الجذابة، والخطط، والتعليقات، والوسوم، ودعوات الإجراء، وأفكار المحتوى خلال دقائق.",
        "Never go live unprepared again.": "لا تدخل البث المباشر غير مستعد مرة أخرى.",
        "⚡ Full live plans": "⚡ خطط بث كاملة",
        "🔥 Viral hooks": "🔥 افتتاحيات فيروسية",
        "🌍 Multilingual": "🌍 متعدد اللغات",
        "💎 Creator SaaS": "💎 منصة SaaS للمبدعين",
        "This language controls both the app interface and the AI-generated content.": "تتحكم هذه اللغة في واجهة التطبيق والمحتوى الذي ينشئه الذكاء الاصطناعي.",
        "Language Settings": "إعدادات اللغة",
        "App Language": "لغة التطبيق",
        "Apply Language": "تطبيق اللغة",
        "Creator Studio": "استوديو المنشئ",
        "Choose AI tool": "اختر أداة الذكاء الاصطناعي",
        "Livestream topic": "موضوع البث المباشر",
        "Goal of the live": "هدف البث",
        "Language": "اللغة",
        "Generate Complete Live Pack": "إنشاء حزمة بث كاملة",
        "Go Live in 60 Seconds": "جهّز بثك في 60 ثانية",
        "Premium Plan": "خطة بريميوم",
    },

    "Mandarin Chinese": {
        "LiveCreator AI": "LiveCreator AI",
        "Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.": "在几分钟内准备直播标题、开场钩子、提纲、文案、话题标签、行动号召和内容创意。",
        "Never go live unprepared again.": "再也不要毫无准备地开播。",
        "⚡ Full live plans": "⚡ 完整直播方案",
        "🔥 Viral hooks": "🔥 爆款开场钩子",
        "🌍 Multilingual": "🌍 多语言",
        "💎 Creator SaaS": "💎 创作者 SaaS",
        "This language controls both the app interface and the AI-generated content.": "此语言会同时控制应用界面和 AI 生成内容。",
        "Language Settings": "语言设置",
        "App Language": "应用语言",
        "Apply Language": "应用语言",
        "Creator Studio": "创作者工作室",
        "Choose AI tool": "选择 AI 工具",
        "Livestream topic": "直播主题",
        "Goal of the live": "直播目标",
        "Language": "语言",
        "Generate Complete Live Pack": "生成完整直播方案",
        "Go Live in 60 Seconds": "60 秒快速开播方案",
        "Premium Plan": "高级计划",
    },

    "Hindi": {
        "LiveCreator AI": "LiveCreator AI",
        "Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.": "कुछ ही मिनटों में लाइवस्ट्रीम शीर्षक, हुक, रूपरेखा, कैप्शन, हैशटैग, कॉल-टू-एक्शन और कंटेंट आइडिया तैयार करें।",
        "Never go live unprepared again.": "अब कभी भी बिना तैयारी के लाइव न जाएँ।",
        "⚡ Full live plans": "⚡ पूरे लाइव प्लान",
        "🔥 Viral hooks": "🔥 वायरल हुक",
        "🌍 Multilingual": "🌍 बहुभाषी",
        "💎 Creator SaaS": "💎 क्रिएटर SaaS",
        "This language controls both the app interface and the AI-generated content.": "यह भाषा ऐप इंटरफ़ेस और AI द्वारा बनाए गए कंटेंट दोनों को नियंत्रित करती है।",
        "Language Settings": "भाषा सेटिंग्स",
        "App Language": "ऐप भाषा",
        "Apply Language": "भाषा लागू करें",
        "Creator Studio": "क्रिएटर स्टूडियो",
        "Choose AI tool": "AI टूल चुनें",
        "Livestream topic": "लाइवस्ट्रीम विषय",
        "Goal of the live": "लाइव का लक्ष्य",
        "Language": "भाषा",
        "Generate Complete Live Pack": "पूरा लाइव पैक बनाएं",
        "Go Live in 60 Seconds": "60 सेकंड में लाइव तैयारी",
        "Premium Plan": "प्रीमियम योजना",
    },
}

TRANSLATIONS = UI_TRANSLATIONS


def t(text: str) -> str:
    lang = st.session_state.get("active_app_language", "English")
    return UI_TRANSLATIONS.get(lang, {}).get(text, text)


def thtml(html: str) -> str:
    lang = st.session_state.get("active_app_language", "English")
    for src, dst in UI_TRANSLATIONS.get(lang, {}).items():
        html = html.replace(src, dst)
    return html


def current_language() -> str:
    return st.session_state.get("active_app_language", "English")


def get_secret_value(name: str, default: str = "") -> str:
    """Read a setting from .env first, then Streamlit secrets without crashing locally."""
    value = os.getenv(name, "")
    if value:
        return value

    try:
        return st.secrets[name]
    except Exception:
        return default


def build_stripe_checkout_url(base_url: str) -> str:
    """Add the logged-in Supabase user ID and email to a Stripe Payment Link.

    The Stripe webhook reads client_reference_id to upgrade the correct user.
    """
    if not base_url:
        return ""

    params = {}
    user = st.session_state.get("user")
    if user:
        user_id = getattr(user, "id", "")
        user_email = getattr(user, "email", "")
        if user_id:
            params["client_reference_id"] = user_id
        if user_email:
            params["prefilled_email"] = user_email

    if not params:
        return base_url

    parts = urlsplit(base_url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update(params)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def get_stripe_monthly_link() -> str:
    return build_stripe_checkout_url(get_secret_value("STRIPE_MONTHLY_LINK", ""))


def is_premium_user():
    if not supabase or not st.session_state.get("user"):
        return False

    try:
        result = (
            supabase.table("user_profiles")
            .select("is_premium")
            .eq("id", st.session_state.user.id)
            .single()
            .execute()
        )

        return result.data.get("is_premium", False)

    except Exception:
        return False



# ============================================================
# STATE
# ============================================================

defaults = {
    "active_app_language": "English",
    "user": None,
    "live_pack": "",
    "hooks": "",
    "captions": "",
    "repurpose": "",
    "retention": "",
    "debate": "",
    "trends": "",
    "simulation": "",
    "translation_result": "",
    "saved_packs": [],
    "brand_voice": {"style": "", "catchphrases": "", "avoid": ""},
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(236,72,153,.24), transparent 28%),
        radial-gradient(circle at top right, rgba(34,211,238,.22), transparent 28%),
        linear-gradient(145deg, #020617 0%, #080816 48%, #000000 100%);
    color: white;
}

.block-container {
    max-width: 760px;
    padding-top: 0rem;
    padding-bottom: 4rem;
    padding-left: .75rem;
    padding-right: .75rem;
}

h1, h2, h3, p, div, span, label {
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.hero {
    text-align: center;
    padding: 18px 14px;
    border-radius: 26px;
    background: linear-gradient(145deg, rgba(255,255,255,.14), rgba(255,255,255,.04));
    border: 1px solid rgba(255,255,255,.14);
    box-shadow: 0 28px 90px rgba(0,0,0,.48);
    backdrop-filter: blur(22px);
    margin-top: 0rem !important;
    margin-bottom: 10px;
}

.hero-title {
    font-size: clamp(34px, 10vw, 54px);
    line-height: .92;
    letter-spacing: -3px;
    font-weight: 950;
    margin: 0;
    background: linear-gradient(90deg, #ffffff, #fbcfe8, #a5f3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: rgba(255,255,255,.75);
    line-height: 1.55;
    max-width: 560px;
    margin: 14px auto 0;
    font-size: 16px;
}

.slogan {
    display: inline-block;
    margin-top: 16px;
    color: #020617;
    font-weight: 900;
    padding: 10px 16px;
    border-radius: 999px;
    background: linear-gradient(90deg, #ffffff, #a5f3fc, #fbcfe8);
}

.glass-card {
    padding: 13px 14px;
    border-radius: 22px;
    margin: 8px 0;
    background: rgba(255,255,255,.075);
    border: 1px solid rgba(255,255,255,.13);
    box-shadow: 0 16px 48px rgba(0,0,0,.30);
}

.result-card {
    padding: 20px;
    border-radius: 28px;
    background: rgba(255,255,255,.96);
    color: #111827;
    box-shadow: 0 18px 65px rgba(0,0,0,.45);
    margin: 18px 0;
}

.result-card h1, .result-card h2, .result-card h3,
.result-card p, .result-card li, .result-card div {
    color: #111827;
}

.mini-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-top: 16px;
}

.mini-card {
    border-radius: 22px;
    padding: 14px;
    background: rgba(255,255,255,.085);
    border: 1px solid rgba(255,255,255,.12);
    color: rgba(255,255,255,.86);
    font-size: 14px;
}

.metric-grid {
    display:grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap:10px;
    margin:10px 0 14px;
}

.metric-card {
    padding:14px;
    border-radius:22px;
    background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.12);
}

.small {
    color: rgba(255,255,255,.67);
    font-size: 14px;
    line-height: 1.5;
}

.footer {
    text-align: center;
    color: rgba(255,255,255,.55);
    font-size: 13px;
    margin-top: 30px;
}

label {
    color: rgba(255,255,255,.88) !important;
    font-weight: 800 !important;
}

div[data-baseweb="input"],
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"],
div[data-baseweb="textarea"] > div {
    background: #111827 !important;
    background-color: #111827 !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
input,
textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
}

input::placeholder,
textarea::placeholder {
    color: #cbd5e1 !important;
    opacity: 1 !important;
}

.stButton > button {
    width: 100%;
    min-height: 3.2rem;
    border-radius: 999px;
    border: 0;
    font-size: 16px;
    font-weight: 950;
    color: #020617;
    background: linear-gradient(90deg, #ffffff, #a5f3fc, #fbcfe8);
    box-shadow: 0 18px 55px rgba(34,211,238,.18);
    transition: .18s ease;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
}

.stDownloadButton > button {
    width: 100%;
    min-height: 3rem;
    border-radius: 999px;
    font-weight: 900;
    color: white;
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.16);
}

div[data-testid="stExpander"] {
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    background: rgba(255,255,255,.045) !important;
}

button,
button *,
.stButton button,
.stButton button *,
.stDownloadButton button,
.stDownloadButton button *,
div[data-testid="stButton"],
div[data-testid="stButton"] *,
div[data-testid="stDownloadButton"],
div[data-testid="stDownloadButton"] *,
div[data-testid="stSelectbox"],
div[data-testid="stSelectbox"] *,
div[data-baseweb="select"],
div[data-baseweb="select"] *,
[role="button"],
[role="button"] * {
    cursor: pointer !important;
}

@media (max-width: 540px) {
    .block-container {
        padding: 0rem .65rem 4rem !important;
    }

    .hero {
        border-radius: 26px;
        padding: 20px 14px;
    }

    .mini-grid,
    .metric-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def call_ai(prompt: str, system: str, temperature: float = 0.85) -> str:
    if not client:
        return "OpenAI API key is missing. Add OPENAI_API_KEY to your .env file, then restart Streamlit."

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI generation failed: {e}"


def brand_voice_text() -> str:
    bv = st.session_state.get("brand_voice", {})
    style = bv.get("style", "")
    catchphrases = bv.get("catchphrases", "")
    avoid = bv.get("avoid", "")
    if not any([style, catchphrases, avoid]):
        return ""
    return f"""
Creator Brand Voice:
- Style: {style}
- Favorite phrases / CTAs: {catchphrases}
- Avoid: {avoid}
"""


def build_full_live_prompt(data: dict) -> str:
    faith_extra = ""
    if "Faith" in data["niche"] or "Bible" in data["niche"]:
        faith_extra = """
Also include Bible verse ideas with references, a respectful spiritual reflection, and a short prayer-style closing if appropriate.
"""

    product_extra = ""
    if data["product"]:
        product_extra = """
Also include a soft product, affiliate, or service promotion section with a non-pushy offer script.
"""

    return f"""
Create a complete premium livestream preparation pack.

{brand_voice_text()}

Creator details:
- Topic: {data["topic"]}
- Goal: {data["goal"]}
- Niche: {data["niche"]}
- Platform: {data["platform"]}
- Language: {data["language"]}
- Tone: {data["tone"]}
- Audience: {data["audience"]}
- Duration: {data["duration"]}
- Creator mode: {data["creator_mode"]}

IMPORTANT:

Write 100% of the response in {data["language"]}.

Translate:
- all titles
- all headings
- all bullet points
- all captions
- all hashtags
- all explanations
- all calls to action
- all labels such as Topic, Goal, Niche, Platform, Language, Tone, Audience, Duration, and Creator Mode

Do not use English unless {data["language"]} is English.

Include:
1. 5 viral livestream title options
2. 10 scroll-stopping opening hooks
3. Short welcome script
4. Full timestamped livestream outline
5. Main talking points
6. Emotional storytelling prompts
7. Viewer engagement questions
8. Comment prompts the host can say live
9. Pinned comment ideas
10. Audience retention ideas
11. Call-to-action options
12. Closing script
13. Post-live captions
14. Hashtags
15. Short promo text before the live
16. Mistakes to avoid
17. Confidence note for the creator
18. Repurposing ideas after the live
19. Suggested pinned comment
20. One memorable closing line

{faith_extra}
{product_extra}
"""


def generic_prompt(tool_name: str, details: str, language: str = "English") -> str:
    return f"""
You are LiveCreator AI, a premium AI livestream producer and creator growth strategist.

{brand_voice_text()}

Tool: {tool_name}

Details:
{details}

IMPORTANT:

Write 100% of the response in {language}.

Translate all titles, headings, bullet points, captions, hashtags, explanations, calls to action, and labels.
Do not use English unless {language} is English.

Make it practical, modern, social-media optimized, creator-friendly, and ready to use.
"""


def save_live_pack_to_supabase(topic: str, content: str):
    """Save one generated live pack for the logged-in user.

    Returns:
        tuple[bool, str | None]: (success, error_message)
    """
    if not supabase:
        return False, "Supabase is not connected."

    if not st.session_state.get("user"):
        return False, "Please log in to save packs."

    try:
        supabase.table("live_packs").insert({
            "user_id": st.session_state.user.id,
            "topic": topic,
            "content": content,
        }).execute()
        return True, None
    except Exception as e:
        return False, str(e)


def load_live_packs_from_supabase():
    if not supabase or not st.session_state.get("user"):
        return []
    try:
        response = (
            supabase.table("live_packs")
            .select("id, topic, content, created_at")
            .eq("user_id", st.session_state.user.id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data or []
    except Exception as e:
        st.warning(f"Could not load saved packs: {e}")
        return []

def make_pdf(text: str, filename: str):
    if not REPORTLAB_AVAILABLE:
        return None

    output_dir = Path.cwd() / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph("LiveCreator AI Creator Pack", styles["Title"]), Spacer(1, 12)]

    cleaned = re.sub(r"#|\*", "", text)

    for line in cleaned.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 8))
        else:
            story.append(Paragraph(line, styles["BodyText"]))
            story.append(Spacer(1, 5))

    doc.build(story)

    return str(output_path)


def output_block(title: str, text: str, file_prefix: str):
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(text)
    st.markdown("</div>", unsafe_allow_html=True)

    st.text_area(f"Copy {title}", value=text, height=230, key=f"copy_{file_prefix}_{len(text)}")

    st.download_button(
        f"📥 Download {title}",
        data=text,
        file_name=f"{file_prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True,
        key=f"download_txt_{file_prefix}_{len(text)}",
    )

    if REPORTLAB_AVAILABLE:
        pdf_path = make_pdf(text, f"{file_prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        if pdf_path:
            with open(str(pdf_path), "rb") as f:
                st.download_button(
                f"📄 Download {title} as PDF",
                data=f,
                file_name=Path(pdf_path).name,
                mime="application/pdf",
                use_container_width=True,
                key=f"download_pdf_{file_prefix}_{len(text)}",
            )                
    else:
        st.caption("PDF export available after: pip install reportlab")

def get_creator_stats():
    if not supabase or not st.session_state.get("user"):
        return None

    user_id = st.session_state.user.id

    try:
        result = (
            supabase.table("creator_stats")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        if result.data:
            return result.data[0]

        supabase.table("creator_stats").insert({
            "user_id": user_id
        }).execute()

        return {
            "live_packs_generated": 0,
            "hooks_generated": 0,
            "captions_generated": 0,
            "last_activity": None,
            "created_at": None,
        }

    except Exception:
        return None


def update_creator_stat(stat_name):
    if not supabase or not st.session_state.get("user"):
        return

    stats = get_creator_stats()
    current_value = stats.get(stat_name, 0) if stats else 0

    try:
        supabase.table("creator_stats").update({
            stat_name: current_value + 1,
            "last_activity": datetime.now().isoformat()
        }).eq("user_id", st.session_state.user.id).execute()
    except Exception:
        pass

def creator_score_card():
    st.markdown(
        """
<div class="metric-grid">
    <div class="metric-card"><b>🧠 Engagement Score</b><br><span class="small">92/100</span></div>
    <div class="metric-card"><b>🔥 Hook Strength</b><br><span class="small">Strong</span></div>
    <div class="metric-card"><b>🧲 Retention Potential</b><br><span class="small">High</span></div>
    <div class="metric-card"><b>🚀 CTA Clarity</b><br><span class="small">Strong</span></div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
<div class="hero">
    <h1 class="hero-title">{t("LiveCreator AI")}</h1>
    <p class="hero-subtitle">
        {t("Prepare livestream titles, hooks, outlines, captions, hashtags, CTAs, and content ideas in minutes.")}
    </p>
    <div class="slogan">{t("Never go live unprepared again.")}</div>
    <div class="mini-grid">
        <div class="mini-card">{t("⚡ Full live plans")}</div>
        <div class="mini-card">{t("🔥 Viral hooks")}</div>
        <div class="mini-card">{t("🌍 Multilingual")}</div>
        <div class="mini-card">{t("💎 Creator SaaS")}</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LANGUAGE SETTINGS
# ============================================================

with st.expander(f"🌍 {t('Language Settings')}", expanded=False):
    st.caption(t("This language controls both the app interface and the AI-generated content."))
    selected_language = st.selectbox(
        t("App Language"),
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.active_app_language),
        key="language_picker",
    )
    if st.button(t("Apply Language"), use_container_width=True, key="apply_lang"):
        st.session_state.active_app_language = selected_language
        st.rerun()


# ============================================================
# ACCOUNT ACCESS
# ============================================================

with st.expander(f"🔐 {t('Account Access')}", expanded=False):
    if supabase is None:
        st.info("Supabase is not connected yet. Add SUPABASE_URL and SUPABASE_KEY to your .env file, then restart Streamlit.")
    else:
        if st.session_state.user:
            st.success(f"{t('Logged in as')} {st.session_state.user.email}")

            if st.session_state.get("user"):
                if is_premium_user():
                    st.success("💎 Premium Creator")
                else:
                    st.info("🆓 Free Creator")

            if st.button(t("Logout"), use_container_width=True, key="logout_btn"):
                try:
                    supabase.auth.sign_out()
                except Exception:
                    pass
                st.session_state.user = None
                st.rerun()
        else:
            email = st.text_input(t("Email"), key="auth_email")
            password = st.text_input(t("Password"), type="password", key="auth_password")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(t("Create Account"), use_container_width=True, key="signup_btn"):
                    if not email.strip() or not password.strip():
                        st.error("Please enter both email and password.")
                    else:
                        try:
                            supabase.auth.sign_up({"email": email.strip(), "password": password})
                            st.success("Account created. Check your email if confirmation is required.")
                        except Exception as e:
                            st.error(f"Sign up failed: {e}")
            with col2:
                if st.button(t("Login"), use_container_width=True, key="login_btn"):
                    if not email.strip() or not password.strip():
                        st.error("Please enter both email and password.")
                    else:
                        try:
                            result = supabase.auth.sign_in_with_password({"email": email.strip(), "password": password})
                            st.session_state.user = result.user

                            try:
                                existing = (
                                    supabase.table("user_profiles")
                                    .select("*")
                                    .eq("id", result.user.id)
                                    .execute()
                                )

                                if not existing.data:
                                    supabase.table("user_profiles").insert({
                                        "id": result.user.id,
                                        "email": result.user.email,
                                        "is_premium": False
                                    }).execute()
                            except Exception as e:
                                st.warning(f"Profile creation failed: {e}")

                            st.success("Logged in.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Login failed: {e}")

        stripe_monthly_link = get_stripe_monthly_link()
        if st.session_state.get("user") and not is_premium_user():
            if stripe_monthly_link:
                st.link_button("💎 Upgrade to Premium", stripe_monthly_link, use_container_width=True)
            else:
                st.warning("Stripe payment link is missing.")
    

# ============================================================
# CREATOR STUDIO
# ============================================================

st.markdown(
    thtml("""
<div class="glass-card">
<h3>🧠 Creator Studio</h3>
<p class="small">Choose what you want LiveCreator AI to build.</p>
</div>
"""),
    unsafe_allow_html=True,
)

tool_options = [
    ("🎥", "Complete Live Pack"),
    ("🔥", "Viral Hooks"),
    ("✍️", "Captions"),
    ("♻️", "Repurpose Live"),
    ("🧲", "Audience Retention"),
    ("⚔️", "Debate Engine"),
    ("🧬", "Creator Brand Voice"),
    ("📈", "Trend Radar"),
    ("🎭", "Live Simulator"),
    ("🎙️", "Teleprompter"),
    ("🌍", "Translate"),
    ("📂", "Saved Packs"),
    ("💎", "Premium"),
]

tool_choice = st.selectbox(
    t("Choose AI tool"),
    [f"{icon} {t(label)}" for icon, label in tool_options],
)

tool_key = tool_choice.split(" ", 1)[1]
reverse_lookup = {t(label): label for _, label in tool_options}
tool_key = reverse_lookup.get(tool_key, tool_key)


# ============================================================
# COMPLETE LIVE PACK
# ============================================================

if tool_key == "Complete Live Pack":
    st.markdown(
        thtml("""
<div class="glass-card" style="background:linear-gradient(135deg,#7c3aed,#06b6d4);">
<h3 style="color:white;">🎥 Create a complete livestream pack</h3>
<p style="color:white;">Enter your live idea. The AI prepares your title, hook, outline, prompts, captions, hashtags, and closing script.</p>
</div>
"""),
        unsafe_allow_html=True,
    )

    topic = st.text_area(t("Livestream topic"), placeholder="Example: Why people give up before their breakthrough", height=85)
    goal = st.text_area(t("Goal of the live"), placeholder="Example: encourage viewers, sell my book, get comments, build trust...", height=80)

    col1, col2 = st.columns(2)
    with col1:
        niche = st.selectbox(t("Niche"), ["Faith / Bible Teaching", "Motivation", "Relationships", "Business / Coaching", "Education", "Gaming", "Beauty / Fashion", "Fitness", "Finance", "Comedy", "Personal Storytelling"])
    with col2:
        platform = st.selectbox(t("Platform"), ["TikTok Live", "YouTube Live", "Facebook Live", "Instagram Live", "Twitch", "Multiple Platforms"])

    col3, col4 = st.columns(2)
    with col3:
        language = current_language()
        st.text_input(
            t("Language"),
            value=language,
            disabled=True,
            key="live_pack_language_display",
        )
    with col4:
        duration = st.selectbox(t("Duration"), ["10 minutes", "20 minutes", "30 minutes", "45 minutes", "1 hour", "90 minutes"])

    col5, col6 = st.columns(2)
    with col5:
        tone = st.selectbox(t("Tone"), ["Motivational", "Emotional", "Professional", "Biblical", "Funny", "Controversial but respectful", "Educational", "Luxury and polished"])
    with col6:
        creator_mode = st.selectbox(t("Creator mode"), ["Beginner Creator", "Faith Speaker", "Coach", "Influencer", "Seller / Affiliate", "Gaming Streamer", "Educator"])

    audience = st.text_input(t("Target audience"), placeholder="Example: young couples, church members, small creators, entrepreneurs")
    product = st.toggle(t("Include product / affiliate promotion section"), value=False)

    if st.button(f"🚀 {t('Generate Complete Live Pack')}", use_container_width=True):
        if not topic.strip():
            st.error(t("Please enter a livestream topic first."))
        else:
            data = {
                "topic": topic.strip(),
                "goal": goal.strip() or "grow engagement and provide value",
                "niche": niche,
                "platform": platform,
                "language": language,
                "tone": tone,
                "audience": audience.strip() or "general viewers",
                "duration": duration,
                "creator_mode": creator_mode,
                "product": product,
            }

            with st.spinner(t("LiveCreator AI is preparing your live pack...")):
                st.session_state.live_pack = call_ai(
                    build_full_live_prompt(data),
                    "You are LiveCreator AI, a premium AI livestream producer for creators.",
                    temperature=0.85,
                )


    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    if st.button(f"⚡ {t('Go Live in 60 Seconds')}", use_container_width=True):
        if not topic.strip():
            st.error(t("Please enter a livestream topic first."))
        else:
            instant_prompt = generic_prompt(
                "Go Live in 60 Seconds",
                f"""
Topic: {topic}
Platform: {platform}
Language: {language}
Tone: {tone}
Audience: {audience.strip() or 'general viewers'}
Duration: {duration}

IMPORTANT:
Write 100% of the response in {language}.
Translate all headings, labels, bullets, hooks, explanations, captions, hashtags, and calls to action.
Do not use English unless {language} is English.

Include only:
1. One powerful title
2. Three opening hooks
3. Simple 5-step outline
4. Three engagement questions
5. One CTA
6. Five hashtags
""",
                language,
            )

            with st.spinner("Building your 60-second live pack..."):
                st.session_state.live_pack = call_ai(
                    instant_prompt,
                    "You create fast livestream packs for busy creators.",
                    temperature=0.85,
                )


    if st.session_state.live_pack:
        creator_score_card()
        output_block("Live Pack", st.session_state.live_pack, "livecreator_ai_pack")

        if st.button("💾 Save This Pack", use_container_width=True, key="save_this_live_pack_btn"):
            if not st.session_state.get("user"):
                st.warning("Please log in to save packs.")
            elif not supabase:
                st.session_state.saved_packs.insert(0, {
                    "topic": topic.strip() or "Untitled Live Pack",
                    "content": st.session_state.live_pack,
                    "created_at": datetime.now().isoformat(),
                })
                st.warning("Supabase is not connected. Pack saved locally for this session.")
            else:
                success, error = save_live_pack_to_supabase(
                    topic.strip() or "Untitled Live Pack",
                    st.session_state.live_pack,
                )
                if success:
                    st.success("✅ Pack saved to your account.")
                else:
                    st.error(f"Save failed: {error}")


# ============================================================
# VIRAL HOOKS
# ============================================================

if tool_key == "Viral Hooks":
    st.markdown(thtml('<div class="glass-card"><h3>🔥 Viral Hook Generator</h3><p class="small">Generate scroll-stopping opening lines for your next live.</p></div>'), unsafe_allow_html=True)

    hook_topic = st.text_input(t("Hook topic"), placeholder="Example: Why discipline is harder than motivation")
    hook_niche = st.selectbox(t("Hook niche"), ["Motivation", "Faith", "Relationships", "Business", "Education", "Gaming"], key="hook_niche")
    hook_language = current_language()
    st.text_input(t("Hook language"), value=hook_language, disabled=True, key="hook_lang_display")
    hook_tone = st.selectbox(t("Hook tone"), ["Emotional", "Bold", "Curious", "Funny", "Biblical", "Professional"], key="hook_tone")

    if st.button(f"🔥 {t('Generate Viral Hooks')}", use_container_width=True):
        if not hook_topic.strip():
            st.error(t("Please enter a hook topic."))
        else:
            prompt = generic_prompt(
                "Viral Hooks",
                f"""
Topic: {hook_topic}
Niche: {hook_niche}
Tone: {hook_tone}

Generate:
- 25 viral livestream hooks
- emotional hooks
- controversy hooks
- storytelling hooks
- curiosity hooks
- sales hooks
""",
                hook_language,
            )
            with st.spinner("Generating viral hooks..."):
                st.session_state.hooks = call_ai(prompt, "You create viral livestream hooks for creators.", 0.95)

            update_creator_stat("hooks_generated")

    if st.session_state.hooks:
        output_block("Hooks", st.session_state.hooks, "livecreator_ai_hooks")


# ============================================================
# CAPTIONS
# ============================================================

if tool_key == "Captions":
    st.markdown(thtml('<div class="glass-card"><h3>✍️ Caption Bundle Generator</h3><p class="small">Generate captions, hashtags, and promo text for after your live.</p></div>'), unsafe_allow_html=True)

    caption_topic = st.text_input(t("Caption topic"), placeholder="Example: What tonight's live taught us about discipline")
    caption_platform = st.selectbox(t("Caption platform"), ["TikTok", "YouTube Shorts", "Facebook Reels", "Instagram Reels"], key="cap_platform")
    caption_language = current_language()
    st.text_input(t("Caption language"), value=caption_language, disabled=True, key="cap_lang_display")
    caption_tone = st.selectbox(t("Caption tone"), ["Motivational", "Emotional", "Bold", "Professional", "Biblical", "Funny"], key="cap_tone")

    if st.button(f"✍️ {t('Generate Caption Bundle')}", use_container_width=True):
        if not caption_topic.strip():
            st.error("Please enter a caption topic.")
        else:
            prompt = generic_prompt(
                "Caption Bundle",
                f"""
Topic: {caption_topic}
Platform: {caption_platform}
Tone: {caption_tone}

Include:
1. 10 short captions
2. 5 emotional captions
3. 5 bold captions
4. 5 call-to-action captions
5. 25 hashtags
6. 5 short promo texts for the next live
""",
                caption_language,
            )
            with st.spinner("Writing captions..."):
                st.session_state.captions = call_ai(prompt, "You write strong social media captions for creators.", 0.85)

            update_creator_stat("captions_generated")

    if st.session_state.captions:
        output_block("Captions", st.session_state.captions, "livecreator_ai_captions")


# ============================================================
# OTHER TOOLS
# ============================================================

if tool_key == "Repurpose Live":
    st.markdown(thtml('<div class="glass-card"><h3>♻️ Repurpose Live</h3><p class="small">Turn one livestream into TikToks, Shorts, Reels, captions, clips, and viral content ideas.</p></div>'), unsafe_allow_html=True)
    repurpose_topic = st.text_area(t("Livestream topic"), placeholder="Paste your livestream topic or summary here...", height=120)
    repurpose_platform = st.selectbox(t("Platform"), ["TikTok", "YouTube", "Instagram", "Facebook"], key="repurpose_platform")
    repurpose_language = current_language()
    st.text_input(t("Language"), value=repurpose_language, disabled=True, key="repurpose_lang_display")

    if st.button("♻️ Generate Repurposing Ideas", use_container_width=True):
        if not repurpose_topic.strip():
            st.error("Please enter a livestream topic.")
        else:
            prompt = generic_prompt(
                "Repurpose Live",
                f"""
Topic: {repurpose_topic}
Platform: {repurpose_platform}

Include:
1. 10 TikTok ideas
2. 10 YouTube Shorts ideas
3. 10 Reel hooks
4. 10 captions
5. 10 controversy clips
6. 10 emotional moments
7. 10 audience questions
8. 5 carousel post ideas
9. 5 story post ideas
10. viral clip timestamps
""",
                repurpose_language,
            )
            with st.spinner("Creating repurposing ideas..."):
                st.session_state.repurpose = call_ai(prompt, "You are an elite viral content strategist.", 0.95)

    if st.session_state.repurpose:
        output_block("Repurposing Ideas", st.session_state.repurpose, "livecreator_ai_repurpose")


if tool_key == "Audience Retention":
    st.markdown(thtml('<div class="glass-card"><h3>🧲 Audience Retention Engine</h3><p class="small">Generate prompts that keep viewers watching, commenting, and staying until the end.</p></div>'), unsafe_allow_html=True)
    live_topic = st.text_input("Live topic", key="retention_topic")
    retention_language = current_language()
    st.text_input(t("Language"), value=retention_language, disabled=True, key="retention_lang_display")
    if st.button("🧲 Generate Retention Prompts", use_container_width=True):
        if not live_topic.strip():
            st.error("Please enter a live topic.")
        else:
            prompt = generic_prompt("Audience Retention", f"Live topic: {live_topic}\nGenerate retention lines, cliffhangers, comment prompts, and watch-time boosters.", retention_language)
            with st.spinner("Creating retention plan..."):
                st.session_state.retention = call_ai(prompt, "You create retention systems for livestream creators.", 0.9)
    if st.session_state.retention:
        output_block("Retention Plan", st.session_state.retention, "livecreator_ai_retention")


if tool_key == "Debate Engine":
    st.markdown(thtml('<div class="glass-card"><h3>⚔️ AI Debate Engine</h3><p class="small">Generate respectful controversy and engagement-driving discussion prompts.</p></div>'), unsafe_allow_html=True)
    debate_topic = st.text_input("Debate topic", key="debate_topic")
    debate_tone = st.selectbox("Debate tone", ["Respectful", "Bold", "Philosophical", "Emotional"], key="debate_tone")
    debate_language = current_language()
    st.text_input(t("Language"), value=debate_language, disabled=True, key="debate_lang_display")
    if st.button("⚔️ Generate Debate Prompts", use_container_width=True):
        if not debate_topic.strip():
            st.error("Please enter a debate topic.")
        else:
            prompt = generic_prompt("Debate Engine", f"Debate topic: {debate_topic}\nTone: {debate_tone}\nGenerate respectful controversy prompts, audience questions, and debate angles.", debate_language)
            with st.spinner("Creating debate pack..."):
                st.session_state.debate = call_ai(prompt, "You create respectful debate prompts for livestream creators.", 0.9)
    if st.session_state.debate:
        output_block("Debate Pack", st.session_state.debate, "livecreator_ai_debate")

if st.session_state.get("user"):
    stats = get_creator_stats()

    if stats:
        st.markdown(
            f"""
<div class="glass-card">
<h3>📊 Creator Dashboard</h3>
<p class="small">Your LiveCreator AI activity</p>

<div class="metric-grid">
    <div class="metric-card"><b>🎥 Live Packs</b><br>{stats.get("live_packs_generated", 0)}</div>
    <div class="metric-card"><b>🔥 Hooks</b><br>{stats.get("hooks_generated", 0)}</div>
    <div class="metric-card"><b>✍️ Captions</b><br>{stats.get("captions_generated", 0)}</div>
    <div class="metric-card"><b>🕒 Last Activity</b><br>{stats.get("last_activity", "New")}</div>
</div>
</div>
""",
            unsafe_allow_html=True,
        )

if tool_key == "Trend Radar":
    st.markdown(thtml('<div class="glass-card"><h3>📈 AI Trend Radar</h3><p class="small">Discover livestream ideas, viral angles, and trending discussions for creators.</p></div>'), unsafe_allow_html=True)
    trend_niche = st.selectbox("Creator niche", ["Motivation", "Faith", "Relationships", "Business", "Gaming", "Fitness", "Finance"], key="trend_niche")
    trend_language = current_language()
    st.text_input(t("Language"), value=trend_language, disabled=True, key="trend_lang_display")
    if st.button("📈 Generate Trend Ideas", use_container_width=True):
        prompt = generic_prompt("Trend Radar", f"Niche: {trend_niche}\nGenerate 25 trend-style livestream ideas, hooks, debate topics, and audience questions.", trend_language)
        with st.spinner("Creating trend report..."):
            st.session_state.trends = call_ai(prompt, "You are a creator trend strategist.", 0.95)
    if st.session_state.trends:
        output_block("Trend Report", st.session_state.trends, "livecreator_ai_trends")


if tool_key == "Live Simulator":
    st.markdown(thtml('<div class="glass-card"><h3>🎭 AI Live Simulator</h3><p class="small">Practice difficult livestream situations before going live.</p></div>'), unsafe_allow_html=True)
    sim_topic = st.text_input("Live topic", key="sim_topic")
    sim_mode = st.selectbox("Simulation mode", ["Supportive audience", "Mixed audience", "Difficult audience", "Debate audience", "Troll-heavy livestream"], key="sim_mode")
    sim_language = current_language()
    st.text_input(t("Language"), value=sim_language, disabled=True, key="sim_lang_display")
    if st.button("🎭 Simulate Live Audience", use_container_width=True):
        if not sim_topic.strip():
            st.error("Please enter a live topic.")
        else:
            prompt = generic_prompt("Live Simulator", f"Topic: {sim_topic}\nAudience mode: {sim_mode}\nSimulate questions, objections, comments, and best host responses.", sim_language)
            with st.spinner("Simulating audience..."):
                st.session_state.simulation = call_ai(prompt, "You simulate livestream audiences for practice.", 0.9)
    if st.session_state.simulation:
        output_block("Simulation", st.session_state.simulation, "livecreator_ai_simulation")


if tool_key == "Creator Brand Voice":
    st.markdown(thtml('<div class="glass-card"><h3>🧬 Creator Brand Voice</h3><p class="small">Save your creator style so future livestream content sounds more like you.</p></div>'), unsafe_allow_html=True)
    style = st.text_area("Describe your creator voice", value=st.session_state.brand_voice.get("style", ""), placeholder="Motivational, emotional, biblical, bold, calm, funny...")
    catchphrases = st.text_area("Favorite phrases or CTAs", value=st.session_state.brand_voice.get("catchphrases", ""), placeholder="Follow for more, share this live, type YES...")
    avoid = st.text_area("Things the AI should avoid", value=st.session_state.brand_voice.get("avoid", ""), placeholder="Avoid sounding robotic, avoid slang...")
    if st.button("💾 Save Brand Voice", use_container_width=True):
        st.session_state.brand_voice = {"style": style, "catchphrases": catchphrases, "avoid": avoid}
        st.success("Brand voice saved for this session.")


if tool_key == "Teleprompter":
    st.markdown(thtml('<div class="glass-card"><h3>🎙️ AI Teleprompter</h3><p class="small">Paste your livestream script and practice before going live.</p></div>'), unsafe_allow_html=True)
    script_text = st.text_area("Paste your script", placeholder="Paste your livestream script here...", height=250)
    font_size = st.slider("Font size", min_value=18, max_value=48, value=30)
    teleprompter_height = st.slider("Teleprompter height", min_value=300, max_value=700, value=500)

    if script_text.strip():
        st.markdown(
            f"""
<div style="
height:{teleprompter_height}px;
overflow-y:auto;
padding:28px;
border-radius:28px;
background:#000000;
color:white;
font-size:{font_size}px;
line-height:1.8;
font-weight:700;
box-shadow:0 12px 40px rgba(0,0,0,.55);
border:1px solid rgba(255,255,255,.16);
">
{script_text}
</div>
""",
            unsafe_allow_html=True,
        )


if tool_key == "Translate":
    st.markdown(thtml('<div class="glass-card"><h3>🌍 Translation Tool</h3><p class="small">Translate livestream scripts, hooks, captions, CTAs, or creator notes into another language.</p></div>'), unsafe_allow_html=True)

    text_to_translate = st.text_area(t("Text to translate"), height=180)
    default_translate_index = LANGUAGES.index(current_language()) if current_language() in LANGUAGES else 0
    target_language = st.selectbox(t("Translate into"), LANGUAGES, index=default_translate_index, key="target_translate_lang")
    style = st.selectbox(t("Translation style"), ["Natural and clear", "Professional", "Social media friendly", "Biblical and respectful"], key="translate_style")

    if st.button(f"🌍 {t('Translate Content')}", use_container_width=True):
        if not text_to_translate.strip():
            st.error("Please paste text to translate first.")
        else:
            prompt = f"""
Translate the following text into {target_language}.
Style: {style}

Keep it natural, clear, and useful for livestream creators.

Text:
{text_to_translate}
"""
            with st.spinner("Translating your content..."):
                st.session_state.translation_result = call_ai(prompt, "You are a professional multilingual translator for creators.", 0.4)

    if st.session_state.translation_result:
        output_block("Translation", st.session_state.translation_result, "livecreator_ai_translation")


if tool_key == "Saved Packs":
    st.markdown(thtml('<div class="glass-card"><h3>📂 Saved Creator Packs</h3><p class="small">Your previously generated livestream packs.</p></div>'), unsafe_allow_html=True)

    cloud_packs = load_live_packs_from_supabase()
    local_packs = st.session_state.saved_packs
    packs = cloud_packs if cloud_packs else local_packs

    if not packs:
        st.info(t("No saved packs yet."))
    else:
        for pack in packs:
            topic = pack.get("topic", "Untitled")
            created = pack.get("created_at", "")
            with st.expander(f"{t('Open Pack')}: {topic}"):
                if created:
                    st.caption(str(created))
                st.markdown(pack.get("content", ""))


if tool_key == "Premium":
    st.markdown(thtml('<div class="glass-card"><h3>💎 Premium Plan</h3><p class="small">This section is ready for Stripe and Supabase later.</p></div>'), unsafe_allow_html=True)

    st.markdown(
        """
<div class="glass-card">
<h3>Free Creator</h3>
<h1>$0</h1>
<p class="small">Limited generations<br>Basic livestream packs<br>Manual downloads</p>
</div>

<div class="glass-card">
<h3>Premium Creator</h3>
<h1>$15/mo</h1>
<p class="small">
Unlimited livestream packs<br>
Viral hooks engine<br>
Caption bundles<br>
Advanced multilingual generation<br>
PDF creator packs<br>
Saved profiles<br>
Trend suggestions<br>
Audience simulator
</p>
</div>

<div class="glass-card">
<h3>Lifetime Early Access</h3>
<h1>$49–$99</h1>
<p class="small">One-time early supporter offer for first users.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    stripe_monthly_link = get_stripe_monthly_link()

    if is_premium_user():
        st.success("💎 You are already a Premium Creator.")
    elif stripe_monthly_link:
        st.link_button("💎 Upgrade to Premium", stripe_monthly_link, use_container_width=True)
    else:
        st.warning("Stripe payment link is missing.")


st.markdown(f'<div class="footer">{t("LiveCreator AI")} — {t("Never go live unprepared again.")}</div>', unsafe_allow_html=True)
