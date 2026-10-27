# Busca semanal de peneiras reais

Instruções para a tarefa agendada que procura peneiras reais toda semana. Também servem para quem quiser fazer a busca à mão.

## O que fazer

1. Abra `dados/peneiras-encontradas.json`.
2. Apague da lista as peneiras cuja `data` já passou (hoje em diante fica).
3. Procure na internet peneiras, seletivas, avaliações ou testes de **futebol ou futsal de base (Sub-9 a Sub-20)** no **estado de São Paulo** que vão acontecer nos próximos 60 dias. Boas buscas:
   - "peneira futebol [mês] [ano] São Paulo", "seletiva sub-15 SP", "avaliação técnica categoria de base [cidade]", "peneira futsal feminino SP"
   - sites de clubes paulistas (Palmeiras, Corinthians, São Paulo, Santos, Ponte Preta, Guarani, Red Bull Bragantino, Ferroviária, Ituano, Mirassol, Novorizontino, Botafogo-SP, XV de Piracicaba, Portuguesa, Juventus, São Bernardo, Santo André etc.)
   - portais de divulgação, como futebolpeneira.com.br, e notícias locais
4. **Abra a página de cada peneira** e confira as informações lá. Não use só o resumo da busca.
5. Acrescente ao arquivo só peneiras que tenham, confirmados na fonte: **clube, data, cidade e categorias (ou anos de nascimento)**. Se faltar um desses, não acrescente.
6. Não repita uma peneira que já está no arquivo (mesmo clube e mesma data).
7. Nunca invente nem "complete" dado. O que a fonte não diz fica `null` (ou some, nos campos opcionais) e pode ser explicado em `fonte_texto`.
8. Atualize `atualizado_em` com a data de hoje.
9. Confira o arquivo com `python3 scripts/importar_peneiras.py dados/peneiras-encontradas.json --dry-run`. Toda peneira nova deve aparecer como "nova (oculta)"; corrija as que aparecerem como "pulada".
10. Faça commit no ramo `main` com a mensagem `Busca semanal de peneiras: N novas` e dê push. O GitHub Actions envia as novas para o banco, **ocultas**, e o administrador revisa e publica pelo painel do app.

Se não achar nada novo, não faça commit.

## Formato de cada peneira

```json
{
  "clube": "Ferroviária",
  "divisao": "Seletiva feminina Sub-13 a Sub-17",
  "cidade": "Mauá",
  "endereco": "Rua Rosa Kasinski, 802 – Capuapava",
  "lat": -23.667,
  "lon": -46.461,
  "data": "2026-11-14",
  "hora": "12:00",
  "horarios": "Sub-13: 12h\nSub-15 e Sub-17: 13h",
  "preco": null,
  "vagas": null,
  "total": null,
  "cat_min": 13,
  "cat_max": 17,
  "ano_min": 2010,
  "ano_max": 2016,
  "generos": ["F"],
  "modalidades": ["Futebol"],
  "levar": "Documento com foto, chuteira e água",
  "prazo": "2026-10-31",
  "fonte_url": "https://...",
  "fonte_texto": "Divulgada pelo clube no site oficial em 18/09/2026. Inscrição por formulário até 31/10.",
  "telefone": null
}
```

| Campo | Obrigatório | Como preencher |
|---|---|---|
| `clube` | sim | Nome do clube ou escolinha. |
| `divisao` | sim | Descrição curta: "Base masculina Sub-11 a Sub-15", "Futsal feminino" etc. |
| `cidade` | sim | Cidade da peneira, com acento. |
| `lat`, `lon` | sim | Coordenadas do local ou, se não houver endereço, do centro da cidade. Precisam estar dentro do estado de SP. |
| `data` | sim | `AAAA-MM-DD`. Se a peneira tem vários dias, use o primeiro e explique em `horarios`. |
| `hora` | sim | `HH:MM`, 24 h. Se a fonte não diz, use o horário mais provável informado e avise em `fonte_texto`. |
| `cat_min`, `cat_max` | sim | Números de 9 a 20 (Sub-9 a Sub-20). Calcule pelo ano de nascimento se a fonte só der o ano. |
| `generos` | sim | `["M"]`, `["F"]` ou `["M", "F"]`. |
| `modalidades` | sim | `["Futebol"]`, `["Futsal"]` ou os dois. |
| `fonte_url` | sim | Link `https://` da página onde a informação foi conferida. |
| `ano_min`, `ano_max` | não | Anos de nascimento aceitos, quando a fonte divulga assim. Os dois juntos ou nenhum. |
| `endereco`, `horarios`, `levar`, `prazo`, `telefone` | não | Só o que a fonte disser. `prazo` = inscrições até, `AAAA-MM-DD`. |
| `preco` | não | Número em reais; `0` = grátis; `null` = não informado. |
| `vagas`, `total` | não | Quase nunca divulgados: deixe `null`. |
| `fonte_texto` | não | Quem divulgou, quando, e como se inscrever. |
