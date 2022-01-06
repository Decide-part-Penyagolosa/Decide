from rest_framework import serializers
from . import validators
from .models import Detector, Percentage, Question, QuestionOption, Voting
from base.serializers import KeySerializer, AuthSerializer


class DetectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detector
        fields = ('word')

class PercentageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Percentage
        fields = ('number')

class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    def validate_desc(self, data):
        if(validators.lofensivo(data['desc'])):
            raise serializers.ValidationError("Se ha detectado lenguaje ofensivo")
        return data
    class Meta:
        model = Question
        fields = ('desc', 'options')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    validators.lofensivo(question.Meta.fields[1])
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')
