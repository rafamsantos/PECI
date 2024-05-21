import React, {useState}from 'react'
import { View, Text, Image, StyleSheet, useWindowDimensions, Alert} from 'react-native'
//import AsyncStorage from '@react-native-async-storage/async-storage';
import Logo from '../../../assets/images/ua2.png'
import CustomInput from '../../components/CustomInput';
import CustomButton from '../../components/CustomButton';
import { useNavigation } from '@react-navigation/native';
import LowerBar from '../../components/LowerBar';
import CONFIG from '../../config_url';


const RegisterScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');

    const {height} = useWindowDimensions();
    const navigation = useNavigation();

    const API_URL =CONFIG.FLASK_URL;

    const handleRegistration = async () => {
        if (!validateEmail(email)) {
            Alert.alert('Invalid Email', 'Please enter a valid UA email.');
            return;
        }
      
        if (!validatePassword(password)) {
            Alert.alert('Invalid Password', 'Password must be between 12 and 128 characters.');
            return;
        }

        if (!validatePasswordMatch(confirmPassword, password)) {
            Alert.alert('Password Mismatch', 'Please make sure the passwords match.');
            return;
        }

        // Envio dos dados de register para o backend
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password, confirmPassword })
            });
            const result = await response.json();
            setMessage(result.message);
            
            if (result.message === 'Redirecting to Email Verification'){
                navigation.navigate('VerifyEmailScreen' , {email, password});
            }else if (result.message === 'Password has been compromised before. Use a different one'){
                Alert.alert('Password Compromised', 'Please use another password.');
            }else if (result.message === 'Use a stronger password'){
                Alert.alert('Password is too weak', 'Use a stronger password.');
            }else{
                Alert.alert('Email Verification error', 'Failure in Sending Email Verification Code');
            }
    };
    

    const validateEmail = (email) => {
        return /\b[A-Za-z0-9._%+-]+@ua\.pt\b/.test(email);
    };
    
    const validatePassword = (password) => {
        return password.length >= 12 && password.length <= 128;
    };

    const validatePasswordMatch = (confirmPassword, password) => {
        return password === confirmPassword;
    };

    return (
        <View style={[style.root, {backgroundColor: 'white',height: height}]}>
            <Image source={Logo} style={[style.Logo,{height: height*0.3}]} resizeMode='contain'/>
            <CustomInput placeholder="email" value={email} setValue={setEmail}/>
            <CustomInput placeholder="Password" value= {password} setValue={setPassword} secureTextEntry={true}/> 
            <CustomInput placeholder="Confirm Password" value= {confirmPassword} setValue={setConfirmPassword} secureTextEntry={true}/>   
            <CustomButton text="Register" onPress={handleRegistration} disabled={!validatePasswordMatch(password, confirmPassword)}/>
        </View>
    );
};

const style = StyleSheet.create({
    root:{
        alignItems: 'center',
        padding: 20,
        marginTop: 0,
    },
    Logo:{
        width: '70%',
        maxWidth:500,
        maxHeight: 200,
    },
});
 export default RegisterScreen;