/*
  ==============================================================================

    SampleProcessor.h
    Created: 27 Oct 2024 4:32:53pm
    Author:  pwmag

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
#include "ChoppedSampleBuffer.h"

namespace aidolon {
    class SampleProcessor {
    public:
        SampleProcessor(juce::AudioProcessorValueTreeState& ts);

        bool loadAndPrepareSample(juce::String filePath, ChoppedSampleBuffer& buffer);

    private:
        juce::AudioProcessorValueTreeState& treeState;
        juce::AudioFormatManager formatManager;

    };
}