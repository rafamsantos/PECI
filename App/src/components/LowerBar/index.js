import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';

const LowerBar = () => {
  const navigation = useNavigation();

  const buttonClickListener = (buttonName) => {
    if (buttonName === 'Logs') {
      navigation.navigate('Logs');
    } else if (buttonName === 'Acessos') {
      navigation.navigate('DoorAccess');
    }
  };

  return (
    <View style={styles.absoluteBottomBar}>
      <View style={styles.bottomBar}>
        <TouchableOpacity
          style={styles.button}
          onPress={() => buttonClickListener('Logs')}
        >
          <Text style={styles.buttonText}>Logs</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.button}
          onPress={() => buttonClickListener('Acessos')}
        >
          <Text style={styles.buttonText}>Portas</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  absoluteBottomBar: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
  },
  bottomBar: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: 15,
    backgroundColor: 'lightgray',
  },
  button: {
    padding: 15,
    backgroundColor: '#0BDA51',
    borderRadius: 5,
    width: '45%',
    textAlign: 'center',
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
    fontSize: 16,
  },
});

export default LowerBar;