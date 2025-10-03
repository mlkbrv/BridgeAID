import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
  Image,
} from 'react-native';
import {
  Text,
  Card,
  Title,
  Paragraph,
  Button,
  TextInput,
  Switch,
  List,
  Divider,
  Avatar,
} from 'react-native-paper';
import { useAuth } from '../context/AuthContext';
import { authAPI } from '../services/api';

const ProfileScreen = ({ navigation }) => {
  const { user, logout } = useAuth();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
  });

  useEffect(() => {
    if (user) {
      setProfileData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone: user.phone || '',
      });
    }
  }, [user]);

  const handleSave = async () => {
    setLoading(true);
    try {
      await authAPI.updateProfile(profileData);
      Alert.alert('Success', 'Profile updated');
      setEditing(false);
    } catch (error) {
      Alert.alert('Error', 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Logout', onPress: logout, style: 'destructive' },
      ]
    );
  };

  const getRoleInfo = () => {
    if (user?.email?.includes('employer')) {
      return { emoji: '🏢', title: 'Employer', description: 'Job management' };
    }
    if (user?.email?.includes('officer')) {
      return { emoji: '👮', title: 'Officer', description: 'Visa case processing' };
    }
    return { emoji: '👤', title: 'Candidate', description: 'Job search' };
  };

  const roleInfo = getRoleInfo();

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Avatar.Text 
          size={80} 
          label={user?.first_name?.[0] || 'U'} 
          style={styles.avatar}
        />
        <Title style={styles.name}>
          {user?.first_name} {user?.last_name}
        </Title>
        <Paragraph style={styles.email}>{user?.email}</Paragraph>
        
        <View style={styles.roleContainer}>
          <Text style={styles.roleEmoji}>{roleInfo.emoji}</Text>
          <View style={styles.roleInfo}>
            <Text style={styles.roleTitle}>{roleInfo.title}</Text>
            <Text style={styles.roleDescription}>{roleInfo.description}</Text>
          </View>
        </View>
      </View>

      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <Title style={styles.cardTitle}>👤 Personal Information</Title>
            <Button
              mode="text"
              onPress={() => setEditing(!editing)}
              style={styles.editButton}
            >
              {editing ? 'Cancel' : 'Edit'}
            </Button>
          </View>

          <Divider style={styles.divider} />

          <View style={styles.form}>
            <TextInput
              label="First Name"
              value={profileData.first_name}
              onChangeText={(text) => setProfileData({...profileData, first_name: text})}
              style={styles.input}
              mode="outlined"
              disabled={!editing}
            />
            <TextInput
              label="Last Name"
              value={profileData.last_name}
              onChangeText={(text) => setProfileData({...profileData, last_name: text})}
              style={styles.input}
              mode="outlined"
              disabled={!editing}
            />
            <TextInput
              label="Email"
              value={profileData.email}
              onChangeText={(text) => setProfileData({...profileData, email: text})}
              style={styles.input}
              mode="outlined"
              disabled={!editing}
              keyboardType="email-address"
            />
            <TextInput
              label="Phone"
              value={profileData.phone}
              onChangeText={(text) => setProfileData({...profileData, phone: text})}
              style={styles.input}
              mode="outlined"
              disabled={!editing}
              keyboardType="phone-pad"
            />

            {editing && (
              <Button
                mode="contained"
                onPress={handleSave}
                style={styles.saveButton}
                loading={loading}
                disabled={loading}
              >
                Save
              </Button>
            )}
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.cardTitle}>📊 Statistics</Title>
          <Divider style={styles.divider} />
          
          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Text style={styles.statEmoji}>📋</Text>
              <View style={styles.statInfo}>
                <Text style={styles.statValue}>12</Text>
                <Text style={styles.statLabel}>Applications submitted</Text>
              </View>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statEmoji}>💼</Text>
              <View style={styles.statInfo}>
                <Text style={styles.statValue}>5</Text>
                <Text style={styles.statLabel}>Jobs viewed</Text>
              </View>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statEmoji}>📁</Text>
              <View style={styles.statInfo}>
                <Text style={styles.statValue}>8</Text>
                <Text style={styles.statLabel}>Documents uploaded</Text>
              </View>
            </View>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.cardTitle}>⚙️ Settings</Title>
          <Divider style={styles.divider} />
          
          <List.Item
            title="🔔 Notifications"
            description="Receive notifications about new jobs"
            right={() => <Switch value={true} />}
            onPress={() => {}}
          />
          <List.Item
            title="🌙 Dark Theme"
            description="Use dark theme for the app"
            right={() => <Switch value={false} />}
            onPress={() => {}}
          />
          <List.Item
            title="🌍 Language"
            description="English"
            right={() => <Text>›</Text>}
            onPress={() => {}}
          />
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.cardTitle}>ℹ️ Information</Title>
          <Divider style={styles.divider} />
          
          <List.Item
            title="📞 Support"
            description="Contact support"
            right={() => <Text>›</Text>}
            onPress={() => Alert.alert('Support', 'Feature in development')}
          />
          <List.Item
            title="📋 Terms of Service"
            description="Read terms of service"
            right={() => <Text>›</Text>}
            onPress={() => Alert.alert('Terms', 'Feature in development')}
          />
          <List.Item
            title="🔒 Privacy Policy"
            description="Read privacy policy"
            right={() => <Text>›</Text>}
            onPress={() => Alert.alert('Policy', 'Feature in development')}
          />
          <List.Item
            title="ℹ️ About App"
            description="Version 1.0.0"
            right={() => <Text>›</Text>}
            onPress={() => Alert.alert('About App', 'BridgeAID v1.0.0')}
          />
        </Card.Content>
      </Card>

      <View style={styles.logoutContainer}>
        <Button
          mode="outlined"
          onPress={handleLogout}
          style={styles.logoutButton}
          textColor="#F44336"
          icon="logout"
        >
          Logout
        </Button>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#FFFFFF',
    marginBottom: 16,
  },
  avatar: {
    backgroundColor: '#2196F3',
    marginBottom: 16,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#212121',
    marginBottom: 4,
  },
  email: {
    fontSize: 16,
    color: '#757575',
    marginBottom: 16,
  },
  roleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8F9FA',
    padding: 12,
    borderRadius: 8,
  },
  roleEmoji: {
    fontSize: 24,
    marginRight: 12,
  },
  roleInfo: {
    flex: 1,
  },
  roleTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#212121',
  },
  roleDescription: {
    fontSize: 14,
    color: '#757575',
  },
  card: {
    margin: 16,
    marginTop: 0,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#212121',
  },
  editButton: {
    marginLeft: 8,
  },
  divider: {
    marginVertical: 12,
  },
  form: {
    marginTop: 8,
  },
  input: {
    marginBottom: 16,
  },
  saveButton: {
    marginTop: 8,
  },
  statsContainer: {
    marginTop: 8,
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  statEmoji: {
    fontSize: 20,
    marginRight: 12,
    width: 24,
  },
  statInfo: {
    flex: 1,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  statLabel: {
    fontSize: 14,
    color: '#757575',
  },
  logoutContainer: {
    padding: 16,
    paddingBottom: 32,
  },
  logoutButton: {
    borderColor: '#F44336',
  },
});

export default ProfileScreen;
