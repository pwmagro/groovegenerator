/*
  ==============================================================================

    ChoppedSampleBuffer.h
    Created: 27 Oct 2024 4:49:35pm
    Author:  pwmag

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>

namespace aidolon
{
    class ChoppedSampleBuffer : public juce::AudioBuffer<float>
    {
    public:
        bool isReady()          { return ready; }
        void setReady(bool r)   { ready = r; }
    private:
        bool ready;
    };
}