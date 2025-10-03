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
  FAB,
  ActivityIndicator,
  SegmentedButtons,
} from 'react-native-paper';
import { coreAPI } from '../services/api';

const ApplicationsScreen = ({ navigation }) => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = async () => {
    try {
      const response = await coreAPI.getCandidateApplications();
      setApplications(response.data.results || response.data);
    } catch (error) {
      console.log('Error loading applications:', error);
      Alert.alert('Error', 'Failed to load applications');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadApplications();
    setRefreshing(false);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'applied': return '#2196F3';
      case 'screening': return '#FF9800';
      case 'interview': return '#9C27B0';
      case 'offered': return '#4CAF50';
      case 'accepted': return '#4CAF50';
      case 'rejected': return '#F44336';
      default: return '#757575';
    }
  };

  const getStatusEmoji = (status) => {
    switch (status) {
      case 'applied': return '📝';
      case 'screening': return '🔍';
      case 'interview': return '💼';
      case 'offered': return '🎉';
      case 'accepted': return '✅';
      case 'rejected': return '❌';
      default: return '⚪';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'applied': return 'Applied';
      case 'screening': return 'Under Review';
      case 'interview': return 'Interview';
      case 'offered': return 'Offered';
      case 'accepted': return 'Accepted';
      case 'rejected': return 'Rejected';
      default: return status;
    }
  };

  const filteredApplications = applications.filter(app => {
    if (filter === 'all') return true;
    return app.status === filter;
  });

  const filterButtons = [
    { value: 'all', label: 'All' },
    { value: 'applied', label: 'Applied' },
    { value: 'screening', label: 'Under Review' },
    { value: 'interview', label: 'Interview' },
    { value: 'offered', label: 'Offered' },
    { value: 'accepted', label: 'Accepted' },
    { value: 'rejected', label: 'Rejected' },
  ];

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Loading applications...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.filterContainer}>
        <SegmentedButtons
          value={filter}
          onValueChange={setFilter}
          buttons={filterButtons}
          style={styles.segmentedButtons}
        />
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {filteredApplications.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content style={styles.emptyContent}>
              <Text style={styles.emptyEmoji}>📋</Text>
              <Title style={styles.emptyTitle}>
                {filter === 'all' ? 'No applications' : 'No applications in this category'}
              </Title>
              <Paragraph style={styles.emptyText}>
                {filter === 'all' 
                  ? 'Apply for a job that interests you'
                  : 'No applications in this category yet'
                }
              </Paragraph>
            </Card.Content>
          </Card>
        ) : (
          filteredApplications.map((application) => (
            <Card key={application.id} style={styles.applicationCard}>
              <Card.Content>
                <View style={styles.applicationHeader}>
                  <View style={styles.applicationTitleContainer}>
                    <Title style={styles.applicationTitle}>
                      {application.vacancy}
                    </Title>
                    <View style={styles.statusContainer}>
                      <Text style={styles.statusEmoji}>
                        {getStatusEmoji(application.status)}
                      </Text>
                      <Chip
                        style={[
                          styles.statusChip,
                          { backgroundColor: getStatusColor(application.status) }
                        ]}
                        textStyle={styles.statusText}
                      >
                        {getStatusText(application.status)}
                      </Chip>
                    </View>
                  </View>
                </View>

                <View style={styles.applicationInfo}>
                  <View style={styles.infoRow}>
                    <Text style={styles.infoEmoji}>👤</Text>
                    <Text style={styles.infoText}>{application.candidate}</Text>
                  </View>
                  <View style={styles.infoRow}>
                    <Text style={styles.infoEmoji}>📅</Text>
                    <Text style={styles.infoText}>
                      Подана: {new Date(application.submitted_at).toLocaleDateString('ru-RU')}
                    </Text>
                  </View>
                  {application.score && (
                    <View style={styles.infoRow}>
                      <Text style={styles.infoEmoji}>⭐</Text>
                      <Text style={styles.infoText}>
                        Оценка: {application.score}/100
                      </Text>
                    </View>
                  )}
                </View>

                {application.cover_letter && (
                  <Paragraph style={styles.coverLetter} numberOfLines={3}>
                    {application.cover_letter}
                  </Paragraph>
                )}

                <View style={styles.applicationFooter}>
                  <Text style={styles.updatedAt}>
                    Обновлено: {new Date(application.updated_at).toLocaleDateString('ru-RU')}
                  </Text>
                  <View style={styles.actionButtons}>
                    <Button
                      mode="outlined"
                      onPress={() => {
                        // Навигация к деталям заявки
                        Alert.alert('Детали заявки', 'Функция в разработке');
                      }}
                      style={styles.actionButton}
                      icon="eye"
                    >
                      Подробнее
                    </Button>
                    {application.status === 'applied' && (
                      <Button
                        mode="contained"
                        onPress={() => {
                          Alert.alert('Отозвать заявку', 'Вы уверены?');
                        }}
                        style={styles.actionButton}
                        icon="close"
                      >
                        Отозвать
                      </Button>
                    )}
                  </View>
                </View>
              </Card.Content>
            </Card>
          ))
        )}
      </ScrollView>

      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => {
          // Навигация к поиску вакансий
          navigation.navigate('Vacancies');
        }}
      />
    </View>
  );
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
  filterContainer: {
    padding: 16,
    paddingBottom: 8,
  },
  segmentedButtons: {
    backgroundColor: '#FFFFFF',
  },
  scrollContent: {
    padding: 16,
    paddingTop: 8,
    paddingBottom: 80,
  },
  applicationCard: {
    marginBottom: 16,
    elevation: 2,
  },
  applicationHeader: {
    marginBottom: 12,
  },
  applicationTitleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  applicationTitle: {
    flex: 1,
    fontSize: 18,
    fontWeight: 'bold',
    color: '#212121',
    marginRight: 8,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusEmoji: {
    fontSize: 16,
    marginRight: 4,
  },
  statusChip: {
    height: 24,
  },
  statusText: {
    color: '#FFFFFF',
    fontSize: 12,
  },
  applicationInfo: {
    marginBottom: 12,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  infoEmoji: {
    fontSize: 14,
    marginRight: 8,
    width: 20,
  },
  infoText: {
    fontSize: 14,
    color: '#757575',
    flex: 1,
  },
  coverLetter: {
    fontSize: 14,
    color: '#212121',
    lineHeight: 20,
    marginBottom: 16,
    fontStyle: 'italic',
  },
  applicationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  updatedAt: {
    fontSize: 12,
    color: '#757575',
    flex: 1,
  },
  actionButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  actionButton: {
    borderRadius: 20,
  },
  emptyCard: {
    marginTop: 50,
    elevation: 2,
  },
  emptyContent: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyEmoji: {
    fontSize: 60,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#757575',
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 14,
    color: '#757575',
    textAlign: 'center',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2196F3',
  },
});

export default ApplicationsScreen;
