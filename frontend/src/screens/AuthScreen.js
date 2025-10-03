import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import {
  Text,
  TextInput,
  Button,
  Card,
  Title,
  Paragraph,
  Switch,
  Divider,
} from 'react-native-paper';
import { useAuth } from '../context/AuthContext';

const AuthScreen = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);

  const { login, register } = useAuth();

  const handleAuth = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please fill in all required fields');
      return;
    }

    if (!isLogin && password !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      let result;
      if (isLogin) {
        result = await login(email, password);
      } else {
        result = await register({
          email,
          password,
          password2: confirmPassword,
          first_name: firstName,
          last_name: lastName,
          phone,
        });
      }

      if (!result.success) {
        Alert.alert('Error', result.error || 'An error occurred');
      }
    } catch (error) {
      Alert.alert('Error', 'An error occurred during authentication');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container} 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <View style={styles.header}>
          <Text style={styles.emoji}>🌉</Text>
          <Title style={styles.title}>BridgeAID</Title>
          <Paragraph style={styles.subtitle}>
            Bridge to your new career
          </Paragraph>
        </View>

        <Card style={styles.card}>
          <Card.Content>
            <View style={styles.switchContainer}>
              <Text style={styles.switchLabel}>Login</Text>
              <Switch
                value={!isLogin}
                onValueChange={() => setIsLogin(!isLogin)}
              />
              <Text style={styles.switchLabel}>Register</Text>
            </View>

            <Divider style={styles.divider} />

            {!isLogin && (
              <>
                <TextInput
                  label="First Name *"
                  value={firstName}
                  onChangeText={setFirstName}
                  style={styles.input}
                  mode="outlined"
                />
                <TextInput
                  label="Last Name *"
                  value={lastName}
                  onChangeText={setLastName}
                  style={styles.input}
                  mode="outlined"
                />
                <TextInput
                  label="Phone"
                  value={phone}
                  onChangeText={setPhone}
                  style={styles.input}
                  mode="outlined"
                  keyboardType="phone-pad"
                />
              </>
            )}

            <TextInput
              label="Email *"
              value={email}
              onChangeText={setEmail}
              style={styles.input}
              mode="outlined"
              keyboardType="email-address"
              autoCapitalize="none"
            />

            <TextInput
              label="Пароль *"
              value={password}
              onChangeText={setPassword}
              style={styles.input}
              mode="outlined"
              secureTextEntry
            />

            {!isLogin && (
              <TextInput
                label="Confirm Password *"
                value={confirmPassword}
                onChangeText={setConfirmPassword}
                style={styles.input}
                mode="outlined"
                secureTextEntry
              />
            )}

            <Button
              mode="contained"
              onPress={handleAuth}
              style={styles.button}
              loading={loading}
              disabled={loading}
            >
              {isLogin ? 'Login' : 'Register'}
            </Button>
          </Card.Content>
        </Card>

        <View style={styles.footer}>
          <Paragraph style={styles.footerText}>
            {isLogin ? 'No account? ' : 'Already have an account? '}
            <Text 
              style={styles.linkText}
              onPress={() => setIsLogin(!isLogin)}
            >
              {isLogin ? 'Register' : 'Login'}
            </Text>
          </Paragraph>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  emoji: {
    fontSize: 60,
    marginBottom: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2196F3',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#757575',
    textAlign: 'center',
  },
  card: {
    elevation: 4,
    marginBottom: 20,
  },
  switchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  switchLabel: {
    fontSize: 16,
    marginHorizontal: 10,
  },
  divider: {
    marginBottom: 20,
  },
  input: {
    marginBottom: 15,
  },
  button: {
    marginTop: 10,
    paddingVertical: 5,
  },
  footer: {
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    color: '#757575',
  },
  linkText: {
    color: '#2196F3',
    fontWeight: 'bold',
  },
});

export default AuthScreen;
