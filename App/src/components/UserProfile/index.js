import React from 'react';
import { View, Text, Image } from 'react-native';

const UserProfile = ({ photoURL, name, email, personalInfo }) => {
  return (
    <View style={{ flex: 1, alignItems: 'center' , padding: 80}}>
      <Image
        source={{ uri: photoURL }}
        style={{ width: 100, height: 100, borderRadius: 50 }}
      />
      <Text style={{ fontSize: 24, fontWeight: 'bold' , padding: 20}}>{name}</Text>
      <Text style={{ fontSize: 20, marginTop: 10 }}>{email}</Text>
      <Text style={{ fontSize: 16, padding:50}}>{personalInfo}</Text>
    </View>
  );
};

export default UserProfile;
