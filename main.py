from graphics import Canvas
import time

class PongGame:
    def __init__(self):
        self.canvas = Canvas(width=600, height=400)
        
        self.canvas.create_rectangle(0, 0, 600, 400, 'black')

        self.paddle_left = self.canvas.create_polygon(
            30, 150, 50, 150, 50, 250, 30, 250,
            color='white',
            outline='white'
        )
        self.paddle_right = self.canvas.create_polygon(
            550, 150, 570, 150, 570, 250, 550, 250,
            color='white',
            outline='white'
        )
        self.ball = self.canvas.create_polygon(
            285, 195, 315, 195, 315, 225, 285, 225,
            color='white',
            outline='white'
        )

        # Track the coordinates of paddle and ball
        self.paddle_left_coords = [30, 150, 50, 250]
        self.paddle_right_coords = [550, 150, 570, 250]
        self.ball_coords = [285, 195, 315, 225]

        self.ball_dx = 3
        self.ball_dy = 3

        self.score_left = 0
        self.score_right = 0
        self.score_display = self.canvas.create_text(300, 20, text='0 - 0', font='Arial', font_size=20, color='white')

        # AI movement delay counter
        self.ai_move_counter = 0

        self.game_over = False

        self.run_game_loop()

    def run_game_loop(self):
        while not self.game_over:
            self.update_game()
            time.sleep(0.017)  # 60 FP

    def update_game(self):
        keys = self.canvas.get_new_key_presses()
        
        for key in keys:
            if key == 'w':
                self.move_paddle(self.paddle_left, 0, -10, self.paddle_left_coords)
            elif key == 's':
                self.move_paddle(self.paddle_left, 0, 10, self.paddle_left_coords)
        
        self.move_ball()
        self.move_ai_paddle()

    def move_ball(self):
        self.ball_coords = [coord + self.ball_dx if i % 2 == 0 else coord + self.ball_dy for i, coord in enumerate(self.ball_coords)]
        self.canvas.moveto(self.ball, self.ball_coords[0], self.ball_coords[1])

        print(f"Ball coordinates: {self.ball_coords}")
        
        if self.ball_coords[1] <= 0 or self.ball_coords[3] >= 400:
            self.ball_dy = -self.ball_dy
        if self.check_collision(self.ball_coords, self.paddle_left_coords) or self.check_collision(self.ball_coords, self.paddle_right_coords):
            self.ball_dx = -self.ball_dx
        if self.ball_coords[0] <= 0:
            self.score_right += 1
            self.check_winner()
            self.reset_ball()
        elif self.ball_coords[2] >= 600:
            self.score_left += 1
            self.check_winner()
            self.reset_ball()
        
        self.canvas.change_text(self.score_display, f'{self.score_left} - {self.score_right}')

    def move_paddle(self, paddle, dx, dy, coords):
        new_coords = [coord + dx if i % 2 == 0 else coord + dy for i, coord in enumerate(coords)]
        if new_coords[1] >= 0 and new_coords[3] <= 400:
            coords[] = new_coords
            self.canvas.moveto(paddle, coords[0], coords[1])

    def move_ai_paddle(self):
        self.ai_move_counter += 1

        # AI move every few frames
        if self.ai_move_counter % 5 == 0:
            paddle_center_y = (self.paddle_right_coords[1] + self.paddle_right_coords[3]) / 2
            ball_center_y = (self.ball_coords[1] + self.ball_coords[3]) / 2
            
            if ball_center_y < paddle_center_y and self.paddle_right_coords[1] > 0:
                self.move_paddle(self.paddle_right, 0, -5, self.paddle_right_coords)
            elif ball_center_y > paddle_center_y and self.paddle_right_coords[3] < 400:
                self.move_paddle(self.paddle_right, 0, 5, self.paddle_right_coords)

    def check_collision(self, ball_coords, paddle_coords):
        return (paddle_coords[0] < ball_coords[2] and paddle_coords[2] > ball_coords[0] and
                paddle_coords[1] < ball_coords[3] and paddle_coords[3] > ball_coords[1])

    def reset_ball(self):
        self.ball_coords = [285, 195, 315, 225]
        self.canvas.moveto(self.ball, self.ball_coords[0], self.ball_coords[1])
        self.ball_dx = -self.ball_dx

    def check_winner(self):
        if self.score_left >= 5:
            self.game_over = True
            self.canvas.create_text(300, 200, text='Left Wins!', font='Arial', font_size=30, color='white')
        elif self.score_right >= 5:
            self.game_over = True
            self.canvas.create_text(300, 200, text='Right Wins!', font='Arial', font_size=30, color='white')

if __name__ == '__main__':
    game = PongGame()
    game.canvas.mainloop()
