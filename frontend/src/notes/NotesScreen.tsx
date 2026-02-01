import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
  ActivityIndicator,
} from "react-native";

import { fetchNotes, Note } from "../api/notesApi";
import { DarkTheme } from "../utils/theme";
import KVButton from "../components/KVButton";

export default function NotesScreen({ navigation }: any) {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  async function loadNotes() {
    try {
      const data = await fetchNotes();
      setNotes(data);
    } catch (err) {
      console.log("Fetch notes error:", err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    const unsub = navigation.addListener("focus", loadNotes);
    return unsub;
  }, [navigation]);

  async function onRefresh() {
    setRefreshing(true);
    await loadNotes();
  }

  function openEditor(noteId?: string) {
    navigation.navigate("NoteEditor", { noteId });
  }

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={DarkTheme.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={notes}
        keyExtractor={(item) => item.id}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={DarkTheme.textPrimary}
          />
        }
        ListEmptyComponent={
          <Text style={styles.empty}>No notes yet</Text>
        }
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.title}>{item.title}</Text>
            <Text style={styles.preview} numberOfLines={2}>
              {item.content}
            </Text>

            <KVButton
              title="Edit"
              onPress={() => openEditor(item.id)}
            />
          </View>
        )}
      />

      <KVButton
        title="New Note"
        onPress={() => openEditor()}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: DarkTheme.background,
    padding: 16,
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: DarkTheme.background,
  },
  card: {
    backgroundColor: DarkTheme.surface,
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: DarkTheme.border,
  },
  title: {
    fontSize: 18,
    fontWeight: "600",
    color: DarkTheme.textPrimary,
    marginBottom: 4,
  },
  preview: {
    color: DarkTheme.textSecondary,
    marginBottom: 8,
  },
  empty: {
    textAlign: "center",
    marginTop: 40,
    color: DarkTheme.textSecondary,
  },
});
