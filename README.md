# Summit Math

A Khan Academy style prep site for the AMC 10 and AMC 12: short lessons, practice with hints and solutions, mastery levels, unit quizzes and tests, and timed mock exams.

The course has 10 units and 51 skills (32 core skills on both tests, 19 AMC 12 only skills) with **1,530 original practice problems**: 20 basics and 10 challenge problems per skill. The topic list follows recent AMC 10 and 12 exams. Every problem is newly written in the style of AMC problems; none are copied from real exams, which are copyrighted by the MAA. Lessons are not written yet, so skill pages say "Lesson coming soon".

---

## 1. Run it on your computer

You need [Node.js](https://nodejs.org) version 20 or newer.

```bash
npm install
npm run dev
```

Open http://localhost:3000.

Without Supabase connected, the site runs in **local mode**: accounts and progress are saved only in your browser, and passwords are not checked. That is fine for building and testing. Connect Supabase before real students use it.

Other commands:

| Command | What it does |
| --- | --- |
| `npm run validate` | Checks every content file and points to any mistakes |
| `npm run build` | Checks content, then builds the site for production |
| `npm start` | Runs the production build |

---

## 2. Connect Supabase (accounts and saved progress)

1. Create a free project at [supabase.com](https://supabase.com).
2. In the project, open **SQL Editor**, paste everything from `supabase/migrations/0001_init.sql`, and click **Run**. Then do the same with `0002_climb.sql`. This creates the tables and the security rules that keep each student's data private.
3. Open **Project Settings, then API**. Copy the **Project URL** and the **publishable key** (called the anon key in older projects).
4. Copy `.env.example` to a new file called `.env.local` and paste the two values in:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-key
   ```
5. In Supabase, open **Authentication, then URL Configuration**:
   - Set **Site URL** to your site's address (http://localhost:3000 while testing).
   - Under **Redirect URLs**, add `http://localhost:3000/**` and later your live address, for example `https://your-site.vercel.app/**`.
6. Restart `npm run dev`. The local mode notes disappear and real accounts work.

### Turn on "Continue with Google"

1. In Supabase, open **Authentication, then Sign In / Providers, then Google**, turn it on, and copy the **Callback URL** it shows.
2. Go to [Google Cloud Console](https://console.cloud.google.com), create a project, then open **APIs and Services**.
3. Set up the **OAuth consent screen**: app name, support email, and your site's address.
4. Open **Credentials, then Create credentials, then OAuth client ID**. Pick **Web application**.
   - Under **Authorized JavaScript origins**, add http://localhost:3000 and your live address.
   - Under **Authorized redirect URIs**, paste the Supabase callback URL from step 1.
5. Copy the **Client ID** and **Client secret** back into the Google provider settings in Supabase and save.
6. While your Google app is in **Testing** mode, only email addresses you add as test users can log in. Click **Publish app** on the consent screen page when you are ready for everyone.

Students who sign in with Google get a profile automatically and go straight to their dashboard.

---

## 3. Deploy to Vercel

1. Put this folder in a GitHub repository.
2. At [vercel.com](https://vercel.com), click **Add New, then Project** and import the repository.
3. Under **Environment Variables**, add `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`.
4. Click **Deploy**.
5. Add your new Vercel address to the Supabase **Site URL** and **Redirect URLs**, and to the Google **Authorized JavaScript origins**.

---

## 4. Adding content

All course content lives in the `content` folder. You never need to touch the code to add lessons or problems. Run `npm run validate` after any change: it tells you the exact file and field if something is wrong.

### Add a unit or a skill

Units are in `content/units`, one JSON file each. The file name does not matter, but numbering them keeps them tidy.

```json
{
  "id": "geometry",
  "title": "Geometry",
  "description": "Triangles, circles, polygons, area, and solids.",
  "track": "both",
  "order": 2,
  "skills": [
    { "id": "similar_triangles", "title": "Similar triangles", "description": "Ratios of sides and areas." },
    { "id": "power_of_a_point", "title": "Power of a point", "description": "" }
  ]
}
```

- `track`: `"both"` for units on both tests, `"amc12"` for units only on the AMC 12. Skills in AMC 12 units get a small "12" marker in the corner and are tracked separately on the Climb page.
- To mark a single skill as AMC 12 only inside a shared unit, add `"track": "amc12"` to that skill.
- `order`: where the unit appears in the course.
- Ids use lowercase letters, numbers and underscores, and every skill id must be unique across the whole course.

### Add a lesson

Create `content/lessons/<skill id>.mdx`, for example `content/lessons/similar_triangles.mdx`:

```mdx
---
title: Similar triangles
videoUrl: https://www.youtube.com/watch?v=YOUR_VIDEO_ID
---

Write the lesson in Markdown. Inline math: $\frac{a}{b}$. Display math:

$$
\frac{[ABC]}{[DEF]} = k^2
$$

<Callout title="Tip">A highlighted tip or common mistake.</Callout>

<Example title="Example 1">A worked example.</Example>
```

`videoUrl` is optional and works with YouTube and Vimeo links.

### Add problems

Problems go in any JSON file in `content/problems` (one file per unit works well). Each file holds a list:

```json
[
  {
    "id": "geo_sim_001",
    "skillId": "similar_triangles",
    "level": "basics",
    "track": "both",
    "prompt": "Triangle $ABC$ is similar to triangle $DEF$ with ratio $2:3$. ...",
    "choices": { "A": "$4$", "B": "$6$", "C": "$9$", "D": "$12$", "E": "$18$" },
    "answer": "C",
    "hints": ["First hint.", "Second hint."],
    "solution": "Full worked solution. Answer **(C)**.",
    "image": "/problems/geo_sim_001.png"
  }
]
```

- `level`: `"basics"` or `"challenge"`. Students answer sets of 4 basics (from a bank of at least 20) and sets of 2 challenge problems (from a bank of at least 10). No problem repeats until the student has seen the whole bank. Change the set and bank sizes in `src/config/mastery.ts`.
- `track`: `"amc12"` keeps the problem out of AMC 10 mock exams.
- `image` is optional. Put the image file in `public/problems`.
- Problems are used everywhere automatically: practice sets, unit quizzes, unit tests and mock exams. Mock exams pick 25 random problems (AMC 10 mocks skip AMC 12 problems), so add plenty.

### The problem generators

The current banks are made by Python scripts in `scripts/problems/`, one per unit group (`algebra.py`, `geometry.py`, `numbertheory.py`, `counting.py`, `amc12.py`). Each problem type is a template that picks new numbers and settings and computes the answer, the wrong choices and the worked solution. To rebuild every unit and problem file:

```bash
python3 scripts/problems/build.py
```

The seeds are fixed, so rebuilding gives the same problems with the same ids, and students' history stays valid. If you change a template, problem ids for that skill may now point to different questions; that only affects the no repeat rotation, not saved mastery. `build.py` also holds the unit and skill titles. Hand written problems can go in a separate file in `content/problems`; the build only replaces the files it writes.

---

## 5. The climb

Students climb from the Trailhead (0 m) toward two peaks:

- **AMC 10 Summit (7,500 m):** reached by mastering every core skill (the ones on both tests).
- **AMC 12 Summit (10,000 m):** the last 2,500 m come from the AMC 12 only skills.

Each mastery level fills more of a skill's share of the climb, so altitude always reflects real skill.

**Checkpoints** stop the climb until the student proves themselves on mock exams. The top three need full length (25 question) mocks and the score on 2 of the last 3, so one lucky exam is not enough:

| Checkpoint | Requirement |
| --- | --- |
| 2,500 m | Take any mock exam |
| 5,500 m (Cloud Pass) | Score 60 or more on an AMC 10 mock (shorter mocks are scaled to 150) |
| 7,000 m (just below the AMC 10 Summit) | 100 or more on 2 of the last 3 full AMC 10 mocks |
| 8,500 m | 85 or more on 2 of the last 3 full AMC 12 mocks |
| 9,500 m (just below the AMC 12 Summit) | 100 or more on 2 of the last 3 full AMC 12 mocks |

**Mastery ladder:** Basics practice takes a skill to Familiar, a perfect Challenge set takes it to Proficient, and only a unit test takes it to Mastered.

**Review:** a Proficient or Mastered skill that has not been practiced for 30 days drops one level and shows "Review due" until the student practices or tests it again. Altitude drops with it, but unlocked colors and icons are never taken away.

Mastery rules and the review period are in `src/config/mastery.ts`. Change any of these numbers in `src/config/climb.ts`.

## 6. Changing the look and the rules

| What | Where |
| --- | --- |
| Every color | `src/app/theme.css` |
| Fonts | `src/app/layout.tsx` and `src/app/globals.css` |
| Site name, tagline, contact email | `src/config/site.ts` |
| Mastery rules and quiz and test lengths | `src/config/mastery.ts` |
| Mock exam length, timer, scoring, AIME cutoffs | `src/config/exam.ts` |
| Landing page sample problem | `src/components/TryProblem.tsx` |
| Camps, altitude, mock exam checkpoints, unlockable colors and icons | `src/config/climb.ts` |
| Unlockable color scheme colors | `src/app/theme.css` (bottom of the file) |
| Contact, Privacy, Terms | `src/app/contact`, `privacy`, `terms` |

"Summit Math" is a placeholder name. Pick your own; using "AMC" in a site name may conflict with the MAA's trademarks.

---

## 7. How the code is organized

```
content/                 Course content (units, lessons, problems)
supabase/migrations/     Database tables and security rules
scripts/                 Content checker
src/app/                 Pages (one folder per address)
src/components/          Reusable pieces: ProblemCard, ChoiceButton, HintPanel,
                         MasteryBadge, ProgressRing, Timer, UnitCard, ProblemSession, MockExam
src/config/              Settings you are likely to change
src/lib/content/         Reads and validates the content folder
src/lib/store/           Saves progress (browser storage or Supabase)
src/lib/mastery.ts       How levels go up and down
src/proxy.ts             Keeps Supabase logins fresh
```

## Before launch

- Write a real privacy policy. Many students will be under 18, and some under 13, so check the rules that apply (such as COPPA in the United States).
- Write the lessons (one MDX file per skill in `content/lessons`), and have a strong student or teacher spot check the problem banks.
- Publish your Google OAuth app.
