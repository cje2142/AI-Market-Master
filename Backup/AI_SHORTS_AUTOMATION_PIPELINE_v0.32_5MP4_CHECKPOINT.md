# AI Shorts Automation Pipeline v0.32 - 5MP4

## Backup Checkpoint

- Checkpoint: 1차 목표 완료
- Version: AI Shorts Automation Pipeline v0.32 - 5MP4
- Status: ComfyUI 영상 5개 생성 완료
- TTS: 미진행
- Audio/video merge: 미진행
- Final production pipeline: 미진행

## Confirmed workflow state

The n8n workflow currently used for this checkpoint is named `AI Shorts Automation Pipeline v0.32 - 5MP4`.

Confirmed node flow at the checkpoint:

When clicking 'Execute workflow'
→ HTTP Request
→ Code in JavaScript
→ HTTP Request1
→ Code in JavaScript1
→ Code in JavaScript2
→ Image Prompt Generator
→ HTTP Request2 (ComfyUI video generation)
→ Wait
→ HTTP Request3
→ Code in JavaScript3
→ If
→ HTTP Request4
→ Read/Write Files from Disk
→ Final MP4 Result
→ Save Final MP4

## Validation

- 5 image/video generation items were confirmed in the n8n execution.
- 5 MP4 output files were confirmed at the `Save Final MP4` stage.
- This checkpoint is the baseline before adding the TTS stage.

## Important limitation

This file is a state/checkpoint backup only. The GitHub connector cannot directly read the user's local n8n instance at `localhost:5678`, so the exact n8n workflow JSON was not exported from the running instance by this backup operation. The actual workflow JSON should be exported from n8n and committed separately when available.
