import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import numpy as np
import matplotlib.pyplot as plt

# Функция для загрузки и подготовки данных
def load_and_prepare_data():
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    
    # Нормализация данных
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    # Преобразование меток в формат one-hot encoding
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    return x_train, y_train, x_test, y_test

# Загрузка данных
x_train, y_train, x_test, y_test = load_and_prepare_data()

print(f"Форма обучающего набора: {x_train.shape}")
print(f"Форма тестового набора: {x_test.shape}")

# Класс для создания, компиляции и управления моделью
class CNNModel:
    def __init__(self):
        self.model = None

    def build_model(self):
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(10, activation='softmax')
        ])
        print("Модель построена.")

    def compile_model(self):
        self.model.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        print("Модель скомпилирована.")

    def train_model(self, x_train, y_train, x_val, y_val, epochs=20, batch_size=64):           
        history = self.model.fit(
            x_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(x_val, y_val)
        )
        return history

    def save_model(self, filepath):
        self.model.save(filepath)
        print(f"Модель сохранена в {filepath}.")

    def load_model(self, filepath):
        self.model = tf.keras.models.load_model(filepath)
        print(f"Модель загружена из {filepath}.")

# Инициализация и построение модели
cnn_model = CNNModel()
cnn_model.build_model()
cnn_model.compile_model()

# Обучение модели
history = cnn_model.train_model(
    x_train, y_train,
    x_test, y_test,
    epochs=20,
    batch_size=64
)

# Сохранение модели
cnn_model.save_model('cnn_cifar10_model.h5')

# Загрузка сохранённой модели
cnn_model.load_model('cnn_cifar10_model.h5')

# Оценка модели
test_loss, test_accuracy = cnn_model.model.evaluate(x_test, y_test, verbose=2)
print(f"Точность модели на тестовых данных: {test_accuracy:.2f}")

# Построение графиков точности и потерь
def plot_accuracy_loss(history):
    plt.figure(figsize=(12, 5))
    
    # График точности
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Точность на обучении')
    plt.plot(history.history['val_accuracy'], label='Точность на тесте')
    plt.xlabel('Эпоха')
    plt.ylabel('Точность')
    plt.title('График точности')
    plt.legend()

    # График потерь
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Потери на обучении')
    plt.plot(history.history['val_loss'], label='Потери на тесте')
    plt.xlabel('Эпоха')
    plt.ylabel('Потери')
    plt.title('График потерь')
    plt.legend()

    plt.show()

# Вызов функции визуализации
plot_accuracy_loss(history)

# Функция для отображения изображений с предсказаниями
def predict_and_visualize(model, x_test, y_test, class_names):
    indices = np.random.choice(len(x_test), 10, replace=False)
    images = x_test[indices]
    true_labels = np.argmax(y_test[indices], axis=1)
    predictions = np.argmax(model.predict(images), axis=1)

    plt.figure(figsize=(15, 5))
    for i, (image, true_label, pred_label) in enumerate(zip(images, true_labels, predictions)):
        plt.subplot(2, 5, i + 1)
        plt.imshow(image)
        plt.title(f"Истинный: {class_names[true_label]}\nПредсказание: {class_names[pred_label]}")
        plt.axis('off')

    plt.show()

# Классы CIFAR-10
class_names = ['Самолёт', 'Автомобиль', 'Птица', 'Кошка', 'Олень', 'Собака', 'Лягушка', 'Лошадь', 'Корабль', 'Грузовик']

# Вызов функции
predict_and_visualize(cnn_model.model, x_test, y_test, class_names)
