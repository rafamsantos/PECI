import React, {useState}from 'react'
import { View, Text , Image, StyleSheet, useWindowDimensions} from 'react-native'
import Logo from '../../../assets/images/ua.png'
import CustomInput from '../../components/CustomInput';
import CustomButton from '../../components/CustomButton';
import { useNavigation } from '@react-navigation/native';
import LowerBar from '../../components/LowerBar';


const SignInScreen = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const {height} = useWindowDimensions();
    const navigation = useNavigation();

    const onSignInPressed = () => {
        console.warn('Sign In Pressed');
        console.log('Username before navigation:', username);
        // should obviously check if credentials are correct
        navigation.navigate('Home', { username: username });

    };

    return (
        <View style={style.root}>
            <Image source={Logo} style={[style.Logo,{height: height*0.3}]} resizeMode='contain'/>
            <CustomInput placeholder="email" value={username} setValue={setUsername}/>
            <CustomInput placeholder="Password" value= {password} setValue={setPassword} secureTextEntry={true}/>    
            <CustomButton text="Sign In" onPress={onSignInPressed}/>
        
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
 export default SignInScreen;