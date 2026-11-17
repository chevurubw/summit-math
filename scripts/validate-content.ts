// Checks every file in /content and prints any problems.
// Run with: npm run validate
import { loadContent } from "../src/lib/content/load";

try {
  const { units, problems, warnings } = loadContent();
  const skills = units.reduce((n, u) => n + u.skills.length, 0);
  console.log(`Content looks good: ${units.length} units, ${skills} skills, ${problems.length} problems.`);
  for (const w of warnings) console.log(`  Note: ${w}`);
} catch (e) {
  console.error((e as Error).message);
  process.exit(1);
}
