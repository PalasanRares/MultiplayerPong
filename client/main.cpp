#include "SDL2/SDL.h"
#include "SDL2/SDL_image.h"

#include <iostream>

enum {LOGO = 0, MIDDLE_LINE = 1, PONG_PLAYER = 2, BALL = 3, START_BUTTON = 4};

typedef struct Player {
    int x;
    int y;
    SDL_Rect collisionBox;
    SDL_Texture* texture;

    Player(int x, int y, SDL_Texture* texture) : x(x), y(y), texture(texture) {
        collisionBox.x = x;
        collisionBox.y = y;
        collisionBox.w = 32;
        collisionBox.h = 128;
    }

} Player;

typedef struct Ball {
    int x;
    int y;
    SDL_Rect collisionBox;
    SDL_Texture* texture;

    Ball(SDL_Texture* texture) : x(468), y(218), texture(texture) {
        collisionBox.x = 468;
        collisionBox.y = 218;
        collisionBox.w = 64;
        collisionBox.h = 64;
    }

} Ball;

void initializeWindowRenderer(SDL_Window* &window, SDL_Renderer* &renderer) {
    window = SDL_CreateWindow("Pong", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 1000, 500, 0);
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
}

void renderMainMenu(SDL_Renderer* renderer, SDL_Texture** textures) {
    SDL_Rect logoDest; logoDest.x = 372; logoDest.y = 25; logoDest.w = 256; logoDest.h = 64;
    SDL_Rect middleLineDest; middleLineDest.x = 484; middleLineDest.y = 0; middleLineDest.w = 32; middleLineDest.h = 500;
    SDL_Rect playerDest1; playerDest1.x = 0; playerDest1.y = 186; playerDest1.w = 32; playerDest1.h = 128;
    SDL_Rect playerDest2; playerDest2.x = 968; playerDest2.y = 186; playerDest2.w = 32; playerDest2.h = 128;
    SDL_Rect ballDest; ballDest.x = 468; ballDest.y = 218; ballDest.w = 64; ballDest.h = 64;
    SDL_Rect startButtonDest; startButtonDest.x = 436; startButtonDest.y = 300; startButtonDest.w = 128; startButtonDest.h = 64;

    SDL_SetRenderDrawColor(renderer, 64, 64, 64, 255);
    SDL_RenderClear(renderer);
    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
    SDL_RenderCopy(renderer, textures[MIDDLE_LINE], nullptr, &middleLineDest);
    SDL_RenderCopy(renderer, textures[LOGO], nullptr, &logoDest);
    SDL_RenderCopy(renderer, textures[PONG_PLAYER], nullptr, &playerDest1);
    SDL_RenderCopy(renderer, textures[PONG_PLAYER], nullptr, &playerDest2);
    SDL_RenderCopy(renderer, textures[BALL], nullptr, &ballDest);
    SDL_RenderCopy(renderer, textures[START_BUTTON], nullptr, &startButtonDest);
    SDL_RenderPresent(renderer);

}

void loadTextures(SDL_Texture** &textures, SDL_Renderer* renderer) {
    textures[LOGO] = IMG_LoadTexture(renderer, "./assets/PongLogo.png");
    textures[MIDDLE_LINE] = IMG_LoadTexture(renderer, "./assets/MiddleLine.png");
    textures[PONG_PLAYER] = IMG_LoadTexture(renderer, "./assets/PongPlayer.png");
    textures[BALL] = IMG_LoadTexture(renderer, "./assets/Ball.png");
    textures[START_BUTTON] = IMG_LoadTexture(renderer, "./assets/StartButton.png");

}

void destroyTextures(SDL_Texture** textures) {
    SDL_DestroyTexture(textures[LOGO]);
    SDL_DestroyTexture(textures[MIDDLE_LINE]);
    SDL_DestroyTexture(textures[PONG_PLAYER]);
    SDL_DestroyTexture(textures[BALL]);

}

int main() {
    SDL_Init(SDL_INIT_VIDEO);
    IMG_Init(IMG_INIT_PNG);

    SDL_Window* window = nullptr;
    SDL_Renderer* renderer = nullptr;
    initializeWindowRenderer(window, renderer);

    SDL_Texture** textures = new SDL_Texture*[10];
    loadTextures(textures, renderer);

    bool running = true;

    int time = SDL_GetTicks();
    while (running) {
        SDL_Event event;
        if (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    running = false;
                    break;
            }
        }

        renderMainMenu(renderer, textures);

        if ((SDL_GetTicks() - time) < 10) {
            SDL_Delay(10);
            time = SDL_GetTicks();
        }

    }

    destroyTextures(textures);
    SDL_DestroyWindow(window);
    SDL_DestroyRenderer(renderer);
    SDL_Quit();

    return 0;

}