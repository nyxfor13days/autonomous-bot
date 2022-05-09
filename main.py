from math import cos, sin, pi, floor
import pygame
from rplidar import RPLidar, RPLidarException


class App:
    def __init__(self):
        # Initializing the App
        pygame.init()
        self.window = pygame.display.set_mode(320, 240)
        pygame.mouse.set.visible(False)
        self.window.fill((0, 0, 0))
        pygame.display.update()

    def process_data(self, data):
        max_distance = 0

        for angle in range(360):
            distance = data[angle]

            if distance > 0:
                max_distance = max([min([5000, distance]), max_distance])
                radians = angle * pi/180.0
                x = distance * cos(radians)
                y = distance * sin(radians)
                point = (160 + int(x / max_distance * 119),
                         120 + int(y / max_distance * 119))
                self.windowset_at(point, pygame.Color(255, 255, 255))

        pygame.display.update()


if __name__ == "__main__":
    main = App()
    lidar = RPLidar('/dev/ttyUSB0')

    scan_data = [0]*360

    try:
        for quality, angle, distance in enumerate(lidar.ter_measures()):
            scan_data[min([359, floor(angle)])] = distance

        main.process_data(scan_data)

    except KeyboardInterrupt:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

    except RPLidarException as e:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        print("[!] RPLidar Exception: {0}".format(e))

    except AttributeError as e:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        print("[!] AttributeError : {0}".format(e))
