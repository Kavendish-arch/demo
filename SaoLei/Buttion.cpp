//#include "Buttion.h"
//Button::Button(const std::string& text, const sf::Font& font, const sf::Vector2f& position, const sf::Vector2f& size)
//        {
//    text = text;
//
//        m_rect.setPosition(position);
//        m_rect.setFillColor(sf::Color::Green);
//        m_rect.setOutlineThickness(2);
//        m_rect.setOutlineColor(sf::Color::Black);
//
//        m_text.setPosition(position.x + 10, position.y + 10);
//        m_text.setFillColor(sf::Color::White);
//    }
//
//void Button:: draw(sf::RenderWindow& window) const {
//    window.draw(m_rect);
//    window.draw(m_text);
//}
//
//bool Button::isClicked(const sf::Vector2i& mousePos) const {
//    return m_rect.getGlobalBounds().contains(mousePos.x, mousePos.y);
//}
//
