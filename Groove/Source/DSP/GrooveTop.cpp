/*
  ==============================================================================

    GrooveTop.cpp
    Created: 27 Oct 2024 4:32:16pm
    Author:  pwmag

  ==============================================================================
*/

#include "GrooveTop.h"

namespace aidolon {
    GrooveTop::GrooveTop(juce::AudioProcessorValueTreeState& ts) : treeState(ts), sampleProcessor(ts)
    {

    }

    void GrooveTop::loadAndPrepareSample(juce::String samplePath)
    {
        sampleProcessor.loadAndPrepareSample(samplePath, choppedSampleBuffer);
    }

    bool GrooveTop::isInterestedInFileDrag(const juce::StringArray& files)
    {
        // only one file
        if (files.size() != 1)
        {
            return false;
        }

        // wav only (for now)
        if (!files[0].endsWithIgnoreCase(".wav"))
        {
            return false;
        }

        return true;
    }

    void GrooveTop::processSamples(juce::AudioBuffer<float> buffer)
    {
        if (!choppedSampleBuffer.isReady())
        {
            return;
        }

        auto ch = buffer.getNumChannels();
        auto sp = buffer.getNumSamples();
        auto hostBuffer = buffer.getArrayOfWritePointers();
        auto sampleBuffer = choppedSampleBuffer.getArrayOfReadPointers();

        for (int s = 0; s < sp; s++, playhead++)
        {
            if (playhead > choppedSampleBuffer.getNumSamples())
            {
                playhead = 0;
            }

            for (int c = 0; c < ch; c++)
            {
                hostBuffer[c][s] = sampleBuffer[c][playhead];
            }
        }
    }

    void GrooveTop::filesDropped(const juce::StringArray& files, int x, int y)
    {
        loadAndPrepareSample(files[0]);
    }
}