#include <iostream>
#include <SFML/Graphics.hpp>
#include "main.h"
#include "const.h"
#include "Map.h"

using namespace sf;
// 中文乱码



int main() {
	const std::basic_string windowTitle = L"扫雷";
	// 使用 sf::VideoMode 和 sf::WindowStyle 创建窗口
	sf::RenderWindow win(
		sf::VideoMode(sf::Vector2(windowWidth, windowHeight), pix),
		windowTitle,
		sf::Style::Default
	);
	// 加载纹理
	sf::Texture t;
	if (!t.loadFromFile("mine.png")) {
		// 如果纹理加载失败，输出错误信息并退出
		std::cerr << "Failed to load texture!" << std::endl;
		return -1;
	}

	Map mapD;
	// 创建精灵并绑定纹理
	sf::Sprite s(t);

	Grid grid[MAP_COL + 1][MAP_ROW + 1];
	mapD.init(&win, &s);

	sf::Clock clock;
	const sf::Time timePerFrame = sf::seconds(1.f / 30.f); // 限制为每秒 60 帧

	win.setFramerateLimit(60); // 限制为每秒 60 帧
	win.setVerticalSyncEnabled(true); // 启用垂直同步
	while (win.isOpen()) {
		sf::Time elapsedTime = clock.restart(); // 获取上一帧的时间
		sf::Vector2i pos = sf::Mouse::getPosition(win);
		int x = pos.x / GRID_SIZE;
		int y = pos.y / GRID_SIZE;
		std::cout << "鼠标位置" << x << ":" << y << std::endl;
		while (const std::optional event = win.pollEvent()) {
			if (event->is<sf::Event::Closed>())
			{
				std::cout << "按下关闭按钮" << std::endl;
				win.close();
			}
			mapD.handleMouseEvent(event, x, y);
		}	
		win.clear(); // 清空窗口
		mapD.draw(x, y);
		win.display();
		sf::sleep(timePerFrame - clock.getElapsedTime()); // 限制帧率
	}
	return 0;
}