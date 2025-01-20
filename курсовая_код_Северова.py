import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.metrics import accuracy_score

# Инициализация токенизатора
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Пример текстов и меток для обучения
train_texts = ["This is a positive sentence.", "This is a negative sentence."]
train_labels = [1, 0]
val_texts = ["I love this.", "I hate this."]
val_labels = [1, 0]

# Класс для Dataset
class TextDataset(Dataset):
    def __init__(self, encodings, labels):
        self.input_ids = encodings['input_ids']
        self.attention_mask = encodings['attention_mask']
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            'input_ids': torch.tensor(self.input_ids[idx]),
            'attention_mask': torch.tensor(self.attention_mask[idx]),
            'labels': torch.tensor(self.labels[idx])
        }

# Токенизация данных
def tokenize_data(texts, labels):
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)
    return encodings, labels

train_encodings, train_labels = tokenize_data(train_texts, train_labels)
val_encodings, val_labels = tokenize_data(val_texts, val_labels)

train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# Загрузка модели
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Определение устройства (GPU или CPU)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Оптимизатор
from torch.optim import AdamW

optimizer = AdamW(model.parameters(), lr=5e-6)

# Обучение модели
def train_model(model, train_loader, val_loader, optimizer, device, epochs=5):
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            # Переносим данные на нужное устройство
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            # Прогон через модель
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()

        print(f"Epoch {epoch + 1}: Training Loss = {train_loss / len(train_loader)}")
        
        # Оценка на валидации
        val_loss, val_acc = evaluate_model(model, val_loader, device)
        print(f"Epoch {epoch + 1}: Validation Loss = {val_loss}, Validation Accuracy = {val_acc}")

def evaluate_model(model, loader, device):
    model.eval()
    val_loss = 0
    predictions, true_labels = [], []
    with torch.no_grad():
        for batch in loader:
            # Переносим данные на нужное устройство
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            val_loss += loss.item()
            
            # Получаем предсказания
            preds = torch.argmax(outputs.logits, dim=1)
            predictions.extend(preds.cpu().numpy())
            true_labels.extend(labels.cpu().numpy())

    accuracy = accuracy_score(true_labels, predictions)
    return val_loss / len(loader), accuracy

# Запуск обучения
train_model(model, train_loader, val_loader, optimizer, device, epochs=3)

# Сохранение модели
model.save_pretrained('text_classification_model')
tokenizer.save_pretrained('text_classification_model')

print("Model training complete and saved!")