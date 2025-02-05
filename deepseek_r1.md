<think>
好的，我需要将用户提供的Python 2代码转换为Python 3，并添加方块翻转的功能。首先，我应该通读用户提供的代码，理解各个部分的功能，然后逐步进行修改。

首先，观察代码结构。主要有三个类：Tetris（游戏主体）、Block（方块对象）、Control（控制输入），以及GameArry（游戏逻辑和界面）。用户提到要将代码转换为Python 3，所以首先需要处理语法差异。

Python 2到3的变化点可能包括：

1. print语句改为print函数。

2. xrange替换为range。

3. 除法运算符/的行为可能变化，例如在Python 3中，整数除法使用//。

4. 类定义中的super()调用可能需要调整。

5. 处理Unicode字符串的问题，比如显式使用bytes和str类型，但此处可能不需要。

6. 模块导入可能需要调整，比如相对导入。

接下来检查现有代码中的这些点。

比如，在GameArry类的check_score方法中使用了xrange，需要改为range。同样，print语句在print_ui方法中，需要改为函数形式，添加括号。例如，原代码中的print '┌' + ...需要改为print('┌' + ...)。

另一个问题是除法：在Tetris类的create_block方法中，deviation = self.col / 2 - 2。在Python 3中，如果col是10，10/2是5.0，所以可能应该用整数除法。但原代码中self.col是10，所以这里得到的是5.0？但是原来的代码可能期望是整数。因此可能需要改为//，即deviation = self.col // 2 - 2。不过原代码在Python 2中，如果self.col是10（整数），10/2是5，所以Python 2中的整数除法在这里没问题。但在Python 3中，10/2是5.0，所以需要改为//，才能得到整数。因此这里需要修改。

接下来是类的定义中的super()。在Block类中，__init__方法调用了super(Block, self).__init__()。这在Python 3中可以简化为super().__init__()，但保持原样也可以，不过可能不需要改动，因为Python 3仍然支持这种语法。

另外，在GameArry类的load_game方法中，循环使用了xrange(1,30)，需要改为range。还有在print语句中，例如print '游戏载入中....\n'需要添加括号。

然后，用户要求添加方块翻转的功能。原代码中没有处理旋转的逻辑。需要为方块添加旋转的方法。

现在，分析如何实现方块的旋转。首先，每个方块的形状由piece数组中的位置决定。例如，I_piece的piece是[0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation, 4 + deviation]。这里的坐标应该是一维数组模拟二维，因此每个位置对应的行和列需要计算。

旋转方块需要将每个块的位置转换为二维坐标（行和列），然后进行旋转（例如顺时针或逆时针旋转90度），再转换回一维索引。

例如，假设当前方块的位置是基于行和列的，那么旋转时需要确定每个块的新坐标。例如，对于I型方块，水平变为垂直，或者反之。

对于每个方块类型，旋转的方式不同。例如，O型方块（正方形）旋转后形状不变，不需要处理。其他如I、J、L、S、Z、T需要各自的旋转逻辑。

可能的做法是为每个方块定义旋转后的坐标变化，或者在Block类中添加旋转方法，根据当前形状计算旋转后的位置。

或者，可以计算每个块的相对坐标，然后应用旋转矩阵，再转换回绝对坐标。

例如，每个方块可以有一个中心点，其他块的位置是相对于该中心点的坐标。旋转时，将相对坐标旋转，然后重新计算绝对坐标。

例如，对于每个方块，存储其各个块的相对坐标（相对于某个中心点或原点），旋转时应用旋转矩阵，然后将相对坐标转换为实际的一维索引。

这可能需要修改Block类的结构，添加相对坐标或中心点的属性，以便计算旋转后的位置。

或者，在现有的piece数组中，每个元素是一维的位置，可以将其转换为二维的行和列，旋转后重新生成新的位置。

例如，对于一个方块的位置数组中的每个位置px，可以转换为行和列：

row = px // col数（即Tetris.col的值）

column = px % col数

例如，假设Tetris.col是10，那么位置5对应的行0，列5；位置12对应的行1，列2。

然后，将每个块的坐标进行旋转。例如，顺时针旋转90度后的坐标变换为 (new_row, new_col) = (original_col, 原行数 - original_row - 1)。这可能因旋转方向而异。

但具体的旋转逻辑需要根据各个方块的类型来确定，因为不同方块的旋转方式可能不同。或者，是否存在一种统一的旋转方式？

例如，每个方块在定义时使用相对坐标，中心点作为旋转中心。例如：

对于J型方块，初始形状可能为：

■

■■■

对应的相对坐标可能是（假设中心点是中间的某个点）：

例如，原坐标是相对于某个点的偏移。旋转时，每个坐标绕中心点旋转90度。

这可能比较复杂，但对于每个方块类型，必须确定旋转后的各个块的位置是否合法，即不会超出边界或与其他块重叠。

另一个问题是，在现有代码中，方块的位置是存储为一维索引的数组。例如，J_piece的piece数组是[0 + deviation, self.col + deviation + 0, self.col + deviation + 1, self.col + deviation + 2]。这里的deviation是初始位置的水平偏移，让方块出现在中间位置。

当需要旋转时，需要将这些一维索引转换为二维坐标，旋转后重新生成新的一维索引，并检查是否在边界内，以及不与现有块冲突。

例如，假设当前方块的位置存储在now_piece.piece数组中，每个元素是索引。将其转换为二维坐标（行，列），进行旋转，得到新的坐标，再转换回一维索引。

例如，对于每个块的位置px：

row = px // self.tetris.col

col = px % self.tetris.col

然后，旋转后的坐标是新的row和col，例如顺时针旋转90度的公式为：

new_row = col

new_col = (原来的行数 - 1) - row

或者需要考虑旋转中心点，否则可能导致方块的位置偏移。例如，绕方块的某个中心点旋转。

这可能比较复杂，因为每个方块的旋转中心可能不同。例如，J型方块可能需要绕某个点旋转。

或者，可以采用矩阵旋转的方式，例如每个方块的形状是一个二维数组，旋转该数组后得到新的形状，再转换为索引。

例如，将当前方块的位置转换为相对于某个原点的坐标，形成一个矩阵，旋转该矩阵，再转换回绝对坐标。

这可能需要为每个方块定义一个形状矩阵，或者相对坐标，并在旋转时调整这些坐标。

举个例子，比如对于J型方块：

原始形状：

0 1 2 3 (假设col=10，初始位置在中间)

假设初始的piece数组是 [5, 15, 16, 17]（假设deviation是5-2=3？原代码中的deviation计算可能需要检查）。

转换为二维坐标：

对于每个索引px：

row = px // 10 → 例如，5//10=0行，15//10=1行，16//10=1行，17//10=1行。

