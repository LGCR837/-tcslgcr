import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("贪吃蛇游戏")
        self.master.geometry("650x650")
        self.master.resizable(False, False)  # 禁止最大化

        self.canvas = tk.Canvas(self.master, bg='black', width=650, height=650)
        self.canvas.pack()

        self.snake = [(250, 250), (240, 250), (230, 250), (220, 250)]  # 初始长度为4
        self.direction = "Right"
        self.food = []
        self.score = 0
        self.start_time = time.time()  # 记录开始时间
        self.accelerated = False
        self.slow_mode = False
        self.last_accelerate_time = time.time()
        self.last_slow_time = time.time()

        self.create_food()
        self.update_display()

        self.master.bind("<KeyPress>", self.change_direction)
        self.game_loop()

    def create_food(self):
        while len(self.food) < 4:  # 默认生成4个食物
            x = random.randint(0, 64) * 10  # 调整食物生成范围以适应新窗口大小
            y = random.randint(0, 64) * 10
            self.food.append((x, y))
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill='red')

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.direction = event.keysym
        elif event.keysym == "v":  # 按 v 进入/退出加速模式
            if not self.accelerated:  # 仅在未加速时切换加速模式
                self.accelerated = True
                self.slow_mode = False  # 进入加速模式时自动关闭缓慢模式
                self.last_accelerate_time = time.time()  # 记录进入加速模式时的时间
            else:
                self.accelerated = False  # 退出加速模式
        elif event.keysym == "c":  # 按 c 进入/退出缓慢模式
            if not self.slow_mode:  # 仅在未缓慢时切换缓慢模式
                self.slow_mode = True
                self.accelerated = False  # 进入缓慢模式时自动关闭加速模式
                self.last_slow_time = time.time()  # 记录进入缓慢模式时的时间
            else:
                self.slow_mode = False  # 退出缓慢模式

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= 10
        elif self.direction == "Down":
            head_y += 10
        elif self.direction == "Left":
            head_x -= 10
        elif self.direction == "Right":
            head_x += 10

        # 检查边界碰撞
        if head_x < 0 or head_x >= 650 or head_y < 0 or head_y >= 650:
            self.score -= 3
            self.snake = [(250, 250), (240, 250), (230, 250), (220, 250)]  # 重置为4个长度
            self.direction = "Right"  # 重置方向
        else:
            self.snake.insert(0, (head_x, head_y))
            if (head_x, head_y) in self.food:
                self.food.remove((head_x, head_y))
                points = random.randint(1, 3)
                self.score += points
                self.create_food()  # 生成新的食物
            else:
                self.snake.pop()  # 移动蛇

            # 加速模式处理
            if self.accelerated:
                current_time = time.time()
                if current_time - self.last_accelerate_time >= 2:  # 每2秒消耗1个长度
                    if len(self.snake) > 1:  # 确保蛇的长度大于1
                        self.snake.pop()  # 去掉蛇的尾巴
                    self.last_accelerate_time = current_time  # 更新最后加速时间
            else:
                if self.slow_mode:
                    current_time = time.time()
                    if current_time - self.last_slow_time >= 1:  # 每1秒增加5个长度
                        self.snake.append(self.snake[-1])  # 增加1节长度
                        self.snake.append(self.snake[-1])  # 增加1节长度
                        self.snake.append(self.snake[-1])  # 增加1节长度
                        self.snake.append(self.snake[-1])  # 增加1节长度
                        self.snake.append(self.snake[-1])  # 增加1节长度
                        self.last_slow_time = current_time  # 更新最后缓慢时间

            # 自动关闭加速模式
            if len(self.snake) <= 2:
                self.accelerated = False

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        # 绘制蛇的头部
        head_x, head_y = self.snake[0]
        self.canvas.create_rectangle(head_x, head_y, head_x + 10, head_y + 10, fill='green', outline='')  # 头部颜色
        for x, y in self.snake[1:]:
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill='green')  # 身体颜色
        for x, y in self.food:
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill='red')
        self.update_display()

    def update_display(self):
        length = len(self.snake)  # 计算蛇的长度
        elapsed_time = int(time.time() - self.start_time)  # 计算经过的时间
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.canvas.create_text(10, 10, anchor='nw', text=f"分数: {self.score}", fill='white')
        self.canvas.create_text(10, 30, anchor='nw', text=f"蛇的长度: {length}", fill='white')
        self.canvas.create_text(10, 50, anchor='nw', text=f"时间: {minutes}:{seconds:02d}", fill='white')  # 显示经过的时间

        # 显示模式状态
        if self.accelerated:
            self.canvas.create_text(10, 70, anchor='nw', text="加速模式", fill='yellow')  # 显示加速模式
        elif self.slow_mode:
            self.canvas.create_text(10, 70, anchor='nw', text="缓慢模式", fill='red')  # 显示缓慢模式
        else:
            self.canvas.create_text(10, 70, anchor='nw', text="正常模式", fill='white')  # 显示正常模式

    def game_loop(self):
        self.move_snake()
        self.master.after(100 if not self.accelerated and not self.slow_mode else 200 if self.slow_mode else 50, self.game_loop)  # 调整速度

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()



    