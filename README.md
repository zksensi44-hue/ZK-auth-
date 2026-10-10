# ZK Auth — callback OAuth2 do Discord

Interface responsiva em português com botão de login e página de autorização concluída.

## Publicar no Render
1. Suba todos estes arquivos para um repositório GitHub.
2. No Render, selecione New → Blueprint e conecte o repositório.
3. Configure as variáveis `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET` e `DISCORD_REDIRECT_URI`.
4. Defina `DISCORD_REDIRECT_URI` como o endereço HTTPS publicado seguido de `/api/auth/callback`.
5. No Discord Developer Portal → sua aplicação → OAuth2 → Redirects, cadastre exatamente a mesma URL.
6. Mantenha o escopo `identify` para este exemplo. Não solicite email ou acesso a servidores sem necessidade clara e consentimento informado.

## Limitação importante
Este projeto é um exemplo funcional de login OAuth2 que confirma a identidade básica (`identify`). Ele **não** implementa a API privada nem o WebSocket do DCloud, não marca membros como verificados no bot e não adiciona pessoas a servidores. Para substituir integralmente o DCloud, é necessário conhecer o protocolo/API esperado pelo bot e implementar as rotas correspondentes.

Nunca compartilhe seu Client Secret ou token de bot. Não colete senha do Discord. O usuário deve ver e aceitar as permissões na página oficial do Discord.
