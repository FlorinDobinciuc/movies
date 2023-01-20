from django.http import JsonResponse
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.urlpatterns import format_suffix_patterns

@api_view(['GET', 'POST'])
def movie_list(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse({'movies': serializer.data})
    
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, id):
    try:
        movie = Movie.objects.get(pk=id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'The movie does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return JsonResponse({'message': 'Movie was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

