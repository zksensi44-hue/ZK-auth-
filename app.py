import os
import secrets
from urllib.parse import urlencode

import requests
from flask import Flask, redirect, request, session, render_template_string

app = Flask(name)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get(
"DISCORD_REDIRECT_URI",
"https://zk-auth-callback.onrender.com/api/auth/callback"
)

Permissões solicitadas no login OAuth2

SCOPES = "identify email guilds guilds.join"

STYLE = """

<style>
:root {
  color-scheme: dark;
  --bg: #0a0812;
  --panel: #121020;
  --purple: #8b5cf6;
  --muted: #aaa5c4;
  --line: #30264c;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: radial-gradient(ellipse at 12% 20%, #241342 0, transparent 42%), var(--bg);
  font: 16px system-ui, Arial, sans-serif;
  color: #f6f2ff;
  min-height: 100vh;
}
header {
  min-height: 70px;
  border-bottom: 1px solid #2a2040;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 7%;
  gap: 16px;
}
.brand { font-size: 22px; font-weight: 800; }
.brand span { color: #a78bfa; }
.nav { color: #c4b5fd; font-size: 14px; }
main {
  width: min(1000px, 92%);
  margin: 7vh auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}
.eyebrow {
  color: #bda8ff;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  font-weight: 700;
}
h1 { font-size: clamp(30px, 5vw, 48px); line-height: 1.1; }
p { line-height: 1.65; color: var(--muted); }
.card {
  background: linear-gradient(145deg, #141124, #0e0c18);
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: clamp(24px, 4vw, 42px);
  box-shadow: 0 25px 80px #0007;
  text-align: center;
}
.logo {
  width: 64px; height: 64px;
  margin: 0 auto 20px;
  border-radius: 20px;
  display: grid; place-items: center;
  background: #251640; color: #c4b5fd;
  font-size: 30px; border: 1px solid #6845a7;
}
.button {
  display: flex; justify-content: center; align-items: center;
  width: 100%; padding: 15px 18px;
  border: 0; border-radius: 10px;
  background: linear-gradient(100deg, #6d28d9, #9333ea);
  color: white; font-size: 16px; font-weight: 750;
  text-decoration: none; cursor: pointer;
}
.note {
  margin-top: 20px; text-align: left;
  border: 1px solid #2b2441; background: #0d0b17;
  padding: 16px; border-radius: 12px;
  font-size: 14px; color: #c4b5fd;
}
.status {
  width: 76px; height: 76px; border-radius: 50%;
  display: grid; place-items: center;
  background: #172a22; border: 1px solid #28684a;
  color: #86efac; font-size: 38px; margin: 0 auto 18px;
}
footer {
  padding: 22px 7%; border-top: 1px solid #2a2040;
  color: #77718f; font-size: 13px;
  display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
}
@media(max-width:760px) {
  header { padding: 18px 5%; }
  main { grid-template-columns: 1fr; margin: 5vh auto; gap: 26px; }
  .intro { text-align: center; }
  .nav { display: none; }
  .card { padding: 28px 22px; }
  footer { padding: 20px 5%; }
}
</style>"""

HOME = """<!doctype html>

<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZK Auth — Login Discord</title>
</head>
""" + STYLE + """
<body>
<header>
  <div class="brand">◆ ZK <span>Auth</span></div>
  <div class="nav">Autenticação da comunidade</div>
</header>
<main>
  <section class="intro">
    <div class="eyebrow">Autenticação da comunidade</div>
    <h1>Conecte sua conta<br><span style="color:#a78bfa">com segurança.</span></h1>
    <p>Conecte sua conta Discord para continuar.</p>
    <p>Você será direcionado ao Discord oficial para analisar e autorizar as permissões solicitadas.</p>
  </section>
  <section class="card">
    <div class="logo">◆</div>
    <h2>Entrar com Discord</h2>
    <p>Confira as permissões antes de continuar.</p>
    <a class="button" href="/login">Continuar com Discord</a>
    <div class="note">
      <b>Permissões solicitadas</b>
      <p>Perfil básico, endereço de e-mail e acesso à lista de servidores. A permissão de entrada em servidores pode ser usada apenas com autorização e conforme os requisitos do Discord.</p>
      <p>Este site nunca pede sua senha ou token do Discord.</p>
    </div>
  </section>
</main>
<footer>
  <span>ZK Auth · Autenticação Discord</span>
  <span>Revise as permissões antes de autorizar.</span>
</footer>
</body>
</html>
"""@app.get("/")
def home():
return render_template_string(HOME)

@app.get("/login")
def login():
if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
return (
"Configuração incompleta. Confira DISCORD_CLIENT_ID, "
"DISCORD_CLIENT_SECRET e DISCORD_REDIRECT_URI no Render.",
500,
)

state = secrets.token_urlsafe(32)
session["oauth_state"] = state

params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": SCOPES,
    "state": state,
}

return redirect(
    "https://discord.com/oauth2/authorize?" + urlencode(params)
)

@app.get("/api/auth/callback")
def callback():
if request.args.get("error"):
return render_template_string(
"""<!doctype html><html lang="pt-br"><meta charset="utf-8">"""
+ STYLE
+ """<body><main style="display:block;max-width:620px">
<section class="card"><h2>Autorização cancelada</h2>
<p>Você cancelou a autorização. Nenhuma ação foi concluída.</p>
<a class="button" href="/">Voltar</a></section>
</main></body></html>"""
), 400

expected_state = session.pop("oauth_state", None)
received_state = request.args.get("state")
code = request.args.get("code")

if (
    not expected_state
    or not received_state
    or not secrets.compare_digest(expected_state, received_state)
):
    return "Falha de segurança: state inválido. Tente novamente.", 400

if not code or not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
    return "Código ou configuração OAuth2 ausente.", 400

try:
    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        timeout=15,
    )

    if not token_response.ok:
        app.logger.warning(
            "Discord token exchange failed: %s",
            token_response.status_code,
        )
        return (
            "Não foi possível concluir o login. Confira as configurações OAuth2.",
            400,
        )

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return "O Discord não retornou um token de acesso.", 400

    headers = {"Authorization": f"Bearer {access_token}"}

    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers=headers,
        timeout=15,
    )

    if not user_response.ok:
        return "Não foi possível consultar o perfil Discord.", 400

    user = user_response.json()

except requests.RequestException:
    return "Não foi possível conectar ao Discord. Tente novamente.", 502

# Não armazenamos o token nem o e-mail.
username = user.get("global_name") or user.get("username") or "Conta Discord"

return render_template_string(
    """<!doctype html>
    <html lang="pt-br">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>ZK Auth — Concluído</title>
    </head>
    """
    + STYLE
    + """
    <body>
    <header><div class="brand">◆ ZK <span>Auth</span></div></header>
    <main style="display:block;max-width:620px">
      <section class="card">
        <div class="status">✓</div>
        <h2>Autorização concluída</h2>
        <p>Conta conectada: <b style="color:white">{{ username }}</b></p>
        <p>O login foi concluído. Esta versão ainda não salva uma lista de membros nem os adiciona a outro servidor.</p>
        <a class="button" href="/">Concluir</a>
      </section>
    </main>
    <footer><span>ZK Auth</span><span>Gerencie as autorizações nas configurações do Discord.</span></footer>
    </body>
    </html>
    """,
    username=username,
)

@app.get("/health")
def health():
return {"status": "ok"}

if name == "main":
app.run(
host="0.0.0.0",
port=int(os.environ.get("PORT", "10000")),
)
