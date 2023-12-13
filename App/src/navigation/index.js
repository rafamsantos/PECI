import React from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import SignInScreen from '../screens/SignInScreen';
import HomeScreen from '../screens/HomeScreen';
import DoorAccessScreen from '../screens/DoorAccessScreen';
import LogsScreen from '../screens/LogsScreen';


const Stack = createStackNavigator();


const Navigation = () => {
    return (
        <NavigationContainer>
            <Stack.Navigator screenOptions={{headerShown:false}}>
                <Stack.Screen name="SignIn" component={SignInScreen} />
                <Stack.Screen name="Home" component={HomeScreen} />
                <Stack.Screen name="DoorAccess" component={DoorAccessScreen} />
                <Stack.Screen name="Logs" component={LogsScreen} />
            </Stack.Navigator>            
        </NavigationContainer>
    );
};

const style = StyleSheet.create({
   

});

export default Navigation;