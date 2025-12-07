Here's a draft based on what I know about your project:

---

# AMD_Robotics_Hackathon_2025_Voice_Controlled_Pick_and_Place

## Team Information

**Team:** 12 (LeGemma)

**Summary:** A voice-controlled robotic manipulation system that combines speech-to-text with vision-language-action models. Users speak natural language commands like "pick up the cube and place it in the bin," which are processed by Faster Whisper and executed by a fine-tuned SmolVLA model on an SO-101 robotic arm.




## Submission Details



<img width="952" height="852" alt="Screenshot 2025-12-06 at 18 37 54" src="https://github.com/user-attachments/assets/a888cf3f-4e9a-4c52-adb3-e39be860f133" />

<img width="1231" height="640" alt="Screenshot 2025-12-07 at 16 12 16" src="https://github.com/user-attachments/assets/e87146e9-27dd-4dc0-9305-d0d6d3e39de3" />

### 1. Mission Description

- Voice-controlled pick-and-place for accessibility and hands-free operation
- Applications include warehouse automation, assistive robotics for people with limited mobility, and intuitive human-robot interaction in manufacturing settings

### 2. Creativity

- Speech-visual-language-action pipeline combining STT with VLA models
- Natural language interface removes the need for programming knowledge or physical controllers


### 3. Technical Implementations

- **Teleoperation / Dataset Capture**
    - SO-101 leader-follower arm setup for kinesthetic teaching
    - Dual camera configuration (top and side views) at 640×480 @ 30fps
    - 60 episodes collected, 10 seconds per episode
    

- **Training**
    - Fine-tuned SmolVLA model
    - 1000 training steps
    - Dataset: [lecubeset](https://huggingface.co/datasets/Alfaxad/lecubeset)
    - Model: [a[https://huggingface.co/Alfaxad/act-pnp50](https://huggingface.co/datasets/Alfaxad/eval_act_pnp50)

- **Inference**
    - Faster Whisper for real-time speech-to-text
    - Act policy inference on recognized commands
    -

### 4. Ease of Use

- Fully voice-controlled—no technical expertise required to operate
- Generalizable to other pick-and-place tasks by retraining on new demonstrations
- Simple command interface: speak the task in natural language
- Modular pipeline allows swapping STT or VLA models independently

## Additional Links

- Evaluation dataset: https://huggingface.co/datasets/Alfaxad/eval_act_pnp_50v2
- Trained model: https://huggingface.co/Alfaxad/act-pnp50
- Training dataset: https://huggingface.co/datasets/Alfaxad/lecubeset
