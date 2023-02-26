"""
Script for importing chess data from a PGN file into the application's database.
"""
import logging

import chess.pgn
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from data.models import ChessGame, Move, Opening, Variation


class Command(BaseCommand):
    """
    Management command for importing chess data from a PGN file into the application's database.
    """

    help = "Imports chess data from a PGN file into the application's database."

    max_move_num = 10

    def handle(self, *args, **options):
        """
        Handles the command to import chess data from a PGN file into the application's database.
        """
        logging.info("Starting import of chess data from PGN file.")

        with open("PircClassical.pgn") as pgn_file:
            opening = Opening.objects.create(
                name="Classical Pirc",
                pgn="1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Nf3",
                fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", #Not what I want but try it...
            )
 
            for game_data in self.parse_pgn_file(pgn_file):
                with transaction.atomic():
                    try:
                        variation, created = Variation.objects.get_or_create(
                            name=game_data["eco"],
                            start_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                            end_fen=game_data["end_fen"],
                            openings = opening
                        )

                        moves = [
                            Move(
                                move_number=move_data["ply"],
                                san=move_data["san"],
                                fen=move_data["fen"],
                            )
                            for move_data in game_data["moves"]
                        ]
                        Move.objects.bulk_create(moves)
                        
                        # variation.moves = variation.moves.set([moves])
                        variation.pgn = " ".join(
                            [
                                f"{i // 2 + 1} {move_data['san']}"
                                for i, move_data in enumerate(game_data["moves"][: self.max_move_num])
                                if i % 2 == 0
                            ]
                        )
                        variation.save()

                        if created:
                            variation.openings = opening

                        else:
                            if not variation.openings.filter(pk=opening.pk).exists():
                                variation.openings.add(opening)
                        game = ChessGame.objects.create(
                            event=game_data["event"],
                            site=game_data["site"],
                            date=game_data["date"],
                            round=game_data["round"],
                            white=game_data["white"],
                            black=game_data["black"],
                            result=game_data["result"],
                            eco=game_data["eco"],
                            pgn=" ".join(
                                [
                                    f"{i // 2 + 1} {move_data['san']}"
                                    for i, move_data in enumerate(game_data["moves"][: self.max_move_num])
                                    if i % 2 == 0
                                ]
                            ),
                        )
                        game.variations.set([variation.pk])
                        game.save()
                    except IntegrityError as e:
                        logging.warning(f"Error occurred while saving game data: {e}")

        logging.info("Finished import of chess data from PGN file.")

    @staticmethod
    def parse_pgn_file(pgn_file):
        """
        Parses a PGN file and yields the data for each game
        """
        while True:
            try:
                game = chess.pgn.read_game(pgn_file)
            except Exception as e:
                logging.warning(f"Error occurred while parsing game data: {e}")
                continue

            if not game:
                break

            game_data = {
                "event": game.headers.get("Event", ""),
                "site": game.headers.get("Site", ""),
                "date": game.headers.get("Date", ""),
                "round": game.headers.get("Round", ""),
                "white": game.headers.get("White", ""),
                "black": game.headers.get("Black", ""),
                "result": game.headers.get("Result", ""),
                "eco": game.headers.get("ECO", ""),
                "end_fen": game.end().board().fen(),
                "moves": [],
            }

            board = game.board()
            for move_num, move in enumerate(game.mainline_moves()):
                if move_num >= Command.max_move_num:
                    break

                board.push(move)
                game_data["moves"].append({
                    "ply": move_num + 1,
                    "san": move.uci(),
                    "fen": board.fen(),
                })

            yield game_data
