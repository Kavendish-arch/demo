///c++
#include <iostream>
#include <Windows.h>
#include <conio.h>

using namespace std;

// 定义游戏地图的宽度和高度
const int W = 50;
const int H = 28;

// 定义方块类型：空闲或食物
enum BlockType {
    EMPTY = 0,
    FOOD = 1,
};

// 定义地图结构体，用于存储地图信息
struct Map {
    BlockType data[H][W];
    bool hasFood = false;
};

// 定义点结构体，用于表示坐标位置
struct Point {
    int x;
    int y;
};

// 定义蛇结构体，用于存储蛇的相关信息
struct Snake {
    Point snake[H * W];
    int sankeDir;
    int sankeLen;
    int lastMoveTime = 0;
    int moveFrequer = 200;
};

// 定义四个方向的坐标变化
const int direction[4][2] = {
        {0,  -1}, // 上
        {1,  0}, // 右
        {0,  1}, // 下
        {-1, 0}, // 左
};

// 隐藏光标函数
void hideCursor() {
    HANDLE hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO cursorInfo = {1, false};
    SetConsoleCursorInfo(hOutput, &cursorInfo);
}

// 清屏函数（跨平台）
void clearScreen() {
#ifdef _WIN32
    system("cls"); // Windows 系统
#else
    cout << "\033[2J\033[1;1H"; // Linux/Mac 系统
#endif
}

// 绘制顶部和底部边框
void drawBorder(int width) {
    cout << "[";
    for (int i = 0; i < width; ++i) {
        cout << "-";
    }
    cout << "]" << endl;
}

// 绘制中间内容
void drawContent(int height, int width, Map map) {
    for (int y = 0; y < height; ++y) {
        cout << "|";
        for (int i = 0; i < width; ++i) {
            if (map.data[y][i] == BlockType::FOOD) {
                cout << "*";
            } else {
                cout << " ";
            }
        }
        cout << "|" << endl;
    }
}

// 主绘制函数
void drawMap(Map map) {
    if (W <= 0 || H <= 0) {
        cerr << "Width and Height must be positive integers." << endl;
        return;
    }

    clearScreen(); // 清屏
    drawBorder(W); // 绘制顶部边框
    drawContent(H, W, map); // 绘制中间内容
    drawBorder(W); // 绘制底部边框
}

// 初始化地图
void initMap(Map &map) {
    for (int i = 0; i < H; i++) {
        for (int j = 0; j < W; ++j) {
            map.data[i][j] = BlockType::EMPTY;
        }
    }
    map.hasFood = false;
}

// 初始化蛇
void initSnake(Snake &snake) {
    snake.sankeLen = 3;
    snake.sankeDir = 1;
    snake.snake[0] = {8, 8};
    snake.snake[1] = {8, 9};
    snake.snake[2] = {8, 10};
}

// 绘制单元格
void drawUnit(Point point, const char unit[]) {
    COORD coord;
    HANDLE hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    coord.X = point.x + 1;
    coord.Y = point.y + 1;

    SetConsoleCursorPosition(hOutput, coord);
    cout << unit;
}

// 绘制蛇
void drawSnake(Snake snake) {
    for (int i = 0; i < snake.sankeLen; ++i) {
        drawUnit(snake.snake[i], "#");
    }
}

// 检查并改变蛇的方向
void checkChangeDir(Snake &snake) {
    if (kbhit()) {
        switch (_getch()) {
            case 'w':
                if (snake.sankeDir != 2) {
                    snake.sankeDir = 0;
                };
                break;
            case 'd':
                if (snake.sankeDir != 3) {
                    snake.sankeDir = 1;
                };
                break;
            case 's':
                if (snake.sankeDir != 0) {
                    snake.sankeDir = 2;
                };
                break;
            case 'a':
                if (snake.sankeDir != 1) {
                    snake.sankeDir = 3;
                };
                break;
            default:
                break;
        }
    }
}

// 移动蛇
void moveSnake(Snake &snake) {
    for (int i = snake.sankeLen - 1; i > 0; --i) {
        snake.snake[i] = snake.snake[i - 1];
    }
    snake.snake[0].x += direction[snake.sankeDir][0];
    snake.snake[0].y += direction[snake.sankeDir][1];
}

// 执行移动蛇的操作
void doMove(Snake &snake) {
    Point tail = snake.snake[snake.sankeLen - 1];
    drawUnit(tail, " ");
    moveSnake(snake);
    drawUnit(snake.snake[0], "#");
}

// 检查蛇的移动并更新
void checkSankeMove(Snake &snake, Map map) {
    int curTime = GetTickCount();
    if (curTime - snake.lastMoveTime > snake.moveFrequer) {
        doMove(snake);
        snake.lastMoveTime = curTime;
    }
}

// 检查食物的生成
void checkFoodGenerate(Snake &snake, Map &map) {
    if (false == map.hasFood) {
        srand(static_cast<unsigned int>(time(0)));
        map.hasFood = true;
        const int maxAttempts = W * H;
        for (int attempt = 0; attempt < maxAttempts; ++attempt) {
            int x = rand() % W;
            int y = rand() % H;
            int i = 0;
            for (i = 0; i < snake.sankeLen; ++i) {
                if (snake.snake[i].x == x && snake.snake[i].y == y) {
                    map.hasFood = false;
                    break;
                }
            }
            if (i == snake.sankeLen) {
                map.hasFood = true;

                if (map.data[y][x] == BlockType::EMPTY) {
                    map.data[y][x] = BlockType::FOOD;
                    drawUnit({x, y}, "$");
                    break;
                }
            }
        }
    }
}

// 检查蛇是否超出地图边界
bool checkOutOfMap(Snake &snake) {
    if (snake.snake[0].x < 0 || snake.snake[0].x >= W || snake.snake[0].y < 0 || snake.snake[0].y >= H) {
        return false;
    } else {
        return true;
    }
}

// 检查蛇是否吃到食物
void checkEatFood(Snake &snake, Map &map, Point food) {
    Point head = snake.snake[0];
    if (map.data[head.y][head.x] == BlockType::FOOD) {
        snake.snake[snake.sankeLen++] = food;
        map.data[head.y][head.x] = BlockType::EMPTY;
        map.hasFood = false;
        drawUnit(food, "&");
        checkFoodGenerate(snake, map);
    }
}

// 初始化游戏
void initGame(Snake &snake, Map &map) {
    hideCursor();
    initMap(map);
    initSnake(snake);
    drawMap(map);
    drawSnake(snake);
}

int main() {
    Map map;
    Snake snake;


    initGame(snake, map);
    checkFoodGenerate(snake, map);
    while (true) {
        checkSankeMove(snake, map);
        checkChangeDir(snake);

        if (!checkOutOfMap(snake)) {
            break;
        }

//        checkFoodGenerate(snake, map);
        checkEatFood(snake, map, snake.snake[0]);

    }
    std::string gameOverMessage = "gameOver!!! score=" + std::to_string(snake.sankeLen);
    drawUnit({W / 2 - 10, H / 2}, gameOverMessage.c_str());
    cin >> ws;
    return 0;
}
