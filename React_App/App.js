import React from 'react';
import Camera from './components/Camera';
import {Text,View,SafeAreaView} from 'react-native';

const App = () => {
  return(
    <>
      <SafeAreaView>
        <Camera />
      </SafeAreaView>
    </>
  ) 
};
export default App;