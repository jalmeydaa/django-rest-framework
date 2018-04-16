from rest_framework import serializers
from snippets.models import Snippet, SnippetDetail,\
LANGUAGE_CHOICES, STYLE_CHOICES
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)



class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class SnippetDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    code = serializers.CharField(required=True)

    class Meta:
        model = SnippetDetail
        fields = '__all__'


class SnippetModelSerializer(serializers.ModelSerializer):
    details = SnippetDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Snippet
        fields = '__all__'

    def create(self, validated_data):
        details = validated_data.pop('details')
        snippet = Snippet.objects.create(**validated_data)

        for detail in details:
            detail_id = detail.pop('id', None)
            d, created = SnippetDetail.objects.update_or_create(
                id=detail_id,
                defaults={
                    'snippet_id': snippet.id,
                    'name': detail.get('name'),
                    'code': detail.get('code')
                })
        return snippet


    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        ok = Snippet.objects.update(**validated_data)
        for detail in details:
            detail_id = detail.pop('id', None)
            d, created = SnippetDetail.objects.update_or_create(
                id=detail_id,
                defaults={
                    'snippet_id': instance.id,
                    'name': detail.get('name'),
                    'code': detail.get('code')
                }
            )
            print(d, created)

        return instance
