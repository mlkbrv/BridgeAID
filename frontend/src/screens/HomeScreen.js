import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Alert,
} from 'react-native';
import {
  Text,
  Card,
  Title,
  Paragraph,
  Button,
  Chip,
  ActivityIndicator,
  FAB,
} from 'react-native-paper';
import { coreAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const HomeScreen = ({ navigation }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      const response = await coreAPI.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.log('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardStats();
    setRefreshing(false);
  };

  const getWelcomeMessage = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  const getRoleEmoji = () => {
    // Determine user role by email or other indicators
    if (user?.email?.includes('employer')) return '🏢';
    if (user?.email?.includes('officer')) return '👮';
    return '👤';
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Welcome Section */}
        <Card style={styles.welcomeCard}>
          <Card.Content>
            <View style={styles.welcomeHeader}>
              <Text style={styles.emoji}>{getRoleEmoji()}</Text>
              <View style={styles.welcomeText}>
                <Title style={styles.welcomeTitle}>
                  {getWelcomeMessage()}, {user?.first_name || 'User'}!
                </Title>
                <Paragraph style={styles.welcomeSubtitle}>
                  Welcome to BridgeAID
                </Paragraph>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Quick Actions */}
        <Card style={styles.actionsCard}>
          <Card.Content>
            <Title style={styles.sectionTitle}>🚀 Quick Actions</Title>
            <View style={styles.actionButtons}>
              <Button
                mode="contained"
                onPress={() => navigation.navigate('Vacancies')}
                style={styles.actionButton}
                icon="briefcase"
              >
                Search Jobs
              </Button>
              <Button
                mode="outlined"
                onPress={() => navigation.navigate('Applications')}
                style={styles.actionButton}
                icon="file-document"
              >
                My Applications
              </Button>
            </View>
          </Card.Content>
        </Card>

        {/* Statistics */}
        {stats && (
          <Card style={styles.statsCard}>
            <Card.Content>
              <Title style={styles.sectionTitle}>📊 Statistics</Title>
              <View style={styles.statsGrid}>
                {Object.entries(stats).map(([key, value]) => (
                  <View key={key} style={styles.statItem}>
                    <Text style={styles.statValue}>{value}</Text>
                    <Text style={styles.statLabel}>
                      {getStatLabel(key)}
                    </Text>
                  </View>
                ))}
              </View>
            </Card.Content>
          </Card>
        )}

        {/* Recent Activity */}
        <Card style={styles.activityCard}>
          <Card.Content>
            <Title style={styles.sectionTitle}>📈 Recent Activity</Title>
            <View style={styles.activityItem}>
              <Text style={styles.activityEmoji}>📝</Text>
              <View style={styles.activityContent}>
                <Text style={styles.activityTitle}>New application submitted</Text>
                <Text style={styles.activityTime}>2 hours ago</Text>
              </View>
            </View>
            <View style={styles.activityItem}>
              <Text style={styles.activityEmoji}>📄</Text>
              <View style={styles.activityContent}>
                <Text style={styles.activityTitle}>Document uploaded</Text>
                <Text style={styles.activityTime}>1 day ago</Text>
              </View>
            </View>
            <View style={styles.activityItem}>
              <Text style={styles.activityEmoji}>💼</Text>
              <View style={styles.activityContent}>
                <Text style={styles.activityTitle}>Job updated</Text>
                <Text style={styles.activityTime}>3 days ago</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Tips */}
        <Card style={styles.tipsCard}>
          <Card.Content>
            <Title style={styles.sectionTitle}>💡 Tips</Title>
            <View style={styles.tipItem}>
              <Text style={styles.tipEmoji}>📋</Text>
              <Text style={styles.tipText}>
                Regularly update your resume
              </Text>
            </View>
            <View style={styles.tipItem}>
              <Text style={styles.tipEmoji}>📁</Text>
              <Text style={styles.tipText}>
                Upload all necessary documents
              </Text>
            </View>
            <View style={styles.tipItem}>
              <Text style={styles.tipEmoji}>📞</Text>
              <Text style={styles.tipText}>
                Respond to employer messages
              </Text>
            </View>
          </Card.Content>
        </Card>
      </ScrollView>

      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => navigation.navigate('Applications')}
      />
    </View>
  );
};

const getStatLabel = (key) => {
  const labels = {
    total_vacancies: 'Jobs',
    open_vacancies: 'Open',
    total_applications: 'Applications',
    pending_applications: 'Pending',
    accepted_applications: 'Accepted',
  };
  return labels[key] || key;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#757575',
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 80,
  },
  welcomeCard: {
    marginBottom: 16,
    elevation: 2,
  },
  welcomeHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  emoji: {
    fontSize: 40,
    marginRight: 16,
  },
  welcomeText: {
    flex: 1,
  },
  welcomeTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  welcomeSubtitle: {
    fontSize: 14,
    color: '#757575',
    marginTop: 4,
  },
  actionsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#212121',
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 4,
  },
  statsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statItem: {
    width: '48%',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#F8F9FA',
    borderRadius: 8,
    marginBottom: 8,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  statLabel: {
    fontSize: 12,
    color: '#757575',
    textAlign: 'center',
    marginTop: 4,
  },
  activityCard: {
    marginBottom: 16,
    elevation: 2,
  },
  activityItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  activityEmoji: {
    fontSize: 20,
    marginRight: 12,
  },
  activityContent: {
    flex: 1,
  },
  activityTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: '#212121',
  },
  activityTime: {
    fontSize: 12,
    color: '#757575',
    marginTop: 2,
  },
  tipsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 6,
  },
  tipEmoji: {
    fontSize: 16,
    marginRight: 12,
  },
  tipText: {
    flex: 1,
    fontSize: 14,
    color: '#212121',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2196F3',
  },
});

export default HomeScreen;
