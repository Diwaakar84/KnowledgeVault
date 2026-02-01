import React from "react";
import { TouchableOpacity, Text, StyleSheet } from "react-native";
import { DarkTheme } from "../utils/theme";

interface Props {
  title: string;
  onPress: () => void;
  variant?: "primary" | "danger";
  disabled?: boolean;
}

export default function AppButton({
  title,
  onPress,
  variant = "primary",
  disabled,
}: Props) {
  return (
    <TouchableOpacity
      style={[
        styles.button,
        variant === "danger" && styles.danger,
        disabled && styles.disabled,
      ]}
      onPress={onPress}
      disabled={disabled}
    >
      <Text style={styles.text}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: DarkTheme.primary,
    padding: 14,
    borderRadius: 10,
    marginVertical: 8,
  },
  danger: {
    backgroundColor: DarkTheme.danger,
  },
  disabled: {
    opacity: 0.6,
  },
  text: {
    color: DarkTheme.textPrimary,
    textAlign: "center",
    fontWeight: "600",
    fontSize: 16,
  },
});
