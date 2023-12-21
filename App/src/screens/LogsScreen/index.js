import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import LowerBar from '../../components/LowerBar';
import HigherBar from '../../components/HigherBar';
import Navigation from '../../navigation';
import { useRoute } from '@react-navigation/native';

const Styles = StyleSheet.create({
  container: {
    flex: 1, // Fill the available space
  },
  content: {
    flex: 1, // Take up the remaining space
    justifyContent: 'center', // Center content vertically
    padding: 20, // Add some padding for better readability
  },
  item: {
    borderRadius: 10, // Round the corners of the list item
    padding: 20, // Add some padding for better readability
    backgroundColor: '#fff', // Set background color to white
    marginBottom: 10, // Add some margin between items
  },
});

const Logs = () => {
  const personalInfo = JSON.parse('[{"doorName": "4.1.01", "entranceTime": "2023-12-21 15:20:00"}, {"doorName": "4.3.14", "entranceTime": "2023-12-21 15:30:15"}, {"doorName": "4.2.30", "entranceTime": "2023-12-21 16:30:00"}, {"doorName": "4.3.30", "entranceTime": "2023-12-21 17:30:00"}, {"doorName": "4.4.30", "entranceTime": "2023-12-21 18:30:00"},{"doorName": "4.1.01", "entranceTime": "2023-12-21 15:20:00"},{"doorName": "4.1.01", "entranceTime": "2023-12-21 15:20:00"},{"doorName": "4.1.01", "entranceTime": "2023-12-21 15:20:00"}]')

  const styles = Styles;

  return (
    <View style={styles.container}>
      {personalInfo.length > 0 ? (
        <View>
          
          <FlatList
            data={personalInfo}
            renderItem={({ item }) => (
              <View style={styles.item}>
                <Text style={{ fontSize: 18, fontWeight: 'bold' }}>{item.doorId}</Text>
                <Text style={{ fontSize: 16 }}>{item.doorName}</Text>
                <Text style={{ fontSize: 14, color: '#ccc' }}>{item.entranceTime}</Text>
              </View>
            )}
            keyExtractor={item => item.doorId}
            padding={50}
          />
          <HigherBar />
        </View>
      ) : (
        <Text>No data found</Text>
      )}
    </View>
  );
};

export default Logs;
