<div align="center">

<h1>RVC Data Prep: An Open-Source RVC Data Preparation Tool</h1>
a Dubverse Black initiative <br> <br>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1NA2GuJ2y-zRfoG3NearNiMCQa8NbidSh?usp=sharing)
![Discord Shield](https://discordapp.com/api/guilds/1162007551987171410/widget.png?style=shield)

</div>

------

## Description
RVC Data Prep is an advanced tool for transforming audio/video content into isolated vocals. If a video contains multiple speakers, it will generate separate files for each one. The core functionality leverages Facebook's Demucs to isolate vocals and Pyannote embeddings to ideally identify and differentiate speakers.

## Features
1. Isolate vocals from YouTube videos
2. Distinguish multiple speakers and provide separate files
3. Trim silences greated than 300ms from the audio

## Prerequisites
Before you start using this tool, ensure that you have the following installed:
- Python version 3.10 or newer
- Accept [`pyannote/segmentation-3.0`](https://hf.co/pyannote/segmentation-3.0) user conditions
- Accept [`pyannote/speaker-diarization-3.0`](https://hf.co/pyannote/speaker-diarization-3.0) user conditions
- Create access token at [`hf.co/settings/tokens`](https://hf.co/settings/tokens)

## How to use

1. Start by first cloning the repository.
2. Run the Jupyter notebook locally or on Google Colab
3. Input a YouTube video link and wait for it to process

*(Integration with the RVC UI is parked for later)*

## Examples
| **Input Video**                                                                       | **Separated Files**                                                                                                                                                                                                                                         |
|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Shahrukh Khan's Speech](https://www.youtube.com/shorts/tsgWNmVU_B0)                  | [Vocals](https://dl.sndup.net/qhp6/srk-cleaned.mp3)                                                                                                                                                                                                         |
| [Yeh Ladka Haaye Allah - Bollywood Song](https://www.youtube.com/watch?v=BE8_rNJOQ-0) | [Udit Narayan's Vocals](https://dl.sndup.net/rqmp/SPEAKER_00.mp3), [Alka Yagnik's Vocals](https://dl.sndup.net/rg4g/SPEAKER_02.mp3), [Chorous](https://dl.sndup.net/d8s9/SPEAKER_01.mp3), [Other ambigous sounds](https://dl.sndup.net/wd2y/SPEAKER_03.mp3) |
| [Perfect - Ed Sheeran Duet](https://www.youtube.com/watch?v=817P8W8-mGE)              | [Ed Sheeran's Vocals](https://dl.sndup.net/gmjf/perfect.mp3), [Beyonce's Vocals](https://dl.sndup.net/h4qs/perfectf.mp3)                                                                                                                                    |
## Contributing 
We welcome contributions from anyone and everyone. Details about how to contribute, what we are looking for and how to get started can be found in our contributing guidelines.

## Support
For any issues, queries, and suggestions, join our [Discord server](https://discord.gg/4VGnrgpBN). Will be glad to help!

## Future Scope
- Enhance the precision of vocal isolation
- Integrate this in the RVC workflow - base data preparation and creating AI covers
- Improve the efficiencies of speaker identification using other models like Titanet

## About Us
We, at **Dubverse.ai**, are a dedicated and passionate group of developers who have been working for over three years on generative AI with a specific emphasis on audio. We deeply believe in the potential of AI to revolutionize the fields of video, voiceover, podcasts and other media-related applications. 

Our passion and dedication don't stop at development. We believe in sharing knowledge and nurturing a community of like-minded enthusiasts. That's why we maintain a deep tech blog where we talk about our latest research, development, trends in the field, and insights about generative AI and audio technologies. 

Check out some of our RVC blog posts:

1. [Evals are all we need](https://black.dubverse.ai/p/evals-are-all-we-need)
2. [Running RVC Models on the Easy GUI](https://black.dubverse.ai/p/running-rvc-models-on-the-easy-gui)

We are always open to hear from others who share our passion. Whether you're an expert in the field, a hobbyist, or just someone intrigued by AI and audio, feel free to reach out and connect with us.


## License 
RVC Data Prep is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

*Disclaimer: This repo is not affiliated with YouTube, Facebook AI Research, or Pyannote. All trademarks referred to are the property of their respective owners.*

## Acknowledgements
1. FaceBook Demucs
2. Pyannote Audio
3. Librosa
4. FFMPEG

-----------------------------------------------------------------------------

We value your feedback and encourage you to provide us with any suggestions or issues that you may encounter. Let's make this tool better together!
