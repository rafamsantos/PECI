import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import LowerBar from '../../components/LowerBar';
import Navigation from '../../navigation';
import { useRoute } from '@react-navigation/native';
import UserProfile from '../../components/UserProfile';

const Home = () => {
  const route = useRoute();
  const { username } = route.params;

  const userProfile = {
    photoURL: 'https://picsum.photos/200',
    name: 'John Doe',
    email: 'johndoe@example.com',
    personalInfo: 'Engenharia de Computadores e Informática',
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <UserProfile
          photoURL={userProfile.photoURL}
          name={userProfile.name}
          email={userProfile.email}
          personalInfo={userProfile.personalInfo}
        />
      </View>
      <LowerBar />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1, // Fill the available space
  },
  content: {
    flex: 1, // Take up the remaining space
    justifyContent: 'center', // Center content vertically
  },
});

export default Home;
