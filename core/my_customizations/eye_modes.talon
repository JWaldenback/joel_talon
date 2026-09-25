gaze mode:
    user.enable_gaze_control()

no eye tracker mode:
    user.enable_no_eye_tracker_mode()

hiss mode:
    user.enable_hiss_control()

^use both eyes$:
    user.set_eye_tracking_mask("both")

^use only left eye$:
    user.set_eye_tracking_mask("left")

^use only right eye$:
    user.set_eye_tracking_mask("right")
