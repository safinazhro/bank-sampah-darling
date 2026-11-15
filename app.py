import os
import json
import time
import hmac
import hashlib
import secrets
import sqlite3
import threading
import urllib.parse
import base64
from functools import lru_cache
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st

LOGO = "assets/ecoledger_darling_logo_384.png"  # logo EcoLedger Darling (salinan 384 px dari berkas asli)
FAVICON = "assets/favicon.png"
st.set_page_config(page_title="EcoLedger Darling", page_icon=FAVICON if os.path.exists(FAVICON) else "♻️", layout="wide", initial_sidebar_state="auto")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root{--g9:#174D35;--g7:#27834D;--g1:#E7F1E5;--lime:#B8E64B;--bg:#F5F7F2;--ink:#25372C;--mute:#778379;--line:#E3E9E0}
html,body,.stApp,button,input,textarea{font-family:'Plus Jakarta Sans',sans-serif!important}
.stApp{background:var(--bg);color:var(--ink)}
#MainMenu,footer,[data-testid="stDecoration"],[data-testid="stAppDeployButton"]{display:none}
header[data-testid="stHeader"]{background:transparent}
[data-testid="stExpandSidebarButton"],[data-testid="stExpandSidebarButton"] *{color:var(--g9)!important}
.block-container{max-width:1120px;padding:3.2rem 1.8rem 4rem}
h2,h3{font-weight:700;color:var(--g9);font-size:1.05rem}
.hd{display:flex;justify-content:space-between;align-items:flex-end;gap:.8rem;flex-wrap:wrap;margin-bottom:1.2rem}
.hd h1{font-size:1.5rem;font-weight:800;color:var(--g9);margin:0;padding:0;letter-spacing:-.02em}
.hd p{margin:.15rem 0 0;color:var(--mute);font-size:.9rem}
.hd .rt{color:var(--mute);font-size:.8rem;background:#fff;border:1px solid var(--line);border-radius:99px;padding:.3rem .85rem}
[data-testid="stSidebar"]{background:var(--g9)}
[data-testid="stSidebar"] *{color:#e4efe8}
.bx{display:flex;gap:.65rem;align-items:center;padding:.2rem 1.8rem .8rem .8rem}
.bx img{flex:0 0 52px;width:52px;height:52px;object-fit:contain;background:#FDF9EB;border-radius:12px;padding:0}
.bx div{min-width:0}
.bx b{display:block;color:#fff;font-size:1rem;font-weight:800;line-height:1.2}
.bx span{display:block;color:#a9cbb6;font-size:.68rem;line-height:1.3;margin-top:.1rem}
.me{border-bottom:1px solid rgba(255,255,255,.12);padding:.1rem .8rem .8rem;margin-bottom:.7rem}
.me b{display:block;color:#fff;font-size:.9rem;font-weight:700}
.me span{font-size:.75rem;color:#a9cbb6}
.chip{display:inline-block;background:rgba(184,230,75,.18);color:var(--lime)!important;border-radius:99px;font-size:.72rem;font-weight:700;padding:.15rem .7rem;margin:.8rem 0 .3rem .8rem}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:.2rem}
[data-testid="stSidebar"] [data-testid="stSidebarHeader"]{position:absolute;top:.45rem;right:.45rem;left:auto;width:auto;height:auto;min-height:0;padding:0;margin:0;background:transparent;z-index:5}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding:.9rem .8rem 1rem}
[data-testid="stSidebar"] button{justify-content:flex-start;align-items:center;gap:.7rem;border-radius:8px;min-height:2.6rem;padding:.35rem .8rem .35rem calc(.8rem - 3px);font-weight:500;font-size:.92rem;text-align:left}
[data-testid="stSidebar"] button [data-testid="stMarkdownContainer"]{flex:1 1 auto;width:auto;justify-content:flex-start;text-align:left}
[data-testid="stSidebar"] button p{text-align:left;margin:0}
[data-testid="stSidebar"] button [data-testid="stIconMaterial"]{font-size:1.25rem}
[data-testid="stSidebar"] [data-testid="stRadioGroup"]{align-items:stretch;gap:.2rem;width:100%}
[data-testid="stSidebar"] [data-testid="stRadioGroup"]>div{width:100%}
[data-testid="stSidebar"] [data-testid="stRadioOption"]{display:block;width:100%;box-sizing:border-box;min-height:2.6rem;margin:0;padding:.55rem .8rem .55rem calc(.8rem - 3px);border-radius:8px;border-left:3px solid transparent;cursor:pointer;font-size:.92rem;font-weight:500;text-align:left}
[data-testid="stSidebar"] [data-testid="stRadioOption"]>div{display:flex;align-items:center;justify-content:flex-start}
[data-testid="stSidebar"] [data-testid="stRadioOption"]>div>div:first-child{display:none}
[data-testid="stSidebar"] [data-testid="stRadioOption"]:hover{background:rgba(255,255,255,.08)}
[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected]{background:rgba(184,230,75,.15);border-left-color:var(--lime);font-weight:700}
[data-testid="stSidebar"] [data-testid="stRadioOption"] [data-testid="stMarkdownContainer"] p{display:flex;align-items:center;gap:.7rem;margin:0;text-align:left}
[data-testid="stSidebar"] [data-testid="stRadioOption"] [data-testid="stIconMaterial"]{font-size:1.25rem}
[data-testid="stSidebar"] .stButton>button,[data-testid="stSidebar"] .stButton>button *{justify-content:flex-start!important;text-align:left!important}
[data-testid="stSidebar"] .stButton>button{background:transparent;border:0;border-left:3px solid transparent;min-height:2.6rem;padding:.35rem .8rem .35rem calc(.8rem - 3px);gap:.7rem}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.08)}
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button{background:var(--g7);color:#fff;border:0;border-radius:10px;font-weight:600;min-height:2.7rem}
.stButton>button:hover,.stDownloadButton>button:hover{background:var(--g9);color:#fff}
.stButton>button:disabled{background:#cfd8cd;color:#fff}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:.9rem 1.1rem;height:100%}
.card small{display:block;color:var(--mute);font-size:.78rem;font-weight:500;margin-bottom:.15rem}
.card b{display:block;font-size:1.35rem;font-weight:800;color:var(--g9);font-variant-numeric:tabular-nums}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.8rem}
.net{background:var(--g9);border-radius:18px;padding:1.3rem 1.6rem;color:#cfe3d6}
.net .nt{display:flex;justify-content:space-between;align-items:center}
.net span{font-size:.85rem;font-weight:600}
.net b{display:block;font-size:2.6rem;font-weight:800;color:var(--lime);line-height:1.15;font-variant-numeric:tabular-nums}
.net small{display:block;color:#9fc3ad;font-size:.8rem;margin-top:.25rem}
.pill{display:inline-block;padding:.12rem .65rem;border-radius:99px;font-size:.75rem;font-weight:700}
.p-w{background:#fff3cf;color:#7a5600}.p-o{background:#e3f4d0;color:#1f6b2e}.p-x{background:#eee;color:#666}
.demo{background:#fff3cf;color:#7a5600;border-radius:10px;padding:.4rem .9rem;font-size:.82rem;margin-bottom:.8rem}
.brand{font-weight:800;font-size:1.25rem;color:var(--g9)}
.brand span{display:block;font-weight:500;font-size:.75rem;color:var(--mute)}
.bar{height:6px;background:var(--g1);border-radius:9px;margin-top:.5rem}.bar i{display:block;height:100%;background:var(--g7);border-radius:9px}
.bc{font-size:.74rem;color:var(--mute);margin-bottom:.3rem}.bc b{color:var(--g9);font-weight:600}
.sec{margin:1.5rem 0 .6rem}.sec b{font-size:1rem;font-weight:700;color:var(--g9)}.sec span{margin-left:.6rem;font-size:.78rem;color:var(--mute)}
.fin{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:.8rem}
.fc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem}
.fc small{display:block;color:var(--mute);font-size:.76rem;font-weight:500}
.fc b{display:block;font-size:1.3rem;font-weight:700;color:var(--ink);margin:.25rem 0 .2rem;font-variant-numeric:tabular-nums}
.fc i{display:block;font-style:normal;font-size:.74rem;color:var(--mute);line-height:1.4}
.fc.main{background:var(--g9);border-color:var(--g9)}.fc.main small,.fc.main i{color:#a9cbb6}.fc.main b{color:var(--lime);font-size:1.9rem;font-weight:800}
.ops{display:grid;grid-template-columns:repeat(3,1fr);background:#fff;border:1px solid var(--line);border-radius:12px}
.ops>div{padding:.85rem 1.1rem;border-right:1px solid var(--line)}.ops>div:last-child{border:0}
.ops small{display:block;color:var(--mute);font-size:.76rem}.ops b{font-size:1.25rem;font-weight:700;color:var(--g9);margin-right:.4rem}
.tw{overflow-x:auto}.tbl{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid var(--line);border-radius:12px;font-size:.84rem}
.tbl th{text-align:left;color:var(--mute);font-weight:600;font-size:.72rem;padding:.55rem .8rem;border-bottom:1px solid var(--line);background:#FAFBF8}
.tbl td{padding:.55rem .8rem;border-bottom:1px solid #EEF2EC}.tbl tr:last-child td{border-bottom:0}.tbl .r{text-align:right;font-variant-numeric:tabular-nums}
.empty{background:#fff;border:1px dashed #cfdacd;border-radius:12px;padding:1.3rem;text-align:center;color:var(--mute);font-size:.88rem}
[data-testid="stMain"] [data-testid="stBaseButton-secondary"]{background:#fff;color:var(--g9);border:1px solid #c5d6c9;border-radius:8px}
[data-testid="stMain"] [data-testid="stBaseButton-secondary"]:hover{background:var(--g1);color:var(--g9);border-color:var(--g7)}
[data-testid="stMain"] [data-testid="stBaseButton-primary"]{background:var(--g7);color:#fff;border:0;border-radius:8px}
[data-testid="stMain"] [data-testid="stBaseButton-primary"]:hover{background:var(--g9)}
[data-testid="stMain"] [data-testid="stBaseButton-primary"]:disabled{background:#cfd8cd;color:#fff}
[data-testid="stMain"] [data-testid="stPlotlyChart"],[data-testid="stMain"] [data-testid="stDataFrame"],[data-testid="stMain"] [data-testid="stExpander"]{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
[data-testid="stMain"] [data-baseweb="select"]>div,[data-testid="stMain"] [data-baseweb="input"]{border-radius:8px}
@media(max-width:900px){.fin{grid-template-columns:1fr 1fr}.fin .main{grid-column:1/-1}.ops{grid-template-columns:1fr}.ops>div{border-right:0;border-bottom:1px solid var(--line)}.ops>div:last-child{border-bottom:0}}
/* ===== kontras area konten (variabel baru; variabel lama milik sidebar tidak diubah) ===== */
:root{--pg:#EEF2EC;--cd:#FFFFFF;--bd:#D8E2D7;--ttl:#174F38;--ac:#2F855A;--bdg:#E1F2D5;--sec:#748176;--sh:0 2px 8px rgba(23,79,56,.05)}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:var(--pg)}
h1,h2,h3,.hd h1,.sec b,.bc b{color:var(--ttl)}
.card,.fc,.ops,.tbl,.hd .rt,[class*="st-key-trx"],[class*="st-key-jbox"],[class*="st-key-loginbox"]{background:var(--cd);border:1px solid var(--bd)!important;box-shadow:var(--sh)}
.card,.fc,.ops,.tbl,[class*="st-key-trx"],[class*="st-key-jbox"],[class*="st-key-loginbox"]{border-radius:16px}
.empty{background:var(--cd);border:1px dashed #B9CBB8;box-shadow:var(--sh);border-radius:16px;color:var(--sec)}
.fc.main{background:var(--ttl);border-color:var(--ttl)!important;box-shadow:0 2px 10px rgba(23,79,56,.18)}
.net{box-shadow:0 2px 10px rgba(23,79,56,.18)}
.card b,.fc b,.ops b{color:var(--ttl)}
.card small,.fc small,.ops small,.hd p,.bc,.sec span,.tbl th,.hd .rt{color:var(--sec)}
.ops>div{border-right:1px solid var(--bd)}
.tbl th{background:#F6F9F4;border-bottom:1px solid var(--bd)}.tbl td{border-bottom:1px solid #E6EDE4}
.p-o{background:var(--bdg);color:var(--ttl)}
.bar{background:var(--bdg)}.bar i{background:var(--ac)}
[data-testid="stMain"] [data-testid="stPlotlyChart"],[data-testid="stMain"] [data-testid="stDataFrame"],[data-testid="stMain"] [data-testid="stExpander"]{background:var(--cd);border:1px solid var(--bd);border-radius:16px;box-shadow:var(--sh);overflow:hidden}
[data-testid="stMain"] [data-baseweb="input"],[data-testid="stMain"] [data-baseweb="base-input"],[data-testid="stMain"] [data-baseweb="select"]>div,[data-testid="stMain"] [data-baseweb="textarea"]{background:var(--cd);border-color:var(--bd)}
[data-testid="stMain"] [data-testid="stBaseButton-secondary"]{border-color:#B9CBB8}
.lg{text-align:center;margin:.2rem 0 1.1rem}
.lg img{display:block;width:150px;max-width:52%;height:auto;aspect-ratio:1/1;object-fit:contain;border-radius:20px;margin:0 auto .5rem}
.lg b{display:block;font-size:1.3rem;font-weight:800;color:var(--ttl);line-height:1.25}
.lg span{display:block;margin-top:.2rem;font-size:.9rem;color:var(--sec)}
.lg em{display:block;margin-top:.45rem;font-style:normal;font-size:.8rem;color:var(--sec)}
.lg i{display:block;margin-top:.55rem;font-style:normal;font-size:.78rem;color:var(--sec)}
.lgt{font-size:.8rem;font-weight:600;color:var(--sec);margin:.2rem 0 .4rem}
[class*="st-key-rolebox"]{background:#F3F8F0;border:1px solid var(--bd)!important;border-radius:12px}
/* ===== sidebar menempel ke tepi atas dan memenuhi tinggi layar (hanya posisi/ukuran, bukan tampilan) ===== */
html,body{margin:0;padding:0}
[data-testid="stApp"],[data-testid="stAppViewContainer"]{margin:0;padding:0;border:0;top:0}
[data-testid="stSidebar"]{top:0!important;margin:0!important;border:0!important;min-height:100vh;min-height:100dvh}
[data-testid="stSidebarContent"]{min-height:100vh;min-height:100dvh}
header[data-testid="stHeader"]{border:0;box-shadow:none}
.notice{background:#FFF8E1;border:1px solid #F0DFA6;border-radius:12px;padding:.7rem 1rem;margin:.6rem 0;font-size:.88rem;color:#5c4a00}
.notice b{color:#5c4a00}.notice .tw{margin-top:.5rem}
[class*="st-key-opsi"],[class*="st-key-wrq"]{background:var(--cd);border:1px solid var(--bd)!important;border-radius:16px;box-shadow:var(--sh)}
@media(max-width:640px){.block-container{padding:3.2rem .8rem 3rem}.net b{font-size:2.1rem}.hd h1{font-size:1.3rem}}
/* ===== area konten kanan: gaya tenang ala SaaS keuangan (hanya tampilan) ===== */
:root{--forest:#14543B;--emer:#21834F;--lime2:#B5E83B;--soft:#EAF3EA;--off:#F4F7F1;--sh1:0 1px 2px rgba(20,84,59,.08),0 2px 6px rgba(20,84,59,.04)}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:var(--off)}
.block-container{padding-top:2.4rem}
.hd{align-items:center;margin-bottom:1.4rem;padding-bottom:1rem;border-bottom:1px solid var(--bd)}
.hd h1{font-size:1.6rem;font-weight:700;letter-spacing:-.015em;line-height:1.2}
.hd p{font-size:.9rem;margin-top:.3rem;line-height:1.5}
.bc{font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;font-weight:500;margin-bottom:.4rem}
.hd .rt{display:inline-flex;align-items:center;gap:.45rem;font-size:.8rem;font-weight:600;color:var(--forest);background:#fff;border:1px solid var(--bd);box-shadow:none;padding:.4rem .9rem}
.hd .rt::before{content:"";width:14px;height:14px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2314543B' stroke-width='2' stroke-linecap='round'%3E%3Crect x='3' y='5' width='18' height='16' rx='3'/%3E%3Cpath d='M3 10h18M8 3v4M16 3v4'/%3E%3C/svg%3E") center/contain no-repeat}
.sec{margin:1.8rem 0 .75rem;display:flex;align-items:baseline;flex-wrap:wrap}
.sec b{font-size:1rem;font-weight:700;letter-spacing:-.005em}
.ic{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:9px}
.ic svg{width:17px;height:17px}
/* ===== SISTEM WARNA CARD: semua card bergradasi hijau (tidak ada yang putih / memudar ke putih) ===== */
.fin .f1,.card,.grid .card:nth-child(4n+1){--a:#14543B;--b:#21834F;--t:#D5EADD;--n:#B5E83B;--s:#B3D5C0;--chip:rgba(255,255,255,.14);--ic:#B5E83B}
.fin .f2,.grid .card:nth-child(4n+2){--a:#176B49;--b:#369B65;--t:#E3F3E9;--n:#FFFFFF;--s:#CDEAD8;--chip:rgba(255,255,255,.18);--ic:#FFFFFF}
.fin .f3,.grid .card:nth-child(4n+3){--a:#4DA574;--b:#8CC29E;--t:#123F29;--n:#0A3322;--s:#1D5239;--chip:rgba(255,255,255,.45);--ic:#14543B}
.fin .f4,.grid .card:nth-child(4n+4){--a:#86BD98;--b:#A8D5B5;--t:#14472F;--n:#0C3724;--s:#235139;--chip:rgba(255,255,255,.5);--ic:#14543B}
.ops .o1{--a:#176B49;--b:#369B65;--t:#E3F3E9;--n:#FFFFFF;--s:#CDEAD8;--chip:rgba(255,255,255,.18);--ic:#FFFFFF}
.ops .o2{--a:#4DA574;--b:#8CC29E;--t:#123F29;--n:#0A3322;--s:#1D5239;--chip:rgba(255,255,255,.45);--ic:#14543B}
.ops .o3{--a:#86BD98;--b:#A8D5B5;--t:#14472F;--n:#0C3724;--s:#235139;--chip:rgba(255,255,255,.5);--ic:#14543B}
.fin .fc,.ops>div,.grid .card,.card{background:linear-gradient(135deg,var(--a),var(--b));border:1px solid rgba(255,255,255,.14)!important;border-left-width:1px!important;box-shadow:0 1px 2px rgba(20,84,59,.18),0 3px 8px rgba(20,84,59,.1);border-radius:14px}
.fin .fc small,.ops small,.card small{color:var(--t)}
.fin .fc b,.ops b,.card b{color:var(--n)}
.fin .fc i,.card i{color:var(--s)}
.fin .fc .ic,.ops .ic{background:var(--chip);color:var(--ic)}
.fin{gap:.9rem;grid-template-columns:repeat(4,minmax(0,1fr))}
.fin .fc{position:relative;display:flex;flex-direction:column;min-width:0;padding:1rem 1.1rem}
.fin .fc .fh{display:flex;align-items:center;gap:.6rem;margin-bottom:.85rem;min-height:32px}
.fin .fc .fh .ic{order:-1}
.fin .fc small{font-size:.8rem;font-weight:600;line-height:1.25;margin:0}
.fin .fc b{font-size:clamp(1.3rem,2vw,1.65rem);font-weight:700;letter-spacing:-.015em;line-height:1.15;margin:0 0 .3rem;overflow-wrap:anywhere}
.fin .fc i{font-size:.75rem;line-height:1.45}
.ops{background:transparent;border:0!important;box-shadow:none;border-radius:0;gap:.9rem}
.ops>div{display:flex;align-items:center;gap:.85rem;box-sizing:border-box;min-height:4.6rem;padding:.9rem 1.1rem;min-width:0}
.ops>div>div{min-width:0;line-height:1.3}
.ops .ic{width:38px;height:38px;border-radius:10px}
.ops .ic svg{width:19px;height:19px}
.ops small{font-size:.78rem;font-weight:600;margin-bottom:.1rem}
.ops b{display:inline-block;vertical-align:middle;font-size:1.5rem;font-weight:700;line-height:1.2;letter-spacing:-.015em;margin-right:.5rem}
.grid{gap:.9rem}
.grid .card,.card{position:relative;padding:.95rem 1.1rem;height:auto}
.card small{font-size:.78rem;font-weight:600;margin-bottom:.15rem}
.card b{font-size:1.45rem;font-weight:700;letter-spacing:-.015em;overflow-wrap:anywhere}
.net{background:linear-gradient(135deg,#14543B,#21834F);border-radius:14px;box-shadow:0 1px 2px rgba(20,84,59,.2),0 3px 8px rgba(20,84,59,.12)}
/* kartu berisi (riwayat, persetujuan, penarikan, opsi, form) dan empty state: hijau muda yang tetap hijau */
[class*="st-key-trx"],[class*="st-key-wrq"],[class*="st-key-opsi"],[class*="st-key-rolebox"],[class*="st-key-jbox"],[class*="st-key-loginbox"],[data-testid="stMain"] [data-testid="stExpander"],.empty,.es{background:linear-gradient(135deg,#C4E3CD 0%,#A8D5B5 100%)!important;border:1px solid rgba(20,84,59,.16)!important;border-radius:14px;box-shadow:0 1px 2px rgba(20,84,59,.12),0 3px 8px rgba(20,84,59,.06);color:#0F3F2A}
[data-testid="stMain"] [data-testid="stExpander"] details,[data-testid="stMain"] [data-testid="stExpander"] summary{background:transparent!important}
[class*="st-key-trx"] [data-testid="stCaptionContainer"],[class*="st-key-wrq"] [data-testid="stCaptionContainer"],[class*="st-key-opsi"] [data-testid="stCaptionContainer"],[class*="st-key-rolebox"] [data-testid="stCaptionContainer"],[class*="st-key-jbox"] [data-testid="stCaptionContainer"],[class*="st-key-loginbox"] [data-testid="stCaptionContainer"]{color:#24563E!important}
.lg span,.lg em,.lg i,.lgt{color:#24563E}
.empty{color:#24563E;border-style:solid}
/* analitik */
[data-testid="stMain"] [data-testid="stButtonGroup"]{display:inline-flex;background:#BFE0C9;border:1px solid rgba(20,84,59,.18);border-radius:11px;padding:3px;gap:2px;width:auto}
[data-testid="stMain"] [data-testid="stButtonGroup"] button{background:transparent!important;border:0!important;border-radius:8px;color:#14472F!important;font-weight:600;min-height:2.1rem;padding:.2rem 1rem;box-shadow:none}
[data-testid="stMain"] [data-testid="stButtonGroup"] button:hover{background:rgba(255,255,255,.45)!important}
[data-testid="stMain"] [data-testid="stButtonGroup"] button[data-testid="stBaseButton-segmented_controlActive"],[data-testid="stMain"] [data-testid="stButtonGroup"] button[kind="segmented_controlActive"],[data-testid="stMain"] [data-testid="stButtonGroup"] button[aria-pressed="true"],[data-testid="stMain"] [data-testid="stButtonGroup"] button[aria-checked="true"]{background:var(--forest)!important;color:#fff!important;box-shadow:0 1px 3px rgba(20,84,59,.25)}
[data-testid="stMain"] [data-testid="stButtonGroup"] button[data-testid="stBaseButton-segmented_controlActive"] *,[data-testid="stMain"] [data-testid="stButtonGroup"] button[kind="segmented_controlActive"] *,[data-testid="stMain"] [data-testid="stButtonGroup"] button[aria-pressed="true"] *,[data-testid="stMain"] [data-testid="stButtonGroup"] button[aria-checked="true"] *{color:#fff!important}
[data-testid="stMain"] [data-testid="stPlotlyChart"]{padding:.5rem .4rem .2rem;border-radius:14px;box-shadow:var(--sh1)}
.es{display:flex;flex-direction:column;align-items:center;text-align:center;padding:2rem 1.4rem;margin-top:.5rem}
.es .ic{width:52px;height:52px;border-radius:14px;background:rgba(255,255,255,.55);color:var(--forest);margin-bottom:.9rem}
.es .ic svg{width:25px;height:25px}
.es b{font-size:1rem;font-weight:700;color:var(--forest)}
.es p{margin:.35rem 0 0;max-width:30rem;font-size:.86rem;line-height:1.55;color:#24563E}
/* ===== bagian atas sidebar: identitas aplikasi | identitas pengguna | menu ===== */
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding:1rem .8rem .8rem}
.bx{display:flex;align-items:center;gap:.7rem;box-sizing:border-box;width:100%;margin:0;padding:.1rem 1.9rem .95rem .8rem;border-bottom:1px solid rgba(255,255,255,.12)}
.bx img{flex:0 0 44px;width:44px;height:44px;border-radius:11px}
.bx b{font-size:.98rem;font-weight:700;letter-spacing:-.005em;line-height:1.2}
.bx span{font-size:.66rem;line-height:1.3;margin-top:.15rem;white-space:nowrap;color:#a9cbb6}
.me{box-sizing:border-box;width:100%;margin:0 0 .6rem;padding:.9rem .8rem .9rem;border-bottom:1px solid rgba(255,255,255,.12)}
.me b{font-size:.92rem;font-weight:600;line-height:1.3}
.me span{display:block;margin-top:.15rem;font-size:.72rem;line-height:1.35;color:#a9cbb6}
[data-testid="stSidebar"] [data-testid="stRadio"],[data-testid="stSidebar"] [data-testid="stRadio"]>div{width:100%}
/* ===== RESPONSIVE: tablet (<=1024px) dan HP (<=640px); desktop tidak berubah ===== */
.tw{max-width:100%;-webkit-overflow-scrolling:touch}
.grid>.card{height:auto}.tw+.grid,.tw+.tw{margin-top:.8rem}
.card b,.fc b,.ops b,.net b{overflow-wrap:anywhere}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{max-width:100vw;overflow-x:hidden}
[data-testid="stMain"] [data-testid="stMarkdownContainer"],[data-testid="stMain"] [data-testid="stElementContainer"]{min-width:0;max-width:100%}
[class*="st-key-srow"]{border-bottom:1px solid var(--bd)}
@media(max-width:1024px){
 .block-container{max-width:100%;padding:3.4rem 1.2rem 3rem}
 [data-testid="stSidebar"][aria-expanded="true"]{width:min(17rem,86vw)!important;min-width:0!important;max-width:86vw!important}
 [data-testid="stExpandSidebarButton"]{background:#fff;border:1px solid var(--bd);border-radius:10px;min-width:44px;min-height:44px;box-shadow:var(--sh)}
 [data-testid="stSidebar"] [data-testid="stSidebarHeader"] button{min-width:44px;min-height:44px}
 [data-testid="stSidebar"] [data-testid="stRadioOption"],[data-testid="stSidebar"] button{min-height:2.9rem}
 .grid{grid-template-columns:repeat(2,minmax(0,1fr))}
 .fin{grid-template-columns:repeat(2,minmax(0,1fr))}.fin .main{grid-column:1/-1}
 [data-testid="stMain"] [data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:.7rem!important}
 [data-testid="stMain"] [data-testid="stColumn"]{flex:1 1 calc(50% - .7rem)!important;min-width:calc(50% - .7rem)!important;width:auto!important}
 [data-testid="stMain"] .stButton>button,[data-testid="stMain"] .stDownloadButton>button,[data-testid="stMain"] .stFormSubmitButton>button{min-height:2.9rem}
 [data-testid="stMain"] [data-baseweb="input"] input,[data-testid="stMain"] [data-baseweb="select"] input,[data-testid="stMain"] textarea{font-size:16px}
}
@media(max-width:640px){
 .block-container{padding:3.4rem .75rem 2.5rem}
 .hd{align-items:flex-start;margin-bottom:.9rem}.hd .rt{align-self:flex-start}
 .hd p{font-size:.84rem}
 .grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:.6rem}
 .card{padding:.75rem .85rem}.card b{font-size:1.08rem}.card small{font-size:.74rem}
 .fin{grid-template-columns:repeat(2,minmax(0,1fr));gap:.6rem}.fc{padding:.8rem .85rem}.fc b{font-size:1.05rem}.fc.main b{font-size:1.6rem}
 .net{padding:1.1rem 1.1rem}
 .tbl{font-size:.8rem;min-width:30rem}.tbl th,.tbl td{white-space:nowrap;padding:.5rem .65rem}
 [data-testid="stMain"] [data-testid="stColumn"]{flex:1 1 100%!important;min-width:100%!important}
 [class*="st-key-srow"]{background:linear-gradient(135deg,#C4E3CD,#A8D5B5);border:1px solid rgba(20,84,59,.16);border-radius:14px;padding:.7rem .75rem .5rem;margin-bottom:.6rem;box-shadow:0 1px 2px rgba(20,84,59,.12)}
 [class*="st-key-srow"] [data-testid="stHorizontalBlock"]{gap:.5rem!important}
 [data-testid="stMain"] .stButton>button,[data-testid="stMain"] .stDownloadButton>button{width:100%}
 [class*="st-key-loginbox"] [data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;gap:.4rem!important}
 [class*="st-key-loginbox"] [data-testid="stColumn"]{flex:1 1 0!important;min-width:0!important}
 [class*="st-key-loginbox"] .stButton>button{padding:.3rem .25rem;font-size:.78rem;gap:.2rem}
 [class*="st-key-loginbox"] [data-testid="stColumn"] .stButton>button p{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
 .lg img{width:130px;max-width:46%}.lg b{font-size:1.15rem}
 [data-testid="stMain"] [data-testid="stPlotlyChart"]{max-width:100%}
}
@media(max-width:640px){.hd h1{font-size:1.35rem}.fin{gap:.6rem}.fin .f4{grid-column:1/-1}.fin .fc{padding:.85rem .9rem}.fin .fc .fh{margin-bottom:.6rem}.fin .fc .ic{width:28px;height:28px;border-radius:8px}.fin .fc .ic svg{width:15px;height:15px}.fin .fc i{font-size:.7rem}.ops{gap:.6rem}.ops>div{padding:.8rem .95rem}.ops b{font-size:1.5rem}.es{padding:1.6rem 1rem}}
@media(max-width:380px){.block-container{padding:3.4rem .6rem 2.5rem}.fc b{font-size:.98rem}.hd h1{font-size:1.2rem}}
</style>""", unsafe_allow_html=True)

S = st.session_state
BLN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
HR = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
JENIS0 = [("Kardus", "kg", 2000), ("Emberan", "kg", 1700), ("Besi", "kg", 4000), ("Le Mineral", "kg", 800), ("Buku", "kg", 1000),
          ("Gelas botol", "kg", 2000), ("Kaleng", "kg", 2500), ("Kertas semen", "kg", 500), ("Duplek", "kg", 500), ("Stal", "kg", 3500),
          ("Emberan hitam", "kg", 1200), ("Botol beling", "kg", 500), ("Aki", "kg", 10000), ("Galon aqua", "pcs", 5000), ("Botol plastik", "kg", 1500)]


def rp(n): n = int(round(n)); return ("-" if n < 0 else "") + "Rp" + f"{abs(n):,}".replace(",", ".")
def fmt(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".").rstrip("0").rstrip(",")
def tgl(iso): d = date.fromisoformat(iso); return f"{d.day} {BLN[d.month - 1][:3]} {d.year}"
def now(): return datetime.now().strftime("%Y-%m-%d %H:%M")
def pill(s): return f'<span class="pill {"p-o" if s in ("Disetujui", "Aktif", "Selesai") else "p-w" if s.startswith("Menunggu") else "p-x"}">{s}</span>'


DB_PATH = os.environ.get("BANKSAMPAH_DB", os.path.join("data", "banksampah.db"))


def new_db():
    return dict(types=[dict(nama=n, satuan=s, harga=h, aktif=True) for n, s, h in JENIS0], hist=[], users=[], dep=[], wd=[], sales=[], exp=[], seq=0)


@st.cache_resource
def _store(path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    con = sqlite3.connect(path, check_same_thread=False)
    con.execute("CREATE TABLE IF NOT EXISTS snapshot (id INTEGER PRIMARY KEY CHECK (id = 1), data TEXT NOT NULL, diubah TEXT)")
    row = con.execute("SELECT data FROM snapshot WHERE id = 1").fetchone()
    return dict(con=con, db=json.loads(row[0]) if row else new_db(), lock=threading.RLock(), hash=None, gagal={})


ST = _store(DB_PATH)
D = ST["db"]  # satu data bersama untuk semua pengguna dan semua sesi
D.setdefault("wr", [])  # pengajuan penarikan saldo
D.setdefault("pengaturan", {"wa": ""})


def simpan_jika_berubah():
    txt = json.dumps(D, ensure_ascii=False, sort_keys=True)
    h = hashlib.sha256(txt.encode()).hexdigest()
    if h != ST["hash"]:
        with ST["lock"]:
            ST["con"].execute("INSERT OR REPLACE INTO snapshot (id, data, diubah) VALUES (1, ?, ?)", (txt, now()))
            ST["con"].commit()
        ST["hash"] = h


simpan_jika_berubah()  # menyimpan perubahan dari proses sebelumnya


# ---------- kata sandi: hanya hash scrypt bergaram yang disimpan ----------
def hash_pw(p):
    salt = secrets.token_bytes(16)
    return "scrypt$" + salt.hex() + "$" + hashlib.scrypt(p.encode(), salt=salt, n=2**14, r=8, p=1).hex()


def cek_pw(p, simpan):
    try:
        _, salt, h = simpan.split("$")
        return hmac.compare_digest(hashlib.scrypt(p.encode(), salt=bytes.fromhex(salt), n=2**14, r=8, p=1).hex(), h)
    except Exception:
        return False


def pw_baru(): return secrets.token_urlsafe(9)
def pw_valid(p): return len(p) >= 8


def nid():
    D["seq"] += 1
    return D["seq"]


# ---------- logika inti ----------
def total(items): return sum(i["jml"] * i["harga"] for i in items)
def ok_dep(): return [d for d in D["dep"] if d["status"] == "Disetujui"]
def aktif_sales(): return [s for s in D["sales"] if s["status"] == "Aktif"]
def inr(t, a, b): return a.isoformat() <= t <= b.isoformat()


def saldo(email):
    return (sum(total(d["items"]) for d in ok_dep() if d["email"] == email and d["metode"] == "Tabung")
            - sum(w["jumlah"] for w in D["wd"] if w["email"] == email))


def stok():
    r = {}
    for d in ok_dep():
        if not d["sold"]:
            for i in d["items"]:
                r[i["jenis"]] = r.get(i["jenis"], 0) + i["jml"]
    return r


def netkas(a, b):
    beli = sum(total(d["items"]) for d in ok_dep() if inr(d["tgl"], a, b))
    jual = sum(total(s["items"]) for s in aktif_sales() if inr(s["tgl"], a, b))
    out = sum(e["jumlah"] for e in D["exp"] if inr(e["tgl"], a, b))
    return beli, jual, out, jual - beli - out


def tipe(nama): return next(t for t in D["types"] if t["nama"] == nama)
def cari(email): return next((u for u in D["users"] if u["email"] == (email or "").lower() and u["aktif"]), None)
def nasabah_aktif(): return [u for u in D["users"] if u["peran"] == "Nasabah" and u["aktif"]]
def catat(d, teks): d["log"].append(f"{now()} · {teks}")


def tabel_items(items):
    return pd.DataFrame([dict(Jenis=i["jenis"], Jumlah=f'{fmt(i["jml"])} {i["satuan"]}', Harga=rp(i["harga"]), Subtotal=rp(i["jml"] * i["harga"])) for i in items])


_SV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICO = {"wallet": '<path d="M3 7a2 2 0 0 1 2-2h12v4"/><path d="M3 7v10a2 2 0 0 0 2 2h14a1 1 0 0 0 1-1v-3"/><path d="M21 9H7a2 2 0 0 0 0 4h14z"/>',
       "bag": '<path d="M6 7h12l1 13H5z"/><path d="M9 7a3 3 0 0 1 6 0"/>',
       "truck": '<path d="M3 6h11v10H3z"/><path d="M14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
       "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
       "check": '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 12l3 3 5-6"/>',
       "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
       "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><path d="M16 5.5a3 3 0 0 1 0 5.6M18 14c2 .6 3 2.3 3 5"/>',
       "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>'}
def ico(n): return f'<span class="ic">{_SV}{ICO[n]}</svg></span>'


def kartu(label, nilai): return f'<div class="card"><small>{label}</small><b>{nilai}</b></div>'
def grid(items): return '<div class="grid">' + "".join(kartu(l, v) for l, v in items) + "</div>"


DESC = {"Input Setoran": "Catat sampah yang ditimbang. Total dihitung otomatis.", "Kelola Setoran": "Periksa, edit, atau batalkan setoran nasabah.",
        "Nasabah": "Daftar nasabah, saldo, dan riwayat transaksi.", "Penarikan Saldo": "Proses pengajuan penarikan dari nasabah dan catat penarikan langsung.",
        "Penjualan Pengepul": "Catat hasil timbangan dan harga jual saat pengepul datang.", "Pengeluaran Operasional": "Biaya seperti bensin dan perlengkapan.",
        "Stok Sampah": "Perkiraan sampah yang terkumpul dan belum terjual.", "Jenis Sampah & Harga": "Atur harga beli dan jenis sampah yang diterima.",
        "Data Pengguna": "Daftarkan nasabah, pengepul, dan pengurus.", "Laporan": "Rekap per periode, bisa diunduh dalam CSV.", "Pengaturan": "Status aplikasi dan data demo.",
        "Persetujuan Setoran": "Cocokkan setoranmu dengan hasil timbangan, lalu setujui.", "Riwayat Setoran": "Semua setoran milikmu dan statusnya.",
        "Saldo Saya": "Saldo tabungan dan mutasinya.", "Riwayat Penarikan": "Pengajuan dan riwayat penarikan saldomu.", "Profil Saya": "Data akunmu.",
        "Perkiraan Stok": "Sampah yang terkumpul dan belum diangkut.", "Riwayat Penjualan": "Laporan pengangkutan yang terkait denganmu."}


def head(title, desc="", right=None):
    t = date.today()
    right = f"{t.day} {BLN[t.month - 1]} {t.year}" if right is None else right
    r = f'<div class="rt">{right}</div>' if right else ""
    bc = f'<div class="bc">EcoLedger Darling / <b>{title}</b></div>' if (title in DESC or title == "Ringkasan Dashboard") else ""
    st.markdown(f'<div class="hd"><div>{bc}<h1>{title}</h1><p>{desc or DESC.get(title, "")}</p></div>{r}</div>', unsafe_allow_html=True)


# ---------- formulir baris setoran ----------
def add_row(key, item):
    rid = nid()
    S[key].append(rid)
    if item:
        S[f"j{rid}"] = item["jenis"]
        S[f"q{rid}"] = float(item["jml"])


def form_rows(ctx, dep=None):
    key = f"rows_{ctx}"
    if key not in S:
        S[key] = []
        for i in (dep["items"] if dep else [None]):
            add_row(key, i)
    pre = {i["jenis"]: i["harga"] for i in dep["items"]} if dep else {}
    names = [t["nama"] for t in D["types"] if t["aktif"] or t["nama"] in pre]
    items, seen, dup = [], set(), False
    for rid in list(S[key]):
        with st.container(key=f"srow{ctx}_{rid}"):
            c = st.columns([3, 2, 3, 2])
            kj, kq = f"j{rid}", f"q{rid}"
            j = c[0].selectbox("Jenis", names, key=kj, label_visibility="collapsed", placeholder="Pilih jenis sampah", **({} if kj in S else {"index": None}))
            q = c[1].number_input("Jumlah", min_value=0.0, step=0.5, format="%.2f", key=kq, label_visibility="collapsed", **({} if kq in S else {"value": 0.0}))
            if j:
                t = tipe(j)
                h = pre.get(j, t["harga"])
                c[2].markdown(f'{t["satuan"]} · {rp(h)} → **{rp(q * h)}**' if q > 0 else f'{t["satuan"]} · {rp(h)}')
                if q > 0:
                    dup = dup or j in seen
                    seen.add(j)
                    items.append(dict(jenis=j, satuan=t["satuan"], jml=q, harga=h))
            if c[3].button("Hapus", key=f"x{rid}", icon=":material/delete:"):
                S[key].remove(rid)
                for k in (kj, kq):
                    S.pop(k, None)
                if not S[key]:
                    add_row(key, None)
                st.rerun()
    if dup:
        st.warning("Ada jenis sampah yang dipilih dua kali. Gabungkan jumlahnya jadi satu baris.")
    a, b, _ = st.columns([2, 2, 4])
    if a.button("Tambah baris", icon=":material/add:", key=f"add{ctx}"):
        add_row(key, None)
        st.rerun()
    if b.button("Jenis baru", icon=":material/add_circle:", key=f"jb{ctx}"):
        S.jb = not S.get("jb", False)
    if S.get("jb"):
        with st.container(border=True, key=f"jbox{ctx}"):
            n = st.text_input("Nama jenis sampah", key=f"jn{ctx}")
            u = st.radio("Satuan", ["kg", "pcs"], horizontal=True, key=f"ju{ctx}")
            h = st.number_input("Harga beli dari nasabah (Rp)", min_value=0, step=100, key=f"jh{ctx}")
            s1, s2, _ = st.columns([1, 1, 4])
            if s1.button("Simpan", type="primary", key=f"js{ctx}"):
                if not n.strip() or any(t["nama"].lower() == n.strip().lower() for t in D["types"]):
                    st.error("Nama kosong atau sudah ada.")
                else:
                    D["types"].append(dict(nama=n.strip(), satuan=u, harga=int(h), aktif=True))
                    D["hist"].append(dict(waktu=now(), jenis=n.strip(), lama=0, baru=int(h), oleh=CU["nama"]))
                    S.jb = False
                    st.rerun()
            if s2.button("Batal", key=f"jx{ctx}"):
                S.jb = False
                st.rerun()
    return items, bool(items) and not dup


def reset_rows(ctx):
    for rid in S.pop(f"rows_{ctx}", []):
        for k in (f"j{rid}", f"q{rid}"):
            S.pop(k, None)


# ---------- halaman pengurus ----------
def pg_beranda():
    t = date.today()
    a = t.replace(day=1)
    pb = a - timedelta(days=1)
    pa = pb.replace(day=1)
    beli, jual, out, net = netkas(a, t)
    pbeli, pjual, pout, pnet = netkas(pa, pb)
    ada_lalu = any([pbeli, pjual, pout])
    head("Ringkasan Dashboard", f"Selamat datang, {CU['nama']}. Kondisi kas dan aktivitas Bank Sampah Darling Berseri.", f"Periode {BLN[t.month - 1]} {t.year}")
    notif_wr()
    ok_b = [x for x in ok_dep() if inr(x["tgl"], a, t)]
    nj = len([x for x in aktif_sales() if inr(x["tgl"], a, t)])
    nk = len([e for e in D["exp"] if inr(e["tgl"], a, t)])

    def lalu(v): return f"<i>Bulan lalu {rp(v)}</i>" if ada_lalu else ""
    st.markdown('<div class="fin">'
                f'<div class="fc main f1"><div class="fh"><small>Net Kas Bulan Ini</small>{ico("wallet")}</div><b>{rp(net)}</b><i>Penjualan − Pembelian − Pengeluaran</i>{lalu(pnet)}</div>'
                f'<div class="fc f2"><div class="fh"><small>Pembelian dari Nasabah</small>{ico("bag")}</div><b>{rp(beli)}</b><i>{len(ok_b)} setoran disetujui</i>{lalu(pbeli)}</div>'
                f'<div class="fc f3"><div class="fh"><small>Penjualan ke Pengepul</small>{ico("truck")}</div><b>{rp(jual)}</b><i>{nj} penjualan</i>{lalu(pjual)}</div>'
                f'<div class="fc f4"><div class="fh"><small>Pengeluaran Operasional</small>{ico("receipt")}</div><b>{rp(out)}</b><i>{nk} catatan</i>{lalu(pout)}</div></div>', unsafe_allow_html=True)
    wait = [x for x in D["dep"] if x["status"] == "Menunggu"]
    badge = '<span class="pill p-w">perlu tindakan</span>' if wait else ""
    st.markdown('<div class="sec"><b>Operasional</b></div>'
                f'<div class="ops"><div class="o1">{ico("check")}<div><small>Setoran bulan ini</small><b>{len(ok_b)}</b></div></div>'
                f'<div class="o2">{ico("clock")}<div><small>Menunggu persetujuan</small><b>{len(wait)}</b>{badge}</div></div>'
                f'<div class="o3">{ico("users")}<div><small>Nasabah terdaftar</small><b>{len(nasabah_aktif())}</b></div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec"><b>Analitik Setoran</b></div>', unsafe_allow_html=True)
    per = st.segmented_control("Periode grafik", ["Bulan ini", "30 hari", "Semua"], default="Bulan ini", key="per_graf", label_visibility="collapsed") or "Bulan ini"
    d1 = {"Bulan ini": a, "30 hari": t - timedelta(days=29), "Semua": date.min}[per]
    rows = [x for x in ok_dep() if inr(x["tgl"], d1, t)]
    kg = [(x["tgl"], i["jenis"], i["jml"]) for x in rows for i in x["items"] if i["satuan"] == "kg"]
    if kg:
        LAY = dict(paper_bgcolor="#fff", plot_bgcolor="#fff", height=300, margin=dict(t=44, b=10, l=10, r=10), showlegend=False,
                   font=dict(family="Plus Jakarta Sans", size=12, color="#25372C"), title_font_size=13)
        df = pd.DataFrame(kg, columns=["Tanggal", "Jenis", "Kg"])
        h = df.groupby("Tanggal", as_index=False)["Kg"].sum()
        h["Tanggal"] = pd.to_datetime(h["Tanggal"])
        f = px.area(h, x="Tanggal", y="Kg", title="Berat setoran per hari (kg)", color_discrete_sequence=["#21834F"])
        f.update_traces(line_width=2, fillcolor="rgba(39,131,77,.12)", hovertemplate="%{x|%d %b %Y}<br>%{y:.1f} kg<extra></extra>")
        f.update_layout(**LAY)
        f.update_yaxes(gridcolor="#E3E9E0", title=None)
        f.update_xaxes(title=None, showgrid=False)
        k = df.groupby("Jenis", as_index=False)["Kg"].sum().sort_values("Kg").tail(7)
        f2 = px.bar(k, x="Kg", y="Jenis", orientation="h", title="Komposisi per jenis (kg)", color_discrete_sequence=["#21834F"])
        f2.update_traces(hovertemplate="%{y}: %{x:.1f} kg<extra></extra>")
        f2.update_layout(**LAY)
        f2.update_xaxes(gridcolor="#E3E9E0", title=None)
        f2.update_yaxes(title=None, automargin=True)
        g1, g2 = st.columns([3, 2])
        g1.plotly_chart(f, width="stretch")
        g2.plotly_chart(f2, width="stretch")
        if any(i["satuan"] == "pcs" for x in rows for i in x["items"]):
            st.caption("Barang berasatuan pcs (mis. galon) tidak ikut grafik berat.")
    else:
        st.markdown(f'<div class="es">{ico("chart")}<b>Belum ada transaksi pada periode ini</b><p>Grafik berat setoran dan komposisi jenis sampah akan muncul di sini setelah ada setoran yang disetujui. Coba pilih periode lain di atas.</p></div>', unsafe_allow_html=True)
    b1, b2 = st.columns([3, 2])
    ev = [(x["tgl"], f'Setoran {x["metode"].lower()} · {x["nama"]}', total(x["items"]), x["status"]) for x in D["dep"] if x["status"] != "Dibatalkan"]
    ev += [(w["tgl"], f'Penarikan · {w["nama"]}', w["jumlah"], "Selesai") for w in D["wd"]]
    ev += [(x["tgl"], f'Penjualan · {x["pengepul"]}', total(x["items"]), "Aktif") for x in aktif_sales()]
    ev += [(e["tgl"], f'Pengeluaran · {e["kategori"]}', e["jumlah"], "Tercatat") for e in D["exp"]]
    with b1:
        st.markdown('<div class="sec"><b>Aktivitas Terbaru</b></div>', unsafe_allow_html=True)
        if ev:
            tr = "".join(f'<tr><td>{tgl(a_)}</td><td>{k_}</td><td class="r">{rp(v_)}</td><td>{pill(s_)}</td></tr>' for a_, k_, v_, s_ in sorted(ev, reverse=True)[:6])
            st.markdown(f'<div class="tw"><table class="tbl"><tr><th>Tanggal</th><th>Aktivitas</th><th class="r">Nilai</th><th>Status</th></tr>{tr}</table></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty">Belum ada aktivitas. Mulai dari menu Input Setoran.</div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="sec"><b>Menunggu Persetujuan</b></div>', unsafe_allow_html=True)
        if wait:
            tr = "".join(f'<tr><td>{x["nama"]}</td><td>{tgl(x["tgl"])}</td><td class="r">{rp(total(x["items"]))}</td></tr>' for x in reversed(wait[-4:]))
            st.markdown(f'<div class="tw"><table class="tbl"><tr><th>Nasabah</th><th>Tanggal</th><th class="r">Total</th></tr>{tr}</table></div>', unsafe_allow_html=True)
            st.button("Kelola setoran", on_click=go, args=("Kelola Setoran",))
        else:
            st.markdown('<div class="empty">Tidak ada setoran yang menunggu persetujuan.</div>', unsafe_allow_html=True)

def simpan_setoran(u, items, metode, langsung):
    d = dict(id=nid(), tgl=date.today().isoformat(), email=u["email"], nama=u["nama"], metode=metode, items=items,
             status="Disetujui" if langsung else "Menunggu", sold=None, ver=1, log=[], oleh=CU["nama"], tok=S.tok)
    catat(d, f"Dibuat oleh {CU['nama']}")
    if langsung:
        d["disetujui_oleh"] = f"{CU['nama']} (konfirmasi langsung nasabah di lokasi)"
        d["disetujui_pada"] = now()
        catat(d, "Disetujui: nasabah menyetujui di lokasi, dicatat pengurus")
    D["dep"].append(d)
    return d


def pg_input():
    head("Input Setoran")
    S.setdefault("tok", secrets.token_hex(8))
    d = next((x for x in D["dep"] if x["id"] == S.get("terakhir")), None)
    if d:
        st.success(f"Transaksi #{d['id']} tersimpan: {d['nama']} · {rp(total(d['items']))} · {d['metode']} · {d['status']}")
        st.dataframe(tabel_items(d["items"]), hide_index=True, width="stretch")
        if d["status"] == "Menunggu":
            st.info("Menunggu persetujuan nasabah lewat akunnya. Saldo dan stok belum bertambah.")
        else:
            st.caption(f"Disetujui oleh {d['disetujui_oleh']} pada {d['disetujui_pada']}.")
        if st.button("Selesaikan & Input Nasabah Berikutnya", type="primary"):
            S.terakhir = None
            S.tok = secrets.token_hex(8)
            reset_rows("new")
            st.rerun()
        return
    nas = nasabah_aktif()
    if not nas:
        st.info("Belum ada nasabah. Buat akun nasabah di menu Data Pengguna.")
        return
    nm = st.selectbox("Nasabah yang dilayani", [u["nama"] for u in nas])
    metode = st.radio("Metode", ["Tabung", "Tunai"], horizontal=True)
    st.markdown("**Rincian sampah**")
    items, ok = form_rows("new")
    st.markdown(f'<div class="net"><span>Total setoran</span><b>{rp(total(items))}</b></div>', unsafe_allow_html=True)
    st.write("")
    cara = st.radio("Persetujuan nasabah", ["Nasabah setuju di lokasi", "Nasabah setuju lewat akunnya"], horizontal=True)
    langsung = cara == "Nasabah setuju di lokasi"
    setuju = st.checkbox("Rincian sudah ditunjukkan dan nasabah menyatakan setuju") if langsung else True
    if st.button("Simpan & Setujui" if langsung else "Simpan & Kirim ke Nasabah", type="primary", disabled=not ok or not setuju):
        dup = next((x for x in D["dep"] if x.get("tok") == S.tok), None)
        S.terakhir = dup["id"] if dup else simpan_setoran(next(u for u in nas if u["nama"] == nm), items, metode, langsung)["id"]
        st.rerun()


def pg_kelola():
    head("Kelola Setoran")
    eid = S.get("edit_id")
    if eid:
        d = next(x for x in D["dep"] if x["id"] == eid)
        st.subheader(f"Edit setoran {d['nama']} · {tgl(d['tgl'])}")
        items, ok = form_rows(f"e{eid}", d)
        st.markdown(f'<div class="net"><span>Total baru</span><b>{rp(total(items))}</b></div>', unsafe_allow_html=True)
        a, b, _ = st.columns([2, 1, 3])
        if a.button("Simpan perubahan", type="primary", disabled=not ok):
            d["items"], d["status"], d["ver"] = items, "Menunggu", d["ver"] + 1
            catat(d, f"Diedit oleh {CU['nama']}, menunggu persetujuan ulang")
            reset_rows(f"e{eid}")
            S.edit_id = None
            st.rerun()
        if b.button("Batal"):
            reset_rows(f"e{eid}")
            S.edit_id = None
            st.rerun()
        return
    f = st.selectbox("Status", ["Semua", "Menunggu", "Disetujui", "Dibatalkan"])
    data = [d for d in reversed(D["dep"]) if f == "Semua" or d["status"] == f]
    if not data:
        st.info("Belum ada setoran.")
    for d in data:
        with st.expander(f'{tgl(d["tgl"])} · {d["nama"]} · {rp(total(d["items"]))} · {d["metode"]} · {d["status"]}'):
            st.markdown(pill(d["status"]) + f' versi {d["ver"]}', unsafe_allow_html=True)
            st.dataframe(tabel_items(d["items"]), hide_index=True, width="stretch")
            if d["sold"]:
                st.caption("Sudah masuk penjualan, batalkan penjualannya dulu untuk mengubah setoran ini.")
            elif d["status"] != "Dibatalkan":
                a, b, _ = st.columns([1, 1, 3])
                if a.button("Edit", key=f"e{d['id']}"):
                    S.edit_id = d["id"]
                    st.rerun()
                if b.button("Batalkan", key=f"b{d['id']}"):
                    d["status"] = "Dibatalkan"
                    catat(d, f"Dibatalkan oleh {CU['nama']}")
                    st.rerun()
            st.caption(" | ".join(d["log"]))


def pg_nasabah():
    head("Nasabah")
    nas = nasabah_aktif()
    if not nas:
        st.info("Belum ada nasabah. Daftarkan di menu Data Pengguna.")
        return
    st.dataframe(pd.DataFrame([dict(Nama=u["nama"], Email=u["email"], Saldo=rp(saldo(u["email"]))) for u in nas]), hide_index=True, width="stretch")
    nm = st.selectbox("Lihat riwayat", [u["nama"] for u in nas])
    em = next(u["email"] for u in nas if u["nama"] == nm)
    st.markdown(kartu(f"Saldo {nm}", rp(saldo(em))), unsafe_allow_html=True)
    rows = [dict(Tanggal=tgl(d["tgl"]), Jenis="Setoran " + d["metode"], Rp=rp(total(d["items"])), Status=d["status"]) for d in D["dep"] if d["email"] == em]
    rows += [dict(Tanggal=tgl(w["tgl"]), Jenis="Penarikan", Rp=rp(w["jumlah"]), Status="Selesai") for w in D["wd"] if w["email"] == em]
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    else:
        st.caption("Belum ada transaksi.")


# ---------- pengajuan penarikan saldo ----------
WR_OPEN = ("Menunggu Konfirmasi", "Disetujui", "Menunggu Pengambilan")
WR_INFO = {"Menunggu Konfirmasi": "sedang menunggu konfirmasi pengurus.",
           "Disetujui": "disetujui. Pengurus akan menentukan jadwal pengambilan.",
           "Menunggu Pengambilan": "disetujui. Silakan ambil uangnya ke bank sampah sesuai jadwal."}


def wr_open(email=None): return [r for r in D["wr"] if r["status"] in WR_OPEN and (email is None or r["email"] == email)]
def saldo_tersedia(email): return saldo(email) - sum(r["jumlah"] for r in wr_open(email))


def norm_wa(x):
    d = "".join(c for c in (x or "") if c.isdigit())
    d = "62" + d[1:] if d.startswith("0") else "62" + d if d.startswith("8") else d
    return d if d.startswith("62") and 10 <= len(d) <= 15 else ""


def wa_link(nomor, teks): return "https://wa.me/" + nomor + "?" + urllib.parse.urlencode({"text": teks}, quote_via=urllib.parse.quote)


def pesan_wa(nama, nominal):
    return (f"Assalamu'alaikum, saya {nama}. Saya ingin melakukan penarikan saldo Bank Sampah Darling Berseri sebesar {rp(nominal)}. "
            "Mohon informasi mengenai waktu pengambilan saldo. Terima kasih.")


def kirim_wr(me, j):
    if not me or me["peran"] != "Nasabah":
        return False, "Hanya nasabah yang bisa mengajukan penarikan."
    if j <= 0:
        return False, "Nominal harus lebih dari nol."
    if wr_open(me["email"]):
        return False, "Kamu masih punya pengajuan yang belum selesai. Tunggu sampai selesai atau ditolak."
    if j > saldo_tersedia(me["email"]):
        return False, f"Nominal melebihi saldo tersedia ({rp(saldo_tersedia(me['email']))})."
    r = dict(id=nid(), email=me["email"], nama=me["nama"], jumlah=int(j), status="Menunggu Konfirmasi", diajukan=now(), jadwal="", alasan="", dibayar_pada="", wd=None, log=[])
    catat(r, f"Diajukan oleh {me['nama']} lewat aplikasi")
    D["wr"].append(r)
    return True, f"Pengajuan penarikan {rp(j)} terkirim. Statusnya: menunggu konfirmasi pengurus. Saldo belum berkurang."


def ajukan_wr():
    ok, msg = kirim_wr(cari(S.get("uid")), int(S.get("nominal_wr") or 0))
    S.wr_msg = (ok, msg)
    if ok:
        S.nominal_wr = 0


def proses_wr(wid, aksi, teks="", alasan=""):
    me = cari(S.get("uid"))
    r = next((x for x in D["wr"] if x["id"] == wid), None)

    def gagal(m):
        S.flash = ("error", m)

    if not me or me["peran"] != "Pengurus":
        return gagal("Akses ditolak.")
    if not r or r["status"] not in WR_OPEN:
        return gagal("Pengajuan ini sudah tidak aktif.")
    if aksi == "setujui":
        if r["status"] != "Menunggu Konfirmasi":
            return gagal("Pengajuan ini sudah diproses.")
        if r["jumlah"] > saldo(r["email"]):
            return gagal("Saldo nasabah tidak cukup lagi untuk pengajuan ini.")
        r["status"] = "Disetujui"
        catat(r, f"Disetujui oleh {me['nama']}")
        msg = f"Pengajuan {r['nama']} disetujui."
    elif aksi == "jadwal":
        if r["status"] == "Menunggu Konfirmasi":
            return gagal("Setujui pengajuan dulu sebelum menentukan jadwal.")
        if not teks.strip():
            return gagal("Isi jadwal pengambilan dulu.")
        r["jadwal"], r["status"] = teks.strip(), "Menunggu Pengambilan"
        catat(r, f"Jadwal pengambilan '{r['jadwal']}' ditetapkan oleh {me['nama']}")
        msg = "Jadwal pengambilan disimpan."
    elif aksi == "selesai":
        if r["status"] == "Menunggu Konfirmasi":
            return gagal("Setujui pengajuan dulu sebelum mengonfirmasi pembayaran.")
        if r.get("wd") or r["jumlah"] > saldo(r["email"]):
            return gagal("Pembayaran sudah tercatat, atau saldo nasabah tidak cukup.")
        w = dict(id=nid(), tgl=date.today().isoformat(), waktu=now(), email=r["email"], nama=r["nama"], jumlah=r["jumlah"], oleh=me["nama"], wr=r["id"])
        D["wd"].append(w)
        r["status"], r["dibayar_pada"], r["wd"] = "Selesai", now(), w["id"]
        catat(r, f"Pembayaran dikonfirmasi selesai oleh {me['nama']}; saldo berkurang {rp(r['jumlah'])}")
        msg = f"Pembayaran {rp(r['jumlah'])} untuk {r['nama']} tercatat. Saldo nasabah sudah berkurang."
    else:
        if not alasan.strip():
            return gagal("Isi alasan penolakan.")
        r["status"], r["alasan"] = "Ditolak", alasan.strip()
        catat(r, f"Ditolak oleh {me['nama']}: {r['alasan']}")
        msg = "Pengajuan ditolak. Nasabah akan melihat alasannya."
    S.flash = ("success", msg)


def flash():
    f = S.pop("flash", None)
    if f:
        (st.success if f[0] == "success" else st.error)(f[1])


def ket_wr(r):
    return r["alasan"] if r["status"] == "Ditolak" else (f"Jadwal: {r['jadwal']}" if r["jadwal"] else "-")


def tabel_wr(rows, nasabah=True):
    return pd.DataFrame([{**({"Nasabah": r["nama"]} if nasabah else {}), "Diajukan": r["diajukan"], "Nominal": rp(r["jumlah"]), "Status": r["status"],
                          "Dibayar": r["dibayar_pada"] or "-", "Keterangan": ket_wr(r)} for r in sorted(rows, key=lambda r: r["id"], reverse=True)])


@st.fragment(run_every="15s")
def notif_wr():
    me = cari(S.get("uid"))
    if not me or me["peran"] != "Pengurus":
        return
    baru = [r for r in D["wr"] if r["status"] == "Menunggu Konfirmasi"]
    proses = [r for r in D["wr"] if r["status"] in ("Disetujui", "Menunggu Pengambilan")]
    if not (baru or proses):
        return
    tr = "".join(f'<tr><td>{r["nama"]}</td><td class="r">{rp(r["jumlah"])}</td><td>{r["diajukan"]}</td><td class="r">{rp(saldo(r["email"]))}</td><td>{pill(r["status"])}</td></tr>' for r in (baru + proses)[:4])
    st.markdown(f'<div class="notice"><b>Pengajuan penarikan saldo:</b> {len(baru)} menunggu konfirmasi, {len(proses)} menunggu pembayaran.'
                f'<div class="tw"><table class="tbl"><tr><th>Nasabah</th><th class="r">Nominal</th><th>Diajukan</th><th class="r">Saldo tersedia</th><th>Status</th></tr>{tr}</table></div></div>', unsafe_allow_html=True)
    if st.button("Buka pengajuan penarikan", key="notif_buka"):
        S["goto"] = "Penarikan Saldo"
        st.rerun()


@st.fragment(run_every="15s")
def status_wr(email):
    for r in wr_open(email):
        st.markdown(f'<div class="notice">{pill(r["status"])} Pengajuan penarikan <b>{rp(r["jumlah"])}</b> {WR_INFO[r["status"]]}'
                    + (f' Jadwal: <b>{r["jadwal"]}</b>.' if r["jadwal"] else "") + "</div>", unsafe_allow_html=True)


def kartu_wr(r):
    i = r["id"]
    with st.container(border=True, key=f"wrq{i}"):
        st.markdown(f'**{r["nama"]}** · {rp(r["jumlah"])} ' + pill(r["status"]), unsafe_allow_html=True)
        st.caption(f'Diajukan {r["diajukan"]} · saldo nasabah saat ini {rp(saldo(r["email"]))}' + (f' · jadwal: {r["jadwal"]}' if r["jadwal"] else ""))
        if r["status"] == "Menunggu Konfirmasi":
            if st.button("Setujui pengajuan", key=f"wrs{i}", type="primary"):
                proses_wr(i, "setujui")
                st.rerun()
        else:
            jd = st.text_input("Jadwal pengambilan (mis. Sabtu 10.00 di bank sampah)", value=r["jadwal"], key=f"wrj{i}")
            c = st.columns(2)
            if c[0].button("Simpan jadwal", key=f"wrk{i}"):
                proses_wr(i, "jadwal", teks=jd)
                st.rerun()
            if c[1].button("Konfirmasi Pembayaran Selesai", key=f"wrf{i}", type="primary"):
                proses_wr(i, "selesai")
                st.rerun()
        al = st.text_input("Alasan jika ditolak", key=f"wra{i}")
        if st.button("Tolak pengajuan", key=f"wrt{i}"):
            proses_wr(i, "tolak", alasan=al)
            st.rerun()
        hp = cari_any(r["email"]).get("hp", "")
        if hp:
            isi = f"Assalamu'alaikum {r['nama']}, pengajuan penarikan saldo Anda sebesar {rp(r['jumlah'])} di Bank Sampah Darling Berseri berstatus: {r['status']}." + (f" Jadwal pengambilan: {r['jadwal']}." if r["jadwal"] else "")
            st.link_button("Hubungi nasabah via WhatsApp", wa_link(hp, isi))
        else:
            st.caption("Nomor WhatsApp nasabah belum diisi (isi di menu Data Pengguna).")


def pg_tarik():
    head("Penarikan Saldo")
    flash()
    st.markdown('<div class="sec"><b>Pengajuan dari nasabah</b></div>', unsafe_allow_html=True)
    aktif = wr_open()
    for r in aktif:
        kartu_wr(r)
    if not aktif:
        st.markdown('<div class="empty">Tidak ada pengajuan penarikan yang sedang berjalan.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec"><b>Catat penarikan langsung</b></div>', unsafe_allow_html=True)
    nas = nasabah_aktif()
    if not nas:
        st.info("Belum ada nasabah.")
        return
    nm = st.selectbox("Nasabah", [u["nama"] for u in nas])
    em = next(u["email"] for u in nas if u["nama"] == nm)
    st.markdown(grid([("Saldo saat ini", rp(saldo(em))), ("Saldo tersedia (tanpa pengajuan berjalan)", rp(saldo_tersedia(em)))]), unsafe_allow_html=True)
    j = st.number_input("Jumlah diambil (Rp)", min_value=0, step=1000)
    if st.button("Proses penarikan", type="primary"):
        if j <= 0:
            st.error("Jumlah harus lebih dari nol.")
        elif j > saldo_tersedia(em):
            st.error(f"Jumlah melebihi saldo tersedia ({rp(saldo_tersedia(em))}).")
        else:
            D["wd"].append(dict(id=nid(), tgl=date.today().isoformat(), waktu=now(), email=em, nama=nm, jumlah=int(j), oleh=CU["nama"]))
            st.success(f"Diambil {rp(j)}. Sisa saldo {rp(saldo(em))}.")
    st.markdown('<div class="sec"><b>Riwayat pengajuan</b></div>', unsafe_allow_html=True)
    if D["wr"]:
        st.dataframe(tabel_wr(D["wr"]), hide_index=True, width="stretch")
    else:
        st.caption("Belum ada pengajuan dari nasabah.")
    st.markdown('<div class="sec"><b>Riwayat penarikan</b></div>', unsafe_allow_html=True)
    if D["wd"]:
        st.dataframe(pd.DataFrame([dict(Waktu=w["waktu"], Nasabah=w["nama"], Jumlah=rp(w["jumlah"]), Diproses=w["oleh"], Sumber=f"Pengajuan #{w['wr']}" if w.get("wr") else "Langsung") for w in reversed(D["wd"])]), hide_index=True, width="stretch")
    else:
        st.caption("Belum ada penarikan.")

def pg_jual():
    head("Penjualan Pengepul")
    pg = [u for u in D["users"] if u["peran"] == "Pengepul" and u["aktif"]]
    stk = stok()
    if not pg:
        st.info("Belum ada pengepul. Daftarkan di menu Data Pengguna.")
    elif not stk:
        st.info("Belum ada stok yang disetujui untuk dijual.")
    else:
        pn = st.selectbox("Pengepul yang datang", [u["nama"] for u in pg])
        tg = st.date_input("Tanggal penjualan", date.today())
        last = {}
        for s in aktif_sales():
            for i in s["items"]:
                last[i["jenis"]] = i["harga"]
        df = pd.DataFrame([dict(Jenis=j, Satuan=tipe(j)["satuan"], Perkiraan=round(v, 2), Berat=round(v, 2), Harga=int(last.get(j, tipe(j)["harga"]))) for j, v in stk.items()])
        st.caption("Isi berat dari timbangan pengepul dan harga jual per satuan.")
        ed = st.data_editor(df, hide_index=True, width="stretch", disabled=["Jenis", "Satuan", "Perkiraan"],
                            column_config={"Berat": st.column_config.NumberColumn(min_value=0.0, step=0.5), "Harga": st.column_config.NumberColumn(min_value=0, step=100)})
        tot = float((ed["Berat"].fillna(0) * ed["Harga"].fillna(0)).sum())
        st.markdown(f'<div class="net"><span>Total dibayar pengepul</span><b>{rp(tot)}</b></div>', unsafe_allow_html=True)
        lebih = ed[ed["Berat"].fillna(0) > ed["Perkiraan"] + 1e-9]["Jenis"].tolist()
        izin = True
        if lebih:
            st.warning("Berat timbangan melebihi perkiraan stok untuk: " + ", ".join(lebih) + ".")
            izin = st.checkbox("Berat timbangan pengepul memang lebih besar dari perkiraan stok, lanjutkan")
        yakin = st.checkbox("Saya konfirmasi seluruh stok ini sudah diangkut pengepul")
        if st.button("Simpan penjualan", type="primary", disabled=not yakin or not izin or tot <= 0):
            sid = nid()
            its = [dict(jenis=r.Jenis, satuan=r.Satuan, jml=float(r.Berat), harga=int(r.Harga)) for r in ed.itertuples() if r.Berat and r.Berat > 0]
            u = next(x for x in pg if x["nama"] == pn)
            D["sales"].append(dict(id=sid, tgl=tg.isoformat(), email=u["email"], pengepul=pn, items=its, status="Aktif", oleh=CU["nama"]))
            for d in ok_dep():
                if not d["sold"]:
                    d["sold"] = sid
            st.success("Penjualan tercatat dan stok kembali nol.")
            st.rerun()
    if D["sales"]:
        st.subheader("Riwayat penjualan")
        for s in reversed(D["sales"]):
            with st.expander(f'{tgl(s["tgl"])} · {s["pengepul"]} · {rp(total(s["items"]))} · {s["status"]}'):
                st.dataframe(pd.DataFrame([dict(Jenis=i["jenis"], Satuan=i["satuan"], Berat=fmt(i["jml"]), Harga=rp(i["harga"]), Jumlah=rp(i["jml"] * i["harga"])) for i in s["items"]]), hide_index=True, width="stretch")
                if s["status"] == "Aktif" and st.button("Batalkan penjualan (stok dikembalikan)", key=f's{s["id"]}'):
                    s["status"] = "Dibatalkan"
                    for d in D["dep"]:
                        if d["sold"] == s["id"]:
                            d["sold"] = None
                    st.rerun()


def pg_keluar():
    head("Pengeluaran Operasional")
    c = st.columns(2)
    tg = c[0].date_input("Tanggal", date.today())
    kat = c[1].selectbox("Kategori", ["Bensin", "Transportasi", "Perlengkapan", "Lainnya"])
    ds = st.text_input("Deskripsi")
    j = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
    if st.button("Simpan pengeluaran", type="primary", disabled=j <= 0):
        D["exp"].append(dict(id=nid(), tgl=tg.isoformat(), kategori=kat, deskripsi=ds, jumlah=int(j), oleh=CU["nama"]))
        st.rerun()
    if D["exp"]:
        st.dataframe(pd.DataFrame([dict(Tanggal=tgl(e["tgl"]), Kategori=e["kategori"], Deskripsi=e["deskripsi"], Jumlah=rp(e["jumlah"]), Dicatat=e["oleh"]) for e in reversed(D["exp"])]), hide_index=True, width="stretch")
    else:
        st.caption("Belum ada pengeluaran.")


def pg_stok():
    head("Stok Sampah")
    stk = stok()
    if not stk:
        st.info("Stok kosong. Stok bertambah setelah nasabah menyetujui setoran.")
        return
    st.markdown(grid([(j, f"{fmt(v)} {tipe(j)['satuan']}") for j, v in stk.items()]), unsafe_allow_html=True)


def pg_jenis():
    head("Jenis Sampah & Harga")
    st.caption("Harga baru hanya berlaku untuk setoran berikutnya. Setoran lama tetap memakai harga saat dibuat.")
    used = {i["jenis"] for d in D["dep"] for i in d["items"]}
    for t in D["types"]:
        c = st.columns([3, 2, 2, 2])
        c[0].markdown(f'**{t["nama"]}** ' + ("" if t["aktif"] else pill("Nonaktif")), unsafe_allow_html=True)
        c[1].write(f'per {t["satuan"]}' + (" (terkunci)" if t["nama"] in used else ""))
        h = c[2].number_input("Harga", min_value=0, step=100, value=int(t["harga"]), key=f'h{t["nama"]}', label_visibility="collapsed")
        if h != t["harga"]:
            D["hist"].append(dict(waktu=now(), jenis=t["nama"], lama=t["harga"], baru=int(h), oleh=CU["nama"]))
            t["harga"] = int(h)
        if c[3].button("Nonaktifkan" if t["aktif"] else "Aktifkan", key=f'n{t["nama"]}'):
            t["aktif"] = not t["aktif"]
            st.rerun()
    with st.expander("Tambah jenis baru"):
        n = st.text_input("Nama jenis")
        u = st.radio("Satuan", ["kg", "pcs"], horizontal=True)
        h = st.number_input("Harga beli (Rp)", min_value=0, step=100, key="hb")
        if st.button("Simpan jenis", type="primary"):
            if not n.strip() or any(t["nama"].lower() == n.strip().lower() for t in D["types"]):
                st.error("Nama kosong atau sudah ada.")
            else:
                D["types"].append(dict(nama=n.strip(), satuan=u, harga=int(h), aktif=True))
                D["hist"].append(dict(waktu=now(), jenis=n.strip(), lama=0, baru=int(h), oleh=CU["nama"]))
                st.rerun()
    st.subheader("Riwayat perubahan harga")
    if D["hist"]:
        st.dataframe(pd.DataFrame([dict(Waktu=x["waktu"], Jenis=x["jenis"], Lama=rp(x["lama"]), Baru=rp(x["baru"]), Oleh=x["oleh"]) for x in reversed(D["hist"])]), hide_index=True, width="stretch")
    else:
        st.caption("Belum ada perubahan harga.")


def ganti_pw_form(paksa=False):
    with st.form("gantipw", clear_on_submit=True):
        lama = st.text_input("Kata sandi sekarang", type="password")
        b1 = st.text_input("Kata sandi baru (minimal 8 karakter)", type="password")
        b2 = st.text_input("Ulangi kata sandi baru", type="password")
        kirim = st.form_submit_button("Simpan kata sandi baru", type="primary")
    if kirim:
        u = cari_any(CU["email"])
        if not cek_pw(lama, u.get("pw", "")):
            st.error("Kata sandi sekarang salah.")
        elif not pw_valid(b1) or b1 != b2:
            st.error("Kata sandi baru minimal 8 karakter dan kedua isian harus sama.")
        elif b1 == lama:
            st.error("Kata sandi baru harus berbeda dari yang lama.")
        else:
            u["pw"] = hash_pw(b1)
            u["wajib_ganti"] = False
            st.success("Kata sandi berhasil diganti.")
            if paksa:
                st.rerun()


def pg_pengguna():
    head("Data Pengguna")
    st.dataframe(pd.DataFrame([dict(Nama=u["nama"], Email=u["email"], Peran=u["peran"], Status="Aktif" if u["aktif"] else "Nonaktif",
                                    Login="Bisa login" if u.get("pw") else "Tanpa akun login") for u in D["users"]]), hide_index=True, width="stretch")
    if S.get("pw_tampil"):
        e, p = S.pop("pw_tampil")
        st.success(f"Kata sandi sementara untuk {e}:")
        st.code(p)
        st.caption("Catat sekarang. Kata sandi ini tidak ditampilkan lagi, dan pengguna wajib menggantinya saat login pertama.")
    with st.expander("Buat akun baru", expanded=True):
        n, e = st.text_input("Nama"), st.text_input("Email")
        p = st.radio("Peran", ["Nasabah", "Pengepul", "Pengurus"], horizontal=True)
        hp_in = st.text_input("Nomor WhatsApp (opsional, mis. 0812xxxxxxx)")
        if st.button("Buat akun", type="primary"):
            if not n.strip() or "@" not in e or any(u["email"] == e.strip().lower() for u in D["users"]):
                st.error("Nama kosong, email tidak valid, atau email sudah terdaftar.")
            else:
                pw = pw_baru()
                D["users"].append(dict(email=e.strip().lower(), nama=n.strip(), peran=p, aktif=True, pw=hash_pw(pw), wajib_ganti=True, hp=norm_wa(hp_in)))
                S.pw_tampil = (e.strip().lower(), pw)
                st.rerun()
    lain = [u["email"] for u in D["users"] if u["email"] != CU["email"]]
    if lain:
        em = st.selectbox("Kelola akun", lain)
        c = st.columns(2)
        if c[0].button("Buat ulang kata sandi sementara"):
            u = cari_any(em)
            pw = pw_baru()
            u["pw"], u["wajib_ganti"] = hash_pw(pw), True
            S.pw_tampil = (em, pw)
            st.rerun()
        if c[1].button("Aktifkan atau nonaktifkan akun"):
            u = cari_any(em)
            u["aktif"] = not u["aktif"]
            st.rerun()
        ur = cari_any(em)
        opsi = ["Nasabah", "Pengepul", "Pengurus"]
        pr = st.radio("Peran akun yang dipilih", opsi, index=opsi.index(ur["peran"]), horizontal=True, key=f"peran_{em}")
        if pr != ur["peran"] and st.button("Simpan perubahan peran"):
            ur["peran"] = pr
            st.rerun()
        st.caption("Mengubah peran tidak mengubah transaksi lama. Pastikan peran baru memang sesuai.")
        hp_baru = st.text_input("Nomor WhatsApp akun yang dipilih", value=ur.get("hp", ""), key=f"hp_{em}")
        if st.button("Simpan nomor WhatsApp"):
            if hp_baru.strip() and not norm_wa(hp_baru):
                st.error("Nomor WhatsApp tidak valid.")
            else:
                ur["hp"] = norm_wa(hp_baru)
                st.rerun()


def cari_any(email): return next(u for u in D["users"] if u["email"] == email)


def lap(kind, a, b):
    if kind == "Pembelian dari nasabah":
        r = [dict(Tanggal=d["tgl"], Nasabah=d["nama"], Metode=d["metode"], Jenis=i["jenis"], Satuan=i["satuan"], Jumlah=i["jml"], Harga=i["harga"], Total=i["jml"] * i["harga"]) for d in ok_dep() if inr(d["tgl"], a, b) for i in d["items"]]
    elif kind == "Penjualan ke pengepul":
        r = [dict(Tanggal=s["tgl"], Pengepul=s["pengepul"], Jenis=i["jenis"], Satuan=i["satuan"], Berat=i["jml"], Harga=i["harga"], Jumlah=i["jml"] * i["harga"]) for s in aktif_sales() if inr(s["tgl"], a, b) for i in s["items"]]
    elif kind == "Pengeluaran":
        r = [dict(Tanggal=e["tgl"], Kategori=e["kategori"], Deskripsi=e["deskripsi"], Jumlah=e["jumlah"], Dicatat_oleh=e["oleh"]) for e in D["exp"] if inr(e["tgl"], a, b)]
    elif kind == "Net kas":
        be, ju, ou, ne = netkas(a, b)
        r = [dict(Komponen="Penjualan ke pengepul", Rupiah=ju), dict(Komponen="Pembelian dari nasabah", Rupiah=be), dict(Komponen="Pengeluaran operasional", Rupiah=ou), dict(Komponen="Net kas", Rupiah=ne)]
    elif kind == "Penarikan saldo":
        r = [dict(Tanggal=w["tgl"], Nasabah=w["nama"], Jumlah=w["jumlah"], Diproses_oleh=w["oleh"], Sumber=f"Pengajuan #{w['wr']}" if w.get("wr") else "Langsung") for w in D["wd"] if inr(w["tgl"], a, b)]
    elif kind == "Saldo nasabah":
        r = [dict(Nasabah=u["nama"], Saldo=saldo(u["email"])) for u in nasabah_aktif()]
    else:
        r = [dict(Jenis=j, Satuan=tipe(j)["satuan"], Perkiraan_stok=v) for j, v in stok().items()]
    return pd.DataFrame(r)


def pg_laporan():
    head("Laporan")
    kind = st.selectbox("Jenis laporan", ["Pembelian dari nasabah", "Penjualan ke pengepul", "Pengeluaran", "Net kas", "Penarikan saldo", "Saldo nasabah", "Stok sampah"])
    p = st.radio("Periode", ["Hari ini", "Bulan ini", "Rentang bebas"], horizontal=True)
    t = date.today()
    a, b = (t, t) if p == "Hari ini" else (t.replace(day=1), t) if p == "Bulan ini" else (None, None)
    if p == "Rentang bebas":
        r = st.date_input("Dari tanggal sampai tanggal", (t.replace(day=1), t))
        if len(r) != 2:
            st.stop()
        a, b = r
    df = lap(kind, a, b)
    if df.empty:
        st.info("Tidak ada data pada periode ini.")
        return
    st.dataframe(df, hide_index=True, width="stretch")
    st.download_button("Unduh CSV (dibuka di Excel)", df.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"), f"{kind.lower().replace(' ', '_')}_{a}_{b}.csv", "text/csv")


def pg_atur():
    head("Pengaturan")
    st.markdown("**EcoLedger Darling** adalah platform digital untuk membantu operasional **Bank Sampah Darling Berseri**.")
    st.markdown(f"**Penyimpanan data:** berkas SQLite `{DB_PATH}`. Data tetap ada saat aplikasi dimulai ulang selama berkas ini dipertahankan. "
                "Di hosting dengan disk sementara (misalnya Streamlit Community Cloud) berkas ini bisa hilang, jadi unduh cadangan secara berkala.")
    aman = {**D, "users": [{k: v for k, v in u.items() if k != "pw"} for u in D["users"]]}
    st.download_button("Unduh cadangan data (JSON, tanpa kata sandi)", json.dumps(aman, ensure_ascii=False, indent=1).encode("utf-8"), f"cadangan_ecoledger_{date.today()}.json", "application/json")
    st.subheader("Nomor WhatsApp pengurus")
    st.caption("Dipakai tombol 'Hubungi Pengurus via WhatsApp' di akun nasabah. Tidak ada nomor bawaan.")
    wa_in = st.text_input("Nomor WhatsApp pengurus", value=D["pengaturan"].get("wa", ""), placeholder="mis. 0812xxxxxxx")
    if st.button("Simpan nomor WhatsApp pengurus", type="primary"):
        if wa_in.strip() and not norm_wa(wa_in):
            st.error("Nomor tidak valid. Gunakan format 08... atau 628... (10 sampai 15 digit).")
        else:
            D["pengaturan"]["wa"] = norm_wa(wa_in)
            st.success("Nomor WhatsApp pengurus disimpan." if norm_wa(wa_in) else "Nomor WhatsApp pengurus dikosongkan.")
    st.subheader("Ganti kata sandi saya")
    ganti_pw_form()
    st.subheader("Data contoh")
    st.caption("Data contoh ditandai dan akun contohnya tidak bisa login. Hapus sebelum dipakai untuk transaksi nyata.")
    c = st.columns(2)
    if c[0].button("Muat data contoh"):
        seed_demo()
        st.rerun()
    if c[1].button("Hapus data contoh"):
        hapus_demo()
        st.rerun()

# ---------- data contoh (ditandai demo=True, bisa dihapus dari Pengaturan) ----------
def dep_demo(hari, email, nama, metode, rows, status="Disetujui"):
    d = dict(id=nid(), tgl=(date.today() - timedelta(days=hari)).isoformat(), email=email, nama=nama, metode=metode,
             items=[dict(jenis=j, satuan=tipe(j)["satuan"], jml=q, harga=tipe(j)["harga"]) for j, q in rows],
             status=status, sold=None, ver=1, log=[], oleh="Pengurus Demo", demo=True)
    catat(d, "Data contoh")
    D["dep"].append(d)
    return d


def seed_demo():
    if D.get("demo_loaded"):
        return
    D["demo_loaded"] = True
    for e_, n_, p_ in [("nasabah1.demo@contoh.com", "Nasabah Demo", "Nasabah"), ("nasabah2.demo@contoh.com", "Nasabah Demo 2", "Nasabah"), ("pengepul.demo@contoh.com", "Pengepul Demo", "Pengepul")]:
        if not any(u["email"] == e_ for u in D["users"]):
            D["users"].append(dict(email=e_, nama=n_, peran=p_, aktif=True, pw="", demo=True))
    n1, n2 = ("nasabah1.demo@contoh.com", "Nasabah Demo"), ("nasabah2.demo@contoh.com", "Nasabah Demo 2")
    lama = [dep_demo(24, *n1, "Tabung", [("Kardus", 12), ("Botol plastik", 4)]), dep_demo(22, *n2, "Tunai", [("Besi", 6), ("Kaleng", 3)])]
    sid = nid()
    its = [dict(jenis=j, satuan=tipe(j)["satuan"], jml=q, harga=h) for j, q, h in [("Kardus", 12.5, 2400), ("Botol plastik", 4.0, 1800), ("Besi", 6.0, 4500), ("Kaleng", 3.0, 2800)]]
    D["sales"].append(dict(id=sid, tgl=(date.today() - timedelta(days=20)).isoformat(), email="pengepul.demo@contoh.com", pengepul="Pengepul Demo", items=its, status="Aktif", oleh="Pengurus Demo", demo=True))
    for d in lama:
        d["sold"] = sid
    dep_demo(9, *n1, "Tabung", [("Kardus", 8.5), ("Buku", 5)])
    dep_demo(6, *n2, "Tabung", [("Galon aqua", 4), ("Gelas botol", 7)])
    dep_demo(3, *n1, "Tabung", [("Emberan", 10), ("Duplek", 6)])
    dep_demo(1, *n1, "Tunai", [("Kardus", 5.5)], status="Menunggu")
    D["wd"].append(dict(id=nid(), tgl=(date.today() - timedelta(days=5)).isoformat(), waktu=now(), email=n1[0], nama=n1[1], jumlah=10000, oleh="Pengurus Demo", demo=True))
    D["exp"].append(dict(id=nid(), tgl=(date.today() - timedelta(days=7)).isoformat(), kategori="Bensin", deskripsi="Antar sampah", jumlah=25000, oleh="Pengurus Demo", demo=True))


def hapus_demo():
    for k in ("dep", "wd", "sales", "exp"):
        D[k] = [x for x in D[k] if not x.get("demo")]
    D["users"] = [u for u in D["users"] if not u.get("demo")]
    D["demo_loaded"] = False


# ---------- dashboard nasabah (semua data difilter dari akun yang login, bukan dari input pengguna) ----------
def mine(): return [d for d in D["dep"] if d["email"] == CU["email"]]
def mine_wd(): return [w for w in D["wd"] if w["email"] == CU["email"]]


def setujui(did):
    d = next((x for x in mine() if x["id"] == did and x["status"] == "Menunggu"), None)
    if d:
        d["status"] = "Disetujui"
        d["disetujui_oleh"] = CU["nama"] + " (nasabah, lewat akunnya)"
        d["disetujui_pada"] = now()
        catat(d, "Disetujui nasabah lewat akunnya")
    st.rerun()


def kartu_trx(d):
    with st.expander(f'#{d["id"]} · {tgl(d["tgl"])} · {rp(total(d["items"]))} · {d["metode"]} · {d["status"]}'):
        st.markdown(pill(d["status"]), unsafe_allow_html=True)
        st.dataframe(tabel_items(d["items"]), hide_index=True, width="stretch")


def n_beranda():
    head(f"Selamat datang, {CU['nama']}!", "Yuk, terus berkontribusi untuk lingkungan yang lebih bersih.")
    ok = [d for d in mine() if d["status"] == "Disetujui"]
    wait = [d for d in mine() if d["status"] == "Menunggu"]
    sd = saldo(CU["email"])
    info = f"{len(wait)} setoran menunggu persetujuan" if wait else "Tidak ada setoran yang menunggu persetujuan"
    st.markdown(f'<div class="net"><div class="nt"><span>Saldo Tabungan Saya</span></div><b>{rp(sd)}</b><small>Dapat ditarik: {rp(sd)} · {info}</small></div>', unsafe_allow_html=True)
    if wait:
        st.button("Periksa setoran sekarang", on_click=go, args=("Persetujuan Setoran",))
    status_wr(CU["email"])
    kg = sum(i["jml"] for d in ok for i in d["items"] if i["satuan"] == "kg")
    pcs = sum(i["jml"] for d in ok for i in d["items"] if i["satuan"] == "pcs")
    st.write("")
    st.markdown(grid([("Sampah disetorkan", f"{fmt(kg)} kg" + (f" + {fmt(pcs)} pcs" if pcs else "")), ("Transaksi disetujui", len(ok)),
                      ("Total pernah ditarik", rp(sum(w["jumlah"] for w in mine_wd())))]), unsafe_allow_html=True)
    st.subheader("Aktivitas terbaru")
    ev = [(d["tgl"], f"Setoran {d['metode']} {rp(total(d['items']))} · {d['status']}") for d in mine() if d["status"] != "Dibatalkan"]
    ev += [(w["tgl"], f"Penarikan {rp(w['jumlah'])}") for w in mine_wd()]
    for tg, tx in sorted(ev, reverse=True)[:5]:
        st.markdown(f"**{tgl(tg)}** · {tx}")
    if not ev:
        st.caption("Belum ada aktivitas. Setoran pertamamu akan muncul di sini.")


def n_setuju():
    head("Persetujuan Setoran")
    wait = [d for d in reversed(mine()) if d["status"] == "Menunggu"]
    if not wait:
        st.info("Tidak ada setoran yang perlu diperiksa.")
    for d in wait:
        with st.container(border=True, key=f"trx{d['id']}"):
            st.markdown(f'**Transaksi #{d["id"]}** · {tgl(d["tgl"])} · {d["metode"]} ' + pill(d["status"]), unsafe_allow_html=True)
            st.markdown(f'Total **{rp(total(d["items"]))}**')
            with st.expander("Lihat Rincian"):
                st.dataframe(tabel_items(d["items"]), hide_index=True, width="stretch")
            cek = st.checkbox("Saya sudah mencocokkan dengan hasil penimbangan", key=f'c{d["id"]}')
            st.caption("Ada yang salah? Hubungi pengurus untuk koreksi. Rincian tidak bisa diubah dari akunmu.")
            if st.button("Setujui Setoran", type="primary", key=f'ok{d["id"]}', disabled=not cek):
                setujui(d["id"])


def n_riwayat():
    head("Riwayat Setoran")
    t = date.today()
    f = st.selectbox("Periode", ["Semua", "Bulan ini", "30 hari terakhir"])
    a = {"Semua": date.min, "Bulan ini": t.replace(day=1), "30 hari terakhir": t - timedelta(days=30)}[f]
    data = [d for d in reversed(mine()) if d["tgl"] >= a.isoformat()]
    for d in data:
        kartu_trx(d)
    if not data:
        st.info("Belum ada setoran pada periode ini.")


def bagian_tarik_saldo():
    em = CU["email"]
    st.markdown('<div class="sec"><b>Ingin Menarik Saldo?</b></div>', unsafe_allow_html=True)
    sd, tsd = saldo(em), saldo_tersedia(em)
    st.markdown(grid([("Saldo tabungan", rp(sd)), ("Saldo tersedia untuk ditarik", rp(tsd))]), unsafe_allow_html=True)
    if tsd != sd:
        st.caption(f"{rp(sd - tsd)} sedang dalam pengajuan penarikan yang belum selesai.")
    pesan = S.pop("wr_msg", None)
    if pesan:
        (st.success if pesan[0] else st.error)(pesan[1])
    status_wr(em)
    nom = st.number_input("Nominal yang ingin ditarik (Rp)", min_value=0, step=1000, key="nominal_wr")
    if nom > tsd:
        st.warning(f"Nominal melebihi saldo tersedia ({rp(tsd)}).")
    a, b = st.columns(2)
    with a:
        with st.container(border=True, key="opsiA"):
            st.markdown("**Pilihan A · Ajukan lewat aplikasi**")
            st.caption("Pengajuan masuk ke pengurus. Saldo baru berkurang setelah pengurus mengonfirmasi uang sudah kamu terima.")
            st.button("Kirim pengajuan", type="primary", key="kirim_wr", on_click=ajukan_wr, disabled=nom <= 0 or nom > tsd or bool(wr_open(em)))
    with b:
        with st.container(border=True, key="opsiB"):
            st.markdown("**Pilihan B · Hubungi pengurus via WhatsApp**")
            st.caption("Membuka WhatsApp dengan pesan yang sudah terisi. Pesan WhatsApp tidak otomatis tercatat di aplikasi, pengurus yang mencatatnya.")
            wa = D["pengaturan"].get("wa", "")
            st.link_button("Hubungi Pengurus via WhatsApp", wa_link(wa, pesan_wa(CU["nama"], nom)) if wa else "https://wa.me/", disabled=not wa or nom <= 0)
            if not wa:
                st.caption("Nomor WhatsApp pengurus belum diatur.")


def n_saldo():
    head("Saldo Saya")
    st.markdown(f'<div class="net"><div class="nt"><span>Saldo Tabungan Saya</span></div><b>{rp(saldo(CU["email"]))}</b><small>Saldo bertambah dari setoran Tabung yang sudah disetujui</small></div>', unsafe_allow_html=True)
    rows = [(d["tgl"], f"Setoran tabung #{d['id']}", total(d["items"])) for d in mine() if d["status"] == "Disetujui" and d["metode"] == "Tabung"]
    rows += [(w["tgl"], "Penarikan", -w["jumlah"]) for w in mine_wd()]
    bagian_tarik_saldo()
    st.subheader("Mutasi tabungan")
    if rows:
        st.dataframe(pd.DataFrame([dict(Tanggal=tgl(t), Keterangan=k, Jumlah=("+" if v > 0 else "−") + rp(abs(v))) for t, k, v in sorted(rows, reverse=True)]), hide_index=True, width="stretch")
    else:
        st.caption("Belum ada mutasi.")


def n_tarik():
    head("Riwayat Penarikan")
    wd, rq = mine_wd(), [r for r in D["wr"] if r["email"] == CU["email"]]
    st.markdown(grid([("Total pernah ditarik", rp(sum(w["jumlah"] for w in wd))), ("Jumlah penarikan", len(wd)), ("Pengajuan berjalan", len(wr_open(CU["email"])))]), unsafe_allow_html=True)
    status_wr(CU["email"])
    st.markdown('<div class="sec"><b>Pengajuan penarikan</b></div>', unsafe_allow_html=True)
    if rq:
        st.dataframe(tabel_wr(rq, nasabah=False), hide_index=True, width="stretch")
    else:
        st.caption("Belum ada pengajuan. Ajukan dari menu Saldo Saya.")
    st.markdown('<div class="sec"><b>Penarikan yang sudah dibayarkan</b></div>', unsafe_allow_html=True)
    if wd:
        st.dataframe(pd.DataFrame([dict(Tanggal=tgl(w["tgl"]), Jumlah=rp(w["jumlah"]), Diproses=w["oleh"]) for w in reversed(wd)]), hide_index=True, width="stretch")
    else:
        st.info("Belum ada penarikan.")


def profil():
    head("Profil Saya")
    st.markdown(grid([("Nama", CU["nama"]), ("Email", CU["email"]), ("Peran", CU["peran"])]), unsafe_allow_html=True)
    st.caption("Data profil dikelola pengurus. Hubungi pengurus untuk mengubah nama atau email.")
    st.subheader("Ganti kata sandi")
    ganti_pw_form()


# ---------- dashboard pengepul (tidak pernah memuat harga beli, saldo, kas, laba, atau pengeluaran) ----------
NOTE = "Stok merupakan perkiraan berdasarkan pencatatan internal. Berat akhir mengikuti hasil penimbangan saat pengangkutan."


def daftar_stok(stk):
    if not stk:
        st.info("Belum ada sampah terkumpul. Stok kembali nol setelah pengangkutan.")
        return
    mx = max(stk.values())
    st.markdown('<div class="grid">' + "".join(f'<div class="card"><small>{j} · <span class="pill p-o">Tersedia</span></small><b>{fmt(v)} {tipe(j)["satuan"]}</b><div class="bar"><i style="width:{max(6, v / mx * 100):.0f}%"></i></div></div>' for j, v in stk.items()) + "</div>", unsafe_allow_html=True)


def p_beranda():
    head(f"Selamat datang, {CU['nama']}!", "Berikut ringkasan stok sampah yang tersedia.")
    stk = stok()
    kg = sum(v for j, v in stk.items() if tipe(j)["satuan"] == "kg")
    pcs = sum(v for j, v in stk.items() if tipe(j)["satuan"] == "pcs")
    upd = max([d["tgl"] for d in ok_dep() if not d["sold"]], default=None)
    st.markdown(grid([("Jenis sampah tersedia", len(stk)), ("Perkiraan berat", f"{fmt(kg)} kg"), ("Perkiraan barang", f"{fmt(pcs)} pcs"), ("Stok diperbarui", tgl(upd) if upd else "-")]), unsafe_allow_html=True)
    st.subheader("Stok per jenis")
    daftar_stok(stk)
    st.caption(NOTE)


def p_stok():
    head("Perkiraan Stok")
    stk = stok()
    daftar_stok(stk)
    if stk:
        st.dataframe(pd.DataFrame([dict(Jenis=j, Satuan=tipe(j)["satuan"], Perkiraan=fmt(v)) for j, v in stk.items()]), hide_index=True, width="stretch")
    st.caption(NOTE)


def p_riwayat():
    head("Riwayat Penjualan")
    mine_s = [x for x in reversed(D["sales"]) if x["email"] == CU["email"]]
    for x in mine_s:
        with st.expander(f'#{x["id"]} · {tgl(x["tgl"])} · {rp(total(x["items"]))} · {x["status"]}'):
            st.dataframe(pd.DataFrame([dict(Jenis=i["jenis"], Satuan=i["satuan"], Berat=fmt(i["jml"]), Harga=rp(i["harga"]), Jumlah=rp(i["jml"] * i["harga"])) for i in x["items"]]), hide_index=True, width="stretch")
            st.markdown(f"Total penjualan **{rp(total(x['items']))}**")
    if not mine_s:
        st.info("Belum ada laporan penjualan untukmu.")


# ---------- login dan router ----------
def logo(side=False):
    if os.path.exists(LOGO):
        st.image(LOGO, width=150 if side else 200)
    else:
        st.markdown('<div class="brand">EcoLedger Darling<span>Sistem Informasi Bank Sampah</span></div>', unsafe_allow_html=True)


def coba_login(email, pw, peran=None):
    e = (email or "").strip().lower()
    n, sampai = ST["gagal"].get(e, (0, 0.0))
    if n >= 5 and time.time() < sampai:
        return None, "Terlalu banyak percobaan gagal. Coba lagi dalam beberapa menit."
    if n >= 5:
        n = 0
    u = next((x for x in D["users"] if x["email"] == e), None)
    if u and u["aktif"] and u.get("pw") and cek_pw(pw, u["pw"]):
        ST["gagal"].pop(e, None)
        if peran and u["peran"] != peran:
            return None, "Jenis akun tidak sesuai dengan akun yang terdaftar. Silakan pilih jenis akun yang benar."
        return u, ""
    ST["gagal"][e] = (n + 1, time.time() + 300)
    return None, "Email atau kata sandi salah."


def setup_awal():
    st.info("Belum ada akun. Buat akun Pengurus pertama untuk memulai.")
    try:
        kode = st.secrets.get("setup_kode")
    except Exception:
        kode = None
    with st.form("setup"):
        n, e = st.text_input("Nama lengkap"), st.text_input("Email")
        p1, p2 = st.text_input("Kata sandi (minimal 8 karakter)", type="password"), st.text_input("Ulangi kata sandi", type="password")
        k = st.text_input("Kode pengaturan awal", type="password") if kode else ""
        kirim = st.form_submit_button("Buat akun Pengurus", type="primary")
    if kirim:
        if kode and k != kode:
            st.error("Kode pengaturan awal salah.")
        elif not n.strip() or "@" not in e:
            st.error("Nama atau email tidak valid.")
        elif not pw_valid(p1) or p1 != p2:
            st.error("Kata sandi minimal 8 karakter dan kedua isian harus sama.")
        else:
            D["users"].append(dict(email=e.strip().lower(), nama=n.strip(), peran="Pengurus", aktif=True, pw=hash_pw(p1), wajib_ganti=False))
            S.uid, S.page = e.strip().lower(), "Beranda"
            st.rerun()


PERAN_LOGIN = {"Pengurus": ("admin_panel_settings", "Pengurus Bank Sampah", "Masuk untuk mengelola operasional dan transaksi bank sampah."),
               "Nasabah": ("person", "Nasabah", "Masuk untuk melihat saldo, riwayat setoran, dan tabungan."),
               "Pengepul": ("local_shipping", "Pengepul", "Masuk untuk melihat stok dan riwayat penjualan sampah.")}


def pilih_peran(p): S.login_role = p


@lru_cache(maxsize=1)
def _logo_login():
    return base64.b64encode(open(LOGO, "rb").read()).decode() if os.path.exists(LOGO) else ""


def login_brand():
    img = f'<img src="data:image/png;base64,{_logo_login()}" alt="Logo EcoLedger Darling">' if _logo_login() else ""
    st.markdown(f'<div class="lg">{img}<b>EcoLedger Darling</b><span>Sistem Informasi Bank Sampah</span><em>Kelola Sampah, Catat Nilai, Ciptakan Dampak.</em><i>Platform digital yang digunakan oleh Bank Sampah Darling Berseri</i></div>', unsafe_allow_html=True)


def login_page():
    _, c, _ = st.columns([1, 1.7, 1])
    with c:
        with st.container(border=True, key="loginbox"):
            login_brand()
            if not D["users"]:
                setup_awal()
                return
            st.markdown('<div class="lgt">Pilih jenis akun</div>', unsafe_allow_html=True)
            sel = S.get("login_role")
            for col, (p, (ik, _, _)) in zip(st.columns(3), PERAN_LOGIN.items()):
                col.button(p, key=f"role_{p}", icon=f":material/{ik}:", type="primary" if sel == p else "secondary", width="stretch", on_click=pilih_peran, args=(p,))
            if sel not in PERAN_LOGIN:
                st.caption("Pilih salah satu jenis akun di atas untuk melanjutkan.")
                return
            ik, nama, ket = PERAN_LOGIN[sel]
            with st.container(border=True, key="rolebox"):
                st.markdown(f":material/{ik}: **{nama}**")
                st.caption(ket)
            with st.form("login"):
                e, pw = st.text_input("Email"), st.text_input("Kata sandi", type="password")
                kirim = st.form_submit_button(f"Masuk sebagai {nama}", type="primary")
            if kirim:
                u, pesan = coba_login(e, pw, sel)
                if u:
                    S.uid, S.page = u["email"], "Beranda"
                    st.rerun()
                st.error(pesan)
            st.caption("Lupa kata sandi? Minta pengurus membuatkan kata sandi sementara yang baru.")


def masuk(): return cari(S.get("uid"))


CU = masuk()
if not CU:
    login_page()
    st.stop()
if CU.get("wajib_ganti"):
    st.caption("EcoLedger Darling · Bank Sampah Darling Berseri")
    st.title("Ganti kata sandi sementara")
    st.write(f"Halo, {CU['nama']}. Kata sandimu masih sementara. Buat kata sandi baru untuk melanjutkan.")
    ganti_pw_form(True)
    if st.button("Keluar"):
        S.pop("uid", None)
        st.rerun()
    st.stop()

PENGURUS = {"Beranda": ("home", pg_beranda), "Input Setoran": ("add_circle", pg_input), "Kelola Setoran": ("receipt_long", pg_kelola),
            "Nasabah": ("groups", pg_nasabah), "Penarikan Saldo": ("payments", pg_tarik), "Penjualan Pengepul": ("local_shipping", pg_jual),
            "Pengeluaran Operasional": ("account_balance_wallet", pg_keluar), "Stok Sampah": ("inventory_2", pg_stok),
            "Jenis Sampah & Harga": ("sell", pg_jenis), "Data Pengguna": ("manage_accounts", pg_pengguna), "Laporan": ("bar_chart", pg_laporan), "Pengaturan": ("settings", pg_atur)}

S.setdefault("page", "Beranda")


NASABAH = {"Beranda": ("home", n_beranda), "Persetujuan Setoran": ("task_alt", n_setuju), "Riwayat Setoran": ("receipt_long", n_riwayat),
           "Saldo Saya": ("account_balance_wallet", n_saldo), "Riwayat Penarikan": ("payments", n_tarik), "Profil Saya": ("person", profil)}
PENGEPUL = {"Beranda": ("home", p_beranda), "Perkiraan Stok": ("inventory_2", p_stok), "Riwayat Penjualan": ("local_shipping", p_riwayat), "Profil Saya": ("person", profil)}
PAGES = {"Pengurus": PENGURUS, "Nasabah": NASABAH, "Pengepul": PENGEPUL}


def go(p): S["goto"] = p


@lru_cache(maxsize=1)
def logo_b64(): return base64.b64encode(open(LOGO, "rb").read()).decode()


def brand():
    img = f'<img src="data:image/png;base64,{logo_b64()}" alt="Logo EcoLedger Darling">' if os.path.exists(LOGO) else ""
    st.markdown(f'<div class="bx">{img}<div><b>EcoLedger Darling</b><span>Sistem Informasi Bank Sampah</span></div></div>', unsafe_allow_html=True)


with st.sidebar:
    brand()
    st.markdown(f'<div class="me"><b>{CU["nama"]}</b><span>{CU["peran"] or "Belum terdaftar"} · Bank Sampah Darling Berseri</span></div>', unsafe_allow_html=True)
    if CU["peran"] in PAGES:
        menu = PAGES[CU["peran"]]
        kunci = f"nav_{CU['peran']}"
        if "goto" in S:
            tujuan = S.pop("goto")
            if tujuan in menu:
                S[kunci] = tujuan
        if S.get(kunci) not in menu:
            S[kunci] = "Beranda"
        lencana = len(wr_open()) if CU["peran"] == "Pengurus" else 0
        st.radio("Menu", list(menu), key=kunci, format_func=lambda k: f":material/{menu[k][0]}: {k}" + (f"  ({lencana})" if k == "Penarikan Saldo" and lencana else ""), label_visibility="collapsed")
        S.page = S[kunci]
    if st.button("Keluar", icon=":material/logout:", type="tertiary", width="stretch"):
        S.page = "Beranda"
        for k in [k for k in S if str(k).startswith("nav_")]:
            S.pop(k)
        S.pop("uid", None)
        st.rerun()

if CU["peran"] is None:
    st.error("Email kamu belum terdaftar. Hubungi pengurus bank sampah.")
else:
    halaman = PAGES[CU["peran"]]
    halaman[S.page if S.page in halaman else "Beranda"][1]()

simpan_jika_berubah()
