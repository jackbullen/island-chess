from django.contrib import admin
from data.models import ChessGame, Move, Repertoire, Opening, Variation

admin.site.register(Repertoire)
admin.site.register(Opening)
admin.site.register(Variation)
admin.site.register(ChessGame)
admin.site.register(Move)
