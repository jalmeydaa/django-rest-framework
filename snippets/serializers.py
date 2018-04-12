from rest_framework import serializers
from snippets.models import Snippet, SnippetDetail,\
LANGUAGE_CHOICES, STYLE_CHOICES


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


class SnippetDetailListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        snippet_detail_mapping = {snippet_detail.id: snippet_detail for snippet_detail in instance}
        data_mapping = {item['id']: item for item in validated_data}
        print(data_mapping)

        # Perform creations and updates.
        ret = []
        for snippet_detail_id, data in data_mapping.items():
            snippet_detail = snippet_detail_mapping.get(snippet_detail_id, None)
            if snippet_detail is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(snippet_detail, data))

        # Perform deletions.
        for snippet_detail_id, snippet_detail in snippet_detail_mapping.items():
            if snippet_detail_id not in data_mapping:
                snippet_detail.delete()

        return ret


class SnippetDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    code = serializers.CharField(required=True)

    class Meta:
        model = SnippetDetail
        fields = '__all__'
        list_serializer_class = SnippetDetailListSerializer


class SnippetModelSerializer(serializers.ModelSerializer):
    details = SnippetDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Snippet
        fields = '__all__'

    def create(self, validated_data):
        snippet_data = {
            'title': validated_data.get('title'),
            'code': validated_data.get('code'),
            'linenos': validated_data.get('linenos'),
            'language': validated_data.get('language'),
            'style': validated_data.get('style')
        }
        snippet = Snippet.objects.create(**snippet_data)

        details = validated_data.get('details')

        for d in details:
            d['snippet'] = snippet.id

        serializer_details = SnippetDetailSerializer(data=details, many=True)
        if serializer_details.is_valid():
            serializer_details.save()

        return snippet


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.lonenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()

        details = validated_data.get('details')
        for d in details:
            d['snippet'] = instance.id


        serializer_details = SnippetDetailSerializer(
            instance=instance.details.all(), data=details, many=True
        )
        if serializer_details.is_valid():
            serializer_details.save()

        return instance
