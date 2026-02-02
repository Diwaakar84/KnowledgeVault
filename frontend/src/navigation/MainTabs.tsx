import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import ProfileScreen from "../profile/ProfileScreen";
import NotesScreen from "../notes/NotesScreen";
import SearchScreen from "../search/SearchScreen";
import { DarkTheme } from "../utils/theme";
import { Ionicons } from "@expo/vector-icons";

const Tab = createBottomTabNavigator();

export default function MainTabs() {

  return (
    <Tab.Navigator 
      screenOptions={({ route }) => ({
        tabBarStyle: {
          backgroundColor: DarkTheme.surface,
          borderTopColor: DarkTheme.border,
          height: 60,
          paddingBottom: 8,
        },

        tabBarActiveTintColor: DarkTheme.primary,
        tabBarInactiveTintColor: DarkTheme.textSecondary,

        tabBarIcon: ({ color, size, focused }) => {
          let iconName: any;

          if (route.name === "Notes") {
            iconName = focused ? "document-text" : "document-text-outline";
          } else if (route.name === "Search") {
            iconName = focused ? "search" : "search-outline";
          } else if (route.name === "Profile") {
            iconName = focused ? "person" : "person-outline";
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Notes" component={NotesScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
