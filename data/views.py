from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Move, ChessGame, Opening
from django.db.models import Q
import re
from django.core.cache import cache
from django.views.generic import ListView
import hashlib

class GameListView(ListView):
    model = ChessGame
    template_name = 'data/games_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Check if cached value exists
            hashed_query = hashlib.sha256(query.encode()).hexdigest()
            cached_value = cache.get(hashed_query)
            if cached_value is not None:
                # Use cached value to filter queryset
                queryset = queryset.filter(moves__san__icontains=cached_value)
            else:
                # Compute pgn() and cache the value
                value = query.replace('\n', ' ').strip()
                print('value:',value)
                cache.set(hashlib.sha256(query.encode()).hexdigest(), value)
                queryset = queryset.filter(moves__san__icontains=value)
        return queryset


# @login_required
# def games_list(request):
#     pgn = request.GET.get('q')
#     pattern = re.compile(r'^\d+\.')
#     if pgn:
#         moves = pgn.strip().split()
#         moves = [move for move in moves if not pattern.match(move)]
#         num_moves = len(moves)
#         games = ChessGame.objects.filter(moves__move_number=num_moves)
#         filtered_games = []
#         for game in games:
#             game_moves = game.moves.order_by('move_number').values_list('san',flat=True)
#             if list(game_moves[:num_moves]) == moves:
#                 filtered_games.append(game)
#         return render(request, 'data/games_list.html', {'games': filtered_games})
#     else:
#         return render(request, 'data/games_list.html', {'games': []})
    
    
# @login_required
# def games_list(request):
#     games = ChessGame.objects.all()
#     return render(request, 'data/games_list.html', {'games': games})

# def filtered_games(request):
#     pattern = re.compile(r'^\d+\.')
#     pgn = request.GET.get('pgn')
#     if pgn:
#         moves = pgn.strip().split()
#         moves = [move for move in moves if not pattern.match(move)]
#         num_moves = len(moves)
#         games = ChessGame.objects.filter(moves__move_number=num_moves)

#         for game in games:
#             game_moves = game.moves.order_by('move_number').values_list('san',flat=True)
#             if list(game_moves[:num_moves]) == moves:
#                 filtered_games.append(game)


    
#     game_data = []
#     for game in games:
#         game_data.append({
#             'pk': game.pk,
#             'status': game.status,
#             'moves': game.moves,
#             'result': game.result,
#             'white': game.white,
#             'black': game.black,
#         })
#     return JsonResponse({'games': game_data})

@login_required
def game_detail(request, pk):
    game = ChessGame.objects.get(pk=pk)
    return render(request, 'data/game_detail.html', {'game': game})

@login_required
def game_create(request):
    if request.method == 'POST':
        game = ChessGame(name=request.POST['name'], pgn=request.POST['pgn'], fen=request.POST['fen'])
        game.save()
        return redirect('games_list')
    return render(request, 'data/game_form.html')

@login_required
def game_update(request, game_id):
    game = ChessGame.objects.get(pk=game_id)
    if request.method == 'POST':
        game.name = request.POST['name']
        game.pgn = request.POST['pgn']
        game.fen = request.POST['fen']
        game.save()
        return redirect('game_detail', game_id=game.game_id)
    return render(request, 'data/game_form.html', {'game': game})

@login_required
def game_delete(request, game_id):
    ChessGame.objects.get(pk=game_id).delete()
    return redirect('games_list')

@login_required
def openings_list(request):
    openings = Opening.objects.all()
    return render(request, 'data/openings_list.html', {'openings': openings})

@login_required
def opening_detail(request, pk):
    opening = Opening.objects.get(pk=pk)
    return render(request, 'data/opening_detail.html', {'opening': opening})