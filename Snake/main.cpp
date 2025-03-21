///c++
#include <iostream>
#include <Windows.h>
#include <conio.h>

using namespace std;

// ������Ϸ��ͼ�Ŀ�Ⱥ͸߶�
const int W = 50;
const int H = 28;

// ���巽�����ͣ����л�ʳ��
enum BlockType {
    EMPTY = 0,
    FOOD = 1,
};

// �����ͼ�ṹ�壬���ڴ洢��ͼ��Ϣ
struct Map {
    BlockType data[H][W];
    bool hasFood = false;
};

// �����ṹ�壬���ڱ�ʾ����λ��
struct Point {
    int x;
    int y;
};

// �����߽ṹ�壬���ڴ洢�ߵ������Ϣ
struct Snake {
    Point snake[H * W];
    int sankeDir;
    int sankeLen;
    int lastMoveTime = 0;
    int moveFrequer = 200;
};

// �����ĸ����������仯
const int direction[4][2] = {
        {0,  -1}, // ��
        {1,  0}, // ��
        {0,  1}, // ��
        {-1, 0}, // ��
};

// ���ع�꺯��
void hideCursor() {
    HANDLE hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO cursorInfo = {1, false};
    SetConsoleCursorInfo(hOutput, &cursorInfo);
}

// ������������ƽ̨��
void clearScreen() {
#ifdef _WIN32
    system("cls"); // Windows ϵͳ
#else
    cout << "\033[2J\033[1;1H"; // Linux/Mac ϵͳ
#endif
}

// ���ƶ����͵ײ��߿�
void drawBorder(int width) {
    cout << "[";
    for (int i = 0; i < width; ++i) {
        cout << "-";
    }
    cout << "]" << endl;
}

// �����м�����
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

// �����ƺ���
void drawMap(Map map) {
    if (W <= 0 || H <= 0) {
        cerr << "Width and Height must be positive integers." << endl;
        return;
    }

    clearScreen(); // ����
    drawBorder(W); // ���ƶ����߿�
    drawContent(H, W, map); // �����м�����
    drawBorder(W); // ���Ƶײ��߿�
}

// ��ʼ����ͼ
void initMap(Map &map) {
    for (int i = 0; i < H; i++) {
        for (int j = 0; j < W; ++j) {
            map.data[i][j] = BlockType::EMPTY;
        }
    }
    map.hasFood = false;
}

// ��ʼ����
void initSnake(Snake &snake) {
    snake.sankeLen = 3;
    snake.sankeDir = 1;
    snake.snake[0] = {8, 8};
    snake.snake[1] = {8, 9};
    snake.snake[2] = {8, 10};
}

// ���Ƶ�Ԫ��
void drawUnit(Point point, const char unit[]) {
    COORD coord;
    HANDLE hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    coord.X = point.x + 1;
    coord.Y = point.y + 1;

    SetConsoleCursorPosition(hOutput, coord);
    cout << unit;
}

// ������
void drawSnake(Snake snake) {
    for (int i = 0; i < snake.sankeLen; ++i) {
        drawUnit(snake.snake[i], "#");
    }
}

// ��鲢�ı��ߵķ���
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

// �ƶ���
void moveSnake(Snake &snake) {
    for (int i = snake.sankeLen - 1; i > 0; --i) {
        snake.snake[i] = snake.snake[i - 1];
    }
    snake.snake[0].x += direction[snake.sankeDir][0];
    snake.snake[0].y += direction[snake.sankeDir][1];
}

// ִ���ƶ��ߵĲ���
void doMove(Snake &snake) {
    Point tail = snake.snake[snake.sankeLen - 1];
    drawUnit(tail, " ");
    moveSnake(snake);
    drawUnit(snake.snake[0], "#");
}

// ����ߵ��ƶ�������
void checkSankeMove(Snake &snake, Map map) {
    int curTime = GetTickCount();
    if (curTime - snake.lastMoveTime > snake.moveFrequer) {
        doMove(snake);
        snake.lastMoveTime = curTime;
    }
}

// ���ʳ�������
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

// ������Ƿ񳬳���ͼ�߽�
bool checkOutOfMap(Snake &snake) {
    if (snake.snake[0].x < 0 || snake.snake[0].x >= W || snake.snake[0].y < 0 || snake.snake[0].y >= H) {
        return false;
    } else {
        return true;
    }
}

// ������Ƿ�Ե�ʳ��
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

// ��ʼ����Ϸ
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
