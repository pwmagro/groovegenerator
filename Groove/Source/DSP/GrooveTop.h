/*
  ==============================================================================

    GrooveTop.h
    Created: 27 Oct 2024 4:32:16pm
    Author:  pwmag

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
#include "SampleProcessor.h"
#include "ChoppedSampleBuffer.h"

namespace aidolon {

    class GrooveTop : public juce::Component, juce::FileDragAndDropTarget {
    public:
        GrooveTop(juce::AudioProcessorValueTreeState& ts);
        ~GrooveTop() { }

        // dsp
        void loadAndPrepareSample(juce::String samplePath);
        void processSamples(juce::AudioBuffer<float> buffer);

    private:
        // file dropping
        bool isInterestedInFileDrag(const juce::StringArray& files) override;
        void filesDropped(const juce::StringArray& files, int x, int y) override;


        // locals
        juce::AudioProcessorValueTreeState &treeState;
        SampleProcessor sampleProcessor;
        ChoppedSampleBuffer choppedSampleBuffer;
        unsigned playhead = 0;
    };

}