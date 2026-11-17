// Mock exam settings. Update the AIME cutoffs here each year.

export type Track = "amc10" | "amc12";

export const TRACK_LABELS: Record<Track, string> = {
  amc10: "AMC 10",
  amc12: "AMC 12",
};

export const examConfig = {
  questionCount: 25,
  timeLimitMinutes: 75,
  scoring: {
    correct: 6,
    blank: 1.5,
    wrong: 0,
  },
  // AIME qualifying scores (fixed thresholds starting with the 2026 to 2027 season)
  aimeCutoffs: {
    amc10: 100,
    amc12: 85,
  } as Record<Track, number>,
};
