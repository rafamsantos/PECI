import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import LowerBar from '../../components/LowerBar';
import Navigation from '../../navigation';
import { useRoute } from '@react-navigation/native';


const Logs = () => {
    
    return (
        <View style={styles.container}>
            <View style={styles.content}>
                <Text style={{ fontSize: 24, alignSelf: 'center' }}>Página de Logs</Text>
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

export default Logs;
