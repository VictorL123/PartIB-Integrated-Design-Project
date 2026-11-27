from robot import Robot
from utime import ticks_ms, sleep_ms, ticks_diff
from config import BASE_SPEED, SPIN_SPEED

def test_drive():
    robot = Robot()
    # t0 = ticks_ms()
    # print("reversing")
    # while ticks_diff(ticks_ms(), t0) < 5000: 
    #     robot.follower.stepreverse(BASE_SPEED)
    # sleep_ms(1000)
    while robot.sensors.at_junction() == False:
        robot.follower.step(BASE_SPEED) # forward
    print("attempting left halfspin")
    robot.follower.turn("LEFT", SPIN_SPEED, polarity="N")
     # left halfspin
    while robot.sensors.at_junction() == False:
            robot.follower.step(BASE_SPEED) # forward MANUALLY TURN AROUND
    print("attempting right halfspin")
    robot.follower.turn("RIGHT", SPIN_SPEED, polarity="N") # right halfspin

    # while robot.sensors.at_junction() != True:
    #     robot.follower.step(BASE_SPEED)

    # robot.follower.turn("RIGHT", SPIN_SPEED)

    # t0 = ticks_ms()
    # while ticks_diff(ticks_ms(), t0) < 1000:
    #     robot.follower.step(BASE_SPEED)

    # while robot.sensors.at_junction() != True:
    #     robot.follower.reverse(BASE_SPEED)

    
    # robot.follower.turn("LEFT", SPIN_SPEED)

    # t0 = ticks_ms()
    # while ticks_diff(ticks_ms(), t0) < 1000:
    #     robot.follower.step(BASE_SPEED)
    
    # robot.drive.stop()
    # print("stopped")


if __name__ == "__main__":
    test_drive()

    
    
# from map import table
# from navigation import Route
# import time

# route = Route()

# route.location = "rack_L_low"
# route.lastlocation = "rack_L_low"

# for i in range(10):
#     if route.arrived() != True:
#         # print(route.peek_next_move())
#         time.sleep(1)
#         route.next_move()
#         print(len(route._plan))
#     else:
#         print("arrived!")
#         print(route.location, route.lastlocation)
#         if route.location == "START":
#             if route.nextlocation != "None": # need to check if there's not more to do:
                
#                 print(f"routing to {route.nextlocation}")
#                 route.plan_to(route.nextlocation)
#                 route.nextlocation = "None"
#         else: 
#             route.plan_to("deposit_R1")
#         print(route._plan)



# print("arrived!")
# print(route.location, route.lastlocation)


# for i in range(5, 9):
#     # cycle through the first dictionary entries for racks
#     # not looking at where is next closest!!
#     val = list(table.values())[i]
#     if val == "UNSEARCHED":
#         route.plan_to(list(table)[i])
#         print(route._plan)
#         planned = True
#         break

