import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';

const HigherBar = () => {
  const navigation = useNavigation();

  const handleBack = () => {
    navigation.pop(); // Navigate back to the previous screen
  };

  return (
    <View style={styles.absoluteTopBar}>
      <View style={styles.backButtonContainer}>
        <TouchableOpacity style={styles.backButton} onPress={handleBack}>
          <Text style={styles.backButtonText}>←</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  absoluteTopBar: {
    position: 'absolute',
    top: 0,
    width: '100%',
  },
  backButtonContainer: {
    position: 'absolute',
    top: 20,
    left: 20,
    width: 60,
    height: 60,
    backgroundColor: '#0BDA51',
    borderRadius: 50,
    alignItems: 'center',
  },
  backButton: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  backButtonText: {
    color: 'white',
    fontSize: 35,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});

export default HigherBar;
