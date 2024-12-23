class Strategy:
    NOOP = 0
    ACCELERATE = 1
    DECELERATE = 2
    TURN_LEFT = 3
    TURN_RIGHT = 4
    GO_STRAIGHT = 5
    FIRE_AMMO = 6

    def __init__(self):
        pass

    def decision(
            self,
            seq: int,
            jetfighter_info: dict,
            propfighter_info: dict,
            obstacle_info: dict,
            bullet_info: list
    ):
        """
        Make strategic decisions for the jetfighter based on the current game state.

        Args:
            seq (int): The sequence number of the clock tick of the game.
                        Ticks have a 25ms interval between them. The tick number starts from 0.
                        It is possible that the method is called with a non-consecutive tick number
                        from the previous call, when the previous call took longer than the tick
                        interval to generate a decision. In this case, some cycles will be skipped,
                        and the tick sequence counter increases without invoking the call to this method.

            jetfighter_info (dict): A dictionary containing information about the jetfighter with the following keys:
                - x (float): The current on-screen x-coordinate of the jetfighter, representing its center.
                - y (float): The current on-screen y-coordinate of the jetfighter, representing its center.
                - heading (float): The current heading direction of the jetfighter, measured in degrees from the y-axis clockwise.
                                   For example, if the fighter is heading upward, heading is 0; if heading to the left, heading is 270.
                                   The heading value ranges from 0 to 359.
                - turning (int): Indicates the turning state of the jetfighter.
                                 0 if not turning, 1 if making a clockwise turn, -1 if making a counterclockwise turn.
                - curr_speed (float): The current speed of the jetfighter, in pixels per second.
                - top_speed (float): The maximum possible speed of the jetfighter, a constant value.
                - min_speed (float): The minimum possible speed of the jetfighter without stalling, a constant value.
                - curr_ammo (int): The amount of ammo currently available to the jetfighter.
                - max_ammo (int): The maximum amount of ammo the jetfighter can carry.
                                   Ammo regeneration will halt when max_ammo is reached, a constant value.
                - ammo_regen_time (int): The time in seconds before a new ammo can be regenerated, a constant value.
                - ammo_fire_delay (float): The cooldown in seconds between firing two bullets, a constant value.

            propfighter_info (dict): A dictionary containing information about the propfighter with the following keys:
                - x (float): The current on-screen x-coordinate of the propfighter, representing its center.
                - y (float): The current on-screen y-coordinate of the propfighter, representing its center.
                - heading (float): The current heading direction of the propfighter, measured in degrees from the y-axis clockwise.
                - turning (int): Indicates the turning state of the propfighter.
                                 0 if not turning, 1 if making a clockwise turn, -1 if making a counterclockwise turn.
                - curr_speed (float): The current speed of the propfighter, in pixels per second.
                - top_speed (float): The maximum possible speed of the propfighter, a constant value.
                - min_speed (float): The minimum possible speed of the propfighter without stalling, a constant value.

            obstacle_info (dict): A dictionary containing information about obstacles in the game with the following keys:
                - x (float): The x-coordinate of the top-left corner of the obstacle rectangle.
                - y (float): The y-coordinate of the top-left corner of the obstacle rectangle.
                - width (float): The width of the obstacle rectangle.
                - height (float): The height of the obstacle rectangle.
                Note: These values are constant, as the obstacle does not move.

            bullet_info (list): A list of dictionaries representing information about all the flying bullets.
                                Each bullet is a dictionary with the following keys:
                - x (float): The x-coordinate of the bullet's center.
                - y (float): The y-coordinate of the bullet's center.
                             Each bullet is a rectangle of 20 pixels in length and 3 pixels in width,
                             and can be rotated to its current heading.
                - heading (float): The current heading direction of the bullet, measured in degrees from the y-axis clockwise.
                - speed (float): The speed of the bullet in its traveling direction, in pixels per second.
                - distance_traveled (float): The distance this bullet has traveled since being fired.
                                             Once it reaches its max_distance, it will disappear.
                - max_distance (float): The maximum distance the bullet can travel before being neutralized (disappear), a constant value.

        Returns:
            int: The method should return one of the following values:
                - Strategy.NOOP: Do nothing, i.e., no change to the jetfighter's operation.
                - Strategy.ACCELERATE: Accelerate the jetfighter by the jetfighter's acceleration amount of speed.
                - Strategy.DECELERATE: Decelerate the jetfighter by the jetfighter's acceleration amount of speed.
                - Strategy.TURN_LEFT: Initiate a counterclockwise turn.
                - Strategy.TURN_RIGHT: Initiate a clockwise turn.
                - Strategy.GO_STRAIGHT: Stop any turning, if applicable, and make the jetfighter start to go straight.
                - Strategy.FIRE_AMMO: Fire an ammo from the jetfighter, if conditions allow, such as there being enough ammo,
                                      and the ammo firing delay has been reached since the previous firing.
                                      Otherwise, ammo will not fire.
        """
        return Strategy.NOOP
