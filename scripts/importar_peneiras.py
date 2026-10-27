#!/usr/bin/env python3
"""Envia as peneiras de dados/peneiras-encontradas.json para o Supabase.

Entram como "Peneira real" e OCULTAS (ativa = false), para o administrador revisar no painel.
Peneiras que já estão no banco (mesmo clube e mesma data) são puladas, então editar ou
mostrar uma peneira no painel nunca é desfeito por este script.

Uso:  python3 scripts/importar_peneiras.py dados/peneiras-encontradas.json [--dry-run]
Precisa de SUPABASE_URL e SUPABASE_SERVICE_KEY (chave secret/service_role) no ambiente.
"""
import json, os, re, sys, unicodedata, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone

HOJE = (datetime.now(timezone.utc) - timedelta(hours=3)).date().isoformat()  # horário de Brasília
CAMPOS = ['clube', 'divisao', 'cidade', 'endereco', 'lat', 'lon', 'data', 'hora', 'horarios', 'preco', 'vagas', 'total',
          'cat_min', 'cat_max', 'ano_min', 'ano_max', 'generos', 'modalidades', 'levar', 'prazo', 'fonte_url', 'fonte_texto', 'telefone']


def chave(clube, data):
    t = unicodedata.normalize('NFKD', str(clube)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', t) + '|' + str(data)


def problema(p):
    """Devolve o motivo para pular a peneira, ou None se ela estiver boa."""
    for k in ('clube', 'divisao', 'cidade', 'data', 'hora', 'cat_min', 'cat_max', 'generos', 'modalidades', 'fonte_url', 'lat', 'lon'):
        if p.get(k) in (None, '', []):
            return 'falta ' + k
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(p['data'])):
        return 'data inválida'
    if p['data'] < HOJE:
        return 'já aconteceu'
    if not re.fullmatch(r'\d{2}:\d{2}', str(p['hora'])):
        return 'hora inválida (use HH:MM)'
    if not (isinstance(p['cat_min'], int) and isinstance(p['cat_max'], int) and 9 <= p['cat_min'] <= p['cat_max'] <= 20):
        return 'categorias precisam ir de 9 a 20'
    if not set(p['generos']) <= {'M', 'F'} or not set(p['modalidades']) <= {'Futebol', 'Futsal'}:
        return 'gênero ou modalidade inválidos'
    if not str(p['fonte_url']).startswith('https://'):
        return 'fonte_url precisa começar com https://'
    if not (-25.5 <= p['lat'] <= -19.5 and -53.5 <= p['lon'] <= -44.0):
        return 'lat/lon fora do estado de São Paulo'
    if (p.get('ano_min') is None) != (p.get('ano_max') is None):
        return 'preencha ano_min e ano_max juntos'
    if p.get('prazo') and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(p['prazo'])):
        return 'prazo inválido'
    return None


def pedir(url, chave_api, metodo='GET', corpo=None):
    h = {'apikey': chave_api, 'Content-Type': 'application/json', 'Prefer': 'return=minimal'}
    if not chave_api.startswith('sb_'):  # chave antiga (JWT) também vai no Authorization
        h['Authorization'] = 'Bearer ' + chave_api
    req = urllib.request.Request(url, method=metodo, headers=h, data=json.dumps(corpo).encode() if corpo is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else None
    except urllib.error.HTTPError as e:
        sys.exit(f'Erro {e.code} do Supabase em {metodo} {url}: {e.read().decode()[:500]}')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    seco = '--dry-run' in sys.argv
    lista = json.load(open(args[0] if args else 'dados/peneiras-encontradas.json', encoding='utf-8'))['peneiras']
    if not lista:
        return print('A lista está vazia: nada a enviar.')
    url, key = os.environ.get('SUPABASE_URL', '').rstrip('/'), os.environ.get('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        if not seco:
            sys.exit('Falta SUPABASE_URL ou SUPABASE_SERVICE_KEY. Veja "Busca automática" no README.')
        existentes = set()
    else:
        existentes = {chave(r['clube'], r['data']) for r in pedir(url + '/rest/v1/peneiras?select=clube,data', key)}

    novas, vistas = [], set()
    for p in lista:
        nome = f"{p.get('clube')} em {p.get('data')}"
        motivo = problema(p)
        if motivo:
            print(f'pulada: {nome}: {motivo}')
            continue
        k = chave(p['clube'], p['data'])
        if k in existentes or k in vistas:
            print(f'já está no banco: {nome}')
            continue
        vistas.add(k)
        linha = {c: p.get(c) for c in CAMPOS}
        linha.update(origem_real=True, ativa=False)
        novas.append(linha)
        print(f'nova (oculta): {nome}')

    if not novas:
        print('Nenhuma peneira nova.')
    elif seco:
        print(f'{len(novas)} peneira(s) seriam enviadas (--dry-run: nada foi gravado).')
    else:
        pedir(url + '/rest/v1/peneiras', key, 'POST', novas)
        print(f'{len(novas)} peneira(s) enviadas, ocultas, para revisão no painel do administrador.')


if __name__ == '__main__':
    main()
