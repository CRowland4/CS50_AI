- I'm starting with on Conv2D input layer and one output layer with the appropriate number of output nodes, just for a
starting point.
- That didn't work, and after a tiny bit of digging and ChatGPT help, it didn't work because the Convolution layer's
output was different than what the following dense layer expected. Adding a Flatten() line of code fixed the issue.
- I can apply my many years of learning to understand that messing around with the layers lines of code isn't going to
be very beneficial to me at this time. My level of understanding of what each type of layer means/does and how it works
isn't robust enough to form the necessary anchor on which I would tie the results of my tinkering. I haven't reached the
learning rate plateau yet where I want to dive into those implementation details. Without someone to bounce questions
off of as I make changes and see the results, and without an on-the-job objective to work towards, I'm better served
at this moment further understanding what's going on under the hood. Learning about the layers and under what conditions
to apply which layer will be a trivial process of trial and error (though probably time-consuming) once I actually
understand what I'm typing.
- This is NOT to say, though, that I came out of this project with no new knowledge of tensorflow. Before this
"project", due to not having used tensorflow much before, the lines between data-gathering and formatting, model
construction, model compiling, and model fitting were blurry to me. This cleared that up significantly, and is a large
step forward in learning how tensorflow works as a whole. Clear mental delineations between concepts is vitally
important to understanding and large and complex thing like tensorflow