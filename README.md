Here's a draft based on what I know about your project:

---

# AMD_Robotics_Hackathon_2025_Voice_Controlled_Pick_and_Place

## Team Information

**Team:** 12 (LeGemma)

**Summary:** A voice-controlled robotic manipulation system that combines speech-to-text with vision-language-action models. Users speak natural language commands like "pick up the cube and place it in the bin," which are processed by Faster Whisper and executed by a fine-tuned SmolVLA model on an SO-101 robotic arm.





## Submission Details

![Screenshot 2025-12-07 at 16 02 26](https://github.com/user-attachments/assets/1af59623-47de-4428-ab54-672e9795f6c3)

<img width="1231" height="640" alt="Screenshot 2025-12-07 at 16 13 41" src="https://github.com/user-attachments/assets/47ab8df9-0c68-4ca5-b1d0-594e67fff295" />




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
