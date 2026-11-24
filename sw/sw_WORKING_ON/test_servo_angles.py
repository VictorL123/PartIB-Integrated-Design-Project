"""test_servo_angles.py - bench test for servo.py (SlowServo) and grabber.py.

BEFORE YOU RUN IT
  * Robot on the bench, gripper clear of blocks, one hand near the power switch.
  * Gripper must physically be at its START positions (vertical 250, horizontal 0),
    or the first command will make it jump.
  * config.py must contain SERVO_HORIZONTAL_PIN and SERVO_VERTICAL_PIN as well as the
    angle constants. Upload config.py, servo.py, grabber.py and this file to the Pico.

WHAT IT CHECKS
  Each move prints the angle reached and whether the move took about as long as
  distance / speed predicts. That checks the CODE. It cannot see the real servo,
  so WATCH THE ROBOT and tick off the "LOOK" lines yourself.
"""
from machine import Pin
from utime import sleep_ms, ticks_ms, ticks_diff
from config import (SERVO_HORIZONTAL_PIN, SERVO_VERTICAL_PIN,
                    SERVO_HOR_START_ANGLE, SERVO_VER_START_ANGLE,
                    VER_BOTTOM_RACK_ANGLE, VER_TOP_ANGLE,
                    HOR_OPEN_ANGLE, HOR_CLOSED_ANGLE, HOR_SPEED_DEG_S, VER_SPEED_DEG_S)
from servo import SlowServo

PAUSE_MS = 2000          # time to look at the robot between moves
results = []             # (name, passed)


def pause(msg=""):
    if msg:
        print("   LOOK:", msg)
    sleep_ms(PAUSE_MS)


def check_angles():
    """All angles must be inside the servo's 0-270 range, or set_angle will clamp them."""
    angles = {
        "SERVO_HOR_START_ANGLE": SERVO_HOR_START_ANGLE,
        "SERVO_VER_START_ANGLE": SERVO_VER_START_ANGLE,
        "VER_BOTTOM_RACK_ANGLE": VER_BOTTOM_RACK_ANGLE,
        "VER_TOP_ANGLE": VER_TOP_ANGLE,
        "HOR_OPEN_ANGLE": HOR_OPEN_ANGLE,
        "HOR_CLOSED_ANGLE": HOR_CLOSED_ANGLE,
    }
    ok = True
    for name, value in angles.items():
        if not 0 <= value <= 270:
            print("BAD:", name, "=", value, "is outside 0-270")
            ok = False
    if HOR_SPEED_DEG_S <= 0:
        print("BAD: SPEED_DEG_S must be above 0 (a speed of 0 would hang move_to)")
        ok = False
    results.append(("config values in range", ok))
    return ok


def timed_move(name, servo, target, speed=HOR_SPEED_DEG_S):
    """Move and report: final angle correct? duration close to distance / speed?"""
    start = servo.angle
    expected_ms = abs(target - start) / speed * 1000
    t0 = ticks_ms()
    servo.move_to(target, speed)
    actual_ms = ticks_diff(ticks_ms(), t0)

    angle_ok = servo.angle == target
    time_ok = abs(actual_ms - expected_ms) <= max(150, 0.2 * expected_ms)
    print("{}: {} -> {} deg | expected {:.0f} ms, took {} ms | angle {} time {}".format(
        name, start, target, expected_ms, actual_ms,
        "OK" if angle_ok else "WRONG", "OK" if time_ok else "OFF"))
    results.append((name, angle_ok and time_ok))


def test_vertical():
    print("\n--- VERTICAL (lift) servo ---")
    lift = SlowServo(Pin(SERVO_VERTICAL_PIN), SERVO_VER_START_ANGLE)
    pause("lift is at its START position (lowest) and has not moved")
    timed_move("lift to bottom-rack height", lift, VER_BOTTOM_RACK_ANGLE)
    pause("small, slow rise. Is this the right height for the LOW rack? (TODO in config)")
    timed_move("lift to top/carry height", lift, VER_TOP_ANGLE)
    pause("higher again. Is this the carry height / top height you intended?")
    timed_move("lift back to start", lift, SERVO_VER_START_ANGLE)
    pause("back at the start, smoothly, no snap")


def test_horizontal():
    print("\n--- HORIZONTAL (grab) servo ---")
    grab = SlowServo(Pin(SERVO_HORIZONTAL_PIN), SERVO_HOR_START_ANGLE)
    pause("gripper is at its START position and has not moved")
    timed_move("grab to closed", grab, HOR_CLOSED_ANGLE)
    pause("gripper CLOSING. Is that the direction you wanted? Does it hit anything?")
    timed_move("grab to open", grab, HOR_OPEN_ANGLE)
    pause("gripper OPENING back to the start")


def test_grabber():
    """Runs the real Grabber methods in the order a pickup would use them."""
    print("\n--- GRABBER class (full pickup sequence) ---")
    from grabber import Grabber           # imported here so a config error shows up clearly
    g = Grabber()

    def show(label):
        print("   {}: vertical {:.0f} deg, horizontal {:.0f} deg".format(
            label, g.servo_vertical.angle, g.horizontal_servo.angle))

    g.open();                      show("open");                      pause()
    g.raise_before_grab("low");    show("raise_before_grab('low')");  pause()
    g.close();                     show("close");                     pause("grip closes")
    g.pick_up();                   show("pick_up");                   pause("lifts to carry height")
    g.lower_to_ground();           show("lower_to_ground");           pause()
    g.open();                      show("open");                      pause()
    g.raise_before_grab("top");    show("raise_before_grab('top')")
    print("   NOTE: if 'top' ends at the same vertical angle as the start, check that in grabber.py")
    pause()
    g.lower_to_ground();           show("lower_to_ground")
    results.append(("grabber sequence ran without error", True))


def summary():
    print("\n=== SUMMARY ===")
    for name, passed in results:
        print(("PASS  " if passed else "FAIL  ") + name)
    print("Remember: PASS only means the code behaved. Your eyes decide if the angles are right.")


def run():
    try:
        if not check_angles():
            return
        test_vertical()
        test_horizontal()
        test_grabber()      # comment this line out if you only want the raw servo tests
    finally:
        summary()


if __name__ == "__main__":
    run()