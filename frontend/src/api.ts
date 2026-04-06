const BASE = "/api";

export interface Caller {
  id: number;
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  phone_number: string;
}

export interface CallSummary {
  id: number;
  call_id: string;
  caller: Caller;
  duration_seconds: number;
  duration_display: string;
  caller_type: "new_client" | "existing_client" | "opposing_party" | "unknown";
  called_at: string;
  summary: string;
  audio_file: string;
  urgent: boolean;
  urgent_reason: string;
  follow_up_sent: boolean;
  requires_appointment: boolean;
  proposed_appointment: string | null;
}

export interface CallDetail extends CallSummary {
  transcript: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface Stats {
  total_calls: number;
  urgent: number;
  email_sent: number;
  no_action: number;
  avg_duration_seconds: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export async function fetchCalls(
  params: Record<string, string> = {}
): Promise<PaginatedResponse<CallSummary>> {
  const q = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE}/calls/${q ? "?" + q : ""}`);
  return res.json();
}

export async function fetchCall(id: number): Promise<CallDetail> {
  const res = await fetch(`${BASE}/calls/${id}/`);
  return res.json();
}

export async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${BASE}/stats/`);
  return res.json();
}

export async function updateNotes(
  id: number,
  notes: string
): Promise<CallDetail> {
  const res = await fetch(`${BASE}/calls/${id}/notes/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ notes }),
  });
  return res.json();
}
