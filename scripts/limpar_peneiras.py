#!/usr/bin/env python3
"""Apaga do Supabase as peneiras de exemplo (fictícias) e as que já aconteceram.

Atenção: apagar uma peneira também apaga os interesses ligados a ela (on delete cascade).

Uso:  python3 scripts/limpar_peneiras.py [--dry-run]
Precisa de SUPABASE_URL e SUPABASE_SERVICE_KEY no ambiente (mesmas do importar_peneiras.py).
"""
import os, sys, urllib.parse
from datetime import datetime, timedelta, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importar_peneiras import pedir

AGORA = datetime.now(timezone.utc) - timedelta(hours=3)  # horário de Brasília
HOJE, HORA = AGORA.date().isoformat(), AGORA.strftime('%H:%M')


def motivo(r):
    if not r['origem_real']:
        return 'fictícia (Exemplo)'
    if r['data'] < HOJE or (r['data'] == HOJE and str(r['hora'])[:5] <= HORA):
        return 'já aconteceu'
    return None


def main():
    seco = '--dry-run' in sys.argv
    url, key = os.environ.get('SUPABASE_URL', '').rstrip('/'), os.environ.get('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        sys.exit('Falta SUPABASE_URL ou SUPABASE_SERVICE_KEY.')
    linhas = pedir(url + '/rest/v1/peneiras?select=id,clube,data,hora,origem_real,ativa&order=data', key)
    apagar = []
    for r in linhas:
        m = motivo(r)
        estado = 'visível' if r['ativa'] else 'oculta'
        print(f"{'APAGAR' if m else 'manter'}: #{r['id']} {r['clube']} em {r['data']} {str(r['hora'])[:5]} ({estado})" + (f' – {m}' if m else ''))
        if m:
            apagar.append(r['id'])
    print(f'{len(apagar)} de {len(linhas)} peneira(s) para apagar.')
    if apagar and not seco:
        ids = ','.join(map(str, apagar))
        pedir(url + '/rest/v1/peneiras?id=in.(' + urllib.parse.quote(ids) + ')', key, 'DELETE')
        print(f'{len(apagar)} peneira(s) apagadas.')
    elif seco:
        print('--dry-run: nada foi apagado.')


if __name__ == '__main__':
    main()