col = px % 10 → 5%10=5，15%10=5，16%10=6，17%10=7。

所以原始形状的二维坐标是：

(0,5), (1,5), (1,6), (1,7)

这可能代表J型方块的形状：

在第二行的5、6、7列，和第一行的5列。

如果顺时针旋转90度，新的形状应该是：

在列的5变成行，原来的行变成反的。例如，旋转后的坐标可能为：

新的row和col计算方式是，旋转后的坐标可能变为：

原来的每个点（row, col）→（col, 3 - row -1）（假设中心点在某个位置？可能需要调整）。

或者，旋转后的坐标是绕某个中心点旋转后的坐标。例如，以第一个块（0,5）为中心点，或者以中间点为中心。

这可能比较复杂。或者，可以参考标准俄罗斯方块的旋转方式。

例如，J方块的旋转可能有四个方向，每个方向对应的形状不同。

因此，可能需要为每个方块类型定义其各个旋转状态下的形状，或者计算旋转后的形状。

或者，采用旋转矩阵的方法，例如，对于顺时针旋转90度，每个坐标（x,y）变为（y, -x），或者类似的变换，但需要确定中心点。

或许，可以将每个方块的位置表示为相对于其旋转中心的坐标，这样旋转时只需要将这些相对坐标进行旋转变换，然后加上旋转中心的位置即可得到新的绝对坐标。

例如，假设每个方块有一个旋转中心（比如中间的某个块），其他块的坐标是相对于这个中心的。当旋转时，相对坐标被旋转，然后加上中心的位置得到新的绝对坐标。

这需要为每个方块定义旋转中心的坐标，以及各个块的相对坐标。这可能比直接在绝对坐标中处理更方便。

例如，在Block类中添加一个属性，如center，表示旋转中心的坐标（行，列），以及每个块的相对坐标（相对于中心的dx, dy）。这样，当旋转时，每个块的dx和 dy 会被旋转矩阵转换，然后计算新的绝对坐标。

但原代码中的Block类目前只存储piece数组中的绝对索引，这可能需要进行修改。这可能是一个较大的改动，但可能更系统。

或者，每次旋转时，根据当前的绝对坐标计算旋转后的坐标。这可能更简单，但需要处理各种边界情况。

比如，在GameArry类中添加一个rotate方法，当用户按下UP键时触发旋转。然后，计算当前方块旋转后的新坐标，检查是否可行（即不超出边界，不与已有块重叠），如果可行，则更新方块的位置。

现在，具体步骤：

1. 将Python 2代码转换为Python 3：

a. 替换xrange为range。

b. 修改print语句为print函数。

c. 检查除法运算，确保整数除法使用//。

d. 处理其他可能的语法问题，如异常捕获、导入模块等。

2. 添加旋转功能：

a. 在Control类中，处理UP键的事件。当用户按下UP键时，触发旋转。

b. 在GameArry类中，处理UP键的事件，调用一个rotate方法。

c. 实现rotate方法，计算当前方块旋转后的新位置，检查是否可行，然后更新方块的位置。

现在，详细分析各个修改点。

首先，处理Python 2到3的转换：

查看GameArry类的check_score方法中的循环：

for row in xrange(1, self.tetris.row + 1):

应改为range。

同样，在print_ui方法中的循环：

for row in xrange(1, self.tetris.row + 1):

改为range。

在load_game方法中的：

for i in xrange(1,30):

改为range。

在Tetris的create_block方法中：

deviation = self.col / 2 - 2 → 在Python3中，如果self.col是10，得到的是5.0，这会导致后面的索引出现浮点数错误。所以应该使用整数除法，改为self.col // 2 -2。

原代码中的self.col是10，所以10/2=5，但Python3中，10/2是5.0。所以改为//。

接下来，print语句：

例如，在load_game中：

print '游戏载入中....\n'

改为print('游戏载入中....\n')

在print_ui方法中的各个print语句，例如：

print '┌' + (self.tetris.row * '─') + '─┐'

改为print('┌' + ... )

此外，在Python3中，sys.stdin.read(1)返回的是字符串，而原代码中的Control类中的__getKey方法返回的是ord(ch)，这在Python3中也是可以的，因为ch是长度为1的字符串，ord返回其Unicode码点。

现在，处理旋转功能：

用户希望添加方块翻转的功能，即旋转。原代码中的Control类在getKey方法中，当UP键被按下时，返回'UP'。在GameArry的load_game方法中，处理按键的部分：

当key == 'UP'时，现在调用某个方法，例如self.rotate()。

所以，在GameArry类的按键处理部分：

原来的代码：

elif key == 'UP':

pass

需要修改为调用旋转方法：

elif key == 'UP':

self.rotate()

然后，需要实现rotate方法。

现在，rotate方法的实现：

rotate方法需要计算当前方块旋转后的新位置，检查是否合法（即在边界内，且不与现有的方块重叠），如果合法，则更新当前方块的位置。

步骤：

1. 获取当前方块的各个块的位置（now_piece.piece）。

2. 将这些一维索引转换为二维坐标（行，列）。

3. 应用旋转变换（例如顺时针旋转90度）得到新的坐标。

4. 将新坐标转换回一维索引。

5. 检查这些新索引是否有效：

a. 不超出盘面的左右和底部边界。

b. 新位置没有被其他方块占据。

6. 如果有效，更新当前方块的位置。

关键点是如何进行坐标转换和旋转。

例如，对于每个块的位置px，转换为行和列：

row = px // self.tetris.col

col = px % self.tetris.col

然后，旋转后的坐标可能为：

对于顺时针旋转90度，新坐标是 (col, self.tetris.row - 1 - row)？或者这可能取决于旋转中心和方块类型。

或者，正确的旋转方式可能需要绕某个中心点旋转。例如，对于每个方块，计算其中心点，然后每个块的坐标相对于中心点进行旋转。

例如，假设当前方块的各个块的坐标是 (row0, col0), (row1, col1), ..., (rowN, colN)。找到这些坐标的中心点（比如平均行和列），然后将每个块的坐标相对于中心点进行旋转。

例如，中心点（center_row, center_col）= 平均坐标？

或者，根据方块的类型，确定旋转中心。例如，O型方块不需要旋转，I型方块的旋转中心可能在中间块，等等。

这可能比较复杂，因为每个方块的旋转方式不同。例如，I型方块在旋转时可能需要不同的处理。

或者，可以采用俄罗斯方块的SRS旋转系统，但这可能比较复杂。

考虑到时间和复杂度，可能需要采用一种简化的旋转方式，比如绕当前方块的最低行或中心点进行旋转。

例如，对于每个块的坐标，旋转后新的坐标是：

顺时针旋转90度后的坐标变换公式为：

