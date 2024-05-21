import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, useWindowDimensions, Image} from 'react-native';
//import AsyncStorage from '@react-native-async-storage/async-storage';
import Logo from '../../../assets/images/ua2.png'
import LowerBar from '../../components/LowerBar';
import { useNavigation, useRoute } from '@react-navigation/native';
import UserProfile from '../../components/UserProfile';
import NfcManager, { Ndef, NfcTech } from "react-native-nfc-manager";
import CONFIG from '../../config_url';

const Home = () => {
  const route = useRoute();
  const { params } = route;
  const [data, setData] = useState(null);
  const username = params && params.username ? params.username : '';
  const navigation = useNavigation();
  const {height} = useWindowDimensions();

  const API_URL =CONFIG.FLASK_URL;

  useEffect(() => {
    fetchDoorData();
  }, []);


  const fetchData = async () => {
    try {
        const response = await fetch(`${API_URL}/door`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Response from Flask backend:', data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
  };

  const fetchDoorNum = async () => {
    try {
        const response = await fetch(`${API_URL}/doorNum`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error('Error fetching data:', error);
        return null
    }
  };
  
  const fetchDoorData = async () => {
    const fetchedDoorData = await fetchDoorNum();
    setData(fetchedDoorData);
  }


  const fetchMore = async () =>{
    try {
      const response = await fetch(`${API_URL}/checkNFC`);
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('Response from Flask backend:', data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }

  }

 /* const [isAdmin, setIsAdmin] = useState(false);

  useEffect(()=> {
    checkUserRole();
  },[])

  const checkUserRole = async () => {

    const userRole = await AsyncStorage.getItem('userRole');

    if (userRole == 'admin'){

      setIsAdmin(true);
    }

  }*/

  //{isAdmin &&<LowerBar />} <-- substituir no LowerBar para implementar accesso exlusivo para o admin 


  async function readNdef() {
    console.log("read NFC button pressed")
    
    try {
      fetchData();
      // Try android beam 
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

  
async function writeNdef() {
  let result = false;
  console.log("WriteNFC button pressed")
  try {
    fetchData();

    // STEP 1
    console.log("STEP1 not done")

    await NfcManager.requestTechnology(NfcTech.Ndef);

    console.log("STEP1 is being done");

    const bytes = Ndef.encodeMessage([Ndef.textRecord('1C443B87')]);

    console.log("STEP1 done");

    if (bytes) {
      await NfcManager.ndefHandler.writeNdefMessage(bytes); // STEP 3
      result = true;
      console.log("STEP2 and 3 done");
    }
  } catch (ex) {
    console.warn('Oops!', ex);
  } finally {
    // STEP 4
    console.log("STEP4 done");
    NfcManager.cancelTechnologyRequest();
  }

  return result;
}


  function generateNdef() {
    console.log("generate NFC button pressed")
    fetchMore();
    
    /*const ndefPayload = Ndef.encodeMessage([
      Ndef.textRecord('Hello, NFC!'),
    ]);
    console.log('NFC code generated:', ndefPayload);*/
  }

  
  const userProfile = {
    email: username,
  };

  const buttonClickListener = (buttonName) => {
    if (buttonName === 'Logs') {
      navigation.navigate('Logs');
    } else if (buttonName === 'Acessos') {
      console.log(data)
      navigation.navigate('DoorAccess',{username:username, fetchedData: data});
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: 'white',height:height,  }]}>
          <Image source={Logo} style={[styles.Logo]} />

        <View style={styles.content}>
            <View style={styles.textContent}>
                <Text style={styles.welcomeText}>Bem-vindo{"\n"}{username}</Text>
            </View>
            <View style={styles.buttonsContainer}>
                <TouchableOpacity style={styles.button} onPress={() => writeNdef()}>
                    <Text style={styles.buttonText}>Read NFC</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={() => generateNdef()}>
                    <Text style={styles.buttonText}>Generate NFC</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={() => buttonClickListener('Logs')}>
                    <Text style={styles.buttonText}>Logs</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={() => buttonClickListener('Acessos')}>
                    <Text style={styles.buttonText}>Portas</Text>
                </TouchableOpacity>
            </View>
        </View>
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
  textContent: {
      alignItems: 'center',
  },
  welcomeText: {
      color: 'black',
      fontSize: 30,
      textAlign: 'center',
  },
  buttonsContainer: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'center',
      marginTop: 150,
  },
  button: {
      padding: 15,
      backgroundColor: '#0080FF',
      borderRadius: 5,
      width: 150,
      height: 80,
      justifyContent: 'center',
      alignItems: 'center',
      margin: 5,
  },
  buttonText: {
      color: 'white',
      textAlign: 'center',
      fontSize: 16,
  },
  Logo:{
    width: 200,
    maxHeight: 80,
    marginTop: 20,
    
    marginLeft:110
},
});
export default Home;
