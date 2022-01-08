from django.core.exceptions import ValidationError
from . import validators
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from base import mods
from base.models import Auth, Key

class Question(models.Model):
    
    desc = models.TextField()
    VOTING=[(0, 'Default'),(1, 'Dhont'),
    (2, 'Paridad'),(3, 'Borda')]
    voting_type= models.SmallIntegerField(choices= VOTING, default=1)
    
    CHOICES=[(0,'Create your questions below'),(1, 'Binary Question'),
    (2, 'Yes/No Question'),(3, 'Very Bad/ Very Good Question')]

    question_type= models.SmallIntegerField(choices= CHOICES, default=0)
    seat= models.PositiveIntegerField(blank=True, null=True)

    def clean(self):
        if(validators.lofensivo(self.desc)):
            raise ValidationError("Se ha detectado lenguaje ofensivo")
        if self.seat==None and self.voting_type==1:
            raise ValidationError("Introduzca los escaños necesarios para usar una votación D'hont")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=Question)
def check_question(sender, instance, **kwargs):
    if instance.question_type==2 and instance.options.all().count()==0 and (instance.voting_type==0,instance.voting_type==2 or instance.voting_type==1):
        option1 = QuestionOption(question=instance, number=1, option="Si", group="g2")
        option1.save()
        option2 = QuestionOption(question=instance, number=2, option="No", group="g2")
        option2.save()
        option3 = QuestionOption(question=instance, number=3, option="NS/NC", group="g2") 
        option3.save()
    
    if instance.question_type==1 and instance.options.all().count()==0 and (instance.voting_type==0,instance.voting_type==2 or instance.voting_type==1):
        option1 = QuestionOption(question=instance, number=1, option="Si", group="g2")
        option1.save()
        option2 = QuestionOption(question=instance, number=2, option="No", group="g2")

    if instance.question_type==3 and instance.options.all().count()==0 and (instance.voting_type==0,instance.voting_type==2 or instance.voting_type==1):
        option1 = QuestionOption(question=instance, number=1, option="Very Bad")
        option1.save()
        option2 = QuestionOption(question=instance, number=2, option="Bad") 
        option2.save()
        option3 = QuestionOption(question=instance, number=3, option="OK") 
        option3.save()
        option4 = QuestionOption(question=instance, number=4, option="Good") 
        option4.save()
        option5 = QuestionOption(question=instance, number=5, option="Very Good") 
        option5.save()

@receiver(post_save, sender=Question)
def check_voting(sender, instance, **kwargs):
    if instance.voting_type==2:

        x=2
        lista=instance.options.all()
        for i in lista:
            x=x+1
            option3= QuestionOption(question=instance, number=x, option=i.option, group="g2")
            i.delete()
            option3.save() 
        
        option1 = QuestionOption(question=instance, number=1, option="Hombre", group="g1")
        option1.save()
        option2 = QuestionOption(question=instance, number=2, option="Mujer", group= "g1") 
        option2.save()
    
class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()
    group= models.CharField(max_length= 50, null= True)

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True, validators=[validators.lofensivo])
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''The tally is a shuffle and then a decrypt'''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
