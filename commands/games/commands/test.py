class Connect_4:
    def __init__(self):
        self.board = [[],[],[],[],[],[]]
        for i in range(6):
            self.board[i] = [':black_large_square:' for j in range(7)]
        print(self.board)


Connect_4()