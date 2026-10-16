# Voice

**The film's code**

```python
import manimgx as m

class VoiceHero(m.Scene):
    def construct(self) -> None:
        square = m.MathTex("x^2", font_size=96).shift(2 * m.LEFT)
        derivative = m.MathTex("2x", font_size=96).shift(2 * m.RIGHT)
        arrow = m.Arrow(square.get_right(), derivative.get_left(), buff=0.4)
        script = m.Text(
            "The derivative of [x squared] is [two x].", font_size=32
        ).to_edge(m.DOWN)
        self.add(square, script)
        self.play(m.Indicate(square))
        self.play(m.GrowArrow(arrow), m.Write(derivative))
        self.wait()
```

say speaks a line with the scene's voice, and plays animations while it speaks. Put the words of each animation in brackets, and give the animations in the same order: each starts with the first of its words. The scene waits until the line ends, so lines don't overlap; change the words, and the animations follow the new words.

The scene's voice speaks through a text-to-speech service. ManimGX keeps what it says in a folder named `voice/`, next to the scene's file, so the scene renders again without the service, and only a changed line goes to it again. What the voice says becomes the video's captions.

## say

**Code**

```python
import manimgx as m

class SayExample(m.Scene):
    def construct(self) -> None:
        x2 = m.MathTex("x^2").shift(2 * m.LEFT)
        dx = m.MathTex("2x").shift(2 * m.RIGHT)
        self.add(x2)
        self.say(
            "The derivative of [x squared] is [two x].",
            m.Indicate(x2),
            m.Write(dx),
        )
```

Speak a script, playing animations as it is said; the scene waits for both.

Mark in brackets the words an animation belongs to: the animations given play, in order, during the bracketed words, each starting as its words start and lasting as long as they take to say, or its own run time if that is longer (an empty `[]` starts one where it stands). Without brackets, the animations play during the whole speech. The brackets are not spoken.

```python
self.say(script, *animations, voice=None)
```

**`script`**

What to say, with a bracketed span for each animation (or none).

**`*animations`**

The animations, one per span.

**`voice`**

Who says it; by default the scene's `voice`.

