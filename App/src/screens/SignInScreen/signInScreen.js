import React, {useState, useEffect}from 'react'
import { View, Text, Image, StyleSheet, useWindowDimensions, Alert} from 'react-native'
//import AsyncStorage from '@react-native-async-storage/async-storage';
import Logo from '../../../assets/images/ua2.png'
import CustomInput from '../../components/CustomInput';
import CustomButton from '../../components/CustomButton';
import { useNavigation } from '@react-navigation/native';
import LowerBar from '../../components/LowerBar';
import CONFIG from '../../config_url';


const SignInScreen = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const {height} = useWindowDimensions();
    const navigation = useNavigation();

    const API_URL = CONFIG.FLASK_URL;

    const onRegisterPressed = async () => {
        navigation.navigate('RegisterScreen');
    };

    useEffect(() => {
        const signIn = async () => {
            const response = await fetch(`${API_URL}/signin`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ username, password })
            });
    
            const result = await response.json();
            setMessage(result.message);
    
            if (result.message === 'Session is open') {
                navigation.navigate('Home', {username : username});
            }
        };
    
        signIn();
      }, []);


    const onSignInPressed = async () => {
        //console.warn('Sign In Pressed');
        console.log('Username before navigation:', username);
        
        const response = await fetch(`${API_URL}/signin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username, password})
            });
    
        const result = await response.json();
        setMessage(result.message);

        if (result.message === 'Success in Sending Verification Code'){
            navigation.navigate('VerifyCodeScreen', {username : username});
        }else if(result.message === 'Session is open'){
            navigation.navigate('Home', {username : username});
        }else{
            Alert.alert('Registration Error', result.message);
        }

    };

    return (
        <View style={[style.root, { backgroundColor: 'white',height: height}]}>
            <Image source={Logo} style={[style.Logo,{height: height*0.3}]} resizeMode='contain'/>
            <CustomInput placeholder="email" value={username} setValue={setUsername}/>
            <CustomInput placeholder="Password" value= {password} setValue={setPassword} secureTextEntry={true}/>    
            <CustomButton text="Sign In" onPress={onSignInPressed}/>
            <CustomButton text="Register" onPress={onRegisterPressed}/>
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
        maxHeight: 100,
        marginTop: 20,
        marginBottom: 100,
    },
});
export default SignInScreen;