# Neural Networks

Neural networks are computational models inspired by biological neural systems. They consist of interconnected nodes called neurons, organized in layers.

## Basic Structure

A simple neuron receives inputs, computes a weighted sum, and produces an output:

$y = f(\sum_{i=1}^{n} w_i x_i + b)$

Where:
- $x_i$ are input values
- $w_i$ are weights
- $b$ is bias
- $f$ is an activation function

## Activation Functions

Common activation functions include:

1. Sigmoid: $f(x) = \frac{1}{1 + e^{-x}}$
2. ReLU: $f(x) = max(0, x)$
3. Tanh: $f(x) = tanh(x)$

## Training Process

Neural networks learn by adjusting weights to minimize a loss function. The backpropagation algorithm is used to calculate gradients:

$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y} \frac{\partial y}{\partial z} \frac{\partial z}{\partial w}$

Where $z = \sum w_i x_i + b$ is the weighted sum.

## Applications

Neural networks power many modern AI applications:
- Image recognition
- Natural language processing
- Speech recognition
- Recommendation systems
- Autonomous vehicles

The ability to learn from data makes neural networks incredibly versatile and powerful.