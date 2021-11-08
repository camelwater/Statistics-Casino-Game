import pygame
from pygame_widgets.button import Button
from operator import sub
import random as rd
from Deck import Deck
from Card import Card, Color
from utils import *

pygame.init()
pygame.display.init()
pygame.font.init()
SCR_WIDTH = 1400
SCR_HEIGHT = 750

SURFACE = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption("Casino Game")
BOLD_FONT = pygame.font.SysFont('Segoe UI', 20, True)
BOLD_FONT_MASS = pygame.font.SysFont('Segoe UI', 50, True)
NORMAL_FONT = pygame.font.SysFont("Segoe UI", 20, False)
EPSILON = 10**-8

total_winnings = 0

rules_button = None
start_button = None
get_rand_num_button = None
draw_cards_button = None
quit_button = None
retry_button = None
back_button = None
next_button = None
red_button = None
blue_button = None

COLOR = None
extra_deck = Deck(extra=True)
rules = False
start_done = False
rand_number = None
randomization_factor = None
rand_done = False
cards_drawn = None
done_drawing = False
card_list = list()
card_buttons = list()
chosen_card = None
added = False

def create_button(text, x, y, w, h, color=None, fontSize = None, clickable = True, radius=20, border = 0, textColor = (0,0,0)):
    color = color or (150, 150, 150)
    if clickable:
        button = Button(
            SURFACE, x, y, w, h,
            text=text, fontSize = min(int(w//((len(text)+EPSILON)/(2))), int(w/5)), margin=25, 
            colour = color,
            hoverColour = tuple(map(sub, color, (25, 25, 25))),
            radius = radius,
            borderThickness = border,
            borderColour = (255,255,255)
        )
    else:
        font_size = min(int(w//((len(text)+EPSILON)/(2))), int(w/5)) if fontSize is None else fontSize
        button = Button(
            SURFACE, x, y, w, h,
            text=text, fontSize = font_size, margin=25, 
            textColour = textColor,
            colour = color,
            radius = radius,
            borderThickness = border,
            borderColour = (255,255,255)

        )
    return button

def determine_cards():
    global card_list, randomization_factor
    card_list = list()

    for i in range(6):
        card = Card(COLOR, i)
        if COLOR == Color.BLUE:
            card.alter_odds(randomization_factor)
        card_list.append(card)
        
   
def paint_card(events, card):
    x_fac, y_fac, x_s, y_s = card.get_coords()
    card_button = create_button("", x = (SCR_WIDTH-x_s)*x_fac, y = (SCR_HEIGHT-y_s)*y_fac, w = x_s, h = y_s, color = card.get_color_tuple(), radius = 7, border=1)
    # card_buttons.append(card_button)
    card.button = card_button
    card_button.listen(events)
    card_button.draw()

def get_rect(button: Button) -> pygame.Rect:
    return pygame.Rect(button.getX(), button.getY(), button.getWidth(), button.getHeight())

def determine_screen():
    if rules:
        return "rules"
    if not start_done:
        return "start"
    elif not rand_done:
        return "number"
    elif not done_drawing:
        return "draw"
    elif not chosen_card:
        return "card"
    else:
        return "end"

def start_mouseHandler(pos):
    global rules, start_done
    if get_rect(rules_button).collidepoint(pos):
        rules = True
    elif get_rect(start_button).collidepoint(pos):
        start_done = True

def rules_mouseHandler(pos):
    global rules
    
    if get_rect(back_button).collidepoint(pos):
        rules = False

def draw_cards_mouseHandler(pos):
    global cards_drawn, done_drawing, draw_cards_button

    if COLOR == Color.RED and rand_number == 0:
        if get_rect(next_button).collidepoint(pos):
            done_drawing = True
    elif not cards_drawn:
        if COLOR == Color.RED:
            if get_rect(draw_cards_button).collidepoint(pos):
                extra_deck.shuffle()
                cards_drawn = list()
                for i in range(rand_number):
                    cards_drawn.append(extra_deck.pop())

        elif COLOR == Color.BLUE:
            if get_rect(next_button).collidepoint(pos):
                done_drawing = True
    else:
        if get_rect(next_button).collidepoint(pos):
            done_drawing = True

def game_screen_mouseHandler(pos):
    global chosen_card
    card_vector = [get_rect(card.button).collidepoint(pos) for card in card_list]
    if any(card_vector):
        index_clicked = card_vector.index(True)
        chosen_card = card_list[index_clicked]

def end_mouseHandler(pos):
    if get_rect(retry_button).collidepoint(pos):
        reset_vars()
    elif get_rect(quit_button).collidepoint(pos):
        pygame.quit()
        exit()

def number_mouseHandler(pos):
    global rand_number, rand_done, COLOR
    if get_rect(red_button).collidepoint(pos):
        COLOR = Color.RED
    elif get_rect(blue_button).collidepoint(pos):
        COLOR = Color.BLUE

    if not rand_number:
        if get_rect(get_rand_num_button).collidepoint(pos):
            rand_number = rd.randint(0, 5)
    else:
        if get_rect(next_button).collidepoint(pos) and COLOR is not None:
            rand_done = True

def calculate_randomization_factor():
    global randomization_factor
    if rand_number == 0:
        randomization_factor = .5
    else:
        randomization_factor = rand_number/(0.5*rand_number + 0.5)

def mouseHandler(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN: #clicked on some node
            if event.button == 1: #left click (set starting node)
                screen = determine_screen()
                if screen == "start":
                    start_mouseHandler(pygame.mouse.get_pos())
                elif screen == "rules":
                    rules_mouseHandler(pygame.mouse.get_pos())
                elif screen == "number":
                    number_mouseHandler(pygame.mouse.get_pos())
                elif screen == "draw":
                    draw_cards_mouseHandler(pygame.mouse.get_pos())
                elif screen == "card":
                    game_screen_mouseHandler(pygame.mouse.get_pos())
                elif screen == "end":
                    end_mouseHandler(pygame.mouse.get_pos())

def paint_start(events):
    global rules_button, start_button
    title_text = BOLD_FONT_MASS.render('RYAN\'S CASINO GAME', True, (255, 255, 255))
    SURFACE.blit(title_text, ((SCR_WIDTH-title_text.get_width())/2, (SCR_HEIGHT-title_text.get_height())*1/6))

    rules_button = create_button("HOW TO PLAY", x = (SCR_WIDTH-150)/2, y = (SCR_HEIGHT-80)/2, w = 150, h = 80)
    rules_button.listen(events)
    rules_button.draw()

    start_button = create_button("START", x = (SCR_WIDTH-225)/2, y = (SCR_HEIGHT-100)*4/5, w = 225, h = 100)
    start_button.listen(events)
    start_button.draw()


def paint_number(events):
    global get_rand_num_button, next_button, red_button, blue_button

    blue_button = create_button("BLUE", x = (SCR_WIDTH-200)*1/4, y = (SCR_HEIGHT-100)/5, w = 200, h = 100, color = (45, 45, 227) if COLOR == Color.BLUE else None)
    red_button = create_button("RED", x = (SCR_WIDTH-200)*3/4, y = (SCR_HEIGHT-100)/5, w = 200, h = 100, color = (224, 49, 70) if COLOR == Color.RED else None)
    blue_button.listen(events)
    blue_button.draw()
    red_button.listen(events)
    red_button.draw()

    num_text = BOLD_FONT.render("Random number:", True, (255, 255, 255))
    number = BOLD_FONT_MASS.render(str(rand_number) if rand_number else '?', True, (255,255,255))
    SURFACE.blit(num_text, ((SCR_WIDTH-num_text.get_width())/2, (SCR_HEIGHT-num_text.get_height())*2/5))
    SURFACE.blit(number, ((SCR_WIDTH-number.get_width())/2, (SCR_HEIGHT-number.get_height())/2))

    if not rand_number:
        
        get_rand_num_button = create_button("GET NUMBER", x = (SCR_WIDTH-150)/2, y = (SCR_HEIGHT-65)*2/3, w = 150, h = 65)
        get_rand_num_button.listen(events)
        get_rand_num_button.draw()
    else:   
        next_button = create_button("NEXT", x = (SCR_WIDTH-150)/2, y = (SCR_HEIGHT-100)*6/7, w = 150, h = 100)

        if COLOR:
            next_button.listen(events)
            next_button.draw()


def paint_rules(events):
    global back_button
    title_text = BOLD_FONT_MASS.render('RULES/INFO', True, (255, 255, 255))
    SURFACE.blit(title_text, ((SCR_WIDTH-title_text.get_width())/2, (SCR_HEIGHT-title_text.get_height())*1/10))

    back_button = create_button("BACK", x = (SCR_WIDTH-150)/2, y = (SCR_HEIGHT-80)*9/10, w = 125, h = 65)
    back_button.listen(events)
    back_button.draw()

def paint_drawing_screen(events):
    global draw_cards_button, done_drawing
    if COLOR == Color.RED:
        if rand_number == 0:
            message = BOLD_FONT.render(f'No cards drawn.', True, (255, 255, 255))
            SURFACE.blit(message, ((SCR_WIDTH-message.get_width())/2, (SCR_HEIGHT-message.get_height())/5))
            next_button.listen(events)
            next_button.draw()
            determine_cards()

        elif not cards_drawn:
            for c, card in enumerate(extra_deck.getDeck()):
                card = create_button("", (SCR_WIDTH-175)/2 + 2*c,(SCR_HEIGHT-250)*2/3 + 2*c, 175, 250, (244, 49, 70), clickable = False, radius=7, border=1)
                card.draw()

            message = BOLD_FONT.render(f"Draw {rand_number} card{'' if rand_number==1 else 's'}:", True, (255, 255, 255))
            SURFACE.blit(message, ((SCR_WIDTH-message.get_width())/2, (SCR_HEIGHT-message.get_height())/5))
            draw_cards_button = create_button("DRAW", (SCR_WIDTH-150)/2,(SCR_HEIGHT-60)/3, 150, 60)
            draw_cards_button.listen(events)
            draw_cards_button.draw()

        else: 
            for c, card in enumerate(cards_drawn):
                card = create_button("", (SCR_WIDTH-175)*((c+1)/(len(cards_drawn)+1)),(SCR_HEIGHT-250)/2, 175, 250, (244, 49, 70), clickable = False, radius=7, border=1)
                card.draw()
            message = BOLD_FONT.render(f'{rand_number} card{"s" if len(cards_drawn)!=1 else ""} drawn:', True, (255, 255, 255))
            SURFACE.blit(message, ((SCR_WIDTH-message.get_width())/2, (SCR_HEIGHT-message.get_height())/5))
            next_button.listen(events)
            next_button.draw()
            determine_cards()
            card_list.extend(cards_drawn)

    elif COLOR == Color.BLUE:
        calculate_randomization_factor()
        message = BOLD_FONT_MASS.render(f'+- multiplied by {randomization_factor:.2f}', True, (255, 255, 255))
        SURFACE.blit(message, ((SCR_WIDTH-message.get_width())/2, (SCR_HEIGHT-message.get_height())/2))
        next_button.listen(events)
        next_button.draw()
        determine_cards()


def paint_card_screen(events):
    title = BOLD_FONT_MASS.render("PICK A CARD:", True, (255,255,255))
    SURFACE.blit(title, ((SCR_WIDTH-title.get_width())/2, (SCR_HEIGHT-title.get_height())/25))

    rd.shuffle(card_list)
    for i, card in enumerate(card_list):
        card.id = i
        card.determine_coords()
        paint_card(events, card)
    

def paint_end_screen(events):
    global total_winnings, added, retry_button, quit_button

    title = BOLD_FONT_MASS.render("CHOSEN CARD", True, (255, 255,255))
    SURFACE.blit(title, ((SCR_WIDTH-title.get_width())/2, (SCR_HEIGHT-title.get_height())/25))

    winnings = chosen_card.getValue()
    if not added:
        total_winnings+=winnings
        added = True

    total_winnings_color = (79, 194, 131) if total_winnings>=0 else (235, 45, 65)
    total_winnings_text = BOLD_FONT.render(f"Total Winnings: {'+' if total_winnings>=0 else ''}{total_winnings:.2f}", True, total_winnings_color)
    SURFACE.blit(total_winnings_text, ((SCR_WIDTH-total_winnings_text.get_width())/2, (SCR_HEIGHT-total_winnings_text.get_height())/6))

    color = (79, 194, 131) if winnings>=0 else (235, 45, 65)
    if chosen_card.color == Color.RED:
        if winnings<0: color = (255,255,255)

    card = create_button(f"{'+' if winnings>=0 else ''}{winnings:.2f}", (SCR_WIDTH-215)/2, (SCR_HEIGHT-350)/2, 215, 350, color = chosen_card.get_color_tuple(), fontSize=50, clickable=False, radius=5, border=1, textColor = color)
    card.draw()

    retry_button = create_button("RETRY", (SCR_WIDTH-130)/2, (SCR_HEIGHT-60)*6/7, 130, 60)
    quit_button = create_button("QUIT", (SCR_WIDTH-130)/2, (SCR_HEIGHT-60)*24/25, 130, 60)
    retry_button.listen(events)
    quit_button.listen(events)
    retry_button.draw()
    quit_button.draw()

def reset_vars():
    global COLOR, extra_deck, rules, start_done, rand_number, randomization_factor, \
    rand_done, cards_drawn, done_drawing, card_list, chosen_card, added

    COLOR = None
    extra_deck = Deck(extra=True)
    rules = False
    start_done = True
    rand_number = None
    randomization_factor = None
    rand_done = False
    cards_drawn = None
    done_drawing = False
    card_list = list()
    chosen_card = None
    added=False

def updateScreen(events):
    mouseHandler(events)

    screen = determine_screen()
    SURFACE.fill((0,0,0))

    if screen == "start":
        paint_start(events)
    elif screen == "rules":
        paint_rules(events)
    elif screen == "number":
        paint_number(events)
    elif screen == "draw":
        paint_drawing_screen(events)
    elif screen == "card":
        paint_card_screen(events)
    elif screen == "end":
        paint_end_screen(events)
    
    pygame.display.update()

def graphics():
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        updateScreen(events)

def simulation():
    global COLOR, extra_deck, chosen_card, card_list, rand_number
    # EXPECTED_VALUE = -5.46
    # extra_deck = Deck(extra=True)
    experimental_val = 0
    experimental_vals = list()
    blue_vals = list()
    red_vals = list()
    deck_values = 0
    card_values = 0
    lengths = 0
    iterations = 1000000

    for n in range(iterations):
        # print(f"iter {n+1}", end='\r')
        extra_deck = Deck(extra=True)

        COLOR = rd.choice([Color.RED, Color.BLUE])
        # COLOR = Color.BLUE
        # COLOR = Color.RED
        rand_number = rd.randint(0, 5)

        if COLOR == Color.RED:
            extra_deck.shuffle()
            extra = [extra_deck.pop() for _ in range(rand_number)]
            # extra = [extra_deck.getDeck()[i] for i in range(rand_number)]
            # extra = list()
            # for i in range(rand_number):
            #     extra.append(rd.choice(extra_deck.getDeck()))
            deck_values += sum([card.getValue() for card in extra])
            determine_cards()
            card_list.extend(extra)

        else:
            calculate_randomization_factor()
            determine_cards()

        # lengths += len(card_list)
        # deck_values+=sum([card.getValue() for card in card_list])
        chosen_card = rd.choice(card_list)

        card_val = chosen_card.getValue()
        experimental_val+=card_val
        experimental_vals.append(card_val)
        if COLOR == Color.RED:
            red_vals.append(card_val)
        else:
            blue_vals.append(card_val)
        
    expected_val = experimental_val/iterations
    red_ex = sum(red_vals)/len(red_vals)
    blue_ex = sum(blue_vals)/len(blue_vals)
    print(f"\nRED mean:{red_ex:.5f}")
    print(f"RED variance: {calculate_variance(red_vals, red_ex):.5f}")
    print(f"RED std dev: {calculate_std_dev(red_vals, red_ex):.5f}")

    print(f"\nBLUE mean: {blue_ex:.5f}")
    print(f"BLUE variance: {calculate_variance(blue_vals, blue_ex):.5f}")
    print(f"BLUE std dev: {calculate_std_dev(blue_vals, blue_ex):.5f}")

    print(f'\n----------------\nMean: {expected_val:.5f}')
    print("Variance: {:.5f}".format(calculate_variance(experimental_vals, expected_val)))
    print(f"STD DEV: {calculate_std_dev(experimental_vals, expected_val):.5f}")
    

if __name__ == "__main__":
    # graphics()

    simulation()