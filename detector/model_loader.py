import tflite_runtime.interpreter as tflite

def load(model_path):
    interpreter = tflite.Interpreter(model_path)
    print("Model loaded.")
    return interpreter