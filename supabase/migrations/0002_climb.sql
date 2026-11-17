-- Adds the climb: chosen color scheme, profile icon, and highest altitude reached.
-- Run this in the Supabase SQL Editor after 0001_init.sql.
alter table public.profiles add column if not exists theme text not null default 'summit';
alter table public.profiles add column if not exists avatar text not null default 'initial';
alter table public.profiles add column if not exists best_altitude integer not null default 0;
