import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from "react-native";

import { api } from "../api/client";
import KVInput from "../components/KVInput";
import KVButton from "../components/KVButton";
import { DarkTheme } from "../utils/theme";

export default function RegisterScreen({ navigation }: any) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRegister() {
    if (!email || !password) {
      Alert.alert("Error", "Enter email and password");
      return;
    }

    try {
      setLoading(true);

      await api.post("/auth/register", {
        email,
        password,
      });

      Alert.alert("Success", "Account created. Please login.");

      navigation.pop();
    } catch (err: any) {
      Alert.alert(
        "Registration Failed",
        err?.response?.data?.detail || "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create Account</Text>

      <KVInput 
        placeholder="Email"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />

      <KVInput 
        placeholder="Password"
        autoCapitalize="none"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <KVButton 
        title={loading ? "Creating..." : "Register"}
        onPress={handleRegister}
        disabled={loading}
      />

      <TouchableOpacity onPress={() => navigation.goBack()}>
        <Text style={styles.link}>Back to Login</Text>
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
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 32,
    textAlign: "center",
    color: DarkTheme.textPrimary,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  button: {
    backgroundColor: "#22c55e",
    padding: 14,
    borderRadius: 8,
    marginBottom: 16,
  },
  buttonText: {
    color: "#fff",
    textAlign: "center",
    fontWeight: "600",
  },
  link: {
    textAlign: "center",
    color: DarkTheme.primary,
    marginTop: 16,
  },
});
