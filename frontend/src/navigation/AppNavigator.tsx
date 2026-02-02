import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import MainTabs from "./MainTabs";
import LoginScreen from "../auth/LoginScreen";
import RegisterScreen from "../auth/RegisterScreen";
import NoteEditor from "../notes/NoteEditor";
import { useAuth } from "../store/AuthContext";
import { NavigationDarkTheme } from "../utils/navigationTheme";

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  const { isLoggedIn, loading } = useAuth();

  if (loading) {
    return null;
  }

  return (
    <NavigationContainer theme={NavigationDarkTheme}>
      <Stack.Navigator>
        {isLoggedIn ? (
          <>
            <Stack.Screen 
              name="Main" 
              component={MainTabs} 
              options={{ headerShown: false }} 
            />
            <Stack.Screen name="NoteEditor" component={NoteEditor} />
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
