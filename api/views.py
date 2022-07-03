from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from quizes.models import Question, Quiz, Result
from .serializers import QuizesSerializer, QuizSerializer, ResultsSerializer


@api_view(['GET'])
def getQuizes(request):
    m = Quiz.objects.all()
    serializer = QuizesSerializer(m, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSingleQuiz(request, pk):
    m = Quiz.objects.get(pk=pk)
    serializer = QuizSerializer(m)
    return Response(serializer.data)


class ResultsAPIView(APIView):
    serializer_class = ResultsSerializer

    def check_answers(self, user_ans, correct_ans):
        for i in range(min(len(user_ans), len(correct_ans))):
            if user_ans[i] != correct_ans[i]:
                return False
        return len(user_ans) == len(correct_ans)

    def post(self, request, pk):
        data = request.data
        quiz = Quiz.objects.get(pk=pk)
        multiplier = 100 / len(quiz.questions.all())
        user = user = User.objects.get(username='admin')
        score = 0

        for question_text in data.keys():
            answers = [data[question_text]]
            question = Question.objects.get(text=question_text)
            correct_answers = list(question.answers.filter(
                correct=True).values_list('text', flat=True))
            if self.check_answers(answers, correct_answers):
                score += 1

        percent_score = score * multiplier
        result = Result.objects.create(
            quiz=quiz, user=user, score=percent_score)
        serializer = ResultsSerializer(result)

        return Response(serializer.data)
