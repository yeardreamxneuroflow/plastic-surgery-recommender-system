import PIL

import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class AutoEncoder(nn.Module):
    def __init__(self):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 12),
            nn.ReLU(),
            nn.Linear(12, 3),  # Compress to 3 features
        )  # MNIST's size '128'
        self.decoder = nn.Sequential(
            nn.Linear(3, 12),
            nn.ReLU(),
            nn.Linear(12, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 28 * 28),
            nn.Sigmoid(),  # Output value between 0 and 1
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)

        return x


def train_model_with_mnist(model: AutoEncoder) -> None:
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ])
    train_dataset = datasets.MNIST(
        './dataset', train=True, download=True, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    epochs = 1

    for epoch in range(epochs):
        for data in train_loader:
            img, _ = data
            img = img.view(img.size(0), -1)  # Flatten operation
            output = model(img)
            loss = criterion(output, img)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')


def vectorize_imgs(face_landmarks: list[PIL.Image]) -> list[torch.Tensor]:
    model = AutoEncoder()

    train_model_with_mnist(model)
    model.eval()

    encoded_imgs = []
    for face_landmark in face_landmarks:
        transform = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,)),
        ])
        transformed_landmark = transform(face_landmark)
        # Flatten operation
        landmark_tensor: torch.Tensor = transformed_landmark.view(-1, 28 * 28)

        with torch.no_grad():  # Disable gradient calculations
            encoded_imgs.append(model.encoder(landmark_tensor))

    return encoded_imgs
