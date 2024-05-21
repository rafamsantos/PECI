import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Modal, Button } from 'react-native';
import HigherBar from '../../components/HigherBar';
import Navigation from '../../navigation';
import { useRoute } from '@react-navigation/native';
import CONFIG from '../../config_url';



const DoorAccessScreen = ({ navigation }) => {
  const doorList = [
    { id: 1, name: '4.3.14' },
    { id: 2, name: '4.2.18' },
    { id: 3, name: 'MakerLab' },
    { id: 4, name: '4.1.8' },
    { id: 5, name: '4.2.27' },
    // Add more doors as needed
  ];

  const route = useRoute();
  const { params } = route;
  const username = params && params.username ? params.username : ''; 
  const data = params.data;

  // //const [doorList,setDoorList] = useState([])

  // useEffect(() => {
  //   if (data) {
  //     setDoorList(data);
  //   }
  // }, [data]);


  const API_URL =CONFIG.FLASK_URL;

  const openDoor = async () => {
    try {
        const response = await fetch(`${API_URL}/opendoor`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Response from Flask backend:', data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
  };

  
  function openTheDoor() {
    console.log("open button pressed")
    openDoor();
    
    /*const ndefPayload = Ndef.encodeMessage([
      Ndef.textRecord('Hello, NFC!'),
    ]);
    console.log('NFC code generated:', ndefPayload);*/
  }

  const styles = Styles;
  const [selectedDoor, setSelectedDoor] = useState(null);

  const handleOpenDoor = (doorName) => {
    setSelectedDoor(doorName);
  };

  const confirmOpenDoor = () => {
    // Implement the logic to open the selected door
    console.log('Opening door: ${selectedDoor}');
    openTheDoor();
    setSelectedDoor(null); // Reset selectedDoor after confirmation
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={doorList}
        contentContainerStyle={{ alignItems: 'center', marginTop: 100, color:"red"}} // Align FlatList content to center
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => handleOpenDoor(item.name)}>
            <View style={[styles.item,{alignItems:"center"}]}>
              <Text style={{ fontSize: 18 }}>{item.name}</Text>
            </View>
          </TouchableOpacity>
        )}
        keyExtractor={(item) => item.id.toString()}
      />
      <HigherBar />
      {username==="admin" &&
        <Modal
        visible={selectedDoor !== null}
        transparent={true}
        animationType="slide"
        onRequestClose={() => setSelectedDoor(null)}>
        <View style={styles.modalContainer}>
            <View style={styles.modalContent}>
            <Text style={styles.modalText}>Do you want to access {selectedDoor}?</Text>
            <View style={styles.modalButtonContainer}>
                <TouchableOpacity style={styles.modalButton} onPress={confirmOpenDoor}>
                <Text style={styles.modalButtonText}>Open</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.modalButton} onPress={() => setSelectedDoor(null)}>
                <Text style={styles.modalButtonText}>Cancel</Text>
                </TouchableOpacity>
            </View>
            </View>
        </View>
        </Modal>
    }

    </View>
  );
};
const Styles = StyleSheet.create({
    container: {
      flex: 1,
    },
    content: {
      flex: 1,
      justifyContent: 'center',
      padding: 20,
      marginTop:20,

    },
    item: {
      borderRadius: 10,
      padding: 20,
      backgroundColor: '#fff',
      color:"black",
      marginBottom: 10,
      width:300,
    },
    modalContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      color:"black",
    },
    modalContent: {
      backgroundColor: 'white',
      padding: 20,
      borderRadius: 10,
      alignItems: 'center',
    },
    modalText: {
      marginBottom: 20,
      fontSize: 18,
      color:"black"
    },
    modalButtonContainer: {
      flexDirection: 'row',
      justifyContent: 'center',
      marginTop: 20,
    },
    modalButton: {
      backgroundColor: '#0080FF',
      borderRadius: 5,
      paddingVertical: 10,
      paddingHorizontal: 20,
      marginHorizontal: 10,
    },
    modalButtonText: {
      color: 'white',
      textAlign: 'center',
      fontSize: 16,
    },
  });
  

export default DoorAccessScreen;