Returns The speech, with its words and when each is said.

        import manimgx as m

        class SayExample(m.Scene):
            def construct(self) -> None:
                x2 = m.MathTex("x^2").shift(2 * m.LEFT)
                dx = m.MathTex("2x").shift(2 * m.RIGHT)
                self.add(x2)
                self.say(
                    "The derivative of [x squared] is [two x].",
                    m.Indicate(x2),
                    m.Write(dx),
                )
        ```
    """
    from manimgx.animation.timeline import AnimationGroup, Succession, Wait
    from manimgx.audio import spans, times

    text, found = spans(script)
    if found and len(found) != len(animations):
        raise ValueError(
            f"{len(found)} bracketed spans for {len(animations)} animations: give"
            " one animation per span"
        )
    speech = self.speech(text, voice)
    parts: list[Animation] = [speech]
    for anim, span in zip(
        animations, found or [None] * len(animations), strict=True
    ):
        start, end = (0.0, speech.duration) if span is None else times(speech, span)
        anim.run_time = max(anim.run_time, end - start)
        parts.append(Succession(Wait(start), anim) if start > 0 else anim)
    self.play(AnimationGroup(*parts))
    return speech
````

## speech

What the scene's voice says for `text`, without playing it.

Spoken once, then kept in `voice/` beside the scene's file (named by the text), so the scene renders again without speaking again; replace a file there with your own recording of the same words, and it is used instead. Play the speech, add it (`add_sound`: it speaks while the scene goes on), or read its `words`.

```python
self.speech(text, voice=None)
```

**`text`**

What to say.

**`voice`**

Who says it; by default the scene's `voice`.

Returns The speech.

## voice

Who speaks the scene's `say`: any voice; None for fal.ai's default model (`Fal()`).

## Speech

Speech: a sound that knows what it says and when it says each word.

A voice returns one. It plays as any sound does; `Scene.say` also times animations by its words.

```python
m.Speech(source, *, text, words=(), rate=None)
```

**`source`**

The audio: a file's path, a file's bytes, or samples.

**`text`**

What it says.

**`words`**

Each word and when it is said, if the voice knows; otherwise they are estimated from the audio.

**`rate`**

The samples' rate; only for samples.

### words

Its words, in order, with when each is said (in seconds from its start): the voice's, or estimated from the audio; a trim or a change of speed moves them with the audio.

```python
speech.words
```

## Voices

The voices ManimGX brings are fal.ai's: `m.voices.Fal`, with the model you choose and its settings. Your editor shows each model's settings.

### Fal

A scene's voice, in its class:

```py
voice = m.voices.Fal(
    "fal-ai/minimax/speech-2.8-hd",
    voice_setting={"voice_id": "Calm_Woman", "speed": 1.1},
)
```

A text-to-speech model on fal.ai, as a voice: `Fal(model, **settings)`, where the settings are the model's own (`ElevenV3` for the default).

```python
m.voices.Fal(model='fal-ai/elevenlabs/tts/eleven-v3', /, *, key=None, **settings)
```

**`model`**

The model's ID on fal.

**`key`**

fal's API key; by default `FAL_KEY`.

The model's settings.

#### model

The model's ID on fal.

#### settings

The model's settings, as given.

#### key

fal's API key, if given; else `FAL_KEY` is read as the voice speaks.

### Models

#### ElevenV3

The settings of ElevenLabs' Eleven v3 (`fal-ai/elevenlabs/tts/eleven-v3`), which times its words. Its text may carry audio tags: `[whispers]`, `[laughs]`, `[excited]`…

**`voice`**

A voice's name or ID in ElevenLabs' library: Aria, Roger, Sarah, Laura, Charlie, George, Callum, River, Liam, Charlotte, Alice, Matilda, Will, Jessica, Eric, Chris, Brian, Daniel, Lily, Bill… (default "Rachel").

**`stability`**

How steady the voice is, from 0 (expressive) to 1 (steady) (default 0.5).

**`language_code`**

The language, as an ISO 639-1 code ("en", "de"…) (default: the text's).

**`apply_text_normalization`**

Whether numbers and the like are spelled out before they are said (default "auto": as the model sees fit).

##### voice

A voice's name or ID in ElevenLabs' library: Aria, Roger, Sarah, Laura, Charlie, George, Callum, River, Liam, Charlotte, Alice, Matilda, Will, Jessica, Eric, Chris, Brian, Daniel, Lily, Bill… (default "Rachel").

##### stability

How steady the voice is, from 0 (expressive) to 1 (steady) (default 0.5).

##### language\_code

The language, as an ISO 639-1 code ("en", "de"…) (default: the text's).

##### apply\_text\_normalization

Whether numbers and the like are spelled out before they are said (default "auto": as the model sees fit).

#### MiniMax

The settings of MiniMax Speech 2.8 HD (`fal-ai/minimax/speech-2.8-hd`). Its text may carry pauses, `<#0.5#>` (in seconds), and interjections: `(laughs)`, `(sighs)`, `(coughs)`, `(clears throat)`, `(gasps)`, `(sniffs)`, `(groans)`, `(yawns)`.

**`voice_setting`**

The voice and how it speaks (`MiniMaxVoice`).

**`audio_setting`**

The audio it makes (`MiniMaxAudio`).

**`language_boost`**

A language or dialect it listens for (default: none).

**`normalization_setting`**

How it evens out the loudness (`MiniMaxLoudness`).

**`voice_modify`**

How it changes the voice itself (`MiniMaxTimbre`).

**`pronunciation_dict`**

How it pronounces particular words (`MiniMaxPronunciation`).

##### voice\_setting

The voice and how it speaks (`MiniMaxVoice`).

##### audio\_setting

The audio it makes (`MiniMaxAudio`).

##### language\_boost

A language or dialect it listens for (default: none).

##### normalization\_setting

How it evens out the loudness (`MiniMaxLoudness`).

##### voice\_modify

How it changes the voice itself (`MiniMaxTimbre`).

##### pronunciation\_dict

How it pronounces particular words (`MiniMaxPronunciation`).

#### MiniMaxVoice

A MiniMax voice and how it speaks.

**`voice_id`**

The voice: Wise\_Woman, Friendly\_Person, Inspirational\_girl, Deep\_Voice\_Man, Calm\_Woman, Casual\_Guy, Lively\_Girl, Patient\_Man, Young\_Knight, Determined\_Man, Lovely\_Girl, Decent\_Boy, Imposing\_Manner, Elegant\_Man, Abbess, Sweet\_Girl\_2, Exuberant\_Girl, or a cloned voice's ID (default "Wise\_Woman").

