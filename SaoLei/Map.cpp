#include "Map.h"
#include <SFML/Graphics.hpp>
#include "const.h"
using namespace sf;


void Map::init(RenderWindow* win, Sprite* sprite) {
	pwin = win;
	psprite = sprite;
	initGame();

}


void Map::handleMouseEvent(const std::optional<sf::Event> & event, int x, int y) {
	if (x < 1 || x > MAP_COL || y < 1 || y > MAP_ROW) {
		return; // 超出边界，直接返回
	}
	if (event->is<sf::Event::MouseButtonPressed>()) {
		const auto& mouseButtonEvent = event->getIf<sf::Event::MouseButtonPressed>();
		if (mouseButtonEvent->button == sf::Mouse::Button::Left)
		{
			//std::cout << "Left mouse button pressed.\n";
			grid[x][y].ShowGrid();
			grid[x][y].doLeftClick();
		}
		else if (mouseButtonEvent->button == sf::Mouse::Button::Right)
		{
			if (grid[x][y].GetShowGridType() == GridType::GT_FLAG) {
				grid[x][y].SetShowGridType(GridType::GT_HIDE);
			}
			else {
				grid[x][y].SetShowGridType(GridType::GT_FLAG);
			}
			//std::cout << "Right mouse button pressed.\n";
			 // = GridType::GT_FLAG;
		}
	}
}
void Map::draw(int x, int y) {


		psprite->setScale(sf::Vector2f(GRID_SIZE * 1.0 / ORI_GRID_SIZE, GRID_SIZE * 1.0 / ORI_GRID_SIZE));

		for (int i = 1; i <= MAP_COL; ++i) {
			for (int j = 1; j <= MAP_ROW; ++j)
			{
				if (grid[x][y].isShow() && grid[x][y].IsRealBomb()) {
					grid[i][j].ShowGrid();
				}

				psprite->setTextureRect(
					IntRect(
						Vector2(ORI_GRID_SIZE * grid[i][j].GetShowGridType(), 0),
						Vector2(ORI_GRID_SIZE, ORI_GRID_SIZE)));
				psprite->setPosition(sf::Vector2f(i * GRID_SIZE, j * GRID_SIZE));
				pwin->draw(*psprite);
			}
		}
	}


void Map::initGame() {
	for (int i = 1; i <= MAP_COL; ++i) {
		for (int j = 1; j <= MAP_ROW; ++j) {
			//showGrid[i][j] = GridType::GT_HIDE;
			grid[i][j].SetShowGridType(GridType::GT_HIDE);
			if (rand() % 6 == 0) {
				grid[i][j].SetRealGridType( GridType::GT_BOMB);
			}
			else {
				grid[i][j].SetRealGridType( GridType::GT_EMPTY);
			}
		}
	}

	for (int i = 1; i <= MAP_COL; ++i) {
		for (int j = 1; j <= MAP_ROW; ++j) {
			if (grid[i][j].IsEmpty()) {
				int cnt = 0;
				for (int k = 0; k < 8; ++k) {
					int ti = i + DIR[k][0];
					int tj = j + DIR[k][1];
					if (grid[ti][tj].IsRealBomb()) {
						++cnt;
					}
				}
				grid[i][j].SetRealGridType( GridType(cnt));
			}
		}
	}

}


