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
  Searchbar,
  FAB,
  ActivityIndicator,
} from 'react-native-paper';
import { coreAPI } from '../services/api';

const VacanciesScreen = ({ navigation }) => {
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadVacancies();
  }, []);

  const loadVacancies = async () => {
    try {
      const response = await coreAPI.getVacancies();
      setVacancies(response.data.results || response.data);
    } catch (error) {
      console.log('Error loading vacancies:', error);
      Alert.alert('Error', 'Failed to load vacancies');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadVacancies();
    setRefreshing(false);
  };

  const handleApply = (vacancy) => {
    Alert.alert(
      'Apply for Job',
      `Do you want to apply for the position "${vacancy.title}"?`,
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Apply', 
          onPress: () => {
            // Navigate to application form
            navigation.navigate('Applications', { 
              screen: 'ApplicationForm',
              params: { vacancyId: vacancy.id }
            });
          }
        },
      ]
    );
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open': return '#4CAF50';
      case 'closed': return '#F44336';
      case 'paused': return '#FF9800';
      default: return '#757575';
    }
  };

  const getStatusEmoji = (status) => {
    switch (status) {
      case 'open': return '🟢';
      case 'closed': return '🔴';
      case 'paused': return '🟡';
      default: return '⚪';
    }
  };

  const filteredVacancies = vacancies.filter(vacancy =>
    vacancy.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    vacancy.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    vacancy.location.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Loading vacancies...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Searchbar
          placeholder="Search vacancies..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchBar}
        />
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {filteredVacancies.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content style={styles.emptyContent}>
              <Text style={styles.emptyEmoji}>🔍</Text>
              <Title style={styles.emptyTitle}>
                {searchQuery ? 'Nothing found' : 'No vacancies'}
              </Title>
              <Paragraph style={styles.emptyText}>
                {searchQuery 
                  ? 'Try changing your search query'
                  : 'Vacancies will appear here when added'
                }
              </Paragraph>
            </Card.Content>
          </Card>
        ) : (
          filteredVacancies.map((vacancy) => (
            <Card key={vacancy.id} style={styles.vacancyCard}>
              <Card.Content>
                <View style={styles.vacancyHeader}>
                  <View style={styles.vacancyTitleContainer}>
                    <Title style={styles.vacancyTitle}>{vacancy.title}</Title>
                    <View style={styles.statusContainer}>
                      <Text style={styles.statusEmoji}>
                        {getStatusEmoji(vacancy.status)}
                      </Text>
                      <Chip
                        style={[
                          styles.statusChip,
                          { backgroundColor: getStatusColor(vacancy.status) }
                        ]}
                        textStyle={styles.statusText}
                      >
                        {vacancy.status === 'open' ? 'Open' : 
                         vacancy.status === 'closed' ? 'Closed' : 'Paused'}
                      </Chip>
                    </View>
                  </View>
                </View>

                <View style={styles.vacancyInfo}>
                  <View style={styles.infoRow}>
                    <Text style={styles.infoEmoji}>🏢</Text>
                    <Text style={styles.infoText}>{vacancy.employer}</Text>
                  </View>
                  <View style={styles.infoRow}>
                    <Text style={styles.infoEmoji}>📍</Text>
                    <Text style={styles.infoText}>{vacancy.location}</Text>
                  </View>
                  {vacancy.salary && (
                    <View style={styles.infoRow}>
                      <Text style={styles.infoEmoji}>💰</Text>
                      <Text style={styles.infoText}>
                        {vacancy.salary} {vacancy.currency}
                      </Text>
                    </View>
                  )}
                  {vacancy.remote && (
                    <View style={styles.infoRow}>
                      <Text style={styles.infoEmoji}>🏠</Text>
                      <Text style={styles.infoText}>Remote work</Text>
                    </View>
                  )}
                </View>

                <Paragraph style={styles.vacancyDescription} numberOfLines={3}>
                  {vacancy.description}
                </Paragraph>

                <View style={styles.vacancyFooter}>
                  <Text style={styles.createdAt}>
                    📅 {new Date(vacancy.created_at).toLocaleDateString('en-US')}
                  </Text>
                  <Button
                    mode="contained"
                    onPress={() => handleApply(vacancy)}
                    style={styles.applyButton}
                    icon="send"
                  >
                    Apply
                  </Button>
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
          // Navigate to create vacancy (for employers)
          Alert.alert('Create Vacancy', 'Feature in development');
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
  searchContainer: {
    padding: 16,
    paddingBottom: 8,
  },
  searchBar: {
    elevation: 2,
  },
  scrollContent: {
    padding: 16,
    paddingTop: 8,
    paddingBottom: 80,
  },
  vacancyCard: {
    marginBottom: 16,
    elevation: 2,
  },
  vacancyHeader: {
    marginBottom: 12,
  },
  vacancyTitleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  vacancyTitle: {
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
  vacancyInfo: {
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
  vacancyDescription: {
    fontSize: 14,
    color: '#212121',
    lineHeight: 20,
    marginBottom: 16,
  },
  vacancyFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  createdAt: {
    fontSize: 12,
    color: '#757575',
  },
  applyButton: {
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

export default VacanciesScreen;
