import React from "react";
import { TextInput, StyleSheet } from "react-native";
import { DarkTheme } from "../utils/theme";

export default function AppInput(props: any) {
  return (
    <TextInput
      {...props}
      style={[styles.input, props.style]}
      placeholderTextColor={DarkTheme.placeholder}
    />
  );
}

const styles = StyleSheet.create({
  input: {
    backgroundColor: DarkTheme.inputBg,
    color: DarkTheme.textPrimary,
    borderWidth: 1,
    borderColor: DarkTheme.border,
    borderRadius: 10,
    padding: 12,
    marginBottom: 16,
  },
});
