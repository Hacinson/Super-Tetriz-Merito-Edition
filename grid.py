class Grid:
    def __init__(self):
        #ilość rzędów 
        self.num_rows = 20
        #ilość kolumn
        self.num_cols = 10
        #wielkość jednego pola
        self.cell_size = 30
        #tworzy listę list wypełnionych zerami, czarna magia
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        #dla siebie: pierwsza część tworzy listę zer o długości odpowiedającej self.num_cols
        #piersza część jest powtarzana sel.num_rows razy - czyli 20 razy
        #note to self po dwóch godzinach siedzenia nad tym, dalej jest to czarna magia

        self.colors = self.get_cell_colors()


    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                #NIE CELL TYLKO SELF!!!!!!!
                #nawet szkoda słów ile mi zajęło żeby się zorientować co jest nie tak
                print(self.grid[row][column], end = " ")
            print()

    def get_cell_colors(self):

        dark_grey = (26, 31, 40)
        red = (209, 27, 36)
        green = (3, 66, 10)
        blue = (8, 11, 168)
        yellow = (175, 201, 22)
        cyan = (22, 111, 158)
        purple = (88, 25, 156)

        #KOLEJNOŚĆ! nie dotykać bo bede używać indexu z listy kolorów!
        return [dark_grey, red, green, blue, yellow, cyan, purple]
        

    def draw(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
