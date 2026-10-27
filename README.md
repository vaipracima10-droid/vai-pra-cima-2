# Vai Pra Cima — 1.0 beta

**A ponte entre você e o seu futuro.** App para celular que mostra peneiras de futebol e futsal no estado de São Paulo (Sub-9 a Sub-20, masculino e feminino).

## Como abrir

- **Pelo GitHub Pages:** em *Settings › Pages*, escolha a branch `main` e a pasta deste projeto. O `index.html` abre o app.
- **No computador:** abra `vai_pra_cima_1_0_beta.html` no Chrome ou no Safari.
- O GPS só funciona quando o app é aberto por um link **HTTPS**.

## O que tem

- Cadastro em 4 respostas: ano de nascimento, gênero, modalidade e cidade (ou GPS).
- Abas **Lista**, **Mapa**, **Agenda** e **Histórico**.
- Filtros: compatíveis, com vagas, fim de semana, favoritas, origem (reais ou exemplos), distância, categoria, modalidade e preço.
- Ficha da peneira explicando se ela combina com o atleta e, se não combinar, por quê.
- "Tenho interesse" pede só **nome e WhatsApp**.
- **Histórico** das peneiras em que você demonstrou interesse, com a situação de cada uma (enviado, lista de espera, inscrição registrada, já aconteceu) e a opção de cancelar.
- Tema claro e escuro (segue o do aparelho; teste com `?tema=claro` ou `?tema=escuro`).
- **Conta com e-mail e senha** (com banco ligado): criar conta, entrar, sair e recuperar senha. Perfil, favoritas e histórico ficam salvos na conta.
- **Painel do administrador** (só para `vaipracima10@gmail.com`): vê todas as peneiras, inclusive as ocultas e as que já aconteceram; adiciona, edita, oculta e exclui; vê quem demonstrou interesse em cada uma, com WhatsApp.

## Dados

- Peneiras com a etiqueta **"Peneira real"** vêm de divulgação pública e trazem a fonte. Confira sempre nos canais oficiais do clube.
- Peneiras com a etiqueta **"Exemplo"** são fictícias (clubes, endereços e telefones inventados).
- **Sem banco configurado** (modo demonstração): tudo fica salvo só no aparelho, no `localStorage` (chave `vpc1`; as chaves antigas `pen_me` e `pen_fav` ainda são lidas). Não há login nem painel do administrador.
- **Com banco (Supabase)**: peneiras, perfis e interesses ficam no Supabase. As regras de acesso estão no próprio banco (`supabase/schema.sql`): qualquer pessoa vê as peneiras visíveis; cada conta vê e muda só os próprios dados; só a conta `vaipracima10@gmail.com`, com o e-mail confirmado, cria, edita e apaga peneiras e vê todos os interessados.

## Como ligar o banco de dados (Supabase)

1. Crie uma conta e um projeto grátis em [supabase.com](https://supabase.com).
2. Em **SQL Editor › New query**, cole o conteúdo de `supabase/schema.sql` e clique em **Run** (uma vez só).
3. Em **Authentication › Sign In / Providers › Email**, deixe **Confirm email** ligado. Isso impede que outra pessoa crie a conta do administrador com o seu e-mail.
4. Em **Authentication › URL Configuration**, coloque o endereço do app (por exemplo, o do GitHub Pages) em **Site URL** e em **Redirect URLs**. Os links de confirmação e de nova senha voltam para esse endereço.
5. Em **Project Settings › API**, copie a **Project URL** e a chave **anon public**. Cole em `SUPABASE_URL` e `SUPABASE_ANON_KEY`, no começo do script de `fonte/Main.dc.html`, e gere o app de novo (veja abaixo). A chave anon é pública por natureza; a proteção vem das regras do banco. Nunca use a chave `service_role` no app.
6. Abra o app, crie a conta com `vaipracima10@gmail.com` e confirme pelo e-mail. O botão com o escudo, ao lado do sino, abre o painel do administrador.

O envio de e-mails do Supabase no plano grátis tem limite baixo por hora. Para muitos cadastros, configure um SMTP próprio em **Authentication › Emails**.

Para trocar o administrador, mude o e-mail na função `is_admin()` de `supabase/schema.sql` (rode só ela de novo no SQL Editor) e em `ADMIN_EMAIL`, em `fonte/Main.dc.html`.

## Gerar o app

```
python3 fonte/build.py fonte/Main.dc.html fonte/vendor/react-19.2.8.js vai_pra_cima_1_0_beta.html
```

## Arquivos

| Arquivo | Para quê |
|---|---|
| `vai_pra_cima_1_0_beta.html` | O app inteiro num só arquivo (HTML, CSS e JS; React e cliente do Supabase embutidos, funciona sem CDN). |
| `index.html` | Abre o arquivo acima (útil no GitHub Pages). |
| `fonte/Main.dc.html` | Fonte do design, editável no canvas do Claude. |
| `fonte/build.py` | Gera o HTML do app a partir da fonte. |
| `fonte/vendor/` | React 19.2.8 e supabase-js 2.117.3 (MIT), embutidos no app pelo `build.py`. |
| `supabase/schema.sql` | Tabelas, regras de acesso e peneiras iniciais do banco. |
