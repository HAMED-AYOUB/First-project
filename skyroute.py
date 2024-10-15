dirfrom graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

# Build your program below:
landmark_string = ""
for letter, landmark in landmark_choices.items():
    landmark_string += "{0} - {1}\n".format(letter, landmark)

stations_under_construction = ['Lansdowne','Olympic Village']

def greet():
    print("Hi there and welcome to SkyRoute!")
    print("We'll help you find the shortest route between the following Vancouver landmarks:\n" + landmark_string)

def set_start_and_end(start_point, end_point):
    if start_point is not None:
        change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': ")
        if change_point == "b":
            start_point = get_start()
            end_point = get_end()
        elif change_point == "o":
            start_point = get_start()
        elif change_point == "d":
            end_point = get_end()
        else:
            print("Oops, that isn't 'o', 'd', or 'b'...")
            return set_start_and_end(start_point, end_point)
    else:
        start_point = get_start()
        end_point = get_end()
    return start_point, end_point


def get_start():
    start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
    if start_point_letter in landmark_choices:
        start_point = landmark_choices[start_point_letter]
        return start_point
    else:
        print("Sorry, that's not a landmark we have data on. Let's try this again...")
        return get_start()


def get_end():
    end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
    if end_point_letter in landmark_choices:
        end_point = landmark_choices[end_point_letter]
        return end_point
    else:
        print("Sorry, that's not a landmark we have data on. Let's try this again...")
        return get_end()


def new_route(start_point=None, end_point=None):
    start_point, end_point = set_start_and_end(start_point, end_point)
    shortest_route_string = get_route(start_point, end_point)
    if shortest_route_string:
        print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
    else:
        print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
    
    again = input("Would you like to see another route? Enter y/n: ")
    if again == "y":
        show_landmarks()
        new_route(start_point, end_point)


def show_landmarks():
    see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")
    if see_landmarks == "y":
        print(landmark_string)



def get_route(start_point, end_point):
    start_stations = vc_landmarks[start_point]
    end_stations = vc_landmarks[end_point]
    routes = []
    
    for start_station in start_stations:
        for end_station in end_stations:
            metro_system = get_active_stations() if stations_under_construction else vc_metro
            
            if stations_under_construction:
                possible_route = dfs(metro_system, start_station, end_station)
                if not possible_route:
                    continue
            
            route = bfs(metro_system, start_station, end_station)
            if route:
                routes.append(route)
    
    if routes:
        shortest_route = min(routes, key=len)
        shortest_route_string = '\n'.join(shortest_route)
        return shortest_route_string
    else:
        return None



def get_active_stations():
    updated_metro = vc_metro.copy()
    
    for station_under_construction in stations_under_construction:
        for current_station, neighboring_stations in vc_metro.items():
            if current_station != station_under_construction:
                updated_metro[current_station] -= set(stations_under_construction)
            else:
                updated_metro[current_station] = set([])

    return updated_metro



def update_stations_under_construction():
    action = input("Would you like to add or remove a station from the construction list? (add/remove): ")
    station = input("Enter the station name: ")
    if action == "add":
        if station not in stations_under_construction:
            stations_under_construction.append(station)
            print(f"{station} has been added to the construction list.")
        else:
            print(f"{station} is already in the construction list.")
    elif action == "remove":
        if station in stations_under_construction:
            stations_under_construction.remove(station)
            print(f"{station} has been removed from the construction list.")
        else:
            print(f"{station} is not in the construction list.")
    else:
        print("Invalid action. Please enter 'add' or 'remove'.")




def goodbye():
    print("Thanks for using SkyRoute!")



def skyroute():
    greet()
    update_stations_under_construction()
    new_route()
    goodbye()

skyroute()

