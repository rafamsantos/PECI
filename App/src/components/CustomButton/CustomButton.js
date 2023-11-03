import React from 'react';
import { View, Text, TextInput, StyleSheet, Pressable } from 'react-native';

const CustomButton = ({onPress, text}) => {
    return (

        <Pressable onPress={onPress} style ={style.container} >
            <Text style = {style.Text}>{text}</Text>
        </Pressable>
    );
};

const style = StyleSheet.create({
    container:{
        backgroundColor: '#3B71F3',
        width : '100%',

        padding: 15,
        marginVertical: 5,

        alignItems: 'center',
        borderRadius: 5,
    
    },
    Text:{
        fontWeight: 'bold',
        color: 'white',
    },
});

export default CustomButton;