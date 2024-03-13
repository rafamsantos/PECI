import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import LowerBar from '../../components/LowerBar';
import { useNavigation, useRoute } from '@react-navigation/native';
import UserProfile from '../../components/UserProfile';
import NfcManager, { Ndef, NfcTech } from "react-native-nfc-manager";

const Home = () => {
  const route = useRoute();
  const { params } = route;
  const username = params && params.username ? params.username : '';
  const navigation = useNavigation();

  const userProfile = {
    photoURL: 'https://picsum.photos/200',
    name: 'John Doe',
    email: 'johndoe@example.com',
    personalInfo: 'Engenharia de Computadores e Informática',
  };

  async function readNdef() {
    try {
      // register for the NFC tag with NDEF in it
      await NfcManager.requestTechnology(NfcTech.Ndef);
      // the resolved tag object will contain `ndefMessage` property
      const tag = await NfcManager.getTag();
      console.log('Tag found', tag);
    } catch (ex) {
      console.warn('Oops!', ex);
    } finally {
      // stop the nfc scanning
      NfcManager.cancelTechnologyRequest();
    }
  }

  function generateNdef() {
    const ndefPayload = Ndef.encodeMessage([
      Ndef.textRecord('Hello, NFC!'),
    ]);
    console.log('NFC code generated:', ndefPayload);
  }

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <UserProfile
          photoURL={userProfile.photoURL}
          name={userProfile.name}
          email={userProfile.email}
          personalInfo={userProfile.personalInfo}
        />
        <View style={styles.content}>
          <TouchableOpacity style={styles.button} onPress={() => readNdef()}>
            <Text style={styles.buttonText}>Read NFC</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={() => generateNdef()}>
            <Text style={styles.buttonText}>Generate NFC</Text>
          </TouchableOpacity>
        </View>
      </View>
      <LowerBar />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    padding: 15,
    backgroundColor: '#0080FF',
    borderRadius: 5,
    width: 150,
    height: 50,
    textAlign: 'center',
    marginBottom: 20,
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
    fontSize: 16,
  },
});

export default Home;
