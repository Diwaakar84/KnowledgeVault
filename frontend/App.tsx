import AppNavigator from "./src/navigation/AppNavigator";
import "react-native-gesture-handler";
import { AuthProvider } from "./src/store/AuthContext";

export default function App() {
  return (
    <AuthProvider>
      <AppNavigator/>
    </AuthProvider>
  );
}
