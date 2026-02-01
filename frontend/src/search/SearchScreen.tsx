import React, { useState } from "react";
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
} from "react-native";

import KVInput from "../components/KVInput";
import { DarkTheme } from "../utils/theme";
import { searchNotes, SearchResult } from "../api/searchApi";

export default function SearchScreen() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSearch(text: string) {
    setQuery(text);

    if (!text.trim()) {
      setResults([]);
      return;
    }

    try {
      setLoading(true);
      const data = await searchNotes(text);
      console.log(data);
      setResults(data);
    } catch(e) {
      console.log("Search failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <KVInput
        placeholder="Search notes..."
        value={query}
        onChangeText={handleSearch}
      />

      {loading && (
        <ActivityIndicator
          size="small"
          color={DarkTheme.primary}
        />
      )}

      <FlatList
        data={results}
        keyExtractor={(item) => item.source_id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.title}>{item.title}</Text>
            <Text
              style={styles.preview}
              numberOfLines={2}
            >
              {item.snippet}
            </Text>
          </View>
        )}
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
  card: {
    backgroundColor: DarkTheme.surface,
    padding: 12,
    borderRadius: 10,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: DarkTheme.border,
  },
  title: {
    color: DarkTheme.textPrimary,
    fontWeight: "600",
    marginBottom: 4,
  },
  preview: {
    color: DarkTheme.textSecondary,
  },
});
