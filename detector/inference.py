import numpy as np

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]["index"]
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image


def analyze_image(interpreter, image):
    set_input_tensor(interpreter, image)

    interpreter.invoke()
    output_details = interpreter.get_output_details()
    print(output_details)
    print("-----output location-----")
    output_location = np.squeeze(interpreter.get_tensor(output_details[0]["index"]))
    print(output_location[:6])
    print("----output category------")
    output_category = np.squeeze(interpreter.get_tensor(output_details[1]["index"]))
    print(output_category)
    print("----output score------")
    output_score = np.squeeze(interpreter.get_tensor(output_details[2]["index"]))
    print(output_score)
    print("----output number of detections------")
    output_freq = np.squeeze(interpreter.get_tensor(output_details[3]["index"]))
    print(output_freq)

    # scale, zero_point = output_details["quantization"]
    # output = scale * (output - zero_point)

    return [output_location, output_category, output_score, output_freq]