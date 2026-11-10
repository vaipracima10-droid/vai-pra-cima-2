-- Atualização de 09/11/2026: rode este arquivo uma vez em Supabase › SQL Editor › New query › Run.
-- Corrige a lista de espera: duas pessoas tocando "Tenho interesse" ao mesmo tempo
-- podiam passar do número de vagas. Agora o banco trava a peneira enquanto conta.
-- (Só troca a função; não mexe em nenhum dado.)

create or replace function public.interesse_antes()
returns trigger language plpgsql security definer set search_path = '' as $$
declare p public.peneiras;
begin
  -- "for update" trava a peneira: dois cliques ao mesmo tempo não passam do número de vagas.
  select * into p from public.peneiras where id = new.peneira_id for update;
  if not found then raise exception 'Peneira não encontrada'; end if;
  new.user_id := auth.uid();
  new.origem_real := p.origem_real;
  new.lista_espera := not p.origem_real and p.vagas is not null and (
    select count(*) from public.interesses i
    where i.peneira_id = p.id and not i.lista_espera and not i.origem_real
  ) >= p.vagas;
  new.criado_em := now();
  return new;
end $$;
