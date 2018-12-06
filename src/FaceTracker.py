
class FaceTracker(object):
    def __init__(self, robot):
        self.tracker = robot.session.service("ALTracker")

    def start_face_tracking(self):
        self.tracker.registerTarget("Face", 0.1)
        self.tracker.track("Face")

    def stop_face_tracking(self):
        # Stop tracker.
        self.tracker.stopTracker()
        self.tracker.unregisterAllTargets()

    def move_to_target(self):
        self.tracker.setMode("Move")
        #return self.tracker.getTargetPosition()
