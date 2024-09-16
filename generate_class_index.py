import json
from torchvision.models import ResNet50_Weights

def generate_class_index():
    weights = ResNet50_Weights.DEFAULT
    class_idx = weights.meta["categories"]
    class_index = {str(i): [f"n{i:08d}", name] for i, name in enumerate(class_idx)}
    
    with open('model/imagenet_class_index.json', 'w') as f:
        json.dump(class_index, f, indent=4)

if __name__ == "__main__":
    generate_class_index()
    print("Complete imagenet_class_index.json file has been generated.")
