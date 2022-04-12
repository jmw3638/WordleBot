import time

import guesser
import util


class Simulation:
    def __init__(self, word_guesser: guesser.WordGuesser):
        self.word_guesser = word_guesser

    def run_simulation(
        self,
        iterations: int,
        guess: str = None,
        goal: str = None,
        words_dict: list = None,
        guesses_allowed: int = 6,
    ):
        # Initialize simulation results
        stats = []
        guess_distribution = [0] * guesses_allowed
        words_distribution = [(0, 0)] * guesses_allowed
        total_games = 0
        total_guesses = 0
        total_won = 0
        start_time = time.time()

        # Play x iterations of Wordle games, where x is provided
        for i in range(iterations):
            # Choose a random starting word if not persistent
            if not guess:
                # Choose passed in word dictionary if provided
                if words_dict:
                    cur_guess = self.word_guesser.get_random_word(words_dict)
                else:
                    cur_guess = self.word_guesser.get_random_word()
            else:
                cur_guess = guess

            # Choose a random goal word if not persistent
            if not goal:
                cur_goal = self.word_guesser.get_random_word()
            else:
                cur_goal = goal

            util.vlog("Game #{}".format(i + 1))
            util.vlog("Initial guess: {}".format(cur_guess), 2)
            util.vlog("Goal word: {}".format(cur_goal), 2)

            # Play a full game of Wordle
            for j in range(guesses_allowed):
                util.vlog("Guess #{}: {}".format(j + 1, cur_guess), 2)

                # Get guess results
                results = util.get_wordle_results(cur_guess, cur_goal)
                if not results:
                    util.vlog(
                        "Failed to get results for: {} -> {}".format(
                            cur_guess, {cur_goal}
                        )
                    )
                    break

                # Check for win condition
                solved = True
                for r in results:
                    if not r is util.Results.RIGHT:
                        solved = False
                        break
                if solved:
                    util.vlog("Solved Wordle in {} guesses".format(j + 1))
                    total_won += 1
                    break

                # Read results into word guesser
                if not self.word_guesser.read_in_results(cur_guess, results):
                    util.vlog("Failed to read results: {}".format(results))
                    break

                # Get next best guess
                words = self.word_guesser.get_possible_words()
                cur_guess = self.word_guesser.get_random_word(words)

                guess_number_count, total_possible = words_distribution[j]
                words_distribution[j] = (
                    guess_number_count + 1,
                    total_possible + len(words),
                )

            # Update simulation results
            self.word_guesser.reset_game_state()
            total_games += 1
            total_guesses += 1
            guess_distribution[j] += 1

            # Print a progress bar if not verbose logging
            if not util.vlog():
                self.print_progress(total_games, iterations)

        # Calculate simulation statistics
        stop_time = time.time()
        total_time = "{0:.2f}".format(stop_time - start_time)
        avg_guesses = total_guesses / iterations
        total_lost = total_games - total_won
        win_percent = "{0:.2f}".format(100 * (total_won / total_games))

        # Build simulation results set
        stats.append("Simulation Duration: {}s".format(total_time))
        stats.append("Total Games: {}".format(total_games))
        stats.append("Total Guesses: {}".format(total_guesses))
        stats.append("Average Guesses per Game: {}".format(avg_guesses))
        stats.append("Win/Loss Ratio: {} / {}".format(total_won, total_lost))
        stats.append("Win Percentage: {}%".format(win_percent))
        stats.append("Guess Distribution:")
        for i in range(len(guess_distribution)):
            guess_percentage = "{0:.2f}".format(
                100 * (guess_distribution[i] / total_guesses)
            )
            stats.append(
                "Guess #{}: {} - {}%".format(
                    i + 1, guess_distribution[i], guess_percentage
                )
            )
        stats.append("Average Possible Words per Guess Results:")
        for i in range(len(words_distribution)):
            guess_number_count, total_possible = words_distribution[i]
            if total_possible > 0:
                words_avg = "{0:.2f}".format(
                    total_possible / guess_number_count
                )
                stats.append("Guess #{}: {}".format(i + 1, words_avg))

        return stats

    def print_results(self, results: list):
        print("-" * 50)
        print("Simulation Results:")
        print("-" * 50)

        for r in results:
            print(r)

        print("-" * 50)

    # Print iterations progress
    def print_progress(self, iteration, total, decimals=0, length=50, fill="|"):
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / total)
        )
        filledLength = int(length * iteration // total)
        bars = fill * filledLength + " " * (length - filledLength)

        # Replace current console line with updated progress bar
        print(f"\rProgress: [{bars}] {percent}% #{iteration}", end="\r")

        # Print new line on complete
        if iteration == total:
            print()