**`speed`**

How fast, from 0.5 to 2 (default 1).

**`vol`**

How loud, from 0.01 to 10 (default 1).

**`pitch`**

How high, in semitones from -12 to 12 (default 0).

**`emotion`**

The emotion it speaks with (default: as the text reads).

**`english_normalization`**

Whether English numbers are read more carefully, a little slower (default False).

##### voice\_id

The voice: Wise\_Woman, Friendly\_Person, Inspirational\_girl, Deep\_Voice\_Man, Calm\_Woman, Casual\_Guy, Lively\_Girl, Patient\_Man, Young\_Knight, Determined\_Man, Lovely\_Girl, Decent\_Boy, Imposing\_Manner, Elegant\_Man, Abbess, Sweet\_Girl\_2, Exuberant\_Girl, or a cloned voice's ID (default "Wise\_Woman").

##### speed

How fast, from 0.5 to 2 (default 1).

##### vol

How loud, from 0.01 to 10 (default 1).

##### pitch

How high, in semitones from -12 to 12 (default 0).

##### emotion

The emotion it speaks with (default: as the text reads).

##### english\_normalization

Whether English numbers are read more carefully, a little slower (default False).

#### MiniMaxAudio

The audio MiniMax makes.

**`sample_rate`**

Samples a second (default 32000).

**`bitrate`**

Bits a second, for MP3 (default 128000).

**`format`**

The file's format (default "mp3").

**`channel`**

Channels: 1 (mono) or 2 (stereo) (default 1).

##### sample\_rate

Samples a second (default 32000).

##### bitrate

Bits a second, for MP3 (default 128000).

##### format

The file's format (default "mp3").

##### channel

Channels: 1 (mono) or 2 (stereo) (default 1).

#### MiniMaxLoudness

How MiniMax evens out the audio's loudness.

**`enabled`**

Whether it does (default True).

**`target_loudness`**

The loudness it aims at, in LUFS, from -70 to -10 (default -18).

**`target_range`**

The loudness range, in LU, from 0 to 20 (default 8).

**`target_peak`**

The highest peak, in dBTP, from -3 to 0 (default -0.5).

##### enabled

Whether it does (default True).

##### target\_loudness

The loudness it aims at, in LUFS, from -70 to -10 (default -18).

##### target\_range

The loudness range, in LU, from 0 to 20 (default 8).

##### target\_peak

The highest peak, in dBTP, from -3 to 0 (default -0.5).

#### MiniMaxTimbre

How MiniMax changes the voice itself.

**`pitch`**

Higher or lower, from -100 to 100 (default 0).

**`intensity`**

More or less energetic, from -100 to 100 (default 0).

**`timbre`**

Its tone's color, from -100 to 100 (default 0).

##### pitch

Higher or lower, from -100 to 100 (default 0).

##### intensity

More or less energetic, from -100 to 100 (default 0).

##### timbre

Its tone's color, from -100 to 100 (default 0).

#### MiniMaxPronunciation

How MiniMax pronounces particular words.

**`tone_list`**

Each word and its pronunciation: `"text/(pronunciation)"` (Chinese tones 1 to 5: `"燕少飞/(yan4)(shao3)(fei1)"`).

##### tone\_list

Each word and its pronunciation: `"text/(pronunciation)"` (Chinese tones 1 to 5: `"燕少飞/(yan4)(shao3)(fei1)"`).

#### Gemini

The settings of Google's Gemini 3.8 Flash TTS (`google/gemini-3.8-flash-tts`). Its text may carry vocal events: `<laugh>`, `<sigh>`.

**`voice`**

The voice (default "Kore").

**`style_instructions`**

How to say it, in words: "Warm and unhurried, like a patient teacher." (default: none).

##### voice

The voice (default "Kore").

##### style\_instructions

How to say it, in words: "Warm and unhurried, like a patient teacher." (default: none).

#### Inworld

The settings of Inworld TTS-1.5 Max (`fal-ai/inworld-tts`), which speaks up to 2,000 characters a line.

**`voice`**

The voice, with its language (default "Craig (en)").

**`sample_rate_hertz`**

Samples a second (default 48000).

##### voice

The voice, with its language (default "Craig (en)").

##### sample\_rate\_hertz

Samples a second (default 48000).

#### Qwen

