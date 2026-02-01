import React, { useEffect, useState } from "react";
import {
  View,
  StyleSheet,
  Alert,
  ActivityIndicator,
} from "react-native";

import KVInput from "../components/KVInput";
import KVButton from "../components/KVButton";
import { DarkTheme } from "../utils/theme";

import {
  createNote,
  updateNote,
  fetchNoteById,
  deleteNote,
} from "../api/notesApi";

export default function NoteEditor({ route, navigation }: any) {
  const noteId = route?.params?.noteId;

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);

  const isEdit = !!noteId;

  useEffect(() => {
    if (isEdit) {
      loadNote();
    }
  }, []);

  async function loadNote() {
    try {
      setFetching(true);

      const note = await fetchNoteById(noteId);

      setTitle(note.title);
      setContent(note.content);
    } catch(e) {
      console.log(e);
      Alert.alert("Error", "Failed to load note");
    } finally {
      setFetching(false);
    }
  }

  async function save() {
    if (!title || !content) {
      Alert.alert("Error", "Title and content required");
      return;
    }

    try {
      setLoading(true);

      if (isEdit) {
        await updateNote(noteId, {
          title,
          content,
          tags: [],
        });
      } else {
        await createNote({
          title,
          content,
          tags: [],
        });
      }

      navigation.goBack();
    } catch (err) {
      Alert.alert("Error", "Failed to save note");
    } finally {
      setLoading(false);
    }
  }

  async function remove() {
    Alert.alert("Delete Note", "Are you sure?", [
      { text: "Cancel" },
      {
        text: "Delete",
        style: "destructive",
        onPress: async () => {
          try {
            await deleteNote(noteId);
            navigation.goBack();
          } catch {
            Alert.alert("Error", "Delete failed");
          }
        },
      },
    ]);
  }

  if (fetching) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={DarkTheme.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <KVInput
        placeholder="Title"
        value={title}
        onChangeText={setTitle}
      />

      <KVInput
        placeholder="Content"
        value={content}
        onChangeText={setContent}
        multiline
        style={styles.content}
      />

      <KVButton
        title={loading ? "Saving..." : "Save"}
        onPress={save}
        disabled={loading}
      />

      {isEdit && (
        <KVButton
          title="Delete"
          variant="danger"
          onPress={remove}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: DarkTheme.background,
  },
  content: {
    height: 200,
    textAlignVertical: "top",
  },
  center: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: DarkTheme.background,
  },
});
