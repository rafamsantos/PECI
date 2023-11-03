import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

const LowerBar = () => {
  return (
    <View style={styles.bottomBar}>
      <TouchableOpacity
        style={styles.button}
        onPress={buttonClickListener("Home")}
      >
        <Text style={styles.buttonText}>Home</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.button}
        onPress={buttonClickListener("Logs")}
      >
        <Text style={styles.buttonText}>Logs</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.button}
        onPress={buttonClickListener("Acessos")}
      >
        <Text style={styles.buttonText}>Acessos</Text>
      </TouchableOpacity>
    </View>
  );
};

const buttonClickListener = (buttonName) => {
  // Handle button click here
  console.log('button clicked', buttonName);

};

const styles = StyleSheet.create({
  bottomBar: {
    flexDirection: 'row',
    justifyContent: 'space-around', // Center the buttons horizontally
    alignItems: 'center',
    padding: 20,
    backgroundColor: 'lightgray',
  },
  button: {
    padding: 10, // Increase padding to make buttons larger
    backgroundColor: '#0BDA51', // Button background color
    borderRadius: 5, // Add rounded corners
    width: "30%",
    textAlign: "center",
  },
  buttonText: {
    color: 'white', // Text color
    textAlign: 'center', // Center button text horizontally
    fontSize: 16,
  },
});

export default LowerBar;
