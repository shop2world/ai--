import logging
from typing import Annotated
from livekit.agents import llm

# 로거 생성
logger = logging.getLogger("voice-assistant")
logger.setLevel(logging.INFO)

# AssistantFnc 클래스 : 메모장 기능
class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

    # 메모장에 사용자가 말한 내용을 기록하는 메서드
    @llm.ai_callable(description="사용자가 말한 내용을 메모장에 기록합니다.")
    def take_note(
        self, note: Annotated[str, llm.TypeInfo(description="기록할 메모")]
    ):
        logger.info("메모 작성 중: %s", note)
        
        # 메모장을 열고 사용자의 말을 기록
        with open("notepad.txt", "a", encoding="utf-8") as f:
            f.write(note + "\n")
        
        return "메모가 메모장에 기록되었습니다."

    # 메모장에서 특정 메모를 삭제하는 메서드
    @llm.ai_callable(description="사용자가 지정한 메모를 삭제합니다.")
    def delete_note(
        self, note: Annotated[str, llm.TypeInfo(description="삭제할 메모")]
    ):
        logger.info("메모 삭제 중: %s", note)
        
        # 현재 메모장 내용을 읽어옴
        try:
            with open("notepad.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
        
            # 삭제할 메모를 제외한 나머지 메모를 기록
            with open("notepad.txt", "w", encoding="utf-8") as f:
                for line in lines:
                    if line.strip() != note:  # 현재 메모와 동일한 경우 제외
                        f.write(line)

            return "메모가 삭제되었습니다."
        except FileNotFoundError:
            return "메모장이 존재하지 않습니다."
    
    # 메모장에 저장된 내용을 읽고 요약하는 메서드
    @llm.ai_callable(description="메모장에 저장된 내용을 읽고 요약합니다.")
    def read_notes(self):
        logger.info("메모 읽기 중")

        try:
            with open("notepad.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            if not lines:
                return "메모장이 비어 있습니다."

            # 메모 내용을 요약
            notes = [line.strip() for line in lines]
            summary = self.summarize_notes(notes)

            return f"저장된 메모:\n{''.join(notes)}\n\n요약: {summary}"
        except FileNotFoundError:
            return "메모장이 존재하지 않습니다."

    # 메모 내용을 요약하는 메서드
    def summarize_notes(self, notes):
        # 간단한 요약을 위해 첫 번째 메모를 기준으로 사용 (더 정교한 요약 알고리즘을 적용할 수 있음)
        if notes:
            return f"{len(notes)}개의 메모가 있습니다."
        return "메모가 없습니다."
