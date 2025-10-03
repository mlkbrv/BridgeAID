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
  List,
  IconButton,
} from 'react-native-paper';
import * as DocumentPicker from 'expo-document-picker';
import { coreAPI } from '../services/api';

const DocumentsScreen = ({ navigation }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await coreAPI.getUserDocuments();
      setDocuments(response.data.results || response.data);
    } catch (error) {
      console.log('Error loading documents:', error);
      Alert.alert('Error', 'Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDocuments();
    setRefreshing(false);
  };

  const getDocumentEmoji = (docType) => {
    switch (docType) {
      case 'passport': return '🛂';
      case 'photo': return '📷';
      case 'cv': return '📄';
      case 'contract': return '📋';
      case 'visa_form': return '📝';
      case 'other': return '📁';
      default: return '📄';
    }
  };

  const getDocumentTypeText = (docType) => {
    switch (docType) {
      case 'passport': return 'Passport';
      case 'photo': return 'Photo';
      case 'cv': return 'CV';
      case 'contract': return 'Contract';
      case 'visa_form': return 'Visa Form';
      case 'other': return 'Other';
      default: return docType;
    }
  };

  const handleUploadDocument = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: '*/*',
        copyToCacheDirectory: true,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        
        Alert.alert(
          'Document Type',
          'Select the type of document to upload',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Passport', onPress: () => uploadDocument(asset, 'passport') },
            { text: 'CV', onPress: () => uploadDocument(asset, 'cv') },
            { text: 'Photo', onPress: () => uploadDocument(asset, 'photo') },
            { text: 'Other', onPress: () => uploadDocument(asset, 'other') },
          ]
        );
      }
    } catch (error) {
      console.log('Document picker error:', error);
      Alert.alert('Error', 'Failed to select document');
    }
  };

  const uploadDocument = async (asset, docType) => {
    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: asset.uri,
        type: asset.mimeType || 'application/octet-stream',
        name: asset.name || 'document',
      });
      formData.append('doc_type', docType);

      await coreAPI.uploadDocument(formData);
      Alert.alert('Success', 'Document uploaded successfully');
      await loadDocuments();
    } catch (error) {
      console.log('Upload error:', error);
      Alert.alert('Error', 'Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = (documentId) => {
    Alert.alert(
      'Delete Document',
      'Are you sure you want to delete this document?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: () => deleteDocument(documentId)
        },
      ]
    );
  };

  const deleteDocument = async (documentId) => {
    try {
      await coreAPI.deleteDocument(documentId);
      Alert.alert('Success', 'Document deleted');
      await loadDocuments();
    } catch (error) {
      console.log('Delete error:', error);
      Alert.alert('Error', 'Failed to delete document');
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Loading documents...</Text>
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
        {documents.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content style={styles.emptyContent}>
              <Text style={styles.emptyEmoji}>📁</Text>
              <Title style={styles.emptyTitle}>No documents</Title>
              <Paragraph style={styles.emptyText}>
                Upload necessary documents to submit applications
              </Paragraph>
            </Card.Content>
          </Card>
        ) : (
          documents.map((document) => (
            <Card key={document.id} style={styles.documentCard}>
              <Card.Content>
                <View style={styles.documentHeader}>
                  <View style={styles.documentInfo}>
                    <Text style={styles.documentEmoji}>
                      {getDocumentEmoji(document.doc_type)}
                    </Text>
                    <View style={styles.documentDetails}>
                      <Title style={styles.documentTitle}>
                        {getDocumentTypeText(document.doc_type)}
                      </Title>
                      <Paragraph style={styles.documentDate}>
                        📅 {new Date(document.uploaded_at).toLocaleDateString('ru-RU')}
                      </Paragraph>
                    </View>
                  </View>
                  <IconButton
                    icon="delete"
                    size={20}
                    onPress={() => handleDeleteDocument(document.id)}
                    iconColor="#F44336"
                  />
                </View>

                {document.application && (
                  <View style={styles.applicationInfo}>
                    <Text style={styles.applicationEmoji}>📋</Text>
                    <Text style={styles.applicationText}>
                      Related to application: {document.application}
                    </Text>
                  </View>
                )}

                {document.metadata && (
                  <View style={styles.metadataContainer}>
                    {document.metadata.file_size && (
                      <Chip style={styles.metadataChip} textStyle={styles.metadataText}>
                        📏 {document.metadata.file_size}
                      </Chip>
                    )}
                    {document.metadata.pages && (
                      <Chip style={styles.metadataChip} textStyle={styles.metadataText}>
                        📄 {document.metadata.pages} pages
                      </Chip>
                    )}
                  </View>
                )}

                <View style={styles.documentActions}>
                  <Button
                    mode="outlined"
                    onPress={() => {
                      Alert.alert('View', 'View function in development');
                    }}
                    style={styles.actionButton}
                    icon="eye"
                  >
                    View
                  </Button>
                  <Button
                    mode="outlined"
                    onPress={() => {
                      Alert.alert('Download', 'Download function in development');
                    }}
                    style={styles.actionButton}
                    icon="download"
                  >
                    Download
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
        onPress={handleUploadDocument}
        loading={uploading}
        disabled={uploading}
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
  scrollContent: {
    padding: 16,
    paddingBottom: 80,
  },
  documentCard: {
    marginBottom: 16,
    elevation: 2,
  },
  documentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  documentInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  documentEmoji: {
    fontSize: 24,
    marginRight: 12,
  },
  documentDetails: {
    flex: 1,
  },
  documentTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#212121',
    marginBottom: 4,
  },
  documentDate: {
    fontSize: 12,
    color: '#757575',
  },
  applicationInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    padding: 8,
    backgroundColor: '#F8F9FA',
    borderRadius: 8,
  },
  applicationEmoji: {
    fontSize: 16,
    marginRight: 8,
  },
  applicationText: {
    fontSize: 14,
    color: '#757575',
    flex: 1,
  },
  metadataContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 12,
  },
  metadataChip: {
    marginRight: 8,
    marginBottom: 4,
    backgroundColor: '#E3F2FD',
  },
  metadataText: {
    fontSize: 12,
    color: '#2196F3',
  },
  documentActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 4,
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

export default DocumentsScreen;
