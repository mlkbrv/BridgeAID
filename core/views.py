from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Employer, CandidateProfile, Vacancy, Application, Document,
    VisaCase, HousingListing, RelocationSuggestion, ExpenseEstimate,
    AIAssistantInteraction
)
from .serializers import (
    EmployerSerializer, CandidateProfileSerializer, VacancySerializer,
    ApplicationSerializer, DocumentSerializer, VisaCaseSerializer,
    HousingListingSerializer, RelocationSuggestionSerializer,
    ExpenseEstimateSerializer, AIAssistantInteractionSerializer
)


class EmployerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CandidateProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CandidateProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VacancyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        employer = get_object_or_404(Employer, user=self.request.user)
        serializer.save(employer=employer)


class VacancyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (permissions.IsAuthenticated,)


class VacancyListByEmployerAPIView(generics.ListAPIView):
    serializer_class = VacancySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        return Vacancy.objects.filter(employer=employer)


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        candidate = get_object_or_404(CandidateProfile, user=self.request.user)
        serializer.save(candidate=candidate)


class ApplicationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ApplicationListByCandidateAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        candidate = get_object_or_404(CandidateProfile, user=self.request.user)
        return Application.objects.filter(candidate=candidate)


class ApplicationListByVacancyAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        vacancy_id = self.kwargs['vacancy_id']
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        if vacancy.employer.user != self.request.user:
            return Application.objects.none()
        return Application.objects.filter(vacancy=vacancy)


class DocumentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DocumentListByUserAPIView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)


class DocumentListByApplicationAPIView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        application_id = self.kwargs['application_id']
        application = get_object_or_404(Application, id=application_id)
        if (application.candidate.user != self.request.user and 
            application.vacancy.employer.user != self.request.user):
            return Document.objects.none()
        return Document.objects.filter(application=application)


class VisaCaseListCreateAPIView(generics.ListCreateAPIView):
    queryset = VisaCase.objects.all()
    serializer_class = VisaCaseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VisaCaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VisaCase.objects.all()
    serializer_class = VisaCaseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VisaCaseListByOfficerAPIView(generics.ListAPIView):
    serializer_class = VisaCaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return VisaCase.objects.filter(assigned_officer=self.request.user)


class HousingListingListCreateAPIView(generics.ListCreateAPIView):
    queryset = HousingListing.objects.all()
    serializer_class = HousingListingSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HousingListingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HousingListing.objects.all()
    serializer_class = HousingListingSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RelocationSuggestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = RelocationSuggestion.objects.all()
    serializer_class = RelocationSuggestionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RelocationSuggestionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RelocationSuggestion.objects.all()
    serializer_class = RelocationSuggestionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RelocationSuggestionListByApplicationAPIView(generics.ListAPIView):
    serializer_class = RelocationSuggestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        application_id = self.kwargs['application_id']
        application = get_object_or_404(Application, id=application_id)
        if (application.candidate.user != self.request.user and 
            application.vacancy.employer.user != self.request.user):
            return RelocationSuggestion.objects.none()
        return RelocationSuggestion.objects.filter(application=application)


class ExpenseEstimateListCreateAPIView(generics.ListCreateAPIView):
    queryset = ExpenseEstimate.objects.all()
    serializer_class = ExpenseEstimateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExpenseEstimateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseEstimate.objects.all()
    serializer_class = ExpenseEstimateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExpenseEstimateListByApplicationAPIView(generics.ListAPIView):
    serializer_class = ExpenseEstimateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        application_id = self.kwargs['application_id']
        application = get_object_or_404(Application, id=application_id)
        if (application.candidate.user != self.request.user and 
            application.vacancy.employer.user != self.request.user):
            return ExpenseEstimate.objects.none()
        return ExpenseEstimate.objects.filter(application=application)


class AIAssistantInteractionListCreateAPIView(generics.ListCreateAPIView):
    queryset = AIAssistantInteraction.objects.all()
    serializer_class = AIAssistantInteractionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AIAssistantInteractionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AIAssistantInteraction.objects.all()
    serializer_class = AIAssistantInteractionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AIAssistantInteractionListByUserAPIView(generics.ListAPIView):
    serializer_class = AIAssistantInteractionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return AIAssistantInteraction.objects.filter(user=self.request.user)


class AIAssistantInteractionListByApplicationAPIView(generics.ListAPIView):
    serializer_class = AIAssistantInteractionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        application_id = self.kwargs['application_id']
        application = get_object_or_404(Application, id=application_id)
        if (application.candidate.user != self.request.user and 
            application.vacancy.employer.user != self.request.user):
            return AIAssistantInteraction.objects.none()
        return AIAssistantInteraction.objects.filter(application=application)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    try:
        employer = Employer.objects.get(user=user)
        employer_stats = {
            'total_vacancies': Vacancy.objects.filter(employer=employer).count(),
            'open_vacancies': Vacancy.objects.filter(employer=employer, status='open').count(),
            'total_applications': Application.objects.filter(vacancy__employer=employer).count(),
            'pending_applications': Application.objects.filter(
                vacancy__employer=employer, 
                status__in=['applied', 'screening']
            ).count(),
        }
        return Response(employer_stats)
    except Employer.DoesNotExist:
        pass
    
    try:
        candidate = CandidateProfile.objects.get(user=user)
        candidate_stats = {
            'total_applications': Application.objects.filter(candidate=candidate).count(),
            'pending_applications': Application.objects.filter(
                candidate=candidate, 
                status__in=['applied', 'screening', 'interview']
            ).count(),
            'accepted_applications': Application.objects.filter(
                candidate=candidate, 
                status='accepted'
            ).count(),
        }
        return Response(candidate_stats)
    except CandidateProfile.DoesNotExist:
        pass
    
    return Response({'message': 'No profile found'}, status=status.HTTP_404_NOT_FOUND)