The settings of Alibaba's Qwen3-TTS 1.7B (`fal-ai/qwen-3-tts/text-to-speech/1.7b`).

**`voice`**

The voice (default: the model's).

**`language`**

The language (default "Auto": the text's).

**`prompt`**

How to say it, in words (not what to say) (default: none).

**`speaker_voice_embedding_file_url`**

A cloned voice: the URL of the speaker embedding `fal-ai/qwen-3-tts/clone-voice` made; it overrides `voice` and `prompt` (default: none).

**`reference_text`**

What the cloned voice's recording says, which helps it sound like it (default: none).

**`temperature`**

How varied the delivery is, above 0 and up to 1 (default 0.9).

**`top_k`**

Sampling: from the k likeliest sounds (default 50).

**`top_p`**

Sampling: from the likeliest sounds that make up p of the chance, 0 to 1 (default 1).

**`repetition_penalty`**

How strongly it avoids repeating itself (default 1.05).

**`subtalker_dosample`**

Whether its second stage samples (default True).

**`subtalker_temperature`**

Its second stage's temperature, 0 to 1 (default 0.9).

**`subtalker_top_k`**

Its second stage's top k (default 50).

**`subtalker_top_p`**

Its second stage's top p, 0 to 1 (default 1).

**`max_new_tokens`**

The most sound it makes, in its codec's tokens, 1 to 8192 (default 8192 here: fal's own, 200, can cut a long line short).

##### voice

The voice (default: the model's).

##### language

The language (default "Auto": the text's).

##### prompt

How to say it, in words (not what to say) (default: none).

##### speaker\_voice\_embedding\_file\_url

A cloned voice: the URL of the speaker embedding `fal-ai/qwen-3-tts/clone-voice` made; it overrides `voice` and `prompt` (default: none).

##### reference\_text

What the cloned voice's recording says, which helps it sound like it (default: none).

##### temperature

How varied the delivery is, above 0 and up to 1 (default 0.9).

##### top\_k

Sampling: from the k likeliest sounds (default 50).

##### top\_p

Sampling: from the likeliest sounds that make up p of the chance, 0 to 1 (default 1).

##### repetition\_penalty

How strongly it avoids repeating itself (default 1.05).

##### subtalker\_dosample

Whether its second stage samples (default True).

##### subtalker\_temperature

Its second stage's temperature, 0 to 1 (default 0.9).

##### subtalker\_top\_k

Its second stage's top k (default 50).

##### subtalker\_top\_p

Its second stage's top p, 0 to 1 (default 1).

##### max\_new\_tokens

The most sound it makes, in its codec's tokens, 1 to 8192 (default 8192 here: fal's own, 200, can cut a long line short).

## Captions

### add\_subcaption

Caption the film: `content` shown from now plus `offset`, for `duration` seconds.

The film's `captions` hold it, with those of its speech; `manimgx render` writes them beside the video, as subtitles.

```python
self.add_subcaption(content, duration=1, offset=0)
```

**`content`**

The caption's text.

**`duration`**

How long it shows, in seconds.

**`offset`**

How long after now it begins, in seconds.

## A voice of your own

A voice is any function from a text to a Speech: a sound that knows its words, and when each is said. Any text-to-speech service can be one.

### Voice

```python
Voice = Callable[[str], Speech]
```

Anything that speaks: a function from text to `Speech`. Bring any text-to-speech: wrap its call in a function that returns `Speech(audio, text=text)`.

### Word

A word of a speech, and when it is said: from `start` to `end`, in seconds from the speech's start.

```python
m.voices.Word(text, start, end)
```

### timed

The words of `text`, timed by a voice's timed pieces of it, in order (its characters, or its tokens): each word from the start of the piece its first letter is in to the end of the piece its last letter is in. Empty if the pieces don't spell the text's letters (a voice that said "two" for "2"): its words are then estimated.

```python
m.voices.timed(text, pieces)
```

### estimate

When each word of `text` is said in `samples`, estimated: the audio's voiced span shared among the words by their letters, with a share more for the pause after a comma or a full stop.

```python
m.voices.estimate(text, samples)
```

### cached

What `voice` says for `text`: spoken once, then kept in `folder` as its audio and a JSON of its words, named by the text and a digest of the voice and the text.

The audio may be replaced (a recording of the same words, in any format the engine reads, under the same name): its words are then timed again, from it.

```python
m.voices.cached(voice, text, folder)
```
