#include <SFML/Graphics.hpp>
#include <cmath>
#define WIDTH 1920*3/4
#define HEIGHT 1080*3/4
#define GMb 10000000.0

class ParticleSystem : public sf::Drawable, public sf::Transformable{

public:
    ParticleSystem(unsigned int count) : m_particles(count), m_vertices(sf::Points, count), m_lifetime(sf::seconds(3.f)), m_emitter(0.f, 0.f){}

    void setEmitter(sf::Vector2f position){
        m_emitter = position;
    }

    void update(sf::Time elapsed) {
        for (std::size_t i = 0; i < m_particles.size(); ++i) 
            updateParticle(m_particles[i],i,elapsed);
    }

    void reset(){
        for(int i = 0; i < m_particles.size(); i++)
            resetParticle(i);
    }

private:
    virtual void draw(sf::RenderTarget& target, sf::RenderStates states) const{
        states.transform *= getTransform();
        states.texture = NULL;
        target.draw(m_vertices, states);
    }


    struct Particle {
        sf::Vector2f velocity;
        sf::Time lifetime;
    };

    void resetParticle(std::size_t index) {
        float angle = (std::rand() % 360) * 3.14f / 180.f;
        float speed = (std::rand() % 50) + 200.f;
        m_particles[index].velocity = sf::Vector2f(cos(angle) * speed, sin(angle) * speed);
        m_particles[index].lifetime = sf::milliseconds((std::rand() % 2000) + 1000);

        m_vertices[index].position = m_emitter;
    }




    void updateParticle(Particle& p, std::size_t i, sf::Time elapsed){

        m_vertices[i].position += p.velocity * elapsed.asSeconds();
        // acceleration gravitationelle vers le centre
        sf::Vector2f delta = sf::Vector2f((float) WIDTH/2, (float) HEIGHT/2)
            - m_vertices[i].position;
        sf::Vector2f u;
        float length2 = (delta.x * delta.x) + (delta.y * delta.y);
        if (length2 != 0)
            u = sf::Vector2f(delta.x / sqrt(length2), delta.y / sqrt(length2));
        else
            u = delta;
        p.velocity += u*elapsed.asSeconds()*(float)GMb/length2;
        //p.velocity *= 0.9f;

        if (p.lifetime <= sf::Time::Zero || length2 < 10 || length2 > HEIGHT*WIDTH)
            resetParticle(i);

    }


    std::vector<Particle> m_particles;
    sf::VertexArray m_vertices;
    sf::Time m_lifetime;
    sf::Vector2f m_emitter;
};


int main(){
    sf::ContextSettings settings;
    settings.antialiasingLevel = 8;

    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "SFML Particles", sf::Style::Default, settings);
    window.setFramerateLimit(60);

    ParticleSystem particles(1000);
    sf::Clock clock;

    // define a 120x50 rectangle
    sf::RectangleShape rectangle(sf::Vector2f(WIDTH,HEIGHT));
    rectangle.setFillColor(sf::Color(0,0,0,30));

    sf::CircleShape center(10);
    center.setFillColor(sf::Color::White);
    center.setPosition(WIDTH/2-5,HEIGHT/2-5);


    while (window.isOpen()){
        sf::Event event;
        while (window.pollEvent(event))
            switch (event.type){
                case sf::Event::Closed:
                    window.close();
                    break;

                case sf::Event::KeyPressed:
                    if (event.key.code == sf::Keyboard::Escape
                            || event.key.code == sf::Keyboard::Q)
                        window.close();
                    else if(event.key.code == sf::Keyboard::Space)
                        particles.reset();
                    break;

                default:
                    break;
            }


        sf::Vector2i mouse = sf::Mouse::getPosition(window);
        sf::Time elapsed = clock.restart();

        particles.setEmitter(window.mapPixelToCoords(mouse));
        particles.update(elapsed);
        window.draw(rectangle);
        window.draw(center);
        window.draw(particles);
        window.display();
    }

    return 0;
}

