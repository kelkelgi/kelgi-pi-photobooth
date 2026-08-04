"""Simple fullscreen display implemented with pygame."""


class Display:
    def __init__(self, width, height):
        try:
            import pygame
        except ImportError as error:
            raise RuntimeError(
                "pygame is not installed. Run: sudo apt install -y python3-pygame"
            ) from error

        self._pygame = pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        self._screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        self._font = pygame.font.Font(None, max(48, min(width, height) // 5))
        self._small_font = pygame.font.Font(None, 48)

    def _text(self, message, font=None):
        font = font or self._font
        surface = font.render(message, True, (255, 255, 255))
        return surface, surface.get_rect(center=self._screen.get_rect().center)

    def _show_message(self, message, detail=None):
        self._screen.fill((20, 20, 20))
        surface, rect = self._text(message)
        self._screen.blit(surface, rect)
        if detail:
            detail_surface, detail_rect = self._text(detail, self._small_font)
            detail_rect.top = rect.bottom + 20
            self._screen.blit(detail_surface, detail_rect)
        self._pygame.display.flip()

    def show_idle(self):
        self._show_message("Ready - press the button")

    def show_countdown(self, frame, number):
        self._show_frame(frame)
        surface, rect = self._text(str(number))
        self._screen.blit(surface, rect)
        self._pygame.display.flip()

    def show_success(self, printed):
        self._show_message("Photo saved" if not printed else "Photo printed")

    def show_error(self, message):
        self._show_message("Could not take photo", message)

    def _show_frame(self, frame):
        surface = self._pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        surface = self._pygame.transform.scale(surface, self._screen.get_size())
        self._screen.blit(surface, (0, 0))

    def should_exit(self):
        for event in self._pygame.event.get():
            if event.type == self._pygame.QUIT:
                return True
            if event.type == self._pygame.KEYDOWN and event.key == self._pygame.K_ESCAPE:
                return True
        return False

    def close(self):
        self._pygame.quit()
