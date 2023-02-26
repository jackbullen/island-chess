from django.contrib import admin
from board.models import ChessGame, ChessMove

admin.site.register(ChessGame)
admin.site.register(ChessMove)