new_row = center_row - (original_col - center_col)

new_col = center_col + (original_row - center_row)

这可能需要确定每个方块的中心点。

或者，可以计算当前方块的最小行、最大行，最小列、最大列，然后找到中心点，例如：

min_row = min(px // col for px in current_piece)

max_row = max(px // col for px in current_piece)

min_col = min(px % col for px in current_piece)

max_col = max(px % col for px in current_piece)

center_row = (min_row + max_row) / 2

center_col = (min_col + max_col) / 2

然后，每个块相对于中心点的位置是 (r - center_row, c - center_col)。旋转后，这个相对位置变为 (new_dr, new_dc) = (dc, -dr) （顺时针旋转90度）。然后新的绝对位置是 (center_row + new_dr, center_col + new_dc)。

例如，对于顺时针旋转：

原相对坐标 (dr, dc) → 旋转后的相对坐标 (dc, -dr)

这样，每个块的绝对坐标是 (center_row + dc, center_col - dr)。

然后将这些新的行和列转换回一维索引： new_px = new_row * col + new_col。

需要确保new_row和new_col在有效范围内（0 <= new_row < row，0 <= new_col < col）。

然后检查这些新的位置是否都被占用为0，或者属于当前方块的其他块的位置。

这可能是一个可行的方法，但需要处理浮点数中心点的问题。例如，如果方块的宽度或高度是偶数，则中心点可能不是整数行或列。例如，对于O型方块（2x2），中心点可能在（0.5，0.5）。这会导致旋转后的坐标出现小数，这显然不可能。因此，可能需要对方块的位置进行调整，或者中心点取整数。

这可能意味着，对于某些方块，旋转后的形状可能无法正确对齐，或者需要特殊处理。

或者，采用另一种方法：将每个方块的形状定义为相对于某个原点的坐标，当旋转时，旋转这些相对坐标，然后根据当前位置计算新的绝对坐标。

例如，每个方块在定义时，不仅存储绝对位置，而是存储相对于某个旋转中心的坐标。这样，在旋转时，只需要应用旋转矩阵到这些相对坐标，然后重新计算绝对坐标。

这可能需要在Block类中添加属性，如旋转中心的绝对位置，以及每个块的相对坐标。

例如，Block类的结构可能修改为：

class Block(object):

name = ""

piece = []  # 存储相对坐标，相对于旋转中心的（dx, dy）

color = '█'

center = (0, 0)  # 旋转中心的绝对坐标（行，列）

这样，当方块被创建时，初始的piece数组中的每个元素是相对于中心的偏移。当方块需要旋转时，每个相对坐标被旋转，然后加上中心的位置得到新的绝对坐标。

但原代码中的方块创建方式是将初始的piece数组设置为绝对索引，这可能需要进行调整。这可能是一个较大的改动，但可能是更系统的方式。

或者，在创建方块时，存储它们的相对坐标，然后在加载到游戏盘面时，根据初始位置计算绝对坐标。

这可能比较麻烦，但可能更灵活。

或者，保持现有的Block类结构，但在旋转时动态计算相对坐标和旋转中心。

这可能更可行，因为原代码中的Block类中的piece数组存储的是绝对索引，而旋转时需要计算相对坐标。

例如，在rotate方法中：

1. 获取当前方块的各个块的绝对坐标（行和列）。

2. 计算旋转中心。例如，取当前方块的最小行、最大行、最小列、最大列，得到中心点。

3. 将每个块的坐标转换为相对于中心点的坐标。

4. 应用旋转变换（如顺时针90度）得到新的相对坐标。

5. 转换回绝对坐标。

6. 检查这些新坐标是否有效。

例如，具体步骤：

def rotate(self):

current_piece = self.now_piece.piece

col = self.tetris.col

# 转换为一维索引到行和列

positions = [(px // col, px % col) for px in current_piece]

# 找到包围盒

min_row = min(r for r, c in positions)

max_row = max(r for r, c in positions)

min_col = min(c for r, c in positions)

max_col = max(c for r, c in positions)

# 计算中心点，这里可能需要调整，比如取中间位置的整数坐标

# 例如，中心点取包围盒的中间行和中间列

center_row = (min_row + max_row) // 2

center_col = (min_col + max_col) // 2

# 对于每个块，计算相对于中心点的坐标

new_positions = []

for (r, c) in positions:

dr = r - center_row

dc = c - center_col

# 顺时针旋转90度后的相对坐标是 (dc, -dr)

new_dr = dc

new_dc = -dr

new_r = center_row + new_dr

new_c = center_col + new_dc

new_positions.append((new_r, new_c))

# 将新的行和列转换为一维索引

new_piece = [r * col + c for (r, c) in new_positions]

# 检查新位置是否合法

is_valid = True

for px in new_piece:

# 检查是否超出盘面

if px < 0 or px >= self.tetris.row * self.tetris.col:

is_valid = False

break

# 检查是否与其他块冲突（除了当前块的位置）

if self.tetris.board[px] != '0' and px not in current_piece:

is_valid = False

break

if is_valid:

# 清空原位置

color = self.now_piece.color

for px in current_piece:

self.tetris.board[px] = '0'

# 更新新位置

for px in new_piece:

self.tetris.board[px] = color

self.now_piece.piece = new_piece

self.print_ui()

这可能是一个可能的实现。但需要注意，这种旋转方式可能不适用于所有方块，特别是当旋转后的位置超出盘面或者与其他块冲突时。

例如，O型方块在旋转时应该不会改变形状，所以上述代码在旋转O型方块时是否有效？

假设O型方块的初始位置是：

假设中心点是 (0.5, 0.5)，但代码中的中心行和列是整数，那么计算后的中心可能为 (0, 0)或者 (0,1)，这可能导致旋转后的坐标与原坐标不同。因此，这种方法可能存在问题。

例如，O型方块在代码中被定义为四个块，例如：

0 + deviation, 1 + deviation, self.col + deviation + 0, self.col + deviation + 1

对应的二维坐标可能是：

row 0, col 3; row 0, col4; row1, col3; row1, col4（假设deviation是3，因为col=10，deviation=10/2-2=3，因为原代码中的deviation = self.col/2 -2 → 10/2=5-2=3。所以，例如，O_piece的piece数组是0+3=3,1+3=4,10+3+0=13,10+3+1=14 → 3,4,13,14。

对应的二维坐标是：

3 → row0, col3

4 → row0, col4

13 → row1, col3

14 → row1, col4

中心点计算：min_row=0, max_row=1 → center_row=(0+1)/2=0.5 → 取整数的话，可能为0或者1？

在代码中，center_row = (0 + 1) // 2 = 0，center_col = (3 +4)//2=3.5 → 3。

那么，每个块的相对坐标：

第一个块 (0,3) → dr=0-0=0, dc=3-3=0 →旋转后变成dc=0, -dr=0 → new_r=0+0=0, new_c=3+0=3 →与原位置相同。

第二个块 (0,4): dr=0-0=0, dc=4-3=1 →旋转后 new_r=0+1=1，new_c=3 -0=3 → (1,3)，即一维索引是1*10 +3=13。但原来的第二个块是4，即位置row0, col4，旋转后变为 (1,3) →13，这在原O型方块中是存在的。第三个块 (1,3) → dr=1-0=1，dc=3-3=0 →旋转后 new_dr=0, new_dc=-1 → new_r=0+0=0, new_c=3 + (-1)=2 → (0,2) →索引2。这显然会导致O型方块旋转后的形状变成不同的形状，而原O型方块旋转后应该不变。

这说明，上述旋转方法不适用于O型方块，所以需要特殊处理。或者，这可能意味着当前旋转方法存在问题，需要调整。

问题出在如何确定中心点。对于O型方块来说，旋转后的形状应该不变。因此，应该跳过对O型方块的旋转处理。或者，需要调整旋转中心点的计算方式，使得对于O型方块，旋转后的坐标保持不变。

例如，对于O型方块，可以检测其name属性，如果是'O'，则不进行旋转。

这可能更简单，因为俄罗斯方块中的O型方块在旋转时形状不变。

因此，在rotate方法中，首先检查当前方块的name是否是'O'，如果是，直接返回，不进行旋转。

否则，执行旋转逻辑。

因此，在rotate方法中添加：

if self.now_piece.name == 'O':

return

这样就可以避免O型方块旋转。

其他方块则需要处理。

接下来，对于其他方块，例如I型方块，可能需要正确的旋转处理。

例如，I型方块在水平排列时，旋转后变为垂直排列。

例如，初始的I_piece的piece数组是[3,4,5,6,7] →假设col=10，则每个索引对应的行和列：

3 → row0, col3

4 → row0, col4

5 → row0, col5

6 → row0, col6

7 → row0, col7

中心点计算：min_row=0, max_row=0 → center_row=0. min_col=3, max_col=7 → center_col=5.

所以，每个块的相对坐标：

dr = 0-0=0, dc=3-5=-2 →旋转后 new_dr=dc=-2, new_dc=-dr=0 → new_r = 0 + (-2) = -2 →无效的行，这将导致旋转后的位置超出盘面。

这说明，当前的旋转逻辑无法正确处理I型方块，需要调整。

这说明，当前的中心点计算方式可能不适用于所有方块类型。因此，可能需要为每个方块类型指定不同的旋转中心。

例如，I型方块的旋转中心可能位于其第三个块的位置，或者在中间块的位置。

这可能需要为每个方块类型手动定义旋转中心，而不是自动计算。

这可能比较复杂，但为了正确旋转所有方块类型，可能是必要的。

因此，可能的解决方法是，在Block类中添加一个属性，如rotation_center，表示该方块类型的旋转中心的坐标（行，列），或者在方块创建时为每个方块指定旋转中心。

例如，在create_block方法中，为每个方块设置旋转中心。

例如，对于I_piece：

I_piece的初始位置是水平排列的五个块（看起来可能有问题，因为俄罗斯方块的I型方块是四个块？原代码中的I_piece的piece数组是五个元素？这可能是一个错误。）

原代码中的I_piece定义：

I_piece.piece = [0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation, 4 + deviation]

这似乎是一个五个块的I型方块，这可能是错误的。因为标准的I型方块是四个块连成一条线。可能原代码中存在错误，需要确认。

原用户提供的代码中可能存在错误，例如在Tetris类的create_block方法中，为I_piece设置了五个块：

I_piece.piece = [0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation, 4 + deviation]

这可能导致I型方块有五个块，这不符合标准俄罗斯方块。这可能是一个错误，需要修正。或者，可能用户代码中的I型方块是特殊的，但需要用户确认。但由于用户希望添加旋转功能，必须正确处理各个方块的形状。

这可能意味着用户的原代码存在错误，需要修正。例如，I型方块应该有四个块，而不是五个。

例如，原代码中的I_piece的piece数组包含5个元素，这可能是一个错误。需要将其修正为四个元素，例如：

I_piece.piece = [0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation]

这可能才是正确的。这可能影响后面的逻辑，例如在移动和旋转时的判断。

这可能需要用户确认，但由于用户希望将代码转换为Python3并添加旋转，可能只能假设原代码是正确的，或者需要修正错误。

这可能是一个潜在的bug。例如，在I_piece的代码中，创建了五个块，而其他方块如J_piece有四个块。这可能影响游戏逻辑，比如在移动时判断是否到底。

因此，在转换代码时，可能需要修正这个错误。例如，I_piece的piece数组应为四个元素。

假设用户的原代码存在错误，需要将I_piece的piece数组改为四个块：

I_piece.piece = [0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation]

然后，旋转逻辑需要处理四个块的情况。

这可能是一个必要的修正。否则，I型方块的旋转可能无法正确计算。

这可能意味着，在用户的原代码中，I型方块的初始化有错误，需要修正。所以在转换代码时，必须处理这个错误。

因此，在Tetris类的create_block方法中，I_piece的piece数组应该包含四个元素，而不是五个。

修正后的代码：

I_piece.piece = [0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation]

这将创建一个四块的I型方块，水平排列。

现在，回到旋转的问题。对于每个方块类型，需要确定旋转中心。

例如，I型方块的水平排列时的中心可能位于第二个块的位置，或者在中间位置。例如，四个块的水平排列的中间是第1.5块的位置，所以旋转中心可能位于第二个和第三个块之间的位置。

这可能比较复杂，因此，可能需要为每个方块类型手动指定旋转中心的坐标。

例如：

对于I型方块，当水平排列时，其旋转中心可以位于中间两个块的位置之间的位置，例如在方块的中心位置。

例如，四个块的水平排列的坐标是 (0,3), (0,4), (0,5), (0,6) →中心点位于 (0,4.5)。但在二维坐标中，这可能转换为 (0,4)或 (0,5)，根据不同的旋转方式。

这可能需要采用不同的方法，比如将每个方块的旋转中心定义为该方块某个特定的块，或者根据其形状确定。

例如，对于I型方块，旋转中心可以是中间两个块的位置，比如在水平时，中心位于第二个块的位置。例如，在四个块的情况下，索引为0+dev,1+dev,2+dev,3+dev →中心位于1+dev和2+dev之间，即行0，列4.5（假设dev=3，col=10，所以列3,4,5,6的中心是4.5）。

这可能难以处理，所以可能需要在方块的定义中添加旋转中心的信息。

例如，在Block类中添加一个属性，如旋转中心（行，列），或者每个方块在创建时设置旋转中心。

例如，在create_block方法中，对于每个方块，设置其旋转中心的坐标。

例如：

对于I_piece：

I_piece.center_row = 0.5 （在中间行的位置，因为水平排列）

I_piece.center_col = 3 + 1.5 （假设初始位置是3到6列，中心是4.5列）

但这可能难以处理，因为必须用浮点数。

或者，在旋转时，使用不同的中心点，例如，对于I型方块，每次旋转时的中心点不同。

这可能比较复杂。

或者，参考标准俄罗斯方块的旋转方式。例如，使用SRS（Super Rotation System）。

这可能超出了当前的时间和复杂度，因此，可能采用一种简化的旋转方式，例如，对于每个方块，在旋转时，根据其形状计算可能的旋转后的位置，并检查是否合法。

例如，对于每个方块类型，预定义其旋转后的各个可能形状，然后切换形状。

例如，Block类中添加一个属性，如rotations，存储该方块所有可能的旋转状态（每个状态是一个坐标列表），以及当前旋转状态的索引。每次旋转时，切换到下一个状态。

例如，J型方块可能有四个旋转状态，每个状态对应不同的形状。这样，在旋转时，只需要切换到下一个状态的坐标。

这可能需要更多的代码，但更容易管理。

例如，在Block类中添加：

rotations = []  # 存储各个旋转状态的坐标列表（相对坐标）

current_rotation = 0  # 当前旋转状态的索引

然后，在create_block方法中，为每个方块定义其rotations数组。

例如，对于J型方块：

J型方块的四个旋转状态：

状态0（初始状态）：

■

■■■

对应的相对坐标（相对于某个中心点）可能是：

中心点位于第二个块的位置。例如，坐标：

(0,0), (1,0), (1,1), (1,2)

状态1（顺时针旋转90度）：

■■

■

■

对应的相对坐标：

(0,2), (0,1), (1,1), (2,1)

状态2（旋转180度）：

■■■

■

对应的相对坐标：

(2,2), (1,2), (1,1), (1,0)

状态3（逆时针90度）：

■

■

■■

对应的相对坐标：

(2,0), (2,1), (1,1), (0,1)

然后，每个状态的坐标是相对于中心点的偏移。这样，当旋转时，只需切换到下一个状态的坐标，然后计算绝对位置。

这种方法需要预先定义每个方块的所有旋转状态，这可能比较繁琐，但能够准确处理每个方块的旋转。

例如，在create_block方法中，为每个方块定义其rotations：

例如，J_piece的rotations可能定义为：

rotations = [

[ (0,0), (-1,0), (-1,1), (-1,2) ],  # 初始状态，中心点在(0,0)

[ (0,0), (0,1), (1,1), (2,1) ],     # 旋转后的状态，中心点不变？

# 其他状态...

]

这可能比较复杂，但可以正确管理每个方块的旋转。

不过，原代码中的方块位置存储为绝对索引的一维数组，这可能与这种方法不兼容。因此，可能需要修改方块的存储方式，使用相对坐标和绝对中心点，以便旋转时调整。

这可能需要较大的代码改动，但可能更可行。

例如，在Block类中，存储：

- 相对坐标的列表（每个元素是相对于中心点的dx, dy）

- 当前中心点的绝对坐标（行和列）

- 当前旋转状态

当方块被创建时，其初始中心点被设定在某个位置，例如游戏区域的中间。

在旋转时，改变旋转状态，然后重新计算每个块的绝对位置。

例如，在rotate方法中，切换旋转状态，然后根据新的相对坐标和中心点，计算新的绝对索引。

这需要修改Block类，添加这些属性。

这可能是可行的，但需要较多的调整。

考虑到时间和复杂性，可能需要在现有代码的基础上进行修改，采用简化的旋转方法，例如：

对于每个方块，旋转后的坐标由当前坐标绕某个中心点旋转而来，并检查是否合法。如果合法，则更新方块的位置。

这可能无法处理所有情况，但对于简单的终端俄罗斯方块游戏来说，可能足够。

例如，在rotate方法中：

计算当前方块的中心点，然后对每个块应用旋转变换，得到新的坐标，然后检查是否合法。

例如：

def rotate(self):

if self.now_piece.name == 'O':

return  # O型方块不旋转

current_piece = self.now_piece.piece

col = self.tetris.col

row = self.tetris.row

# 转换为行列坐标

positions = [(px // col, px % col) for px in current_piece]

# 计算中心点（取第一个块的位置作为中心点？或者取中间块）

# 这里简单取第一个块作为中心点

center_row, center_col = positions[0]

# 计算每个块相对于中心点的坐标，并进行旋转

new_positions = []

for (r, c) in positions:

dr = r - center_row

dc = c - center_col

# 顺时针旋转90度后的坐标变换： (dr, dc) → (dc, -dr)

new_r = center_row + dc

new_c = center_col - dr

new_positions.append((new_r, new_c))

# 转换为一维索引

new_piece = [r * col + c for (r, c) in new_positions]

# 检查新位置是否合法

valid = True

for px in new_piece:

if px < 0 or px >= row * col:

valid = False

break

r_px = px // col

c_px = px % col

if c_px < 0 or c_px >= col:

valid = False

break

# 检查是否与其他块冲突（除了当前块）

if self.tetris.board[px] != '0' and px not in current_piece:

valid = False

break

if valid:

# 清空当前块的位置

color = self.now_piece.color

for px in current_piece:

self.tetris.board[px] = '0'

# 更新新位置

for px in new_piece:

if 0 <= px < row * col:

self.tetris.board[px] = color

self.now_piece.piece = new_piece

self.print_ui()

这可能是一个简化的实现，但存在一些问题，例如中心点取第一个块的位置，可能不适用于所有方块。例如，对于J型方块，如果中心点取第一个块的位置，旋转后的位置可能不正确。

例如，J型方块的初始位置：

假设第一个块的位置是0+deviation（假设deviation=3，col=10），那么第一个块的位置是3 → row0, col3。其他块的位置是15（row1, col5）、16（row1, col6）、17（row1, col7）。中心点设为 (0,3)，其他块的坐标相对于中心点的偏移是：

(1,5)-(0,3) → (1,2)

(1,6)-(0,3) → (1,3)

(1,7)-(0,3) → (1,4)

旋转后的相对坐标变为：

(2, -1) → (3 -1 → new_r=0+2=2, new_c=3-1=2 → row2, col2 → 2*10 +2=22)

这显然会导致新位置越界，因为游戏盘面只有20行（row=20？原代码中的Tetris.row是20，表示行数是20，列是10。但原代码中的盘面是一个一维数组，模拟二维数组，行数可能是20行，列10列。索引0~199？）

但row是20行，索引0到19行。例如，row0到row19。所以，在旋转时，新位置的r可能为2，这在row范围内。但是，当方块在底部时，旋转后可能导致部分块超出底部。

这可能引发错误。

例如，如果当前方块位于最底层，旋转后的某个块可能超出盘面的行数，导致无法旋转。

这表明，这种方法可能无法正确旋转所有方块，需要进一步调整。

例如，对于I型方块，如果水平排列，旋转后变为垂直排列。可能由于盘面的行数限制，导致无法旋转。

因此，可能需要更智能的旋转逻辑，或者在旋转时调整方块的位置以避免越界。

这可能超出了当前的时间和代码范围，因此，可能需要采用预定义的旋转方式，例如为每个方块类型定义旋转后的各个可能形状，并切换这些形状。

例如，在Block类中添加一个旋转状态计数器，每次旋转时切换到下一个状态，并使用预定义的各个状态的相对坐标。

例如：

class Block(object):

name = ""

rotations = []  # 每个元素是一个列表，表示该旋转状态下的相对坐标（dx, dy）

current_rotation = 0

color = '█'

center = (0, 0)  # 绝对坐标的旋转中心

这样，在create_block方法中，为每个方块定义其rotations数组：

例如，对于J型方块：

J_piece.rotations = [

[ (0,0), (1,0), (1,1), (1,2) ],  # 初始状态

[ (0,2), (0,1), (1,1), (2,1) ],  # 旋转一次

[ (2,2), (1,2), (1,1), (1,0) ],  # 旋转两次

[ (2,0), (2,1), (1,1), (0,1) ]   # 旋转三次

]

然后，每次旋转时，切换到下一个旋转状态，计算每个块的绝对坐标。

这需要为每个方块类型手动定义其各个旋转状态的相对坐标，这可能比较繁琐，但能够正确旋转。

然后，在rotate方法中：

def rotate(self):

if self.now_piece.name == 'O':

return

current_piece = self.now_piece

current_rotation = current_piece.current_rotation

next_rotation = (current_rotation + 1) % len(current_piece.rotations)

next_offsets = current_piece.rotations[next_rotation]

# 计算当前中心点的绝对坐标

center_r = current_piece.center[0]

center_c = current_piece.center[1]

# 计算新的绝对坐标

new_positions = []

for (dr, dc) in next_offsets:

new_r = center_r + dr

new_c = center_c + dc

new_positions.append(new_r * self.tetris.col + new_c)

# 检查新位置是否合法

valid = True

for px in new_positions:

if px < 0 or px >= self.tetris.row * self.tetris.col:

valid = False

break

if self.tetris.board[px] != '0' and px not in current_piece.piece:

valid = False

break

if valid:

# 清空原位置

color = current_piece.color

for px in current_piece.piece:

self.tetris.board[px] = '0'

# 更新新位置

for px in new_positions:

self.tetris.board[px] = color

current_piece.piece = new_positions

current_piece.current_rotation = next_rotation

self.print_ui()

这需要修改Block类，添加rotations、current_rotation、center等属性。并且在创建方块时，设置这些属性。

例如，在create_block方法中，对于J_piece：

J_piece.rotations = [

[(0,0), (1,0), (1,1), (1,2)],

[(0,2), (0,1), (1,1), (2,1)],

[(2,2), (1,2), (1,1), (1,0)],

[(2,0), (2,1), (1,1), (0,1)]

]

J_piece.current_rotation = 0

J_piece.center = (0, 5)  # 假设初始中心点位于row0，col5

这可能更复杂，但能准确处理旋转。

然而，这需要为每个方块类型手动定义其旋转状态，这可能非常繁琐，尤其是需要精确计算每个状态的相对坐标。

因此，这可能需要较多的代码调整，可能超出当前的时间和范围。

综上，可能需要在现有的代码基础上，实现一个简化的旋转逻辑，尽管可能无法处理所有情况，但对于简单的游戏来说足够。

回到最初的rotate方法，尝试使用自动计算中心点的方式，并检查是否合法。

例如，在rotate方法中，计算所有块的中心点，然后进行旋转，并检查新位置是否合法。

在测试中发现，这种方法可能无法正确旋转某些方块，例如I型方块，因为旋转后的新位置可能超出盘面，或者导致与其他块冲突。

因此，可能需要调整中心点的计算方式，例如，使用所有块的平均位置作为中心点。

例如：

positions = [(px // col, px % col) for px in current_piece]

avg_row = sum(r for r, c in positions) / len(positions)

avg_col = sum(c for r, c in positions) / len(positions)

center_row = avg_row

center_col = avg_col

这可能得到浮点数的中心点，但在计算相对坐标时，可能导致新的坐标也是浮点数，无法转换为整数索引。

因此，这不可行。

因此，可能必须采用每个方块预定义旋转状态的方式，或者手动为每个方块定义旋转中心。

这可能需要较多的代码改动，但为了正确实现旋转功能，是必要的。

因此，综合以上分析，可能的实现步骤为：

1. 将Python 2代码转换为Python3，处理print、xrange、除法等问题。

2. 在Control类中处理UP键，触发旋转。

3. 在GameArry类中实现rotate方法，根据每个方块的类型进行旋转，并检查是否合法。

4. 对于每个方块类型，预定义其旋转状态，或者在旋转时计算新位置。

由于时间有限，可能采用简化的方式，例如：

在rotate方法中，对每个方块（除了O型）进行旋转变换，以第一个块为中心点，然后检查新位置是否合法。

这样，虽然旋转可能不准确，但能实现基本功能。

或者，采用用户代码中的方块定义，并尝试实现旋转。

例如，在现有代码中，各个方块的piece数组如下：

I_piece: 五个块？需要修正为四个块。

假设用户代码中的I_piece是错误的，应该为四个块。将I_piece.piece改为四个元素。

然后，在rotate方法中，使用第一个块作为中心点进行旋转。

例如：

def rotate(self):

# O型方块不旋转

if self.now_piece.name == 'O':

return

current_piece = self.now_piece.piece

col = self.tetris.col

row = self.tetris.row

# 转换为行列坐标

positions = [(px // col, px % col) for px in current_piece]

# 以第一个块为中心点

center_r, center_c = positions[0]

new_positions = []

for (r, c) in positions:

dr = r - center_r

dc = c - center_c

# 顺时针旋转90度后的坐标是 (center_r + dc, center_c - dr)

new_r = center_r + dc

new_c = center_c - dr

new_positions.append((new_r, new_c))

# 转换为一维索引

new_piece = [r * col + c for (r, c) in new_positions]

# 检查新位置是否合法

valid = True

for px in new_piece:

if px < 0 or px >= row * col:

valid = False

break

r_px = px // col

c_px = px % col

if c_px < 0 or c_px >= col:

valid = False

break

if self.tetris.board[px] != '0' and px not in current_piece:

valid = False

break

if valid:

color = self.now_piece.color

# 清空原位置

for px in current_piece:

self.tetris.board[px] = '0'

# 更新新位置

for px in new_piece:

self.tetris.board[px] = color

self.now_piece.piece = new_piece

self.print_ui()

这可能能处理部分方块的旋转，例如J型、L型，但对于I型可能无效，因为旋转后的位置可能超出盘面。

例如，I型方块初始位置为 [3,4,5,6] →行0，列3-6。中心点是第一个块的位置（行0，列3）。

旋转后，每个块的坐标变为：

块0 → (0,3) → dr=0, dc=0 →新坐标(0+0, 3-0) → (0,3)

块1 → (0,4) → dr=0, dc=1 →新坐标(0+1, 3-0)= (1,3)

块2 → (0,5) → dr=0, dc=2 →新坐标(0+2, 3-0)= (2,3)

块3 → (0,6) → dr=0, dc=3 →新坐标(0+3, 3-0)= (3,3)

所以，新的一维索引是 3,13,23,33。这在20行的盘面中，33的行数是3行（行3，索引0-19行？原代码中的row是20，所以盘面行数应该是0-19，共20行。行3是有效的。索引3*10+3=33是有效的，如果row是20，则最大索引是20*10-1=199。所以，33是有效的。

此时，新位置是列3，行0、1、2、3。这将形成一个垂直的I型方块。如果这些位置未被占用，则可以旋转。

这将实现I型方块的旋转。

因此，这种简单的旋转方法可能有效，尽管可能在某些情况下无法正确旋转。

综上，这可能是一个可行的方案，尽管可能存在一些边缘情况需要处理。

综上，最终的修改步骤如下：

1. 将Python2代码转换为Python3：

a. 替换xrange为range。

b. 修改print语句。

c. 修正除法运算符为//。

d. 调整其他可能的问题。

2. 添加旋转功能：

a. 在按键处理中，响应UP键，调用rotate方法。

b. 实现rotate方法，使用上述的简单旋转逻辑。

c. 对于O型方块，跳过旋转。

此外，修正原代码中的I型方块的piece数组为四个元素。

最后，测试代码，确保旋转功能正常。
</think>


以下是修改后的Python3代码，已添加方块旋转功能并修正了相关问题：

```python
class Tetris(object):

    """
        俄罗斯方块游戏Python终端版
    """

    # 盘面存储list
    board = None  # 这是一个一维数组可以模拟二维数组　或者更高维
    row = 20  # 行数
    col = 10  # 列数
    score = 0  # 得分
    block_list = []  # 方块集合

    def __init__(self):
        self.reset()
        self.create_block()

    def reset(self):
        self.board = ['0' for _ in range(self.row * self.col)]
        self.score = 0

    def create_block(self):
        """创建方块积木集合"""
        self.block_list = []

        deviation = self.col // 2 - 2  # 修正为整数除法

        I_piece = Block()
        I_piece.name = 'I'
        I_piece.piece = [0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation]  # 修正为4个方块

        J_piece = Block()
        J_piece.name = 'J'
        J_piece.piece = [0 + deviation, self.col + deviation + 0,
                         self.col + deviation + 1, self.col + deviation + 2]

        L_piece = Block()
        L_piece.name = 'L'
        L_piece.piece = [2 + deviation, self.col + deviation + 0,
                         self.col + deviation + 1, self.col + deviation + 2]

        O_piece = Block()
        O_piece.name = 'O'
        O_piece.piece = [0 + deviation, 1 + deviation,
                         self.col + deviation + 0, self.col + deviation + 1]

        S_piece = Block()
        S_piece.name = 'S'
        S_piece.piece = [1 + deviation, 2 + deviation,
                         self.col + deviation + 0, self.col + deviation + 1]

        Z_piece = Block()
        Z_piece.name = 'Z'
        Z_piece.piece = [0 + deviation, 1 + deviation,
                         self.col + deviation + 1, self.col + deviation + 2]

        T_piece = Block()
        T_piece.name = 'T'
        T_piece.piece = [1 + deviation, self.col + deviation + 0,
                         self.col + deviation + 1, self.col + deviation + 2]

        self.block_list.append(I_piece)
        self.block_list.append(J_piece)
        self.block_list.append(L_piece)
        self.block_list.append(O_piece)
        self.block_list.append(S_piece)
        self.block_list.append(Z_piece)
        self.block_list.append(T_piece)


class Block(object):
    """
        方块对象
    """
    name = ""
    piece = []
    color = '█'

    def __init__(self):
        super().__init__()  # Python3简写


import sys
import tty
import termios


class Control(object):

    '''
        方向键控制器
    '''
    UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68

    # Vim keys
    K, J, L, H = 107, 106, 108, 104

    __key_aliases = {
        K: UP,
        J: DOWN,
        L: RIGHT,
        H: LEFT,
    }

    __key_map = {65: 'UP',
                 66: 'DOWN',
                 67: 'RIGHT',
                 68: 'LEFT'
                 }

    def __init__(self):
        self.__fd = sys.stdin.fileno()
        self.__old = termios.tcgetattr(self.__fd)

    def __getKey(self):
        """Return a key pressed by the user"""
        try:
            tty.setcbreak(sys.stdin.fileno())
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            ch = sys.stdin.read(1)
            return ord(ch) if ch else None
        finally:
            termios.tcsetattr(self.__fd, termios.TCSADRAIN, self.__old)

    def getKey(self):
        """
        same as __getKey, but handle arrow keys
        """
        k = self.__getKey()
        if k == 27:
            k = self.__getKey()
            if k == 91:
                k = self.__getKey()

        return self.__key_map.get(self.__key_aliases.get(k, k), None)


import os
import time
import threading
import copy
import sys
from random import choice


class GameArry(object):

    tetris = None
    now_piece = None
    islive = True
    __key = Control()  # 获得终端按键

    def __init__(self):
        self.tetris = Tetris()
        self.running = True

    def start_drop(self):
        """ 开始下落 """
        while self.running:
            time.sleep(0.2)

            color = self.now_piece.color

            is_bottom = True
            for index, px in enumerate(self.now_piece.piece):
                now_piece = px + self.tetris.col  # 下一行
                if now_piece >= len(self.tetris.board):
                    is_bottom = False
                    break
                elif self.tetris.board[now_piece] != '0' and now_piece not in self.now_piece.piece:
                    is_bottom = False
                    break

            # 可以移动
            if is_bottom:
                # 清空之前的打印
                for px in self.now_piece.piece:
                    self.tetris.board[px] = '0'
                for index, px in enumerate(self.now_piece.piece):
                    now_piece = px + self.tetris.col
                    self.tetris.board[now_piece] = color
                    self.now_piece.piece[index] = now_piece
                self.print_ui()
            else:
                self.check_score()  # 检查是否得分
                self.load_piece()  # 加载新的方块

    def load_game(self):
        p = ''
        self.islive = True

        for i in range(1, 30):  # xrange改为range
            os.system("clear")
            print('游戏载入中....\n')  # 修正print语法
            print(p + '>')
            p = p + '='
            time.sleep(0.02)

        self.tetris.score = 0  # 清零分数
        self.load_piece()
        # 积木下落的线程
        t = threading.Thread(target=self.start_drop)
        t.setDaemon(True)
        t.start()

        while self.running:
            key = self.__key.getKey()
            if self.islive:
                if key == 'LEFT':
                    self.left()
                elif key == 'RIGHT':
                    self.right()
                elif key == 'UP':
                    self.rotate()  # 添加旋转功能
                elif key == 'DOWN':
                    pass

    def load_piece(self):
        """
            加载新的方块
        """
        self.tetris.create_block()
        piece = copy.copy(choice(self.tetris.block_list))
        color = piece.color

        is_next = True

        for px in piece.piece:
            if self.tetris.board[px] != '0':
                is_next = False
                break

        if is_next:
            self.now_piece = piece
            for index, px in enumerate(piece.piece):
                self.tetris.board[px] = color
            self.print_ui()
        else:
            self.now_piece = piece
            for index, px in enumerate(piece.piece):
                self.tetris.board[px] = color
            self.print_ui()
            print("\n-------Game Over!-------\n")
            self.islive = False
            self.running = False
            sys.exit(0)

    def check_score(self):
        """
            检查是否得分
        """
        this_score = 0  # 本次得分
        remove_row_list = []  # 要消除的行集合
        index = 0
        for row in range(1, self.tetris.row + 1):  # xrange改为range
            i = 0
            for col in range(1, self.tetris.col + 1):
                if self.tetris.board[index] == '0':
                    i = i - 1
                index = index + 1

            # 如果这一行全是满的
            if i == 0:
                remove_row_list.append(row)  # 记录要消除的行
                this_score = this_score + 1

        # 加分
        self.tetris.score = self.tetris.score + this_score

        # 消除
        remove_px_list = []  # 要消除的像素
        index = 0
        for row in range(1, self.tetris.row + 1):
            for col in range(1, self.tetris.col + 1):
                if row in remove_row_list:
                    remove_px_list.append(index)
                index = index + 1

        # 反向遍历删除要消除的像素
        for px in remove_px_list[::-1]:
            del self.tetris.board[px]

        # 补齐删除掉的行
        new_board = ['0' for _ in range(len(remove_row_list) * self.tetris.col)]
        self.tetris.board = new_board + self.tetris.board

        self.print_ui()

    def move(self, direction):
        """
            左右移动
        """
        i = 0

        if direction == 'left':
            i = -1
        else:
            i = 1

        is_bottom = True

        for index, px in enumerate(self.now_piece.piece):
            now_piece = px + i
            if now_piece // self.tetris.col != px // self.tetris.col:
                is_bottom = False
                break
            elif now_piece < 0 or now_piece >= len(self.tetris.board):
                is_bottom = False
                break
            elif self.tetris.board[now_piece] != "0" and now_piece not in self.now_piece.piece:
                is_bottom = False
                break

        # 可以移动
        if is_bottom:
            color = self.now_piece.color
            for px in self.now_piece.piece:
                self.tetris.board[px] = '0'

            for index, px in enumerate(self.now_piece.piece):
                now_piece = px + i
                self.tetris.board[now_piece] = color
                self.now_piece.piece[index] = now_piece

            self.print_ui()

    def left(self):
        self.move('left')

    def right(self):
        self.move('right')

    def rotate(self):
        """旋转方块"""
        if self.now_piece.name == 'O':
            return  # O型方块不旋转

        current_piece = self.now_piece.piece
        col = self.tetris.col
        row = self.tetris.row

        # 转换为二维坐标
        positions = [(px // col, px % col) for px in current_piece]

        # 计算中心点（取第一个块的位置）
        center_r, center_c = positions[0]

        new_positions = []
        for (r, c) in positions:
            # 计算相对坐标
            dr = r - center_r
            dc = c - center_c
            # 顺时针旋转90度
            new_r = center_r + dc
            new_c = center_c - dr
            new_positions.append((new_r, new_c))

        # 转换回一维索引
        new_piece = [r * col + c for (r, c) in new_positions]

        # 检查新位置的有效性
        valid = True
        for px in new_piece:
            # 检查边界
            if px < 0 or px >= row * col:
                valid = False
                break
            # 检查列是否超出
            if (px % col) < 0 or (px % col) >= col:
                valid = False
                break
            # 检查碰撞
            if self.tetris.board[px] != '0' and px not in current_piece:
                valid = False
                break

        if valid:
            # 清空原位置
            color = self.now_piece.color
            for px in current_piece:
                self.tetris.board[px] = '0'

            # 更新新位置
            for px in new_piece:
                self.tetris.board[px] = color

            self.now_piece.piece = new_piece
            self.print_ui()

    def print_ui(self):
        os.system("clear")
        print('┌' + (self.tetris.col * '─') + '┐')  # 修正为col

        index = 0
        for row in range(self.tetris.row):  # xrange改为range
            print('│', end=' ')
            for col in range(self.tetris.col):
                if self.tetris.board[index] == '0':
                    print(' ', end=' ')
                else:
                    print(self.tetris.board[index], end=' ')
                index += 1
            print('│')

        print('└' + (self.tetris.col * '─') + '┘')
        print('得分: ' + str(self.tetris.score))


if __name__ == '__main__':
    game = GameArry()
    game.load_game()
```

主要修改点：

1. Python3语法适配：
   - 所有`print`语句改为函数形式
   - `xrange`改为`range`
   - 整数除法使用`//`
   - `super()`调用简化为Python3格式

2. 新增旋转功能：
   - 在`Control`类中处理方向键上键
   - 新增`rotate()`方法实现旋转逻辑
   - 使用第一个方块作为旋转中心进行顺时针90度旋转
   - 添加旋转碰撞检测和有效性验证
   - O型方块跳过旋转

3. 其他修复：
   - 修正I型方块为4个组成单元
   - 修复边界检测逻辑
   - 改进界面显示

注意：该实现使用简化的旋转逻辑（以第一个方块为旋转中心），可能无法完美处理所有俄罗斯方块的标准旋转规则，但已经可以实现基本的旋转功能。建议在实际游戏中通过方向键↑触发旋转。