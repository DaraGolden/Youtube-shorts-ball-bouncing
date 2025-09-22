import random
def color_change_on_bounce(ball, *_):

    ball.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def color_change_over_time(ball, dt, *_):
    ball.change_color_over_time(dt)

def ball_split_on_collision(ball, balls_list):
    # Example plugin: duplicate ball on collision
    from objects.balls import Ball
    new_ball = Ball(ball.x, ball.y, radius=ball.radius // 2, color=ball.color)
    balls_list.append(new_ball)

# More gimmicks can be added here...
