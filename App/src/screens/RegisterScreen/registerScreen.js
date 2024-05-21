import React, {useState}from 'react'
import { View, Text, Image, StyleSheet, useWindowDimensions, Alert} from 'react-native'
//import AsyncStorage from '@react-native-async-storage/async-storage';
import Logo from '../../../assets/images/ua.png'
import CustomInput from '../../components/CustomInput';
import CustomButton from '../../components/CustomButton';
import { useNavigation } from '@react-navigation/native';
import LowerBar from '../../components/LowerBar';


const RegisterScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');

    const {height} = useWindowDimensions();
    const navigation = useNavigation();

    const API_URL ='http://192.168.95.27:3000';

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
        console.log("checks passed")
        // Envio dos dados de register para o backend
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password, confirmPassword })
            });
            console.log("waiting response")
            const result = await response.json();
            setMessage(result.message);
            console.log("response got")
            if (result.message === 'Redirecting to Email Verification'){
                navigation.navigate('VerifyEmailScreen' , {email, password});
            }else
            {
                Alert.alert('Registration Error', result.message);
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
        <View style={style.root}>
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
    },
    Logo:{
        width: '70%',
        maxWidth:500,
        maxHeight: 200,
    },
});
 export default RegisterScreen;