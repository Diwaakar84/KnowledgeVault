import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { DarkTheme } from "../utils/theme";
import KVButton from "../components/KVButton";
import { useAuth } from "../store/AuthContext";

export default function ProfileScreen({ navigation }: any) {
  const { logout } = useAuth();

  async function logoutUser() {
    await logout();
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Profile</Text>

      <KVButton
        title="Logout"
        onPress={logoutUser}
        variant="danger"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: DarkTheme.background,
  },
  title: {
    fontSize: 24,
    marginBottom: 24,
    color: DarkTheme.textPrimary,
  },
});
