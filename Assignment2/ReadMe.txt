The virtual computers use Pygame 1.9.6 which has bugs for checking the overlap area of masks. I use this overlap to calculate the collision normal to handle collisions. In the older versions the overlap is wrong, which is why the ball goes through the bricks and paddle. The code works as intended on the newer versions.

I have attached a video of the game working correctly, per instructions of Dr. Volonte.


python3 -m pip install -U pygame==2.6.0 installs the newer version that corrects this
