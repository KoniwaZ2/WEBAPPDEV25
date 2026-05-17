from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
    votes = models.IntegerField(default=0)

class Mahasiswa(models.Model):
    nama = models.CharField(max_length=100)
    telp = models.CharField(max_length=20, unique=True)
    nim = models.IntegerField(unique=True)
    foto = models.ImageField(upload_to='foto_mahasiswa/', null=True, blank=True)

    def __str__(self):
        return f"{self.nim} - {self.nama}"