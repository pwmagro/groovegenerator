/*
  ==============================================================================

    SampleProcessor.cpp
    Created: 27 Oct 2024 4:32:53pm
    Author:  pwmag

  ==============================================================================
*/

#include "SampleProcessor.h"

namespace aidolon {
    SampleProcessor::SampleProcessor(juce::AudioProcessorValueTreeState& ts) : treeState(ts)
    {
        formatManager.registerBasicFormats();
    }

    bool SampleProcessor::loadAndPrepareSample(juce::String filePath, ChoppedSampleBuffer& buffer)
    {
        // load sample
        juce::File file(filePath);
        if (!file.exists())
        {
            DBG("BADBADBADBAD");
            return false;
        }

        auto* reader = formatManager.createReaderFor(file);
        buffer.setSize(reader->numChannels, reader->lengthInSamples);
        reader->read(&buffer, 0, reader->lengthInSamples, 0, true, true);
        delete reader;

        buffer.setReady(true);
        return true;
        // chop sample (spook)
    }
}