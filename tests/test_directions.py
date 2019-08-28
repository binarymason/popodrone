from flight_model import fmodel

def test_flight_directions(box, center_of_frame_coordinates, expected_result):
    adjustments = get_adjustments(box, center_of_frame_coordinates)
    directions = determine_flight_directions(adjustments)

    test_directions = []
    for direction in directions:
        if direction == "":
            test_directions.append(direction)
        else:
            test_directions.append(direction[0])


        if test_directions != expected_result:
            print("FAIL")
            print("Expected:", expected_result)
            print("Got:", test_directions)
            exit(1)
        else:
            print("OK")
            
print("##################### RUNNING TESTS")
center_of_frame_coordinates = [256, 256]

print("# test x axis")
THRESHOLD_Z_PERCENT = .2 
box = {
    "centroid_x": 233,
    "centroid_y": center_of_frame_coordinates[1],
    "width": 50,
    "height": (center_of_frame_coordinates[1] * 2) * THRESHOLD_Z_PERCENT
}
expected_result = ["move_left", "", ""]
test_flight_directions(box, center_of_frame_coordinates, expected_result)

box["centroid_x"] = 257
expected_result = ["move_right", "", ""]
test_flight_directions(box, center_of_frame_coordinates, expected_result)

box["centroid_x"] = center_of_frame_coordinates[0]
expected_result = ["", "", ""]
test_flight_directions(box, center_of_frame_coordinates, expected_result)


print("# test y axis")
box["centroid_y"] = 257
expected_result = ["", "move_down", ""]
test_flight_directions(box, center_of_frame_coordinates, expected_result)

box["centroid_y"] = 254
expected_result = ["", "move_up", ""]
test_flight_directions(box, center_of_frame_coordinates, expected_result)


print("# test z axis")
box = {
    "centroid_x": center_of_frame_coordinates[0],
    "centroid_y": center_of_frame_coordinates[1],
    "width": 50,
    "height": (center_of_frame_coordinates[1]*2) * .25
}
    
expected_result = ["", "", ""]
test_flight_directions(box, center_of_frame_coordinates, expected_result)

box["height"] = (center_of_frame_coordinates[1]*2) * .26
expected_result = ["", "", "move_backward"]
test_flight_directions(box, center_of_frame_coordinates, expected_result)

box["height"] = (center_of_frame_coordinates[1]*2) * .24
expected_result = ["", "", "move_forward"]
test_flight_directions(box, center_of_frame_coordinates, expected_result)