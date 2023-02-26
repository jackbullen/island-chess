from django.core.management.base import BaseCommand
from data.models import ChessGame, Move, Opening, Variation
import chess.pgn
from django.db import IntegrityError
max_move_num = 6
class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('PircClassical.pgn') as pgn_file:
            opening = Opening()
            opening.name = 'Classical Pirc'
            opening.pgn = '1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Nf3'
            opening.fen = 'rnbqkb1r/ppp1pp1p/3p1np1/8/3PP3/2N2N2/PPP2PPP/R1BQKB1R b KQkq - 1 4'
            opening.save()
            # opening.repertoires.set(None)
            while True:
                try:
                    game = chess.pgn.read_game(pgn_file)
                    if game is None:
                        break

                    chess_game = ChessGame()
                    chess_game.event = game.headers.get('Event', '')
                    chess_game.site = game.headers.get('Site', '')
                    chess_game.date = game.headers.get('Date', '')
                    chess_game.round = game.headers.get('Round', '')
                    chess_game.white = game.headers.get('White', '')
                    chess_game.black = game.headers.get('Black', '')
                    chess_game.result = game.headers.get('Result', '')
                    chess_game.eco = game.headers.get('ECO', '')
                    chess_game.pgn = ""
                    
                    board = game.board()

                    variation_pgn = ''
                    variation_end_fen = ''
                     
                    

                    
                    for i,move in enumerate(game.mainline_moves()):
                        i+=1
                        
                        # if i//2 +1 <= max_move_num:
                        #     mov, created = Move.objects.get_or_create(
                        #         move_number=board.ply(),
                        #         san=board.san(move),
                        #         fen=board.fen()
                        #     )
                        #     if created:
                        #         mov.variations.set([variation.pk])
                        if i//2 +1 <= max_move_num:
                            if i%2==1 and i//2 +1 <= max_move_num:
                                variation_pgn+=str(i//2 +1)+' '+board.san(move)+' '
                            else: 
                                variation_pgn+=' '+board.san(move)+' '
                        if i//2 +1 == max_move_num:
                            variation_end_fen = board.fen()
                        if i%2==1:
                            chess_game.pgn += str(i//2 +1)+' '+board.san(move)+' '
                        else:
                            chess_game.pgn += ' '+board.san(move)+' '
                        # variation.pgn += str(i//2)+' '+board.san(move)+' '
                        board.push(move)
                    
                    variation = Variation.objects.filter(end_fen=variation_end_fen, opening=opening).first()
                    if variation is None:
                        variation = Variation.objects.create(name=chess_game.eco, pgn=variation_pgn, start_fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', end_fen=variation_end_fen, opening=opening)

                    chess_game.save()
                    variation.save()
                except IntegrityError as e:
                    print(f'Skipping game due to duplicate variation end_fen: {e}')
                    continue

                except Exception as e:
                    # Print the exception and continue with the next game
                    print(f'Error occurred while processing game: {e}')
                    continue


                        