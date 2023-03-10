# Objects detection with Python OpenCV library 

## Behaviour project analysis

**Social defeat models** are used in animal science to study the effects of social stress and aggression on animal behavior, physiology, and health. In these models, a dominant animal is paired with a subordinate animal, leading to repeated instances of social defeat for the subordinate animal. This can be achieved in various ways, including using resident-intruder paradigms, tube tests, or other social interaction tests.

Some common examples of social defeat models used in animal science include:

- **Resident-intruder model:** This model involves placing a resident animal in a cage and introducing an intruder animal. The resident animal will typically display aggressive behavior towards the intruder, leading to social defeat for the intruder.

- **Tube test:** In this model, two animals are placed in a tube and forced to interact with each other. The tube restricts the movements of the animals, and the subordinate animal is typically forced to retreat and accept defeat.

- **Chronic social defeat model:** In this model, a subordinate animal is repeatedly exposed to a dominant animal over a prolonged period, leading to chronic social defeat.

These social defeat models are used to study the effects of social stress on a variety of physiological and behavioral outcomes. For example, studies using these models have shown that social defeat can lead to changes in brain function, alterations in the immune system, and changes in the way animals interact with their environment. Additionally, social defeat models can be used to test potential interventions, such as drugs or behavioral therapies, for treating the negative effects of social stress.

# Objectives:

- Detect flipped videos and correct their direction
- Identify and track the movement of animals in the videos
- Determine the direction of movement of the animals

# Tasks:

Preprocessing:
1. Remove all moving objects in the video using background subtraction or other techniques
2. Divide the video into groups of frames (e.g. 250 frames per group)
3. Extract parameters (e.g. mean pixel intensity, motion energy, texture) for each group of frames
4. Compare parameter values across groups to identify flipped videos

# Video correction:

- Apply a flipping correction algorithm to the flipped videos to correct their orientation
- Verify the correctness of the correction by visual inspection or automated methods
- Animal detection and tracking:
- Apply a computer vision algorithm (e.g. object detection, segmentation) to detect animals in the videos
- Track the movement of the animals across frames using a tracking algorithm (e.g. Kalman filter, optical flow)
- Associate the tracked animal IDs across different frames to maintain their identity

# Animal movement analysis:

- Compute the direction of movement of each animal in each frame based on its position and velocity
- Visualize the movement trajectories of the animals using plots or videos
- Analyze the movement patterns of the animals (e.g. speed, acceleration, turning angle) to gain insights into their behavior
- Testing and validation:
- Test the performance of the video correction and animal movement analysis algorithms on a subset of the videos
- Evaluate the accuracy and precision of the results using metrics such as error rate, false positive rate, and correlation coefficients
- Iterate on the algorithms and parameters as needed to improve the results

# Deliverables:

- Code for the video correction and animal movement analysis algorithms
- Results of the analysis, including corrected videos and plots of animal movement trajectories
- Report documenting the methods, results, and conclusions of the project
