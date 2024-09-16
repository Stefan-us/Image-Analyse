import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, vgg16, inception_v3, ResNet50_Weights, VGG16_Weights, Inception_V3_Weights
from PIL import Image
import json
import os

class ImageClassifier:
    def __init__(self, model_name='resnet50'):
        self.model_name = model_name
        if model_name == 'resnet50':
            self.weights = ResNet50_Weights.DEFAULT
            self.model = resnet50(weights=self.weights)
        elif model_name == 'vgg16':
            self.weights = VGG16_Weights.DEFAULT
            self.model = vgg16(weights=self.weights)
        elif model_name == 'inception_v3':
            self.weights = Inception_V3_Weights.DEFAULT
            self.model = inception_v3(weights=self.weights)
        else:
            raise ValueError(f"Unsupported model: {model_name}")

        self.model.eval()
        self.transform = self.weights.transforms()
        
        # Load the class index file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', 'model', 'imagenet_class_index.json')
        try:
            with open(json_path) as f:
                self.class_index = json.load(f)
            print(f"Successfully loaded class index from {json_path}")
            print(f"Number of classes loaded: {len(self.class_index)}")
            print(f"Sample classes: {dict(list(self.class_index.items())[:5])}")
            print(f"Keys range: {min(self.class_index.keys())} to {max(self.class_index.keys())}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading class index file: {e}")
            print(f"Attempted to load from: {json_path}")
            raise

    def predict(self, image_path):
        print(f"Attempting to predict image at path: {image_path}")
        print(f"Image file exists: {os.path.exists(image_path)}")
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0)
        
        with torch.no_grad():
            outputs = self.model(image)
        
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        top5_prob, top5_catid = torch.topk(probabilities, 5)
        
        results = []
        for i in range(top5_prob.size(0)):
            cat_id = top5_catid[i].item()
            prob = top5_prob[i].item()
            class_name = self.class_index[str(cat_id)][1]
            results.append((class_name, prob))
        
        print(f"Top 5 predictions: {results}")
        return results[0][0], results[0][1]  # Return the top class name and its probability

classifiers = {
    'resnet50': lambda: ImageClassifier('resnet50'),
    'vgg16': lambda: ImageClassifier('vgg16'),
    'inception_v3': lambda: ImageClassifier('inception_v3')
}
