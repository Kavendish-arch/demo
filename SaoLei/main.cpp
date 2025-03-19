#include <iostream>
#include <SFML/Graphics.hpp>
#include "main.h"
#include "const.h"
#include "Map.h"

using namespace sf;
// ��������



int main() {
	const std::basic_string windowTitle = L"ɨ��";
	// ʹ�� sf::VideoMode �� sf::WindowStyle ��������
	sf::RenderWindow win(
		sf::VideoMode(sf::Vector2(windowWidth, windowHeight), pix),
		windowTitle,
		sf::Style::Default
	);
	// ��������
	sf::Texture t;
	if (!t.loadFromFile("mine.png")) {
		// ����������ʧ�ܣ����������Ϣ���˳�
		std::cerr << "Failed to load texture!" << std::endl;
		return -1;
	}

	Map mapD;
	// �������鲢������
	sf::Sprite s(t);

	Grid grid[MAP_COL + 1][MAP_ROW + 1];
	mapD.init(&win, &s);

	sf::Clock clock;
	const sf::Time timePerFrame = sf::seconds(1.f / 30.f); // ����Ϊÿ�� 60 ֡

	win.setFramerateLimit(60); // ����Ϊÿ�� 60 ֡
	win.setVerticalSyncEnabled(true); // ���ô�ֱͬ��
	while (win.isOpen()) {
		sf::Time elapsedTime = clock.restart(); // ��ȡ��һ֡��ʱ��
		sf::Vector2i pos = sf::Mouse::getPosition(win);
		int x = pos.x / GRID_SIZE;
		int y = pos.y / GRID_SIZE;
		std::cout << "���λ��" << x << ":" << y << std::endl;
		while (const std::optional event = win.pollEvent()) {
			if (event->is<sf::Event::Closed>())
			{
				std::cout << "���¹رհ�ť" << std::endl;
				win.close();
			}
			mapD.handleMouseEvent(event, x, y);
		}	
		win.clear(); // ��մ���
		mapD.draw(x, y);
		win.display();
		sf::sleep(timePerFrame - clock.getElapsedTime()); // ����֡��
	}
	return 0;
}