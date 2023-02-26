from django.core.management.base import BaseCommand
from courses.models import Course, Chapter, Variation, Move
import chess.pgn
from django.db import IntegrityError
from collections import defaultdict
class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        with open('benko.pgn') as pgn_file:
            course = Course()
            course.name = 'Benko Gambit'
            course.player = 'black'
            course.save()
            chapter_dict = defaultdict(list)

            while True:
                try:
                    game = chess.pgn.read_game(pgn_file)
                    if game is None:
                        break
                    if game.headers.get('White','') == "?":
                        continue
                    if game.headers.get('White','') not in list(chapter_dict.keys()):
                        chapter = Chapter()
                        chapter.name = game.headers.get('White','')
                        chapter.start_fen = "rnbqkb1r/ppp1pp1p/3p1np1/8/3PP3/2N2N2/PPP2PPP/R1BQKB1R b KQkq - 1 4"
                        chapter.course = course
                        chapter.save()

                    chapter_dict[game.headers.get('White','')].append({game.headers.get('Black',''):''})
                    

                    pgn = ""
                    
                    board = game.board()                     
                    

                    variation = Variation.objects.create(name=game.headers.get('Black',''), pgn='', end_fen='', chapter=chapter)
                    variation.save()

                    for i,move in enumerate(game.mainline_moves()):
                        i+=1
                        
                        Move.objects.create(
                            move_number=i,
                            san=board.san(move),
                            fen=board.fen(),
                            variation=variation
                        )

                        
                        if i%2==1:
                            pgn += str(board.ply()//2 +1)+'. '+board.san(move)+' '
                        else:
                            pgn += ' '+board.san(move)+' '
 
                        board.push(move)
                    
                    variation.pgn = pgn
                    variation.end_fen = board.fen()
                    variation.save()

                except Exception as e:
                    # Print the exception and continue with the next game
                    print(f'Error occurred while processing game: {e}')
                    continue


                        