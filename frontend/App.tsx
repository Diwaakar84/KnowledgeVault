import AppNavigator from "./src/navigation/AppNavigator";
import { AuthProvider } from "./src/store/AuthContext";
import { StatusBar } from "expo-status-bar";

export default function App() {
  return (
    <AuthProvider>
      <StatusBar style="light" />
      <AppNavigator/>
    </AuthProvider>
  );
}
