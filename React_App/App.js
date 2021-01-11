import React from 'react';
import {View, Text} from 'react-native';

const App = () => {
  return ( // can't return html tags, must be React Native components
    <View style={{flex:1, justifyContent: 'center', alignItems:'center'}}>
      <Text>Bryan's World</Text>
    </View>
  )
}

export default App;