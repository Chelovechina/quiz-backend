from django.db import models
from django.contrib.auth.models import User

DIFF_CHOICES = (
    ("Легко", "Легко"),
    ("Нормально", "Нормально"),
    ("Тяжело", "Тяжело"),
)


class Quiz(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название теста")
    topic = models.CharField(max_length=120, verbose_name="Тема теста")
    time = models.IntegerField(verbose_name="Время для прохождения в минутах")
    required_score_to_pass = models.IntegerField(
        verbose_name="Минимальный результат для прохождения в %")
    difficluty = models.CharField(
        max_length=20, verbose_name="Сложность", choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.topic}"

    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):
    text = models.CharField(max_length=200, verbose_name="Вопрос")
    quiz = models.ForeignKey(
        Quiz, verbose_name="Тест, к которому относится вопрос",
        related_name="questions", on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    multiply_answers = models.BooleanField(
        default=False, verbose_name="Имеет несколько правильных ответов")

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answers.all()

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    text = models.CharField(max_length=200, verbose_name="Ответ")
    correct = models.BooleanField(default=False, verbose_name="Правилен")
    question = models.ForeignKey(
        Question, verbose_name="Вопрос, к которому относится ответ",
        related_name="answers", on_delete=models.CASCADE)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name="quiz",
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="user",
                             on_delete=models.CASCADE)
    score = models.FloatField(verbose_name="Процент правильности")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
