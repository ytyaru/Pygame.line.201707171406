import pygame
import Ghostleg
import Screen
import math
# 画面サイズとあみだくじデータから座標データを作成する（始点座標、1本あたりの幅等）
class CalcSize:
    def __init__(self, ghostleg: Ghostleg.Ghostleg, screen: Screen.Screen):
        self.__ghostleg = ghostleg
        self.__screen = screen
        # あみだくじの縦線最大数: 7      最小:2
        # あみだくじの横線最大数: 6      最小:0
        # あみだくじの結果最大文字数: 2  最小:1
        self.__max_len_goal = max([len(s) for s in ghostleg.Goals])
        self.__start_point = [0, 0] # あみだくじ最左上の座標点(余白)
        self.__line_width = 1 # あみだくじを描く線幅
        self.__width_interval = 0 # 縦線同士の間隔
        self.__height_interval = 0 # 横線同士の間隔
        self.__font = None # 使える等幅フォントとサイズ
        self.__calc_start_point()
    @property
    def GoalStrMaxLen(self): self.__max_len_goal
    @property
    def StartPoint(self): self.__start_point
    @property
    def LineWidth(self): self.__line_width
    @property
    def WidthInterval(self): self.__width_interval
    @property
    def HeightInterval(self): self.__height_interval
    @property
    def Font(self): self.__font
    
    def __calc_start_point(self):
        print(f'screen.Size={self.__screen.Size}')
        
        w_max_interval = self.__screen.Size[0] / self.__ghostleg.VerticalLineMaxNum
        h_max_interval = self.__screen.Size[1] / self.__ghostleg.HorizontalLineMaxNum
#        w_max_interval = self.__ghostleg.VerticalLineMaxNum / self.__screen.Size[0]
#        h_max_interval = self.__ghostleg.HorizontalLineMaxNum / self.__screen.Size[1]
        print(f'w_max_interval={w_max_interval}, h_max_interval={h_max_interval}')
        
        # 最大間隔
        # width  320/7=45.7  4096/7=585.1
        # height 240/6=40    4096/6=682.6  2160/6=360        
#        self.__width_interval = math.floor(w_max_interval)
        
        # 最大線幅
#        line_width_max = w_max_interval / 4
#        if 1 < line_width_max:
#        print(f'line_width_max={line_width_max}')
        # (320,240) line_width=8, select_line_width=2
        # 8/320=1/40
        self.__line_width = round(self.__screen.Size[0] / 40)
        if self.__line_width < 1: self.__line_width = 1
        print(f'self.__line_width={self.__line_width}')
        
        # 最小サイズ（文字サイズ、線幅、余白、選択カーソル表示領域)）
        font_point_min = 12 # 最小文字サイズ point
        font_pixcel_min = math.ceil(self.__point_to_pixcel(font_point_min))
        print(f'font_point_min={font_point_min}, font_pixcel_min={font_pixcel_min}')
        
        # 縦横のうち小さい側からみてn文字分のフォントサイズである
        # 15=240/16。15文字分以上となる最小フォントサイズを採用する
#        num = min(self.__screen.Size[0], self.__screen.Size[1])/font_pixcel_min        
#        15=min(self.__screen.Size[0], self.__screen.Size[1])/x
#        15x=min(self.__screen.Size[0], self.__screen.Size[1])
#        x=min(self.__screen.Size[0], self.__screen.Size[1])/15

#        print(pygame.font.get_fonts()) # 使えるフォント名
#        self.__font = pygame.font.SysFont(value, self.__size, self.__is_bold, self.__is_italic)
        self.__font = pygame.font.Font("/usr/share/fonts/truetype/migmix/migmix-1m-regular.ttf", self.__get_point())
        print(self.__font.size('This is a test string.'))
        
        # ゴール文字列の高さ + 選択肢カーソル(1文字分サイズとして計算する)
        h_max_interval = (self.__screen.Size[1] - ((self.__max_len_goal + 1) * font_pixcel_min)) / self.__ghostleg.VerticalLineMaxNum
        h_max_interval = round(h_max_interval - 1) # 偶数に丸める。ただし端数分が超過する側に丸められぬよう-1する
        print(f'w_max_interval={w_max_interval}, h_max_interval={h_max_interval}')
        
        # 線幅から左端の最低余白を算出できる
        # line_width = 8の場合、中央から左4pixcel分の余白が欲しい
#        w_max_interval = self.__screen.Size[0] - () / self.__ghostleg.HorizontalLineMaxNum
        self.__start_point[0] = round(self.__line_width / 2) - 1 if 2 < self.__line_width else 0
        self.__start_point[1] = font_pixcel_min
        
#        w_max_interval = math.floor(w_max_interval)
        # 45*7=315  320-315=5   width=8 8/2-1 =3     5<3*2
        # 44*7=308  320-308=12  width=8 8/2-1 =3    12<3*2
#        diff = self.__screen.Size[0] - (w_max_interval * self.__ghostleg.VerticalLineMaxNum)
#        if diff < self.__start_point[0]*2: w_max_interval -= 1        
        w_max_interval = math.floor((self.__screen.Size[0] - (self.__start_point[0]*2)) / self.__ghostleg.VerticalLineMaxNum)
        print(f'w_max_interval={w_max_interval}, h_max_interval={h_max_interval}')
        
        self.__width_interval = w_max_interval
        self.__height_interval = h_max_interval
    
    # フォントの単位pointをpixcelに変換する
    # http://spell.vincent.in/upload/pt-to-px-and-px-to-pt.php
    # http://d.hatena.ne.jp/itoasuka/20100104/1262585983
    def __point_to_pixcel(self, point):
        point_per_inch = 1/72 # 1point=1/72inch
        ppi = 72 # inch per point
        dpi = 96 # dot per inch # 大抵は96だが最近は高DPIといって可変なものもある。
        # 72point = 96pixcel
        #  1point = 96/72 = 1.3pixcel
        # 12point = 96*12/72 = 16pixcel
        return dpi * point / ppi
        
    # 縦横のうち小さい側からみて{length=15}文字分以上となる最小のフォントポイントを返す
    # 15=240/16(16pixcel=12point)
    # デフォルトでは15文字分以上となる最小フォントポイントを返す
    def __get_point(self, length=15):
#        num = min(self.__screen.Size[0], self.__screen.Size[1])/font_pixcel_min
#        15=min(self.__screen.Size[0], self.__screen.Size[1])/x
#        15x=min(self.__screen.Size[0], self.__screen.Size[1])
#        x=min(self.__screen.Size[0], self.__screen.Size[1])/15
        return math.ceil(min(self.__screen.Size[0], self.__screen.Size[1]) / length)


if __name__ == '__main__':
    pygame.init()
    g = Ghostleg.Ghostleg()
    g.Create()
    s = Screen.Screen()
    c = CalcSize(g, s)
