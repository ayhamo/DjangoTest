from rest_framework import serializers
from .models import *


# this class helps to tell what to return from the database into json object

class OnlineCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineCourse
        fields = '__all__'


class OfflineCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineCourse
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    online = serializers.SerializerMethodField()
    offline = serializers.SerializerMethodField()

    def get_online(self, obj: Course):
        if obj.course_type == Course.ONLINE:
            return OnlineCourseSerializer(obj.online).data
        return None

    def get_offline(self, obj: Course):
        if obj.course_type == Course.OFFLINE:
            return OfflineCourseSerializer(obj.offline).data
        return None

    # def to_representation(self, obj):
    #     representation = super().to_representation(obj)
    #     if obj.course_type == 1:
    #         online_course = OnlineCourse.objects.get(course_id=obj.id)
    #         representation['online'] = OnlineCourseSerializer(online_course).data
    #         return representation
    #     else:
    #         offline_course = OfflineCourse.objects.get(course_id=obj.id)
    #         representation['offline'] = OfflineCourseSerializer(offline_course).data
    #
    #         return representation


    # online_info = serializers.SerializerMethodField('get_online_info')
    #
    # offline_info = serializers.SerializerMethodField('get_offline_info')
    #
    # def get_online_info(self, obj):
    #     online_course = OnlineCourse.objects.get(course_id=obj.id)
    #     return OnlineCourseSerializer(online_course).data
    #
    # def get_offline_info(self, obj):
    #     offline_course = OfflineCourse.objects.get(course_id=obj.id)
    #     return OfflineCourseSerializer(offline_course).data


    # course_info = serializers.SerializerMethodField()
    #
    # def get_course_info(self, obj):
    #      if obj.course_type == 1:
    #          online_course = OnlineCourse.objects.get(course_id=obj.id)
    #          return OnlineCourseSerializer(online_course).data
    #      else:
    #          offline_course = OfflineCourse.objects.get(course_id=obj.id)
    #      return OfflineCourseSerializer(offline_course).data
