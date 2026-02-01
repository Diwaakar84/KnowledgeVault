import { api } from "./client";

export interface SearchResult {
  source_id: string;
  title: string;
  snippet: string;
}

export async function searchNotes(query: string): Promise<SearchResult[]> {
  if (!query.trim()) return [];

  const res = await api.get("/search", {
    params: { q: query },
  });

  return res.data;
}
