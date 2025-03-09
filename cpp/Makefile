all:
	g++ -c particules.cpp -o main.o
	g++ main.o -o sfml-app -lsfml-graphics -lsfml-window -lsfml-system && ./sfml-app

clean:
	$(RM) main.o
	$(RM) sfml-app 
