import { api } from "./client";

export interface Note {
  id: string;
  title: string;
  content: string;
  version: number;
}

export async function fetchNotes(): Promise<Note[]> {
  const res = await api.get("/notes");
  return res.data;
}

export async function fetchNoteById(id: string): Promise<Note> {
  const res = await api.get(`/notes/${id}`);
  return res.data;
}

export async function createNote(data: {
  title: string;
  content: string;
  tags: string[];
}) {
  const res = await api.post("/notes", data);
  return res.data;
}

export async function updateNote(
  id: string,
  data: {
    title: string;
    content: string;
    tags: string[];
  }
) {
  const res = await api.put(`/notes/${id}`, data);
  return res.data;
}

export async function deleteNote(id: string) {
  const res = await api.delete(`/notes/${id}`);
  return res.data;
}
