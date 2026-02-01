import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from "react-native";

import { api } from "../api/client";
import { saveToken } from "../store/authStorage";
import { DarkTheme } from "../utils/theme";
import KVInput from "../components/KVInput";
import KVButton from "../components/KVButton";
import { useAuth } from "../store/AuthContext";

export default function LoginScreen({ navigation }: any) {
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    if (!email || !password) {
      Alert.alert("Error", "Enter email and password");
      return;
    }

    try {
      setLoading(true);

      const res = await api.post("/auth/login", {
        email,
        password,
      });

      await login(res.data.access_token);
    } catch (err: any) {
      Alert.alert(
        "Login Failed",
        err?.response?.data?.detail || "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Knowledge Vault</Text>

      <KVInput
        placeholder="Email"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />

      <KVInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <KVButton
        title={loading ? "Logging in..." : "Login"}
        onPress={handleLogin}
        disabled={loading}
      />

      <TouchableOpacity onPress={() => navigation.navigate("Register")}>
        <Text style={styles.link}>Create account</Text>
      </TouchableOpacity>
    </View>
);

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
    backgroundColor: DarkTheme.background,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 32,
    textAlign: "center",
    color: DarkTheme.textPrimary,
  },
  link: {
    textAlign: "center",
    color: DarkTheme.primary,
    marginTop: 16,
  },
});
