-- Summit Math database setup.
-- Run this in the Supabase SQL Editor (or with the Supabase CLI). It is safe to run more than once.
-- Row Level Security makes sure each student can only read and change their own data.

-- Profiles: one row per student
create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  display_name text,
  track text check (track in ('amc10', 'amc12')),
  streak integer not null default 0,
  last_active_date date,
  created_at timestamptz not null default now()
);

-- Mastery level for each skill
create table if not exists public.skill_progress (
  user_id uuid not null references auth.users (id) on delete cascade,
  skill_id text not null,
  level text not null check (level in ('not_started', 'attempted', 'familiar', 'proficient', 'mastered')),
  points integer not null default 0,
  updated_at timestamptz not null default now(),
  primary key (user_id, skill_id)
);

-- Every answered problem
create table if not exists public.attempts (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users (id) on delete cascade,
  problem_id text not null,
  skill_id text not null,
  correct boolean not null,
  time_taken_ms integer not null default 0,
  created_at timestamptz not null default now()
);
create index if not exists attempts_user_idx on public.attempts (user_id, created_at desc);

-- Mock exam results
create table if not exists public.mock_exams (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  track text not null check (track in ('amc10', 'amc12')),
  score numeric not null,
  max_score numeric not null,
  correct integer not null,
  wrong integer not null,
  blank integer not null,
  answers jsonb not null default '{}'::jsonb,
  breakdown jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create index if not exists mock_exams_user_idx on public.mock_exams (user_id, created_at);

-- Row Level Security
alter table public.profiles enable row level security;
alter table public.skill_progress enable row level security;
alter table public.attempts enable row level security;
alter table public.mock_exams enable row level security;

drop policy if exists "Students manage their own profile" on public.profiles;
create policy "Students manage their own profile" on public.profiles
  for all using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists "Students manage their own skill progress" on public.skill_progress;
create policy "Students manage their own skill progress" on public.skill_progress
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "Students manage their own attempts" on public.attempts;
create policy "Students manage their own attempts" on public.attempts
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "Students manage their own mock exams" on public.mock_exams;
create policy "Students manage their own mock exams" on public.mock_exams
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Create a profile automatically when someone signs up (email or Google)
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, display_name)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', new.raw_user_meta_data ->> 'name', split_part(new.email, '@', 1))
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
