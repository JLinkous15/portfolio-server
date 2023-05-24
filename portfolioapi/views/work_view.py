from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
import uuid
import base64
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from models import Work, Material, Link, WorkType


class WorkView(ViewSet):
    """Handles requests for Work resources"""

    def list(self, request):
        """GET all works"""
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET a single work"""
        try:
            work = Work.objects.get(pk=pk)
            serializer = WorkSerializer(work)
            return Response(serializer.data)
        except Work.DoesNotExist as ex:
            return Response(
                {'message': ex.args[0]},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """Create a new row for Work"""
        try:
            work_type = WorkType.objects.get(pk=request.data['workTypeId'])
            work = Work()
            work.name = request.data['name']
            work.body = request.data['body']
            work.date = request.data['date']
            work.is_published = request.data['isPublished']
            work.work_type = work_type
            for material in request.data['materials']:
                work.materials.add(Material.objects.get(pk=material))
            for link in request.data['links']:
                try:
                    existing_link = Link.objects.get(url=link.url)
                    work.links.add(existing_link)
                except Link.DoesNotExist:
                    new_link = Link.objects.create(
                        name=link.name, url=link.url
                    )
                    work.links.add(new_link)
            work.save()

            serializer = WorkSerializer(work)
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            work = Work.objects.get(pk=pk)
            work.name = request.data['name']
            work.body = request.data['body']
            work.date = request.data['date']
            work.is_published = request.data['isPublished']
            work.work_type = WorkType.objects.get(
                pk=request.data['workTypeId'])
            work.materials.clear()
            for material in request.data['materials']:
                work.materials.add(Material.objects.get(pk=material))
            work.links.clear()
            for link in request.data['links']:
                try:
                    existing_link = Link.objects.get(url=link.url)
                    work.links.add(existing_link)
                except Link.DoesNotExist:
                    new_link = Link.objects.create(
                        name=link.name, url=link.url
                    )
                    work.links.add(new_link)
            work.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Work.DoesNotExist as ex:
            return Response(
                {'message': ex.args[0]},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        """Delete a work"""
        try:
            work = Work.objects.get(pk=pk)
            work.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Work.DoesNotExist as ex:
            return Response(
                {'message': ex.args[0]},
                status=status.HTTP_404_NOT_FOUND
            )


class WorkMaterialSerializer(serializers.ModelSerializer):
    """JSON serializer for materials"""
    class Meta:
        model = Material
        fields = ('id', 'name')


class WorkLinkSerializer(serializers.ModelSerializer):
    """JSON serializer for links"""
    class Meta:
        model = Link
        fields = ('id', 'name', 'url')


class WorkSerializer(serializers.ModelSerializer):
    """JSON serializer for works"""
    materials = WorkMaterialSerializer(many=True)
    links = WorkLinkSerializer(many=True)

    class Meta:
        model = Work
        fields = ('id', 'name', 'image', 'body', 'date',
                  'work_type', 'materials', 'links')
