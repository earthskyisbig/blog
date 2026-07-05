# 이미지 자리

이 파이프라인은 이미지 생성 API(예: Gemini 이미지 모델) 연동 전 상태이므로, 실제 이미지 파일은 아직 생성되지 않았습니다.

`drafts/*.md`의 `[[IMAGE: 설명]]` 위치와 `prompts/05_image_generation.md`의 프롬프트를 이미지 생성 API에 넣어 만든 결과물을 이 폴더에 `<글 slug>-cover.png`, `<글 slug>-section-1.png` 형식으로 저장하면 된다.

이미지가 준비되면 `html/*.html`의 해당 placeholder `<div>` 자리를 실제 `<img>` 태그로 교체하거나, 네이버 에디터에 붙여넣은 뒤 표시된 자리에 직접 업로드한다.
