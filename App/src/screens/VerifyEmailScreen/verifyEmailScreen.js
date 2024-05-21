import React, {useState}from 'react'
import { View, Text, Image, StyleSheet, useWindowDimensions, Alert} from 'react-native'
//import AsyncStorage from '@react-native-async-storage/async-storage';
import Logo from '../../../assets/images/ua.png'
import CustomInput from '../../components/CustomInput';
import CustomButton from '../../components/CustomButton';
import { useNavigation, useRoute } from '@react-navigation/native';
import LowerBar from '../../components/LowerBar';


const VerifyEmailScreen = () => {
    const [code, setCode] = useState('');
    const [message, setMessage] = useState('');
    const route = useRoute();
    const {email, password} = route.params;

    const {height} = useWindowDimensions();
    const navigation = useNavigation();

    const API_URL ='http://192.168.95.27:3000';

    const onConfirmPressed = async () => {

        const response = await fetch(`${API_URL}/verifyEmail`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({code, email, password})
        });
    
        const result = await response.json();
        setMessage(result.message);

        if (result.message === 'Successful Email Verification'){
            navigation.navigate('SignIn')
        }else
        {
            Alert.alert('Registration Error', result.message);
            navigation.navigate('RegisterScreen');
        }

    };

    return (
        <View style={style.root}>
            <Image source={Logo} style={[style.Logo,{height: height*0.3}]} resizeMode='contain'/>
            <CustomInput placeholder="code" value={code} setValue={setCode}/> 
            <CustomButton text="Confirm" onPress={onConfirmPressed}/>
        
        </View>
    );
};

const style = StyleSheet.create({
    root:{
        alignItems: 'center',
        padding: 20,
    },
    Logo:{
        width: '70%',
        maxWidth:500,
        maxHeight: 200,
    },
});
 export default VerifyEmailScreen;