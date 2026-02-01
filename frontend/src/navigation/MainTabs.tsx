import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import ProfileScreen from "../profile/ProfileScreen";
import NotesScreen from "../notes/NotesScreen";
import SearchScreen from "../search/SearchScreen";

const Tab = createBottomTabNavigator();

export default function MainTabs() {

  return (
    <Tab.Navigator>
      <Tab.Screen name="Notes" component={NotesScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
