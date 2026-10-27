# Prompt do projeto: Vai Pra Cima

Você está me ajudando a desenvolver o **Vai Pra Cima** ("A ponte entre você e o seu futuro"), um app para celular que conecta jovens atletas a **peneiras de futebol e futsal** (testes de seleção em clubes e escolinhas) no estado de São Paulo. Responda sempre em português do Brasil.

## Objetivo

- **Atleta (ou responsável):** encontrar peneiras compatíveis com o seu perfil (Sub-9 a Sub-20, masculino ou feminino, futebol ou futsal, perto da sua cidade), ver quando e onde acontecem, e demonstrar interesse ou entrar na lista de espera com poucos toques.
- **Clube:** criar uma conta, publicar peneiras e receber a lista de atletas interessados, com contato por telefone e WhatsApp.

Hoje é uma **demonstração com dados fictícios**: não há servidor, e tudo fica salvo só no aparelho.

## Stack

- **Um único arquivo HTML** (`vai_pra_cima_0_9_beta.html`, cerca de 400 linhas e 100 KB) com HTML, CSS e JavaScript puro, sem framework nem build.
- **Leaflet 1.9.4** e **Leaflet.markercluster 1.5.3**, carregados do cdnjs, para o mapa com pinos agrupados.
- **localStorage** para guardar o estado (chave `vpc1`; as chaves antigas `pen_me` e `pen_fav` ainda são lidas para manter perfis de versões anteriores) e **sessionStorage** para mostrar a tela de abertura uma vez por sessão.
- Imagens (logo da abertura) embutidas em base64 no próprio arquivo.
- Geolocalização do navegador (botão "📍 GPS"), que só funciona em HTTPS.
- Compartilhamento nativo (`navigator.share`), com cópia do link como alternativa.
- Tema claro e escuro por variáveis CSS (`prefers-color-scheme`), layout com no máximo 600 px de largura, respeito à área segura do iPhone e a `prefers-reduced-motion`.
- Há um aviso para quando o arquivo é aberto num visualizador que não roda JavaScript (WhatsApp, e-mail): o app precisa ser aberto por um link HTTPS no Safari ou no Chrome.

## Estrutura do código

O código é compacto, com nomes curtos. Os principais pontos:

- **Dados fixos:** `CITIES` (15 cidades de SP com coordenadas), `D` (15 peneiras de exemplo) e `SP` (contorno do estado).
- **Estado:** o objeto `S` guarda `role` (`"a"` atleta ou `"c"` clube), `me` (perfil do atleta), `fav` (favoritas), `int` (interesses), `notes` (notificações), `alerts`, `club` (conta do clube) e `cp` (peneiras do clube). A função `save()` grava tudo em `vpc1`.
- **Telas:** elementos com a classe `.v`, trocados pela função `nav(id)`:
  - `s0`: escolha de perfil ("Sou atleta" ou "Sou clube").
  - `s1`: cadastro do atleta (ano de nascimento, gênero, modalidade e cidade ou GPS).
  - `s2`: lista de peneiras, com as abas Lista, Mapa e Calendário.
  - `c1`: criação da conta do clube (nome, cidade, e-mail, WhatsApp e CNPJ fictício).
  - `c2`: painel do clube com as peneiras cadastradas.
  - `c3`: formulário de nova peneira ou de edição.
- **Folha inferior (sheet):** usada para a ficha da peneira (`openSheet`), os filtros (`openFilters`), as notificações (`openNotes`) e a peneira do lado do clube (`openCp`).
- **Funções-chave:** `calc()` monta a lista com distância, compatibilidade e dias que faltam; `ok(p)` diz se a peneira é compatível; `render()`, `drawMap()` e `drawCal()` desenham as três abas; `sendInt()` registra o interesse ou a lista de espera; `contactStep()` pede nome, WhatsApp e posição; `openDeep()` abre o link `?p=ID`; `clubUI()` desenha o painel do clube; `esc()` escapa os textos digitados.

## Modelo de dados

- **Peneira:** `{id, club, div, city, addr, lat, lon, date: "AAAA-MM-DD", time: "HH:MM", price (0 = grátis), vagas, total, cats: [subMín, subMáx], gen: ["M","F"], mod: ["Futebol","Futsal"], req (o que levar), tel}`. As peneiras do clube também têm `st: "open" | "closed"`.
- **Atleta (`me`):** `{ano, gen, mod, city, gps, nome, tel, pos}`. A categoria é calculada como `sub = ano atual − ano de nascimento`.
- **Interesse:** `{id, pid (id da peneira), nome, sub, pos, gen, tel, ts, mine, wait (lista de espera)}`.
- **Clube:** `{nome, city, email, tel, cnpj, verified}`. As peneiras do clube só aparecem para os atletas depois que o clube é verificado (na demo, pelo botão "Simular aprovação").

## Funcionalidades atuais (0.9 beta)

1. **Cadastro enxuto:** a primeira tela pede só ano (já mostra "2013 · Sub-13"), gênero, modalidade e cidade. Nome, WhatsApp e posição só são pedidos ao tocar em "Tenho interesse". Há um "alterar" para corrigir os dados.
2. **Card com a data em destaque:** dia da semana, dia e mês. O card fica verde quando faltam até 6 dias. O km é um detalhe.
3. **Compartilhamento:** o link `?p=7` abre direto a ficha daquela peneira, mesmo para quem nunca usou o app.
4. **Filtros:** chips Compatíveis, Com vagas, Fim de semana e ♥ Favoritas, mais "⚙ Filtros" com contador e a ordenação (Mais próximas ou Mais cedo). Distância, categoria, modalidade e preço ficam numa folha que mostra "Ver N peneiras" ao vivo. Os alertas de novas peneiras ficam numa linha ao lado do contador, com o sininho 🔔 de notificações.
5. **Compatibilidade explicada:** a ficha mostra o motivo de a peneira não servir (ex.: "✗ aceita Sub-15 a Sub-20 (nascidos em 2006–2011); seu atleta é Sub-13") e o card mostra avisos como "Só feminino". Em peneira esgotada, o botão é "Entrar na lista de espera".
6. **Lado do clube:** criar conta, publicar, editar, encerrar, reabrir e excluir peneiras (a exclusão pede um segundo toque), ver os interessados com botões de ligar e WhatsApp, e simular interessados para testar.

## Próximos passos (itens 6 a 10 do plano, ainda não feitos)

- Mini-card ao tocar num pino do mapa.
- Botão voltar do celular funcionando entre telas e folhas.
- Arquivo `.ics` para adicionar a peneira à agenda.
- Transformar em PWA instalável (manifest e service worker; hoje só existem as meta tags de app).
- LGPD, os pinos do mapa e melhorias no painel do clube.

## Como trabalhar comigo

- Mantenha tudo num único arquivo HTML e sem framework, a não ser que eu peça outra coisa.
- Siga o estilo do código existente (compacto, nomes curtos, variáveis CSS para cores).
- Não quebre os dados já salvos no aparelho: continue lendo `vpc1` e as chaves antigas.
- Escape com `esc()` todo texto digitado pelo usuário antes de colocar no HTML.
- Ao entregar uma versão nova, atualize o número no `<title>`, no cabeçalho e no nome do arquivo, e diga o que mudou, o que mudou sem eu pedir e o que ficou para depois.
- Teste em tamanho de celular, nos temas claro e escuro, e avise o que não deu para testar (por exemplo, o mapa sem internet).
- Trate com cuidado os dados de menores de idade (nome e WhatsApp): peça só o necessário.
