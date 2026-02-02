import { DarkTheme } from "./theme";
import { DarkTheme as NavDarkTheme } from "@react-navigation/native";

export const NavigationDarkTheme = {
  ...NavDarkTheme,
  colors: {
    ...NavDarkTheme.colors,

    background: DarkTheme.background,
    card: DarkTheme.surface,
    text: DarkTheme.textPrimary,
    border: DarkTheme.border,
    primary: DarkTheme.primary,
    notification: DarkTheme.primary,
  },
};
