import socket, threading, json, ast, sys, time
import pygame, time
import camera, car, maps, bullet, gui
#graphical variables
pygame.init()
infoObject = pygame.display.Info()
display_width = infoObject.current_w
display_height = infoObject.current_h
#display_width = 700
#display_height = 500
center_w = display_width // 2
center_h = display_height // 2
gameDisplay = pygame.display.set_mode((display_width, display_height),pygame.FULLSCREEN)
pygame.display.set_caption = ('CarBattle')
pygame.display.iconify
clock = pygame.time.Clock()
#colors
white   = (255,255,255)
yellow   = (240,240,120)
black   = (  0,  0,  0)
background = pygame.Surface(gameDisplay.get_size())
background = background.convert_alpha()
background.fill(black)
#stuff for buttons
button_width = 120
button_height = 50
button_interval = display_height // 8
button_begin_y = display_height // 3


#logo
logo_image = pygame.transform.scale(pygame.image.load("media/images/logo.png"), [display_width // 2, display_height // 4])
rules_image = pygame.image.load("media/images/rules.png")

#global sockets
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

exception_caught = False
disconnected_caught = False

#server variables
server_running = False
server_global_data = {
    "game_status" : "wait",
    "players" : {
    },
    "names" : {
    },
    "bullets" : [],
    "status" : {}
}
players_controls = {

}
#client variables
client_running = False
client_data = {
    "name" : "",
    "controls" : []
}
client_global_data = {
    "game_status" : "wait",
    "players" : {
    },
    "names" : {
    },
    "bullets" : [],
    "status" : {}
}

bullets_obj = []
bullets_draw_obj = []

bull_timeout = 20

num_of_lifes = 5

#car_type, health, x,y, angle
start_values = {
    "1" : ["yellow",num_of_lifes,600,400,180,bull_timeout],
    "2" : ["red",num_of_lifes,1540,330,180,bull_timeout],
    "3" : ["blue",num_of_lifes,1710,1880,90,bull_timeout],
    "4" : ["green",num_of_lifes,160,1850,0,bull_timeout]
}

car_yellow = car.Car(start_values["1"][0],start_values["1"][1],start_values["1"][2],start_values["1"][3],start_values["1"][4],start_values["1"][5])
car_red = car.Car(start_values["2"][0],start_values["2"][1],start_values["2"][2],start_values["2"][3],start_values["2"][4],start_values["2"][5])
car_blue = car.Car(start_values["3"][0],start_values["3"][1],start_values["3"][2],start_values["3"][3],start_values["3"][4],start_values["3"][5])
car_green = car.Car(start_values["4"][0],start_values["4"][1],start_values["4"][2],start_values["4"][3],start_values["4"][4],start_values["4"][5])

cars_obj = {}

car_draw_obj = {}

user_number = 0
dead_players = []
disconnected_players = []

#objects for graphics
game_map = maps.Map('media/maps/full.png',0,0)
game_map_s = pygame.sprite.Group()
game_map_s.add(game_map)

collision_map = maps.Map('media/maps/blocks.png',0,0)
collision_map_s = pygame.sprite.Group()
collision_map_s.add(collision_map)

victory_sound = pygame.mixer.Sound("media/music/victory.wav")
lose_sound = pygame.mixer.Sound("media/music/lose.wav")
button_sound = pygame.mixer.Sound("media/music/button.wav")
music_stopped = True

rules_read = False

with open('config/config.json','r') as json_file:
    config = json.load(json_file)
    client_data["name"] = config["name"]
ip_to_connect = ""

def init_vars():
    global server_global_data
    global client_global_data
    global bullets_obj
    global bullets_draw_obj
    global players_controls
    global client_data
    global car_yellow
    global car_red
    global car_blue
    global car_green
    global cars_obj
    global car_draw_obj
    global user_number
    global dead_players
    global disconnected_players
    global rules_read
    rules_read = False

    user_number = 0
    dead_players = []
    disconnected_players = []

    server_global_data = {
        "game_status" : "wait",
        "players" : {
        },
        "names" : {
        },
        "bullets" : [],
        "status" : {}
    }
    add_user(config["ip"],config["name"])

    players_controls = {}
    client_data = {
        "name" : "",
        "controls" : []
    }
    client_global_data = {
        "game_status" : "wait",
        "players" : {
        },
        "names" : {
        },
        "bullets" : [],
        "status" : {}
    }
    bullets_obj = []
    bullets_draw_obj = []

    car_yellow = car.Car(start_values["1"][0],start_values["1"][1],start_values["1"][2],start_values["1"][3],start_values["1"][4],start_values["1"][5])
    car_red = car.Car(start_values["2"][0],start_values["2"][1],start_values["2"][2],start_values["2"][3],start_values["2"][4],start_values["2"][5])
    car_blue = car.Car(start_values["3"][0],start_values["3"][1],start_values["3"][2],start_values["3"][3],start_values["3"][4],start_values["3"][5])
    car_green = car.Car(start_values["4"][0],start_values["4"][1],start_values["4"][2],start_values["4"][3],start_values["4"][4],start_values["4"][5])

    cars_obj = {}

    car_draw_obj = {}

def get_button_size(str_value):
    smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',42)
    rendered_text_button1 = smallfont.render(str_value, True, black)
    return rendered_text_button1.get_width(), rendered_text_button1.get_height()
def button(message, x, y, w, h, ic, ac):
    pressed = False
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',42)
        if click[0] == 1:
            pygame.mixer.Sound.play(button_sound)
            pressed = True
        rendered_text_button1 = smallfont.render(message, True, ac)
    else:
        smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',40)
        rendered_text_button1 = smallfont.render(message, True, ic)
    gameDisplay.blit(rendered_text_button1, [x + w / 2 - rendered_text_button1.get_rect().width / 2, y + h / 2 - rendered_text_button1.get_rect().height / 2])
    return pressed

# ----------------SERVER--------------------------

def add_user(ip,name = None):
    global server_data
    global user_number
    global cars_sprites
    global server_global_data
    user_number += 1
    server_global_data["players"][ip] = start_values[str(user_number)]
    server_global_data["status"][ip] = "connected"
    if name != None:
        server_global_data["names"][ip] = name

def remove_user(ip):
    global server_global_data
    global car_draw_obj
    global cars_obj
    global disconnected_players
    if server_global_data["players"][ip][0] not in disconnected_players:
        disconnected_players.append(server_global_data["players"][ip][0])
    server_global_data["status"][ip] = "disconnected"

def new_client(clientsocket,addr):
    global server_global_data
    global players_controls
    add_user(addr[0])
    while True:
        #recieving data from client
        try:
            msg = clientsocket.recv(1024)
        except ConnectionResetError:
            #delete client from client listen
            #and if the game is in progress then delete his car and
            remove_user(addr[0])
            return 0
        get_data =  msg.decode('utf-8')
        try:
            get_data = ast.literal_eval(get_data)
            server_global_data["names"][addr[0]] = get_data["name"]
        except:
            remove_user(addr[0])
        players_controls[addr[0]] = get_data
        #sending back global data
        send_data = str(server_global_data)
        try:
            clientsocket.send(send_data.encode('utf-8'))
        except:
            remove_user(addr[0])
    clientsocket.close()
def server():
    global sock_server
    global exception_caught
    global server_running
    host = config["ip"]
    port = 8888
    print('Server started. Host : ', host,', Port : ',port)
    print('Waiting for clients...')
    try:
        sock_server.bind((host, port))
        sock_server.listen(4)
    except:
        server_running = False
        exception_caught = True
        return 0

    #check if this works
    add_user(config["ip"],config["name"])
    while True:
        try:
            c, addr = sock_server.accept()
        except:
            return 0
        server_thread = threading.Thread(target=new_client,args=(c,addr))
        server_thread.daemon = True
        server_thread.start()
# ----------------CLIENT--------------------------
def client():
    global sock_client
    global client_global_data
    global client_data
    global exception_caught
    global client_running
    global disconnected_caught
    client = ip_to_connect
    port = 8888
    try:
        sock_client.connect((client,port))
    except:
        client_running = False
        exception_caught = True
        return 0
    print('Client started. Connected to host : ', client,', Port : ',port)
    while True:
        #sending local data to server
        send_data = str(client_data)
        try:
            sock_client.send(send_data.encode('utf-8'))
        except:
            client_running = False
            disconnected_caught = True
            return 0
        #getting data from server
        try:
            msg = sock_client.recv(1024)
        except:
            client_running = False
            disconnected_caught = True
            return 0
        get_data =  msg.decode('utf-8')
        try:
            get_data = ast.literal_eval(get_data)
        except:
            client_running = False
            disconnected_caught = True
            return 0
        client_global_data = get_data
    sock_client.close()
#-----------------WAITING ROOMS-------------------------
def server_room():
    global server_running
    if server_running == False:
        server_running = True
        t_server = threading.Thread(target=server)
        t_server.start()
    else:
        init_vars()
    draw_room_gui('server')

def client_room():
    global client_running
    if client_running == False:
        client_running = True
        t_client = threading.Thread(target=client)
        t_client.start()
    draw_room_gui('client')

def connect_to_room():
    connect_gui()

def game(user):
    global server_global_data
    global client_data
    global players_controls
    global car_draw_obj
    global cars_obj
    global bullets_obj
    global bullets_draw_obj
    global dead_players
    global disconnected_players
    global disconnected_caught
    global music_stopped
    global rules_read

    user_gui = gui.GameGUI(gameDisplay)
    pygame.mixer.music.load("media/music/main_theme.wav")
    pygame.mixer.music.play(-1)
    music_stopped = False

    if user == "server":
        players_ip = server_global_data["players"].keys()
    else:
        players_ip = client_global_data["players"].keys()

    for player_ip in players_ip:
        if user == "server":
            player_lst = list(server_global_data["players"][player_ip])
            player_name = server_global_data["names"][player_ip]
            player_status = server_global_data["status"][player_ip]
        else:
            player_lst = list(client_global_data["players"][player_ip])
            player_name = client_global_data["names"][player_ip]
            player_status = client_global_data["status"][player_ip]
        if player_ip == config["ip"]:
            client_car_color = player_lst[0]

        if player_lst[0] == "yellow":
            car_draw_yellow = car.CarDraw("yellow",player_name,player_lst[1],player_lst[2],player_lst[3],player_lst[4],player_status)
            car_draw_obj["yellow"] = car_draw_yellow
            cars_obj["yellow"] = car_yellow
        if player_lst[0] == "red":
            car_draw_red = car.CarDraw("red",player_name,player_lst[1],player_lst[2],player_lst[3],player_lst[4],player_status)
            car_draw_obj["red"] = car_draw_red
            cars_obj["red"] = car_red
        if player_lst[0] == "blue":
            car_draw_blue = car.CarDraw("blue",player_name,player_lst[1],player_lst[2],player_lst[3],player_lst[4],player_status)
            car_draw_obj["blue"] = car_draw_blue
            cars_obj["blue"] = car_blue
        if player_lst[0] == "green":
            car_draw_green = car.CarDraw("green",player_name,player_lst[1],player_lst[2],player_lst[3],player_lst[4],player_status)
            car_draw_obj["green"] = car_draw_green
            cars_obj["green"] = car_green
    #setting camera on client
    cam = camera.Camera(gameDisplay,car_draw_obj[client_car_color].x - center_w,car_draw_obj[client_car_color].y - center_h)
    cam_x = cam.x
    cam_y = cam.y
    #checking on x
    if (car_draw_obj[client_car_color].x - center_w > 0) and (car_draw_obj[client_car_color].x + center_w < game_map.map_width):
        cam_x = car_draw_obj[client_car_color].x - center_w
    else :
        if (car_draw_obj[client_car_color].x + center_w >= game_map.map_width):
            cam_x = game_map.map_width - display_width
        if (car_draw_obj[client_car_color].x + center_w < display_width):
            cam_x = 0
    #checking on y
    if (car_draw_obj[client_car_color].y - center_h > 0) and (car_draw_obj[client_car_color].y + center_h < game_map.map_height):
        cam_y = car_draw_obj[client_car_color].y - center_h
    else :
        if (car_draw_obj[client_car_color].y + center_h >= game_map.map_height):
            cam_y = game_map.map_height - display_height
        if (car_draw_obj[client_car_color].y + center_h < display_height):
            cam_y = 0
    #creating camera
    cam = camera.Camera(gameDisplay,cam_x,cam_y)
    while True:
        if user == "client":
            if disconnected_caught == True:
                disconnected_caught = False
                error_gui("CONNECTION LOST")
        if user == "server":
            players_ip = server_global_data["players"].keys()
        else:
            players_ip = client_global_data["players"].keys()

        for player_ip in players_ip:
            if user == "server":
                player_lst = list(server_global_data["players"][player_ip])
                player_status = server_global_data["status"][player_ip]
            else:
                player_lst = list(client_global_data["players"][player_ip])
                player_status = client_global_data["status"][player_ip]
            car_draw_obj[player_lst[0]].update(player_lst[1],player_lst[2],player_lst[3],player_lst[4],player_status)
        if user == "server":
            bullets_draw_obj = server_global_data["bullets"]
        else:
            bullets_draw_obj = client_global_data["bullets"]

        #Check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        if rules_read == True:
            #Check for key input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if not ("left" in client_data["controls"]):
                    client_data["controls"].append("left")
            else:
                if "left" in client_data["controls"]:
                    client_data["controls"].remove("left")
            if keys[pygame.K_RIGHT]:
                if not ("right" in client_data["controls"]):
                    client_data["controls"].append("right")
            else:
                if "right" in client_data["controls"]:
                    client_data["controls"].remove("right")
            if keys[pygame.K_UP]:
                if not ("up" in client_data["controls"]):
                    client_data["controls"].append("up")
            else:
                if "up" in client_data["controls"]:
                    client_data["controls"].remove("up")
            if keys[pygame.K_DOWN]:
                if not ("down" in client_data["controls"]):
                    client_data["controls"].append("down")
            else:
                if "down" in client_data["controls"]:
                    client_data["controls"].remove("down")
            if keys[pygame.K_a]:
                if not ("a" in client_data["controls"]):
                    client_data["controls"].append("a")
            else:
                if "a" in client_data["controls"]:
                    client_data["controls"].remove("a")


        if user == "server":
            players_controls[config["ip"]] = client_data

        if user == "server":
            keys_ip = server_global_data["players"]
            for key_ip in keys_ip:
                if server_global_data["players"][key_ip][1] == 0:
                    if key_ip not in dead_players:
                        dead_players.append(server_global_data["players"][key_ip][0])

            #обработка всех контролей в массиве players_controls если сервер с учетом коллижинов
            keys_dict = players_controls.keys()
            for key in keys_dict:
                if server_global_data["players"][key][1] != 0 and server_global_data["status"][key] != "disconnected":
                    player_data = players_controls[key]
                    if ("up" in player_data["controls"]) and ("down" not in player_data["controls"]):
                        cars_obj[server_global_data["players"][key][0]].accelerate()
                    if ("down" in player_data["controls"]) and ("up" not in player_data["controls"]):
                        cars_obj[server_global_data["players"][key][0]].deaccelerate()
                    else:
                        cars_obj[server_global_data["players"][key][0]].soften()
                    if ("left" in player_data["controls"]) and ("right" not in player_data["controls"]):
                        cars_obj[server_global_data["players"][key][0]].steerleft()
                    if ("right" in player_data["controls"]) and ("left" not in player_data["controls"]):
                        cars_obj[server_global_data["players"][key][0]].steerright()
                    if ("a" in player_data["controls"]):
                        if cars_obj[server_global_data["players"][key][0]].current_timeout == bull_timeout:
                            new_bullet = bullet.Bullet(cars_obj[server_global_data["players"][key][0]].global_x,cars_obj[server_global_data["players"][key][0]].global_y,cars_obj[server_global_data["players"][key][0]].dir,key)
                            bullets_obj.append(new_bullet)
                            cars_obj[server_global_data["players"][key][0]].current_timeout = bull_timeout-1
                if (server_global_data["players"][key][0] not in dead_players) and (server_global_data["players"][key][0] not in disconnected_players):
                    #Players collision
                    for car_clr in cars_obj:
                        if (car_clr not in dead_players) and (car_clr not in disconnected_players):
                            if car_clr != server_global_data["players"][key][0]:
                                car_s = pygame.sprite.Group()
                                car_s.add(cars_obj[car_clr])

                                if cars_obj[server_global_data["players"][key][0]].check_wall_collide(car_s):
                                    cars_obj[car_clr].backup_position()

                #Wall collision
                if not cars_obj[server_global_data["players"][key][0]].check_wall_collide(collision_map_s):
                    cars_obj[server_global_data["players"][key][0]].update_global()
                cars_obj[server_global_data["players"][key][0]].update()
                n_lst = [server_global_data["players"][key][0],cars_obj[server_global_data["players"][key][0]].health,cars_obj[server_global_data["players"][key][0]].global_x,cars_obj[server_global_data["players"][key][0]].global_y,cars_obj[server_global_data["players"][key][0]].dir]
                server_global_data["players"][key] = n_lst


            server_global_data["bullets"] = []
            for bullet_obj in bullets_obj:
                bullet_obj.update_global()
                bullet_s = pygame.sprite.Group()
                bullet_s.add(bullet_obj)
                for car_clr in cars_obj:
                    if (car_clr not in dead_players) and (car_clr not in disconnected_players):
                        if car_clr != server_global_data["players"][bullet_obj.owner][0]:
                            if cars_obj[car_clr].check_bullet_collide(bullet_s):
                                cars_obj[car_clr].hit()
                                bullets_obj.remove(bullet_obj)
                                continue
                if bullet_obj.check_wall_collide(collision_map_s):
                    bullets_obj.remove(bullet_obj)
                else:
                    bullet_obj.update()
                    server_global_data["bullets"].append([bullet_obj.global_x,bullet_obj.global_y])

        #а теперь мы высчитываем насколько нужно сдвинуть камеру
        cam_x = cam.x
        cam_y = cam.y
        #checking on x
        if (car_draw_obj[client_car_color].x - center_w > 0) and (car_draw_obj[client_car_color].x + center_w < game_map.map_width):
            cam_x = car_draw_obj[client_car_color].x - center_w
            car_draw_obj[client_car_color].x = center_w
        else :
            if (car_draw_obj[client_car_color].x + center_w >= game_map.map_width):
                car_draw_obj[client_car_color].x = (car_draw_obj[client_car_color].x - cam.x)
        #checking on y
        if (car_draw_obj[client_car_color].y - center_h > 0) and (car_draw_obj[client_car_color].y + center_h < game_map.map_height):
            cam_y = car_draw_obj[client_car_color].y - center_h
            car_draw_obj[client_car_color].y = center_h
        else :
            if (car_draw_obj[client_car_color].y + center_h >= game_map.map_height):
                car_draw_obj[client_car_color].y = (car_draw_obj[client_car_color].y - cam.y)
        #updating camera position
        cam.set_pos(cam_x, cam_y)


        #заливка пустым цветом
        gameDisplay.blit(background, (0,0))
        #отрисовываем карту с учетом сдвига камеры
        game_map.update(cam.x,cam.y)
        game_map_s.draw(gameDisplay)

        #drawing bullets
        for bulletXY in bullets_draw_obj:
            bullet_to_draw = bullet.BulletDraw(bulletXY[0],bulletXY[1])
            bullet_to_draw.draw(gameDisplay,-cam_x,-cam_y)
        possible_win = False
        other_possible = False
        #drawing cars
        color_keys = car_draw_obj.keys()
        for color_key in color_keys:
            if car_draw_obj[color_key].health != 0 and car_draw_obj[color_key].status != "disconnected":
                if client_car_color == color_key:
                    possible_win = True
                    car_draw_obj[color_key].draw(gameDisplay)
                else:
                    other_possible = True
                    car_draw_obj[color_key].draw(gameDisplay, -cam.x , -cam.y)

        if (possible_win) and (not other_possible):
            if music_stopped == False:
                music_stopped = True
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(victory_sound)
            #отрисовываем слой 2 : интерфейс
            user_gui.draw(car_draw_obj[client_car_color].health, car_draw_obj[client_car_color].name,"win")
            if button('EXIT', display_width  - get_button_size('EXIT')[0] - 15, display_height - get_button_size('EXIT')[1] - 15 , get_button_size('EXIT')[0], get_button_size('EXIT')[1], white, yellow):
                pygame.mixer.pause()
                break
                #pygame.quit()
                #quit()
        else:
            user_gui.draw(car_draw_obj[client_car_color].health, car_draw_obj[client_car_color].name)
            if car_draw_obj[client_car_color].health == 0:
                if button('EXIT', display_width  - get_button_size('EXIT')[0] - 15, display_height - get_button_size('EXIT')[1] - 15 , get_button_size('EXIT')[0], get_button_size('EXIT')[1], white, yellow):
                    pygame.mixer.pause()
                    break
                    #pygame.quit()
                    #quit()
                if music_stopped == False:
                    music_stopped = True
                    pygame.mixer.music.pause()
                    pygame.mixer.Sound.play(lose_sound)

        if rules_read == False:
            gameDisplay.blit(rules_image, [display_width // 2 - rules_image.get_width() // 2, display_height // 2 - rules_image.get_height() // 2])
            if button('OK AND GO', display_width // 2  - get_button_size('OK AND GO')[0] // 2, display_height // 2 - get_button_size('OK AND GO')[1] // 2 + 110 , get_button_size('OK AND GO')[0], get_button_size('OK AND GO')[1], white, yellow):
                rules_read = True
        #апдейтим экран
        pygame.display.flip()
        #######
        clock.tick(30)

def error_gui(error_str):
    while True:
        #Check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        #Rendering
        gameDisplay.blit(background, (0,0))
        smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',40)
        rendered_text = smallfont.render(error_str, True, yellow)
        gameDisplay.blit(rendered_text, [display_width // 2 - rendered_text.get_width() // 2, display_height // 2 - rendered_text.get_height() // 2])
        if (button('CONTINUE', display_width // 2 - get_button_size('CONTINUE')[0] // 2, button_begin_y + 4 * button_interval, get_button_size('CONTINUE')[0], get_button_size('CONTINUE')[1], white, white)):
            #pygame.quit()
            #quit()
            break
        pygame.display.flip()
        #######
        clock.tick(30)


#--------------------GUI--------------------------------
def connect_gui():
    global ip_to_connect
    while True:
        #Check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    ip_to_connect = ip_to_connect[0:len(ip_to_connect)-1]
                else :
                    ip_to_connect += chr(event.key)
        #Rendering
        gameDisplay.blit(background, (0,0))
        if (button('BACK', display_width // 2 - get_button_size('BACK')[0] - display_width // 8, button_begin_y + 4 * button_interval, get_button_size('BACK')[0], get_button_size('EXIT')[1], white, yellow)):
            #socket closing and stop threads
            return 0
        if (button('CONNECT', display_width // 2 + display_width // 8, button_begin_y + 4 * button_interval, get_button_size('CONNECT')[0], get_button_size('CONNECT')[1], white, white)):
            client_room()
            return 0
        smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',40)
        rendered_text = smallfont.render('ROOM IP : ' + ip_to_connect + '_', True, yellow)
        gameDisplay.blit(rendered_text, [display_width // 2 - rendered_text.get_width() // 2, display_height // 2])
        pygame.display.flip()
        #######
        clock.tick(30)

def draw_room_gui(user):
    global exception_caught
    global disconnected_caught
    while True:
        if user == "server":
            if exception_caught == True:
                error_gui("PORT IS ALREADY IN USE")
                exception_caught = False
                return 0
        else:
            if exception_caught == True:
                error_gui("CONNECTION ERROR")
                exception_caught = False
                return 0
        if disconnected_caught == True:
            error_gui("CONNECTION LOST")
            disconnected_caught = False
            return 0
        if user == "server":
            if server_global_data["game_status"] == "progress":
                game("server")
                break
        else:
            if client_global_data["game_status"] == "progress":
                game("client")
                break
        #Check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        #Rendering
        gameDisplay.blit(background, (0,0))

        smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',40)
        if user == 'server':
            rendered_text = smallfont.render('ROOM ' + config["ip"], True, white)
        else :
            rendered_text = smallfont.render('ROOM ' + ip_to_connect, True, white)
        gameDisplay.blit(rendered_text, [display_width // 2 - rendered_text.get_width() // 2, display_height // 6])
        #list of clients including server one
        if user == 'server':
            name_list = []
            keys = server_global_data["players"].keys()
            for key in keys:
                if server_global_data["status"][key] == "connected":
                    name_keys = server_global_data["names"]
                    if key in name_keys:
                        name_list.append(server_global_data["names"][key])

        else:
            name_list = list(client_global_data["names"].values())
        for i_name in range(len(name_list)):
            rendered_text = smallfont.render(name_list[i_name], True, white)
            gameDisplay.blit(rendered_text, [display_width // 2 - rendered_text.get_width() // 2, display_height // 3 + 50 * i_name])

        if (button('BACK', display_width // 2 - get_button_size('BACK')[0] - display_width // 8, button_begin_y + 4 * button_interval, get_button_size('BACK')[0], get_button_size('EXIT')[1], white, yellow)):
            break
        if user == 'server':
            if (button('START', display_width // 2 + display_width // 8, button_begin_y + 4 * button_interval, get_button_size('START')[0], get_button_size('START')[1], white, yellow)):
                server_global_data["game_status"] = "progress"
        pygame.display.flip()
        #######
        clock.tick(30)
def config_gui():
    global config
    name_str = config['name']
    ip_str = config['ip']
    correcting = '1'
    while True:
        #Check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    if correcting == '1':
                        name_str = name_str[0:len(name_str)-1]
                    else:
                        ip_str = ip_str[0:len(ip_str)-1]
                else :
                    if correcting == '1':
                        name_str += chr(event.key)
                    else:
                        ip_str += chr(event.key)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #Rendering
        gameDisplay.blit(background, (0,0))

        smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',40)
        rendered_text = smallfont.render('CONFIGURATION ', True, white)
        gameDisplay.blit(rendered_text, [display_width // 2 - rendered_text.get_width() // 2, display_height // 6])
        if correcting == '1':
            rendered_text1 = smallfont.render('NAME : ' + name_str + '_', True, yellow)
            rendered_text2 = smallfont.render('YOUR IP : ' + ip_str, True, white)

            if display_width // 2 - rendered_text2.get_width() // 2 < mouse[0] < display_width // 2 + rendered_text2.get_width() // 2 and display_height // 6 + 2 * button_interval < mouse[1] < display_height // 6 + 2 * button_interval + rendered_text2.get_height():
                smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',42)
                if click[0] == 1:
                    correcting = '2'

        else :
            rendered_text1 = smallfont.render('NAME : ' + name_str, True, white)
            rendered_text2 = smallfont.render('YOUR IP : ' + ip_str + '_', True, yellow)

            if display_width // 2 - rendered_text1.get_width() // 2 < mouse[0] < display_width // 2 + rendered_text1.get_width() // 2 and display_height // 6 + button_interval < mouse[1] < display_height // 6 + button_interval + rendered_text1.get_height():
                smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',42)
                if click[0] == 1:
                    correcting = '1'

        gameDisplay.blit(rendered_text1, [display_width // 2 - rendered_text1.get_width() // 2, display_height // 6 + button_interval])
        gameDisplay.blit(rendered_text2, [display_width // 2 - rendered_text2.get_width() // 2, display_height // 6 + 2 * button_interval])


        if (button('BACK', display_width // 2 - get_button_size('BACK')[0] - display_width // 8, button_begin_y + 3 * button_interval, get_button_size('BACK')[0], get_button_size('EXIT')[1], white, yellow)):
            break

        if (button('SAVE and EXIT', display_width // 2 , button_begin_y + 3 * button_interval, get_button_size('SAVE and EXIT')[0], get_button_size('SAVE and EXIT')[1], white, yellow)):
            config = {'name': name_str,'ip': ip_str}
            with open('config/config.json','w') as json_file:
                json.dump(config,json_file)
            #saveing file
            pygame.quit()
            quit()
        pygame.display.flip()
        #######
        clock.tick(30)
#menu gui
while True:
    if music_stopped == True:
        pygame.mixer.music.load("media/music/menu.wav")
        pygame.mixer.music.play(-1)
        music_stopped = False
    #Rendering
    gameDisplay.blit(background, (0,0))

    gameDisplay.blit(logo_image, (display_width // 4, 10))
    #Check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
    if config["name"] != "" and config["ip"] != "":

        if button('CREATE ROOM', display_width // 2 - get_button_size('CREATE ROOM')[0] // 2, button_begin_y, get_button_size('CREATE ROOM')[0], get_button_size('CREATE ROOM')[1], white, yellow):
            server_room()
        if button('CONNECT TO ROOM' , display_width // 2 - get_button_size('CONNECT TO ROOM')[0] // 2, button_begin_y + button_interval, get_button_size('CONNECT TO ROOM')[0], get_button_size('CONNECT TO ROOM')[1], white, yellow):
            connect_to_room()
    else:
        smallfont = pygame.font.Font('media/fonts/pixelfont.ttf',42)
        rendered_text = smallfont.render('SET YOUR CONFIG FIRST', True, white)
        gameDisplay.blit(rendered_text, [display_width // 2 - rendered_text.get_width() // 2, button_begin_y])


    if button('CONFIG' , display_width // 2 - get_button_size('CONFIG')[0] // 2, button_begin_y + 2 * button_interval, get_button_size('CONFIG')[0], get_button_size('CONFIG')[1], white, yellow):
        config_gui()
    if button('EXIT', display_width // 2 - get_button_size('EXIT')[0] // 2, button_begin_y + 3 * button_interval, get_button_size('EXIT')[0], get_button_size('EXIT')[1], white, yellow):
        pygame.quit()
        quit()
    pygame.display.flip()
    #######
    clock.tick(30)
