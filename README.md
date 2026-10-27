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

## Dados

- Peneiras com a etiqueta **"Peneira real"** vêm de divulgação pública e trazem a fonte. Confira sempre nos canais oficiais do clube.
- Peneiras com a etiqueta **"Exemplo"** são fictícias (clubes, endereços e telefones inventados).
- Tudo fica salvo só no aparelho, no `localStorage` (chave `vpc1`; as chaves antigas `pen_me` e `pen_fav` ainda são lidas).

## Arquivos

| Arquivo | Para quê |
|---|---|
| `vai_pra_cima_1_0_beta.html` | O app inteiro num só arquivo (HTML, CSS e JS; React embutido, funciona sem CDN). |
| `index.html` | Abre o arquivo acima (útil no GitHub Pages). |
| `fonte/Main.dc.html` | Fonte do design, editável no canvas do Claude. |
| `fonte/build.py` | Gera o HTML do app a partir da fonte. |
