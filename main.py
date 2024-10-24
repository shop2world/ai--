import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero  # 'openai'를 'ollama'로 변경할 예정
from note import AssistantFnc  # 메모장 쓰기 AssistantFnc를 사용

load_dotenv()  # 환경 변수를 로드합니다.

async def entrypoint(ctx: JobContext):
    # 초기 채팅 컨텍스트를 설정합니다.
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "너는 나와 대화하면서 필요한 내용을 메모장에 적어주는 비서 역할을 한다. "
            "짧고 간결하게 응답하며, 발음하기 어려운 문장 부호는 피해야 한다."
        ),
    )
    
    # 오디오만 자동 구독하도록 연결합니다.
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    # AssistantFnc 클래스의 인스턴스를 생성합니다.
    fnc_ctx = AssistantFnc()

    # VoiceAssistant 인스턴스를 생성하고 초기화합니다.
    assitant = VoiceAssistant(
        vad=silero.VAD.load(),  # 음성 활동 감지
        stt=openai.STT(),  # 음성을 텍스트로 변환
        llm=openai.LLM(),  # 언어 모델
        tts=openai.TTS(),  # 텍스트를 음성으로 변환
        chat_ctx=initial_ctx,  # 초기 채팅 컨텍스트
        fnc_ctx=fnc_ctx,  # 기능 컨텍스트 (메모장 기록 기능만 포함)
    )
    
    assitant.start(ctx.room)  # 지정된 방에서 음성 비서를 시작합니다.

    await asyncio.sleep(1)  # 1초 대기
    await assitant.say("안녕하세요, 어떻게 도와드릴까요?", allow_interruptions=True)  # 초기 인사

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))  # CLI 앱 실행
