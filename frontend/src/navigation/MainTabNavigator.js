import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text } from 'react-native';

import HomeScreen from '../screens/HomeScreen';
import VacanciesScreen from '../screens/VacanciesScreen';
import ApplicationsScreen from '../screens/ApplicationsScreen';
import DocumentsScreen from '../screens/DocumentsScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

const MainTabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          
          if (route.name === 'Home') {
            iconName = '🏠';
          } else if (route.name === 'Vacancies') {
            iconName = '💼';
          } else if (route.name === 'Applications') {
            iconName = '📋';
          } else if (route.name === 'Documents') {
            iconName = '📁';
          } else if (route.name === 'Profile') {
            iconName = '👤';
          }
          
          return <Text style={{ fontSize: size, color }}>{iconName}</Text>;
        },
        tabBarActiveTintColor: '#2196F3',
        tabBarInactiveTintColor: '#757575',
        headerStyle: {
          backgroundColor: '#2196F3',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{ title: 'Home' }}
      />
      <Tab.Screen 
        name="Vacancies" 
        component={VacanciesScreen} 
        options={{ title: 'Vacancies' }}
      />
      <Tab.Screen 
        name="Applications" 
        component={ApplicationsScreen} 
        options={{ title: 'Applications' }}
      />
      <Tab.Screen 
        name="Documents" 
        component={DocumentsScreen} 
        options={{ title: 'Documents' }}
      />
      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen} 
        options={{ title: 'Profile' }}
      />
    </Tab.Navigator>
  );
};

export default MainTabNavigator;
