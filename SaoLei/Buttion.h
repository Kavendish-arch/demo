#pragma once

#include <SFML/Graphics.hpp>
#include <string>

class Button {
public:
    Button(const std::string& text, const sf::Font& font, const sf::Vector2f& position, const sf::Vector2f& size);

    void draw(sf::RenderWindow& window) const;

    bool isClicked(const sf::Vector2i& mousePos) const;
private:
    sf::RectangleShape m_rect;
    sf::Text m_text;
};