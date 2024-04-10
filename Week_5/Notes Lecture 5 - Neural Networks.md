# Week 5 - Neural Networks

### Technique/Tool within Machine Learning - models mathematical function from inputs to outputs based on the structure and parameters of the network, that allows for the parameters of the network to be learned based on data



- The term "activation function" is associated with neural networks, and refers to the function through which the inputs and their weights are passed through to determine an output
- An example of a basic neural network, and how it would learn the "Or" function, with the step function `(0 if input < 0, 1 if input >= 1)` as the activation function:
  - ![image-20240403132745049](C:\Users\cjrow\AppData\Roaming\Typora\typora-user-images\image-20240403132745049.png)
  - To change the function to an "And" function, change the **bias**, or the constant term, from `-1` to `-2` 
  - The input to the activation function `g(x)` is usually a linear combination of the previous weights and inputs
  - **gradient descent**: algorithm for minimizing loss when training a neural network; the primary accepted way to train neural networks
    - start with a random choice of weights
    - repeat:
      - calculate the gradient based on all data points in order to find the "direction" of the weights that will lead to a decreasing loss
      - update weights according to the gradient
  - **stochastic gradient descent**: same as above, but calculates the gradient based on **one** data point rather than all of them at once
  - **mini-batch gradient descent**: divide data set into groups or "batches" and use that to compute the gradient, falls in between stochastic and full gradient descent.
  - A neural network with multiple outputs is effectively just multiple neural networks with one output
  - **multilayer neural network**: artificial neural network with an input layer, an output layer, and at least one hidden layer
    - Opens up the ability to model data that isn't necessarily linear, but is better defined by more complex functions
    - Each node in a hidden layer comes up with it's own decision boundary, and then those boundaries are combined in the end to come up with the final output
      - Each node "learns a specific important feature" of the model, and the output at the end is a combination of what each node has "learned"
    - **backpropagation**: algorithm for training neural networks with hidden layers
      - start with a random choice of weights
      - repeat:
        - calculate error for output layer
        - for each layer, starting with the output layer, and moving inwards towards earliest hidden layer:
          - propagate the error back one layer
          - update weights
    - **deep neural network**: neural network with multiple hidden layers
    - **dropout**: temporarily removing unit - selected at random - from a neural network to prevent over-reliance on certain units
  - **computer vision**: computational methods for analyzing and understanding images
    - **image convolution**: applying a filter that adds each pixel value of an image to its neighbors, weighted according to a kernel matrix
    - **pooling**: reducing the size of an input by sampling from regions of the input
      - **max-pooling**: pooling by choosing the maximum value in each region
    - **convolutional neural network**: neural networks that use convolution, usually for analyzing images
  - **feed-forward neural network**: neural network that has connections only in one direction
  - **recurrent neural network**: output from the network can feed back into its own network for the next round of calculations
