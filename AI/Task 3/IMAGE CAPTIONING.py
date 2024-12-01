import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image

# Define a custom dataset class
class ImageCaptionDataset(Dataset):
    def __init__(self, image_paths, captions, transform=None):
        self.image_paths = image_paths
        self.captions = captions
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        caption = self.captions[idx]

        # Load and transform the image
        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        # Tokenize and pad the caption (placeholder - replace with actual tokenizer logic)
        caption_tokens = [ord(c) for c in caption][:20]  # Dummy tokenization (ASCII values, max length 20)
        caption_tensor = torch.tensor(caption_tokens, dtype=torch.long)

        return image, caption_tensor

# Example file paths and captions (replace with actual dataset paths)
image_paths = ["dog playing in park.jpg", "cat sitting chair.jpg"]
captions = ["a dog playing in the park", "a cat sitting on a chair"]

# Define transforms for the images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Create the dataset and dataloader
dataset = ImageCaptionDataset(image_paths=image_paths, captions=captions, transform=transform)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=2)

# Define your feature extractor and caption generator models
class FeatureExtractor(nn.Module):
    def __init__(self):
        super(FeatureExtractor, self).__init__()
        self.conv = nn.Conv2d(3, 16, kernel_size=3, stride=2)

    def forward(self, x):
        return self.conv(x)

class CaptionGenerator(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers):
        super(CaptionGenerator, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, features, captions):
        embeddings = self.embedding(captions)
        inputs = torch.cat((features.unsqueeze(1), embeddings), dim=1)
        hiddens, _ = self.lstm(inputs)
        outputs = self.fc(hiddens)
        return outputs

# Hyperparameters
embed_size = 256
hidden_size = 512
vocab_size = 5000  # Based on dataset's vocabulary size
num_layers = 1
learning_rate = 1e-3
num_epochs = 10

# Define the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Models and optimizer
feature_extractor = FeatureExtractor().to(device)
caption_generator = CaptionGenerator(embed_size, hidden_size, vocab_size, num_layers).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(caption_generator.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    for images, captions in dataloader:
        images, captions = images.to(device), captions.to(device)

        # Extract features
        features = feature_extractor(images)

        # Forward pass
        outputs = caption_generator(features, captions[:, :-1])
        loss = criterion(outputs.reshape(-1, vocab_size), captions[:, 1:].reshape(-1))

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")
