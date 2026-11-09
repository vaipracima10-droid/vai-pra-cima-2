#!/usr/bin/env python3
"""Apaga do Supabase as peneiras de exemplo (fictícias) e as que já aconteceram.

- Exemplo: só as fictícias que vieram no schema.sql (números abaixo de 1000). Peneiras criadas
  no painel nunca são tratadas como exemplo, mesmo que estejam marcadas assim.
- Já aconteceu: só depois que o dia inteiro passou (o app mostra a peneira até a meia-noite).
- Peneiras passadas com interesses ficam no banco: apagar levaria junto (on delete cascade)
  o histórico dos atletas e a lista de contatos do administrador.

Uso:  python3 scripts/limpar_peneiras.py [--dry-run]
Precisa de SUPABASE_URL e SUPABASE_SERVICE_KEY no ambiente (mesmas do importar_peneiras.py).
"""
import os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importar_peneiras import HOJE, credenciais, pedir

PRIMEIRA_IMPORTADA = 1000  # o schema.sql faz as peneiras novas começarem em 1000


def motivo(r, com_interesse):
    if not r['origem_real'] and r['id'] < PRIMEIRA_IMPORTADA:
        return 'fictícia (Exemplo)'
    if r['data'] < HOJE:
        return None if r['id'] in com_interesse else 'já aconteceu'
    return None


def main():
    seco = '--dry-run' in sys.argv
    url, key = credenciais()
    if not url or not key:
        sys.exit('Falta SUPABASE_URL ou SUPABASE_SERVICE_KEY.')
    linhas = pedir(url + '/rest/v1/peneiras?select=id,clube,data,hora,origem_real,ativa&order=data', key)
    com_interesse = {i['peneira_id'] for i in pedir(url + '/rest/v1/interesses?select=peneira_id', key)}
    apagar = []
    for r in linhas:
        m = motivo(r, com_interesse)
        estado = 'visível' if r['ativa'] else 'oculta'
        nota = f' – {m}' if m else (' – já aconteceu, mas tem interesses (fica no histórico)' if r['data'] < HOJE else '')
        print(f"{'APAGAR' if m else 'manter'}: #{r['id']} {r['clube']} em {r['data']} {str(r['hora'])[:5]} ({estado}){nota}")
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
